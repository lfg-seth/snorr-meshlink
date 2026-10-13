import { StrictMode, useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  assignDevice,
  initialAssignments,
  initialEvents,
  initialIncidents,
  initialMessages,
  initialTrackers,
  infrastructure as demoInfrastructure,
  members as demoMembers,
} from './demo';
import type {
  Assignment,
  AuditEvent,
  BatteryRule,
  Incident,
  Message,
  NameJob,
} from './demo';
import './style.css';
import Badge from './Badge';
import MapPage from './MapPage';
import UsersPage from './UsersPage';
import MessagesPage from './MessagesPage';
import InfrastructurePage from './InfrastructurePage';
import BackendLogin from './BackendLogin';
import { request } from './backend';
import type { BackendSession, BackendState } from './backend';
type Page = 'Map' | 'Users' | 'Messages' | 'Infrastructure';
const pages: Page[] = ['Map', 'Users', 'Messages', 'Infrastructure'];
const icons = { Map: '◎', Users: '♙', Messages: '☷', Infrastructure: '⌁' };
function pageFromHash(): Page {
  return (
    pages.find((page) => `#${page.toLowerCase()}` === window.location.hash) ??
    'Map'
  );
}
function App() {
  const [page, setPage] = useState<Page>(pageFromHash);
  const [now, setNow] = useState(Date.now());
  const [demoFeedOnline, setFeedOnline] = useState(true);
  const [demoAdmin, setAdmin] = useState(true);
  const [demoAssignments, setAssignments] =
    useState<Assignment[]>(initialAssignments);
  const [demoNameJobs, setNameJobs] = useState<NameJob[]>([]);
  const [selectedId, setSelectedId] = useState('d1');
  const [session, setSession] = useState<BackendSession | null>(null);
  const [snapshot, setSnapshot] = useState<BackendState | null>(null);
  const [backendConnected, setBackendConnected] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [backendError, setBackendError] = useState('');
  const seenMessages = useRef<string[] | null>(null);
  const activeToken = useRef('');
  activeToken.current = session?.token ?? '';

  const [demoMessages, setMessages] = useState<Message[]>(initialMessages);
  const [draft, setDraft] = useState('');
  const [unread, setUnread] = useState(0);
  const [notice, setNotice] = useState('');
  const [demoIncidents, setIncidents] = useState<Incident[]>(initialIncidents);
  const [demoEvents, setEvents] = useState<AuditEvent[]>(initialEvents);
  const [demoRules, setRules] = useState<Record<string, BatteryRule>>({});
  const trackers = snapshot?.trackers ?? initialTrackers;
  const members = snapshot?.members ?? demoMembers;
  const infrastructureNodes = snapshot?.infrastructure ?? demoInfrastructure;
  const assignments = snapshot?.assignments ?? demoAssignments;
  const nameJobs = snapshot?.nameJobs ?? demoNameJobs;
  const messages = snapshot?.messages ?? demoMessages;
  const incidents = snapshot?.incidents ?? demoIncidents;
  const events = snapshot?.events ?? demoEvents;
  const rules = snapshot?.rules ?? demoRules;
  const admin = session ? session.account.role === 'admin' : demoAdmin;
  const feedOnline = session
    ? Boolean(snapshot?.feedOnline && backendConnected)
    : demoFeedOnline;
  const selfMemberId = session?.account.memberId ?? 'm5';
  const accountName =
    session?.account.name ?? (admin ? 'Demo Dispatch' : 'Demo Casey');
  async function refreshBackend() {
    if (!session) return;
    const next = await request<BackendState>(
      '/api/meshlink/state',
      session.token,
    );
    if (session.token !== activeToken.current) return;
    setNow(Date.now());
    setSnapshot(next);
    setBackendConnected(true);
  }
  async function saveBackend(path: string, body: object) {
    if (!session) return false;
    try {
      await request(path, session.token, body);
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
          abort.signal,
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
    if (session) {
      void saveBackend('/api/meshlink/assign', { deviceId, memberId });
      return;
    }
    const at = new Date().toISOString();
    const next = assignDevice(assignments, deviceId, memberId, at, admin);
    if (next === assignments) return;
    setAssignments(next);
    const assignment = next[next.length - 1];
    const device = trackers.find((t) => t.id === deviceId)!;
    const name = members.find((m) => m.id === memberId)!.name;
    const released = assignments.filter(
      (a) => !a.endedAt && a.memberId === memberId && a.deviceId !== deviceId,
    );
    setNameJobs((old) => [
      ...old,
      ...released.map((a) => ({
        assignmentId: `release-${a.id}-${at}`,
        deviceId: a.deviceId,
        longName: `Device [${trackers.find((t) => t.id === a.deviceId)!.number}]`,
        status: 'pending' as const,
      })),
      {
        assignmentId: assignment.id,
        deviceId,
        longName: `${name} [${device.number}]`,
        status: 'pending',
      },
    ]);
  }
  function release(deviceId: string) {
    if (session) {
      void saveBackend('/api/meshlink/release', { deviceId });
      return;
    }
    const at = new Date().toISOString();
    setAssignments((old) =>
      old.map((a) =>
        !a.endedAt && a.deviceId === deviceId ? { ...a, endedAt: at } : a,
      ),
    );
    setNameJobs((old) => [
      ...old,
      {
        assignmentId: `release-${at}`,
        deviceId,
        longName: `Device [${trackers.find((t) => t.id === deviceId)!.number}]`,
        status: 'pending',
      },
    ]);
  }
  function incomingMessage() {
    if (!feedOnline) return;
    setMessages((old) => [
      ...old,
      {
        id: crypto.randomUUID(),
        author: 'Demo Avery',
        text: 'Training update: team at the next checkpoint.',
        at: new Date().toISOString(),
        evidence: 'Simulated inbound',
      },
    ]);
    if (page !== 'Messages') setUnread((value) => value + 1);
    setNotice('Demo Avery: Training update received in the shared channel.');
  }
  const warningCount =
    incidents.filter((i) => !i.resolvedAt).length +
    (snapshot?.warnings.filter((w) => !w.recoveredAt).length ?? 0);
  return (
    <div className="app-shell">
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
        <a className="brand" href="#map">
          <span className="brand-mark">△</span>
          <span>
            SNORR<strong>MeshLink</strong>
          </span>
        </a>
        <p className="nav-label">Dispatch workspace</p>
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
                {session
                  ? `${session.account.role} · authenticated`
                  : admin
                    ? 'Admin preview'
                    : 'Member preview · Demo Casey'}
              </small>
            </span>
          </div>
        </div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <span>
            Search & Rescue <span className="divider">/</span> {page}
          </span>
          <span className="clock">
            {new Date(now).toLocaleTimeString()}{' '}
            <span className="muted">local</span>
          </span>
        </header>
        <div className="demo-banner">
          <span>
            <strong>
              {session
                ? 'Connected backend · synthetic scenario'
                : 'Standalone synthetic prototype'}
            </strong>{' '}
            ·{' '}
            {session
              ? 'Assignments and observations are saved on the server.'
              : 'Local demo actions reset on refresh.'}
          </span>
          {!session && (
            <label>
              Role preview{' '}
              <select
                value={admin ? 'admin' : 'member'}
                onChange={(event) => setAdmin(event.target.value === 'admin')}
              >
                <option value="admin">Admin</option>
                <option value="member">Member</option>
              </select>
            </label>
          )}
          <button
            onClick={() => {
              if (session) {
                setSession(null);
                setSnapshot(null);
                setDraft('');
                setUnread(0);
                setBackendError('');
                seenMessages.current = null;
              } else setShowLogin((value) => !value);
            }}
          >
            {session ? 'Sign out of backend' : 'Backend sign in'}
          </button>
        </div>
        {showLogin && !session && (
          <BackendLogin
            onClose={() => setShowLogin(false)}
            onLogin={(value) => {
              seenMessages.current = null;
              setSession(value);
              setShowLogin(false);
              setDraft('');
            }}
          />
        )}
        {backendError && (
          <div className="backend-error" role="status">
            {backendError}
          </div>
        )}
        <div className={`feed-bar ${feedOnline ? '' : 'offline'}`}>
          <span>
            <span className={`feed-dot ${feedOnline ? '' : 'off'}`} />
            <strong>
              {session
                ? feedOnline
                  ? 'Simulation worker connected'
                  : 'Worker / backend feed unavailable'
                : feedOnline
                  ? 'Demo feed available'
                  : 'Simulated feed outage'}
            </strong>
            <span className="feed-explanation">
              {feedOnline
                ? session
                  ? 'Persisted observations; no live radios connected.'
                  : 'Fixture observations age with time; no live nodes connected.'
                : 'Showing last observations. Health is uncertain; drafts stay unsent. Use local Meshtastic for field viewing.'}
            </span>
          </span>
          <button
            disabled={Boolean(session && !admin)}
            onClick={() => {
              if (session)
                void saveBackend('/api/meshlink/demo/feed', {
                  online: !feedOnline,
                });
              else setFeedOnline((value) => !value);
            }}
          >
            {feedOnline ? 'Simulate outage' : 'Restore demo feed'}
          </button>
        </div>
        <main id="page-content" tabIndex={-1}>
          <div className="page-heading">
            <div>
              <p className="eyebrow">SNORR operations · training scenario</p>
              <h1>
                {page === 'Map'
                  ? 'Member tracking'
                  : page === 'Users'
                    ? 'Members & assignments'
                    : page === 'Messages'
                      ? 'Shared messages'
                      : 'Infrastructure'}
              </h1>
              <p className="muted">
                {page === 'Map'
                  ? 'Last recorded positions, with the age of every GPS measurement.'
                  : page === 'Users'
                    ? 'Keep the device identity stable as its carrier changes.'
                    : page === 'Messages'
                      ? 'One shared channel. Sending evidence stays separate from receipt.'
                      : 'Recorded health, fitted capabilities, and persistent incidents.'}
              </p>
            </div>
            <Badge kind="neutral">
              {page === 'Map'
                ? `${trackers.length} demo trackers`
                : page === 'Users'
                  ? `${members.length} fictional members`
                  : page === 'Messages'
                    ? 'Demo channel'
                    : `${infrastructureNodes.length} demo devices`}
            </Badge>
          </div>
          {session && !snapshot && (
            <p className="empty">Loading authenticated backend records…</p>
          )}
          {(!session || snapshot) && page === 'Map' && (
            <MapPage
              key={session?.account.id ?? 'demo'}
              assignments={assignments}
              trackers={trackers}
              members={members}
              now={now}
              selectedId={selectedId}
              onSelect={setSelectedId}
              labels={labels}
              infrastructureNodes={infrastructureNodes}
            />
          )}
          {(!session || snapshot) && page === 'Users' && (
            <UsersPage
              key={session?.account.id ?? 'demo'}
              assignments={assignments}
              trackers={trackers}
              members={members}
              nameJobs={nameJobs}
              selfMemberId={selfMemberId}
              connected={Boolean(session)}
              admin={admin}
              onAssign={assign}
              onRelease={release}
              onJob={(deviceId, status) => {
                if (session) {
                  const job = nameJobs.findLast((j) => j.deviceId === deviceId);
                  void saveBackend('/api/meshlink/demo/name-job', {
                    deviceId,
                    jobId: job?.id,
                    status,
                  });
                  return;
                }
                setNameJobs((old) => {
                  const latestIndex = old.findLastIndex(
                    (job) => job.deviceId === deviceId,
                  );
                  return old.map((job, index) =>
                    index === latestIndex ? { ...job, status } : job,
                  );
                });
              }}
            />
          )}
          {(!session || snapshot) && page === 'Messages' && (
            <MessagesPage
              key={session?.account.id ?? 'demo'}
              messages={messages}
              authorName={accountName}
              draft={draft}
              onDraft={setDraft}
              online={feedOnline}
              admin={admin}
              onSend={async () => {
                if (!feedOnline || !draft.trim()) return;
                if (session) {
                  const submittedDraft = draft;
                  if (
                    await saveBackend('/api/meshlink/messages', {
                      text: submittedDraft.trim(),
                    })
                  )
                    setDraft((current) =>
                      current === submittedDraft ? '' : current,
                    );
                  return;
                }
                const author = accountName;
                setMessages((old) => [
                  ...old,
                  {
                    id: crypto.randomUUID(),
                    author,
                    text: `${author}: ${draft.trim()}`,
                    at: new Date().toISOString(),
                    evidence:
                      'Simulated gateway submission · radio and human receipt unconfirmed',
                  },
                ]);
                setDraft('');
              }}
              onIncoming={session ? undefined : incomingMessage}
            />
          )}
          {(!session || snapshot) && page === 'Infrastructure' && (
            <InfrastructurePage
              key={session?.account.id ?? 'demo'}
              now={now}
              infrastructureNodes={infrastructureNodes}
              warnings={snapshot?.warnings}
              onAckWarning={
                session
                  ? (id) => {
                      void saveBackend(`/api/meshlink/warnings/${id}/ack`, {});
                    }
                  : undefined
              }
              connected={Boolean(session)}
              online={feedOnline}
              admin={admin}
              incidents={incidents}
              events={events}
              rules={rules}
              onRule={(id, rule) => {
                if (session) {
                  void saveBackend('/api/meshlink/rules', {
                    deviceId: id,
                    ...rule,
                  });
                  return;
                }
                setRules((old) => ({ ...old, [id]: rule }));
                setEvents((old) => [
                  ...old,
                  {
                    id: crypto.randomUUID(),
                    deviceId: id,
                    at: new Date().toISOString(),
                    text: `Demo Dispatch changed illustrative battery thresholds: ${rule.trigger} V trigger / ${rule.recovery} V recovery.`,
                  },
                ]);
              }}
              onIncident={(id, note) => {
                if (session) {
                  void saveBackend(`/api/meshlink/incidents/${id}`, {
                    action: note ? 'resolve' : 'acknowledge',
                    ...(note ? { note } : {}),
                  });
                  return;
                }
                const at = new Date().toISOString();
                setIncidents((old) =>
                  old.map((i) =>
                    i.id === id
                      ? note
                        ? { ...i, resolvedAt: at, note }
                        : { ...i, acknowledgedAt: at }
                      : i,
                  ),
                );
                const incident = incidents.find((i) => i.id === id)!;
                setEvents((old) => [
                  ...old,
                  {
                    id: crypto.randomUUID(),
                    deviceId: incident.deviceId,
                    at,
                    text: note
                      ? `Demo Dispatch resolved intrusion: ${note}`
                      : `${admin ? 'Demo Dispatch' : 'Demo Casey'} acknowledged incident; still open.`,
                  },
                ]);
              }}
            />
          )}
        </main>
        <footer>
          <span>SNORR MeshLink · Development preview</span>
          {!session && (
            <button disabled={!feedOnline} onClick={incomingMessage}>
              Simulate incoming message
            </button>
          )}
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

const root = document.getElementById('root');
if (!root) throw new Error('Portal root element is missing');
createRoot(root).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
