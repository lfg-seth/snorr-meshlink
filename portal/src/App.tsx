import { useCallback, useEffect, useRef, useState } from 'react';
import './style.css';
import snorrLogo from './assets/snorr-logo.png';
import Badge from './Badge';
import MapPage from './MapPage';
import { MapPreferences } from './MapPreferences';
import UsersPage from './UsersPage';
import type { NewMember } from './AddMember';
import MessagesPage from './MessagesPage';
import InfrastructurePage from './InfrastructurePage';
import BackendLogin from './BackendLogin';
import { BackendError, login, request, savedToken, saveToken } from './backend';
import type { BackendSession, BackendState } from './backend';
import type { LoadBatteryHistory } from './BatteryChart';
import type { LoadCurrentHistory } from './current';
import { currentSignalRows } from './signal-freshness';
type Page = 'Map' | 'Users' | 'Messages' | 'Infrastructure';
const pages: Page[] = ['Map', 'Users', 'Messages', 'Infrastructure'];
const icons = { Map: '◎', Users: '♙', Messages: '☷', Infrastructure: '⌁' };
function pageFromHash(): Page {
  return (
    pages.find((page) => `#${page.toLowerCase()}` === window.location.hash) ??
    'Map'
  );
}
export default function App() {
  return <MapPreferences><Portal /></MapPreferences>;
}

