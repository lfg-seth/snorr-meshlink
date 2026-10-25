import { useState } from 'react';
import Badge from './Badge';
import { positionAgeSeconds, positionStatus } from './position';
import { minuteAgeLabel, statusText, trackerMapLabel, trackerStatus } from './tracker';
import TrackerDetail from './TrackerDetail';
import MapShortName from './MapShortName';
import AddMember from './AddMember';
import type { NewMember } from './AddMember';
import {
  timeLabel,
} from './demo';
import type { Assignment, NameJob, Tracker, Member } from './demo';
export default function UsersPage({
  now = Date.now(),
  online = true,
  assignments,
  connected = false,
  simulation = true,
  trackers = [],
  members = [],
  selfMemberId = 'm5',
  nameJobs,
  admin,
  onShortNameSave,
  onCreateMember,
  onAssign,
  onRelease,
  onJob,
  trailId,
  onTrailChange,
}: {
  now?: number;
  online?: boolean;
  assignments: Assignment[];
  connected?: boolean;
  simulation?: boolean;
  trackers?: Tracker[];
  members?: Member[];
  selfMemberId?: string;
  nameJobs: NameJob[];
  admin: boolean;
  onShortNameSave?: (shortName: string) => Promise<boolean>;
  onCreateMember?: (member: NewMember) => Promise<string>;
  onAssign: (deviceId: string, memberId: string) => void;
  onRelease: (deviceId: string) => void;
  onJob: (deviceId: string, status: NameJob['status']) => void;
  trailId: string | null;
  onTrailChange: (id: string | null) => void;
}) {
  const [deviceId, setDeviceId] = useState(
    () =>
      trackers.find(
        (t) => !assignments.some((a) => a.deviceId === t.id && !a.endedAt),
      )?.id ??
      trackers[0]?.id ??
      '',
  );
  const [memberId, setMemberId] = useState(
    () =>
      members.find((m) => m.id === selfMemberId)?.id ?? members[0]?.id ?? '',
  );
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [inspectedId, setInspectedId] = useState<string | null>(null);
  const inspected = trackers.find((tracker) => tracker.id === inspectedId);
  const active = assignments.filter((a) => !a.endedAt);
  function trackerLabel(tracker: Tracker) {
    const assignment = active.find((item) => item.deviceId === tracker.id);
    return members.find((member) => member.id === assignment?.memberId)?.name ?? `Device #${tracker.number}`;
  }
  const filtered = trackers.filter((tracker) =>
    `${tracker.shortName} ${tracker.number} ${trackerLabel(tracker)} ${trackerMapLabel(tracker, assignments, members)}`.toLowerCase().includes(search.toLowerCase()),
  );
  return (
    <div className="stack">
      {admin && onCreateMember && <AddMember onCreate={onCreateMember} onCreated={setMemberId} />}
      {onShortNameSave && <MapShortName key={selfMemberId}
        shortName={members.find((member) => member.id === selfMemberId)?.shortName ?? ''}
        onSave={onShortNameSave} />}
      <div className="summary-grid">
        {[
          [
            String(trackers.length),
            'Member trackers',
            'Provisioned tracker devices',
          ],
          [
            String(
              trackers.filter(
                (t) =>
                  t.position &&
                  positionStatus(positionAgeSeconds(t.position, now)) !==
                    'stale' &&
                  positionStatus(positionAgeSeconds(t.position, now)) !==
                    'unknown',
              ).length,
            ),
            'Within 15 minutes',
            'Based on measurement time',
          ],
          [
            String(
              trackers.filter(
                (t) =>
                  t.position &&
                  positionStatus(positionAgeSeconds(t.position, now)) ===
                    'stale',
              ).length,
            ),
            'Stale positions',
            '15 minutes or older',
          ],
          [
            String(
              trackers.filter(
                (t) =>
                  !t.position || positionAgeSeconds(t.position, now) === null,
              ).length,
            ),
            'Unknown / never seen',
            'No fresh fix inferred',
          ],
        ].map(([value, label, detail]) => (
          <div className="summary-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{detail}</small>
          </div>
        ))}
      </div>

      <section className="panel users-trackers" aria-label="Tracker devices">
        <div className="panel-heading"><h2>Tracker devices</h2><span className="small muted">{filtered.length} of {trackers.length}</span></div>
        <label className="search">
          <span className="sr-only">Search trackers or members</span>
          <input type="search" placeholder="Search member or device…" value={search} onChange={(event) => setSearch(event.target.value)} />
        </label>
        <div className="tracker-list">
          {filtered.map((tracker) => {
            return <button key={tracker.id} className="tracker-row" onClick={() => {
              setInspectedId(tracker.id);
            }}>
              <span className={`tracker-dot ${trackerStatus(tracker, now).kind}`} />
              <span className="tracker-copy"><strong>{trackerLabel(tracker)}</strong><small>{tracker.shortName} · {statusText(tracker, now)}</small></span>
              <span className="tracker-age">{tracker.position ? minuteAgeLabel(tracker.position.measuredAt, now) : 'No position'}</span>
            </button>;
          })}
          {!filtered.length && <p className="empty">No trackers match this search.</p>}
        </div>
      </section>
      {inspected && <TrackerDetail key={inspected.id} selected={inspected} label={trackerLabel(inspected)}
        mapLabel={trackerMapLabel(inspected, assignments, members)}
        now={now} online={online} showTrail={trailId === inspected.id}
        onTrailChange={(visible) => onTrailChange(visible ? inspected.id : null)}
        onClose={() => setInspectedId(null)} />}
      <section className="panel">
        <div className="panel-heading">
          <h2>Active assignments</h2>
          <Badge kind="recent">{active.length} assigned</Badge>
        </div>
        <div className="member-grid">
          {members.map((member) => {
            const assignment = active.find((a) => a.memberId === member.id);
            const tracker = trackers.find((t) => t.id === assignment?.deviceId);
            const job = tracker
              ? nameJobs.findLast((j) => j.deviceId === tracker.id)
              : null;
            return (
              <article className="member-card" key={member.id}>
                <div className="member-heading">
                  <span className="avatar">{member.initials}</span>
                  <div>
                    <h3>{member.name}</h3>
                    <small className="muted">{simulation ? 'Fictional member' : 'Assigned member'}</small>
                  </div>
                </div>
                <p>
                  {tracker ? (
                    <>
                      <strong>Device #{tracker.number}</strong>{' '}
                      <Badge>{tracker.shortName}</Badge>
                    </>
                  ) : (
                    <span className="muted">No active tracker</span>
                  )}
                </p>
                {assignment && (
                  <small className="muted">
                    Assigned {timeLabel(assignment.startedAt)}
                  </small>
                )}
                {tracker && (
                  <div className="card-actions">
                    <button
                      disabled={!admin && member.id !== selfMemberId}
                      onClick={() => onRelease(tracker.id)}
                    >
                      Release tracker
                    </button>
                  </div>
                )}
                {job && (
                  <p className="small">
                    Radio long name:{' '}
                    <Badge kind={job.status === 'failed' ? 'old' : 'neutral'}>
                      {job.status} · simulated
                    </Badge>
                  </p>
                )}
              </article>
            );
          })}
        </div>
      </section>
      <section className="panel">
        <div className="panel-heading">
          <h2>
            {admin
              ? 'Assign or transfer a tracker'
              : 'Claim an unassigned tracker'}
          </h2>
        </div>
        <p className="muted small">
          One active tracker per member. Transfers close the previous dated
          association.{' '}
          {connected
            ? 'The server validates your role and rejects conflicting claims.'
            : 'Role previews demonstrate the UI; authentication and server enforcement come later.'}
        </p>
        <form
          className="assignment-form"
          onSubmit={(event) => {
            event.preventDefault();
            setError('');
            try {
              onAssign(deviceId, admin ? memberId : selfMemberId);
            } catch (e) {
              setError(e instanceof Error ? e.message : 'Assignment failed');
            }
          }}
        >
          <label>
            Tracker
            <select
              value={deviceId}
              onChange={(event) => setDeviceId(event.target.value)}
            >
              {trackers.map((t) => (
                <option
                  key={t.id}
                  value={t.id}
                  disabled={!admin && active.some((a) => a.deviceId === t.id)}
                >
                  #{t.number} · {t.shortName}
                  {active.some((a) => a.deviceId === t.id)
                    ? ' · occupied'
                    : ' · unassigned'}
                </option>
              ))}
            </select>
          </label>
          {admin ? (
            <label>
              Member
              <select
                value={memberId}
                onChange={(event) => setMemberId(event.target.value)}
              >
                {members.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.name}
                  </option>
                ))}
              </select>
            </label>
          ) : (
            <p>
              Claim as{' '}
              <strong>
                {members.find((m) => m.id === selfMemberId)?.name ??
                  'Your account'}
              </strong>
            </p>
          )}
          <button className="primary" type="submit">
            {connected
              ? admin
                ? 'Save assignment / transfer'
                : 'Claim tracker'
              : admin
                ? 'Simulate assignment / transfer'
                : 'Simulate self-claim'}
          </button>
        </form>
        {error && (
          <p className="form-error" role="alert">
            {error}
          </p>
        )}
      </section>
      <section className="panel">
        <h2>Unassigned devices</h2>
        <div className="unassigned-list">
          {trackers
            .filter((t) => !active.some((a) => a.deviceId === t.id))
            .map((t) => (
              <span key={t.id}>
                <strong>#{t.number}</strong> · {t.shortName}
              </span>
            ))}
        </div>
        {active.length === trackers.length && (
          <p>All trackers are assigned.</p>
        )}
        <p className="muted small">
          Reporting unassigned trackers appear on the map by device number.
        </p>
      </section>
      <section className="panel">
        <h2>Radio name jobs</h2>
        <p className="muted small">
          Short names stay fixed. Assignment succeeds independently of a
          long-name job. {simulation
            ? 'These controls simulate outcomes; no radio command is sent. Only the latest job for a device may be confirmed.'
            : 'Remote radio naming is not integrated; pending jobs do not change the radio.'}
        </p>
        {!nameJobs.length ? (
          <p className="empty">
            {simulation ? 'Assign or release a tracker to create a simulated name job.' : 'No radio-name jobs. Member provisioning precedes assignments.'}
          </p>
        ) : (
          <div className="job-list">
            {nameJobs.map((job) => {
              const latest =
                nameJobs.findLast((j) => j.deviceId === job.deviceId) === job;
              return (
                <div className="job-row" key={job.assignmentId}>
                  <span>
                    <strong>
                      {trackers.find((t) => t.id === job.deviceId)?.shortName}
                    </strong>{' '}
                    → {job.longName}
                  </span>
                  <Badge>{latest ? job.status : 'Superseded'}</Badge>
                  {latest && admin && simulation && (
                    <span className="card-actions">
                      <button disabled={!simulation} onClick={() => onJob(job.deviceId, 'confirmed')}>
                        Simulate read-back
                      </button>
                      <button disabled={!simulation} onClick={() => onJob(job.deviceId, 'failed')}>
                        Simulate failure
                      </button>
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </section>
      <section className="panel">
        <h2>Dated assignment history</h2>
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Device</th>
                <th>Carrier</th>
                <th>Started (local)</th>
                <th>Ended (local)</th>
              </tr>
            </thead>
            <tbody>
              {[...assignments].reverse().map((a) => (
                <tr key={a.id}>
                  <td>
                    {trackers.find((t) => t.id === a.deviceId)?.shortName}
                  </td>
                  <td>{members.find((m) => m.id === a.memberId)?.name}</td>
                  <td>{new Date(a.startedAt).toLocaleString()}</td>
                  <td>
                    {a.endedAt
                      ? new Date(a.endedAt).toLocaleString()
                      : 'Active'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
