import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  assignDevice,
  initialAssignments,
  initialEvents,
  initialIncidents,
  initialMessages,
  initialTrackers,
  members,
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
  const [feedOnline, setFeedOnline] = useState(true);
  const [admin, setAdmin] = useState(true);
  const [assignments, setAssignments] =
    useState<Assignment[]>(initialAssignments);
  const [nameJobs, setNameJobs] = useState<NameJob[]>([]);
  const [selectedId, setSelectedId] = useState('d1');
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [draft, setDraft] = useState('');
  const [unread, setUnread] = useState(0);
  const [notice, setNotice] = useState('');
  const [incidents, setIncidents] = useState<Incident[]>(initialIncidents);
  const [events, setEvents] = useState<AuditEvent[]>(initialEvents);
  const [rules, setRules] = useState<Record<string, BatteryRule>>({});
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
      `Device #${initialTrackers.find((t) => t.id === deviceId)?.number}`
    );
  }
  const labels = Object.fromEntries(
    initialTrackers.map((t) => [t.id, carrier(t.id)]),
  );
  function assign(deviceId: string, memberId: string) {
    const at = new Date().toISOString();
    const next = assignDevice(assignments, deviceId, memberId, at, admin);
    if (next === assignments) return;
    setAssignments(next);
    const assignment = next[next.length - 1];
    const device = initialTrackers.find((t) => t.id === deviceId)!;
    const name = members.find((m) => m.id === memberId)!.name;
    const released = assignments.filter(
      (a) => !a.endedAt && a.memberId === memberId && a.deviceId !== deviceId,
    );
    setNameJobs((old) => [
      ...old,
      ...released.map((a) => ({
        assignmentId: `release-${a.id}-${at}`,
        deviceId: a.deviceId,
        longName: `Device [${initialTrackers.find((t) => t.id === a.deviceId)!.number}]`,
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
        longName: `Device [${initialTrackers.find((t) => t.id === deviceId)!.number}]`,
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
  const warningCount = incidents.filter((i) => !i.resolvedAt).length;
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
                  aria-label={`${warningCount} open intrusion incidents`}
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
              <strong>Demo Dispatch</strong>
              <small>
                {admin ? 'Admin preview' : 'Member preview · Demo Casey'}
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
            <strong>Synthetic prototype</strong> · Fictional data and local demo
            actions. Refresh resets changes.
          </span>
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
        </div>
        <div className={`feed-bar ${feedOnline ? '' : 'offline'}`}>
          <span>
            <span className={`feed-dot ${feedOnline ? '' : 'off'}`} />
            <strong>
              {feedOnline ? 'Demo feed available' : 'Simulated feed outage'}
            </strong>
            <span className="feed-explanation">
              {feedOnline
                ? 'Fixture observations age with time; no live nodes connected.'
                : 'Showing last observations. Health is uncertain; drafts stay unsent. Use local Meshtastic for field viewing.'}
            </span>
          </span>
          <button onClick={() => setFeedOnline((value) => !value)}>
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
                ? '6 demo trackers'
                : page === 'Users'
                  ? '5 fictional members'
                  : page === 'Messages'
                    ? 'Demo channel'
                    : '4 demo devices'}
            </Badge>
          </div>
          {page === 'Map' && (
            <MapPage
              assignments={assignments}
              now={now}
              selectedId={selectedId}
              onSelect={setSelectedId}
              labels={labels}
            />
          )}
          {page === 'Users' && (
            <UsersPage
              assignments={assignments}
              nameJobs={nameJobs}
              admin={admin}
              onAssign={assign}
              onRelease={release}
              onJob={(deviceId, status) =>
                setNameJobs((old) => {
                  const latestIndex = old.findLastIndex(
                    (job) => job.deviceId === deviceId,
                  );
                  return old.map((job, index) =>
                    index === latestIndex ? { ...job, status } : job,
                  );
                })
              }
            />
          )}
          {page === 'Messages' && (
            <MessagesPage
              messages={messages}
              draft={draft}
              onDraft={setDraft}
              online={feedOnline}
              admin={admin}
              onSend={() => {
                if (!feedOnline || !draft.trim()) return;
                const author = admin ? 'Demo Dispatch' : 'Demo Casey';
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
              onIncoming={incomingMessage}
            />
          )}
          {page === 'Infrastructure' && (
            <InfrastructurePage
              now={now}
              online={feedOnline}
              admin={admin}
              incidents={incidents}
              events={events}
              rules={rules}
              onRule={(id, rule) => {
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
          <button disabled={!feedOnline} onClick={incomingMessage}>
            Simulate incoming message
          </button>
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