function Portal() {
  const liveBuild = import.meta.env.VITE_PORTAL_MODE === 'live';
  const [page, setPage] = useState<Page>(pageFromHash);
  const [now, setNow] = useState(Date.now());
  const [selectedId, setSelectedId] = useState('d1');
  const [trailId, setTrailId] = useState<string | null>(null);
  const [session, setSession] = useState<BackendSession | null>(null);
  const [restoreToken, setRestoreToken] = useState(savedToken);
  const [restoreAttempt, setRestoreAttempt] = useState(0);
  const [snapshot, setSnapshot] = useState<BackendState | null>(null);
  const [backendConnected, setBackendConnected] = useState(false);
  const [backendError, setBackendError] = useState('');
  const seenMessages = useRef<string[] | null>(null);
  const activeToken = useRef('');
  activeToken.current = session?.token ?? '';

  const [draft, setDraft] = useState('');
  const [unread, setUnread] = useState(0);
  const [notice, setNotice] = useState('');
  const [openingDemo, setOpeningDemo] = useState(!restoreToken);
  const demoAttempt = useRef(0);
  const loadBatteryHistory = useCallback<LoadBatteryHistory>((id, hours, signal) =>
    request(`/api/meshlink/battery-history/${encodeURIComponent(id)}?hours=${hours}`,
      session?.token ?? '', undefined, signal, session?.demo), [session]);
  const loadCurrentHistory = useCallback<LoadCurrentHistory>((id, hours, signal) =>
    request(`/api/meshlink/current-history/${encodeURIComponent(id)}?hours=${hours}`,
      session?.token ?? '', undefined, signal, session?.demo), [session]);
  const demoMode = session?.demo === true;
  const simulation = snapshot?.simulation === true;
  const trackers = snapshot?.trackers ?? [];
  const members = snapshot?.members ?? [];
  const infrastructureNodes = snapshot?.infrastructure ?? [];
  const assignments = snapshot?.assignments ?? [];
  const nameJobs = snapshot?.nameJobs ?? [];
  const messages = snapshot?.messages ?? [];
  const incidents = snapshot?.incidents ?? [];
  const events = snapshot?.events ?? [];
  const rules = snapshot?.rules ?? {};
  const currentLinks = snapshot ? currentSignalRows(snapshot) : [];
  const admin = session?.account.role === 'admin';
  const feedOnline = Boolean(snapshot?.feedOnline && backendConnected);
  const selfMemberId = session?.account.memberId ?? '';
  const accountName = session?.account.name ?? '';
  async function openDemo() {
    const attempt = ++demoAttempt.current;
    setOpeningDemo(true);
    try {
      const next = await login('meshlink-admin', 'fictional-demo-only-password', true);
      const state = await request<BackendState>('/api/meshlink/state', next.token, undefined, undefined, true);
      if (!state.simulation) throw new Error('The demo address must point to a separate simulation database.');
      if (attempt !== demoAttempt.current) return;
      startSession(next);
      setSnapshot(state);
      setBackendConnected(true);
      window.location.hash = '#map';
    } catch (error) {
      if (attempt === demoAttempt.current)
        setBackendError(error instanceof Error ? error.message : 'Demo database unavailable.');
      throw error;
    } finally {
      if (attempt === demoAttempt.current) setOpeningDemo(false);
    }
  }
  useEffect(() => {
    if (!restoreToken) void openDemo().catch(() => {});
    return () => { demoAttempt.current++; };
  }, []);
  function startSession(value: BackendSession) {
    if (!value.demo) saveToken(value.token);
    setRestoreToken('');
    seenMessages.current = null;
    setSession(value);
    setDraft('');
    setUnread(0);
    setBackendError('');
  }
  useEffect(() => {
    if (!restoreToken) return;
    let active = true;
    const abort = new AbortController();
    setBackendError('');
    void request<BackendState>('/api/meshlink/state', restoreToken, undefined, abort.signal)
      .then((next) => {
        if (!active) return;
        startSession({ token: restoreToken, account: next.account });
        setSnapshot(next);
        setBackendConnected(true);
      })
      .catch((error: unknown) => {
        if (!active) return;
        if (error instanceof BackendError && (error.status === 401 || error.status === 403)) {
          saveToken('');
          setRestoreToken('');
        } else {
          setBackendError('Unable to reconnect. Your sign-in is saved; try again when the connection returns.');
        }
      });
    return () => { active = false; abort.abort(); };
  }, [restoreToken, restoreAttempt]);
  async function refreshBackend() {
    if (!session) return;
    const next = await request<BackendState>(
      '/api/meshlink/state',
      session.token, undefined, undefined, session.demo,
    );
    if (session.token !== activeToken.current) return;
    setNow(Date.now());
    setSnapshot(next);
    setBackendConnected(true);
  }
  async function saveBackend(path: string, body: object) {
    if (!session) return false;
    try {
      await request(path, session.token, body, undefined, session.demo);
      await refreshBackend();
      setBackendError('');
      return true;
    } catch (e) {
      setBackendError(
        e instanceof Error ? e.message : 'Backend operation failed',
      );
      return false;
    }
  }
  useEffect(() => setTrailId(null), [session?.account.id]);
  useEffect(() => {
    if (!session) return;
    let active = true;
    let timer: number;
    const abort = new AbortController();
    async function poll() {
      try {
        const next = await request<BackendState>(
          '/api/meshlink/state',
          session!.token,
          undefined,
          abort.signal, session!.demo,
        );
        if (!active) return;
        const inbound = next.messages.filter(
          (message) => message.direction === 'inbound',
        );
        const newMessages = seenMessages.current
          ? inbound.filter(
              (message) => !seenMessages.current!.includes(message.id),
            )
          : [];
        seenMessages.current = inbound.map((message) => message.id);
        if (newMessages.length) {
          if (page !== 'Messages')
            setUnread((value) => value + newMessages.length);
          setNotice(
            `${newMessages[newMessages.length - 1].author}: New shared-channel message received.`,
          );
        }
        setNow(Date.now());
        setSnapshot(next);
        setBackendConnected(true);
        setBackendError('');
      } catch (e) {
        if (active) {
          setBackendConnected(false);
          setBackendError(
            'Backend unavailable or login expired. Last observations retained; sign out and sign in if needed.',
          );
        }
      }
      if (active) timer = window.setTimeout(poll, 2000);
    }
    void poll();
    return () => {
      active = false;
      abort.abort();
      window.clearTimeout(timer);
    };
  }, [session, page]);
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    const navigate = () => setPage(pageFromHash());
    window.addEventListener('hashchange', navigate);
    return () => {
      window.clearInterval(timer);
      window.removeEventListener('hashchange', navigate);
    };
  }, []);
  useEffect(() => {
    if (page === 'Messages') setUnread(0);
  }, [page]);
  useEffect(() => {
    if (!notice) return;
    const timeout = window.setTimeout(() => setNotice(''), 7000);
    return () => window.clearTimeout(timeout);
  }, [notice]);
  function carrier(deviceId: string) {
    const assignment = assignments.find(
      (a) => a.deviceId === deviceId && !a.endedAt,
    );
    return (
      members.find((m) => m.id === assignment?.memberId)?.name ??
      `Device #${trackers.find((t) => t.id === deviceId)?.number}`
    );
  }
  const labels = Object.fromEntries(trackers.map((t) => [t.id, carrier(t.id)]));
  function assign(deviceId: string, memberId: string) {
    void saveBackend('/api/meshlink/assign', { deviceId, memberId });
  }
  async function createMember(member: NewMember): Promise<string> {
    if (!session) throw new Error('Sign in as an admin to add members.');
    const result = await request<{ memberId: string }>('/api/meshlink/accounts', session.token,
      { ...member, role: 'member', createMember: true }, undefined, session.demo);
    // Creation has succeeded even if the following snapshot read loses connectivity.
    try { await refreshBackend(); }
    catch { setBackendError('Member created. Reconnecting to refresh the member list.'); }
    return result.memberId;
  }
  function release(deviceId: string) {
    void saveBackend('/api/meshlink/release', { deviceId });
  }
  const warningCount =
    incidents.filter((i) => !i.resolvedAt).length +
    (snapshot?.warnings.filter((w) => !w.recoveredAt).length ?? 0);
  function signOut() {
    saveToken('');
    setRestoreToken('');
    setSession(null);
    setSnapshot(null);
    setBackendConnected(false);
    demoAttempt.current++;
    setOpeningDemo(false);
    setDraft('');
    setUnread(0);
    setNotice('');
    setBackendError('');
    seenMessages.current = null;
  }
  if (restoreToken)
    return <main className="workspace" style={{ maxWidth: 640, margin: '64px auto', padding: 24 }}>
      <h1>SNORR MeshLink</h1>
      <p role="status">{backendError || 'Restoring your sign-in…'}</p>
      {backendError && <button onClick={() => setRestoreAttempt(value => value + 1)}>Try again</button>}
      <button onClick={signOut}>Sign out</button>
    </main>;
  if (openingDemo)
    return <main className="workspace"><p role="status">Opening the demo database…</p><button onClick={signOut}>Sign in</button></main>;
  if (!session)
    return (
      <main
        className="workspace"
        style={{ maxWidth: 640, margin: '64px auto', padding: 24 }}
      >
        <h1>SNORR MeshLink</h1>
        <p>Sign in to view recorded device positions.</p>
        {backendError && <p role="status">{backendError}</p>}
        <BackendLogin
          demo={!liveBuild}
          onDemo={openDemo}
          onLogin={startSession}
        />
      </main>
    );
  return (
    <div className={`app-shell ${page === 'Map' ? 'map-workspace' : ''}`}>
      <a
        className="skip-link"
        href="#page-content"
        onClick={(event) => {
          event.preventDefault();
          document.getElementById('page-content')?.focus();
        }}
      >
        Skip to page content
      </a>
      <aside className="sidebar">
        <div className="brand-row">
        <a className="brand" href="#map">
          <img className="brand-logo" src={snorrLogo} alt="SNORR" width={3797} height={1418} />
          <strong>MeshLink{demoMode && <small className="demo-mode-label">Demo</small>}</strong>
        </a>
        <button className="access-button" onClick={signOut}>{demoMode ? 'Sign in' : 'Sign out'}</button>
        </div>
        <p className="nav-label">{demoMode ? 'Demo workspace' : 'Dispatch workspace'}</p>
        <nav aria-label="Portal pages">
          {pages.map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              aria-current={page === item ? 'page' : undefined}
            >
              <span className="nav-icon" aria-hidden="true">
                {icons[item]}
              </span>
              {item}
              {item === 'Messages' && unread > 0 && (
                <span className="nav-count">{unread}</span>
              )}
              {item === 'Infrastructure' && warningCount > 0 && (
                <span
                  className="nav-count warning-count"
                  aria-label={`${warningCount} open infrastructure warnings and incidents`}
                >
                  {warningCount}
                </span>
              )}
            </a>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <span className="eyebrow">Pilot workspace</span>
          <p>
            Tracking first.
            <br />
            Clarity in the field.
          </p>
          <div className="profile">
            <span className="avatar">DD</span>
            <span>
              <strong>{accountName}</strong>
              <small>
                {session.account.role} · authenticated
              </small>
            </span>
          </div>
        </div>
      </aside>
      <div className="workspace">
        {page !== 'Map' && <div className="demo-banner">
          <span>
            <strong>
              {simulation ? 'Connected backend · synthetic scenario' : 'Connected backend · real devices'}
            </strong>{' '}· Assignments and observations are saved on the server.
          </span>
        </div>}
        {backendError && (
          <div className="backend-error" role="status">
            {backendError}
          </div>
        )}
        {page !== 'Map' && <div className={`feed-bar ${feedOnline ? '' : 'offline'}`}>
          <span>
            <span className={`feed-dot ${feedOnline ? '' : 'off'}`} />
            <strong>
              {feedOnline
                ? simulation ? 'Simulation worker connected' : 'MQTT worker connected'
                : 'Worker / backend feed unavailable'}
            </strong>
            <span className="feed-explanation">
              {feedOnline
                ? simulation ? 'Persisted observations; no live radios connected.'
                  : 'GPS ingestion active; check each position’s measurement age.'
                : 'Showing last observations. Health is uncertain; drafts stay unsent. Use local Meshtastic for field viewing.'}
            </span>
          </span>
          {simulation && (
          <button
            disabled={!admin}
            onClick={() => {
              void saveBackend('/api/meshlink/demo/feed', { online: !feedOnline });
            }}
          >
            {feedOnline ? 'Simulate outage' : 'Restore demo feed'}
          </button>
          )}
        </div>}
        <main id="page-content" tabIndex={-1}>
          {page !== 'Map' && <div className="page-heading">
            <div>
              <p className="eyebrow">
                SNORR operations · {simulation ? 'training scenario' : 'live bench'}
              </p>
              <h1>
                {page === 'Users'
                    ? 'Members & assignments'
                    : page === 'Messages'
                      ? 'Shared messages'
                      : 'Infrastructure'}
              </h1>
              <p className="muted">
                {page === 'Users'
                    ? 'Keep the device identity stable as its carrier changes.'
                    : page === 'Messages'
                      ? 'One shared channel. Sending evidence stays separate from receipt.'
                      : 'Recorded health, fitted capabilities, and persistent incidents.'}
              </p>
            </div>
            <Badge kind="neutral">
              {page === 'Users'
                  ? `${members.length} ${simulation ? 'fictional ' : ''}members`
                  : page === 'Messages'
                    ? simulation
                      ? 'Demo channel'
                      : 'Messaging not integrated'
                    : `${infrastructureNodes.length} ${simulation ? 'demo ' : ''}devices`}
            </Badge>
          </div>}
          {!snapshot && (
            <p className="empty">Loading authenticated backend records…</p>
          )}
          {snapshot && page === 'Map' && (
            <MapPage
              loadBatteryHistory={loadBatteryHistory}
              loadCurrentHistory={loadCurrentHistory}
              trailId={trailId}
              onTrailChange={setTrailId}
              online={feedOnline}
              key={session?.account.id ?? 'demo'}
              assignments={assignments}
              trackers={trackers}
              members={members}
              now={now}
              selectedId={selectedId}
              onSelect={setSelectedId}
              labels={labels}
              infrastructureNodes={infrastructureNodes}
              links={currentLinks}
            />
          )}
          {snapshot && page === 'Users' && (
            <UsersPage
              trailId={trailId}
              onTrailChange={setTrailId}
              now={now}
              online={feedOnline}
              onShortNameSave={session.account.memberId ? async (shortName) =>
                saveBackend('/api/meshlink/profile', { shortName }) : undefined}
              key={session?.account.id ?? 'demo'}
              assignments={assignments}
              trackers={trackers}
              members={members}
              nameJobs={nameJobs}
              simulation={simulation}
              selfMemberId={selfMemberId}
              connected={true}
              admin={admin}
              onCreateMember={admin ? createMember : undefined}
              onAssign={assign}
              onRelease={release}
              onJob={(deviceId, status) => {
                const job = nameJobs.findLast((j) => j.deviceId === deviceId);
                void saveBackend('/api/meshlink/demo/name-job', { deviceId, jobId: job?.id, status });
              }}
            />
          )}
          {snapshot && page === 'Messages' && (
            <MessagesPage
              key={session?.account.id ?? 'demo'}
              messages={messages}
              sendingEnabled={simulation}
              authorName={accountName}
              draft={draft}
              onDraft={setDraft}
              online={feedOnline}
              admin={admin}
              onSend={async () => {
                if (!feedOnline || !draft.trim()) return;
                const submittedDraft = draft;
                if (await saveBackend('/api/meshlink/messages', { text: submittedDraft.trim() }))
                  setDraft(current => current === submittedDraft ? '' : current);
              }}
            />
          )}
          {snapshot && page === 'Infrastructure' && (
            <InfrastructurePage
              loadBatteryHistory={loadBatteryHistory}
              loadCurrentHistory={loadCurrentHistory}
              key={session?.account.id ?? 'demo'}
              now={now}
              infrastructureNodes={infrastructureNodes}
              links={currentLinks}
              trackers={trackers}
              warnings={snapshot?.warnings}
              onAckWarning={
                session
                  ? (id) => {
                      void saveBackend(`/api/meshlink/warnings/${id}/ack`, {});
                    }
                  : undefined
              }
              connected={true}
              online={feedOnline}
              admin={admin}
              incidents={incidents}
              events={events}
              rules={rules}
              onRule={(id, rule) => {
                void saveBackend('/api/meshlink/rules', { deviceId: id, ...rule });
              }}
              onIncident={(id, note) => {
                void saveBackend(`/api/meshlink/incidents/${id}`, {
                  action: note ? 'resolve' : 'acknowledge', ...(note ? { note } : {}),
                });
              }}
            />
          )}
        </main>
        <footer>
          <span>SNORR MeshLink · {demoMode ? 'Demo' : simulation ? 'Test mode' : 'Live tracking'}</span>
        </footer>
      </div>
      <div className="toast-region" role="status" aria-live="polite">
        {notice && (
          <div className="toast">
            {notice} <a href="#messages">Open messages</a>
            <button
              aria-label="Dismiss message notification"
              onClick={() => setNotice('')}
            >
              ×
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
