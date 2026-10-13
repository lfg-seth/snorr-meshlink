import { useState } from 'react';
import Badge from './Badge';
import { initialTrackers, members, timeLabel } from './demo';
import type { Assignment, NameJob } from './demo';
export default function UsersPage({
  assignments,
  nameJobs,
  admin,
  onAssign,
  onRelease,
  onJob,
}: {
  assignments: Assignment[];
  nameJobs: NameJob[];
  admin: boolean;
  onAssign: (deviceId: string, memberId: string) => void;
  onRelease: (deviceId: string) => void;
  onJob: (deviceId: string, status: NameJob['status']) => void;
}) {
  const [deviceId, setDeviceId] = useState('d5');
  const [memberId, setMemberId] = useState('m5');
  const [error, setError] = useState('');
  const active = assignments.filter((a) => !a.endedAt);
  return (
    <div className="stack">
      <section className="panel">
        <div className="panel-heading">
          <h2>Active assignments</h2>
          <Badge kind="recent">{active.length} assigned</Badge>
        </div>
        <div className="member-grid">
          {members.map((member) => {
            const assignment = active.find((a) => a.memberId === member.id);
            const tracker = initialTrackers.find(
              (t) => t.id === assignment?.deviceId,
            );
            const job = tracker
              ? nameJobs.findLast((j) => j.deviceId === tracker.id)
              : null;
            return (
              <article className="member-card" key={member.id}>
                <div className="member-heading">
                  <span className="avatar">{member.initials}</span>
                  <div>
                    <h3>{member.name}</h3>
                    <small className="muted">Fictional member</small>
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
                      disabled={!admin && member.id !== 'm5'}
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
          association. Role previews demonstrate the UI; authentication and
          server enforcement come later.
        </p>
        <form
          className="assignment-form"
          onSubmit={(event) => {
            event.preventDefault();
            setError('');
            try {
              onAssign(deviceId, admin ? memberId : 'm5');
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
              {initialTrackers.map((t) => (
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
              Claim as <strong>Demo Casey</strong>
            </p>
          )}
          <button className="primary" type="submit">
            {admin ? 'Simulate assignment / transfer' : 'Simulate self-claim'}
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
          {initialTrackers
            .filter((t) => !active.some((a) => a.deviceId === t.id))
            .map((t) => (
              <span key={t.id}>
                <strong>#{t.number}</strong> · {t.shortName}
              </span>
            ))}
        </div>
        {active.length === initialTrackers.length && (
          <p>All demo trackers are assigned.</p>
        )}
        <p className="muted small">
          Reporting unassigned trackers appear on the map by device number.
        </p>
      </section>
      <section className="panel">
        <h2>Radio name jobs</h2>
        <p className="muted small">
          Short names stay fixed. Assignment succeeds independently of a
          long-name job. These controls simulate outcomes; no radio command is
          sent. Only the latest job for a device may be confirmed.
        </p>
        {!nameJobs.length ? (
          <p className="empty">
            Assign or release a tracker to create a simulated name job.
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
                      {
                        initialTrackers.find((t) => t.id === job.deviceId)
                          ?.shortName
                      }
                    </strong>{' '}
                    → {job.longName}
                  </span>
                  <Badge>{latest ? job.status : 'Superseded'}</Badge>
                  {latest && admin && (
                    <span className="card-actions">
                      <button onClick={() => onJob(job.deviceId, 'confirmed')}>
                        Simulate read-back
                      </button>
                      <button onClick={() => onJob(job.deviceId, 'failed')}>
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
                    {
                      initialTrackers.find((t) => t.id === a.deviceId)
                        ?.shortName
                    }
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
