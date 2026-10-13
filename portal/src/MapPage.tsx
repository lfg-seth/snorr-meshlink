import { lazy, Suspense, useState } from 'react';
import Badge from './Badge';
import {
  ageLabel,
  historyInRange,
  initialTrackers,
  members,
  timeLabel,
} from './demo';
import type { Assignment, Fix } from './demo';
import { positionAgeSeconds, positionStatus } from './position';
import { statusText } from './tracker';
const TrackingMap = lazy(() => import('./TrackingMap'));
export default function MapPage({
  assignments,
  now,
  selectedId,
  onSelect,
  labels,
}: {
  assignments: Assignment[];
  now: number;
  selectedId: string;
  onSelect: (id: string) => void;
  labels: Record<string, string>;
}) {
  const [search, setSearch] = useState('');
  const [showInfrastructure, setShowInfrastructure] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [hours, setHours] = useState(4);
  const [point, setPoint] = useState<Fix | null>(null);
  const [listOpen, setListOpen] = useState(true);
  const selected = initialTrackers.find((t) => t.id === selectedId)!;
  const history = showHistory
    ? historyInRange(selected.history, now, hours)
    : [];
  const pointAssignment = point?.measuredAt
    ? assignments.find(
        (a) =>
          a.deviceId === selectedId &&
          Date.parse(a.startedAt) <= Date.parse(point.measuredAt!) &&
          (!a.endedAt || Date.parse(a.endedAt) > Date.parse(point.measuredAt!)),
      )
    : null;
  const pointCarrier =
    members.find((m) => m.id === pointAssignment?.memberId)?.name ??
    `Device #${selected.number} · unassigned at measurement time`;
  const age = selected.position
    ? positionAgeSeconds(selected.position, now)
    : null;
  const status = positionStatus(age);
  const filtered = initialTrackers.filter((t) =>
    `${t.shortName} ${t.number} ${labels[t.id]}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );
  return (
    <>
      <div className="summary-grid">
        {[
          ['6', 'Member trackers', 'Fictional pilot scenario'],
          [
            String(
              initialTrackers.filter(
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
              initialTrackers.filter(
                (t) =>
                  t.position &&
                  positionStatus(positionAgeSeconds(t.position, now)) ===
                    'stale',
              ).length,
            ),
            'Stale positions',
            '15 minutes or older',
          ],
          ['2', 'Unknown / never seen', 'No fresh fix inferred'],
        ].map(([value, label, detail]) => (
          <div className="summary-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{detail}</small>
          </div>
        ))}
      </div>
      <div className="map-toolbar">
        <label className="check">
          <input
            type="checkbox"
            checked={showInfrastructure}
            onChange={(event) => setShowInfrastructure(event.target.checked)}
          />
          Infrastructure layer
        </label>
        <span className="muted small">
          Positions are observations, not a safety status.
        </span>
        <button
          className="mobile-toggle"
          aria-expanded={listOpen}
          onClick={() => setListOpen((value) => !value)}
        >
          {listOpen ? 'Hide' : 'Show'} trackers & detail
        </button>
      </div>
      <div className="tracking-layout">
        <section
          className={`tracker-panel ${listOpen ? '' : 'mobile-hidden'}`}
          aria-label="Tracker list"
        >
          <div className="panel-heading">
            <h2>Trackers</h2>
            <span className="muted small">{filtered.length} of 6</span>
          </div>
          <label className="search">
            <span className="sr-only">Search trackers or members</span>
            <input
              type="search"
              placeholder="Search member or device…"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </label>
          <div className="tracker-list">
            {filtered.map((tracker) => {
              const fixAge = tracker.position
                ? positionAgeSeconds(tracker.position, now)
                : null;
              const state = positionStatus(fixAge);
              return (
                <button
                  className={`tracker-row ${selectedId === tracker.id ? 'active' : ''}`}
                  key={tracker.id}
                  aria-pressed={selectedId === tracker.id}
                  onClick={() => {
                    onSelect(tracker.id);
                    setPoint(null);
                  }}
                >
                  <span className={`tracker-dot ${state}`} />
                  <span className="tracker-copy">
                    <strong>{labels[tracker.id]}</strong>
                    <small>
                      {tracker.shortName} · {statusText(tracker, now)}
                    </small>
                  </span>
                  <span className="tracker-age">
                    {tracker.position ? ageLabel(fixAge) : '—'}
                  </span>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <p className="empty">No trackers match this search.</p>
            )}
          </div>
          <div className="legend">
            <strong>GPS measurement age</strong>
            <span>
              <i className="tracker-dot recent" /> Under 2m · recent
            </span>
            <span>
              <i className="tracker-dot aging" /> 2–5m · aging
            </span>
            <span>
              <i className="tracker-dot old" /> 5–15m · older fix
            </span>
            <span>
              <i className="tracker-dot stale" /> 15m+ · stale, no breathing
            </span>
            <span>
              <i className="tracker-dot unknown" /> Unknown age / never seen
            </span>
          </div>
        </section>
        <Suspense
          fallback={<div className="map-loading">Loading map renderer…</div>}
        >
          <TrackingMap
            trackers={initialTrackers}
            labels={labels}
            selectedId={selectedId}
            now={now}
            showInfrastructure={showInfrastructure}
            history={history}
            onSelect={(id) => {
              onSelect(id);
              setPoint(null);
            }}
            onPoint={setPoint}
          />
        </Suspense>
      </div>
      <section
        className={`detail-panel ${listOpen ? '' : 'mobile-hidden'}`}
        aria-labelledby="selected-device"
      >
        <div className="detail-title">
          <div>
            <p className="eyebrow">Selected tracker · {selected.shortName}</p>
            <h2 id="selected-device">{labels[selected.id]}</h2>
          </div>
          <Badge kind={status}>{statusText(selected, now)}</Badge>
        </div>
        <dl className="detail-grid">
          <div>
            <dt>GPS measurement age</dt>
            <dd>
              {selected.position ? ageLabel(age) : 'No recorded position'}
            </dd>
          </div>
          <div>
            <dt>Measured at</dt>
            <dd>{timeLabel(selected.position?.measuredAt ?? null)}</dd>
          </div>
          <div>
            <dt>Received at</dt>
            <dd>
              {selected.position
                ? timeLabel(selected.position.receivedAt)
                : 'Never received'}
            </dd>
          </div>
          <div>
            <dt>Last contact age</dt>
            <dd>
              {selected.position
                ? ageLabel(
                    (now - Date.parse(selected.position.receivedAt)) / 1000,
                  )
                : 'None'}
            </dd>
          </div>
          <div>
            <dt>Recorded coordinates</dt>
            <dd>
              {selected.position
                ? `${selected.position.latitude.toFixed(5)}, ${selected.position.longitude.toFixed(5)}`
                : 'List only · no pin'}
            </dd>
          </div>
          <div>
            <dt>Reported battery</dt>
            <dd>
              {selected.battery === null
                ? 'Unknown'
                : `${selected.battery}% (demo)`}
            </dd>
          </div>
        </dl>
        <div className="history-controls">
          <label className="check">
            <input
              type="checkbox"
              checked={showHistory}
              onChange={(event) => {
                setShowHistory(event.target.checked);
                setPoint(null);
              }}
            />
            Show recorded history
          </label>
          {showHistory && (
            <label>
              Window{' '}
              <select
                value={hours}
                onChange={(event) => {
                  setHours(Number(event.target.value));
                  setPoint(null);
                }}
              >
                <option value={1}>Last hour</option>
                <option value={4}>Last 4 hours</option>
                <option value={12}>Last 12 hours</option>
              </select>
            </label>
          )}
        </div>
        {showHistory && (
          <div className="history-detail">
            <p className="small muted">
              {history.length} measured points. Dashed lines estimate
              connections; gaps over 15 minutes are left open. Earlier points
              retain their assignment at measurement time.
            </p>
            <div className="point-buttons">
              {history.map((fix) => (
                <button
                  key={fix.measuredAt}
                  aria-pressed={point?.measuredAt === fix.measuredAt}
                  onClick={() => setPoint(fix)}
                >
                  {timeLabel(fix.measuredAt)}
                </button>
              ))}
            </div>
            {!history.length && <p>No timestamped points in this window.</p>}
            {point && (
              <p className="point-detail">
                {pointCarrier} · recorded at {timeLabel(point.measuredAt)} ·{' '}
                {point.latitude.toFixed(5)}, {point.longitude.toFixed(5)} ·
                received {timeLabel(point.receivedAt)}
              </p>
            )}
          </div>
        )}
      </section>
    </>
  );
}
