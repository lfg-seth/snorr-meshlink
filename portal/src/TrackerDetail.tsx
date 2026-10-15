import Badge from './Badge';
import CoordinateCopy from './CoordinateCopy';
import DeviceSheet from './DeviceSheet';
import TrackerBatteryIcon from './TrackerBatteryIcon';
import type { Tracker } from './demo';
import { activeTimeLabel, latestRecordedSession } from './recorded-session';
import { clockTimeLabel, observationLabel, trackerStatus } from './tracker';

export default function TrackerDetail({ selected, now, label, showTrail, onTrailChange, onClose }: {
  selected: Tracker;
  now: number;
  label: string;
  showTrail: boolean;
  onTrailChange: (visible: boolean) => void;
  onClose: () => void;
}) {
  const contactAt = selected.lastContactAt ?? selected.position?.receivedAt ?? null;
  const status = trackerStatus(selected, now);
  const session = latestRecordedSession(selected, now);
  const coordinates = selected.position
    ? `${selected.position.latitude.toFixed(5)}, ${selected.position.longitude.toFixed(5)}`
    : null;
  return (
    <DeviceSheet label={label} eyebrow={`${selected.deviceType || 'Device'} - ${selected.shortName}`}
      status={<span className="sheet-indicators">
        <Badge kind={status.kind}>{status.label}</Badge>
        <TrackerBatteryIcon battery={selected.battery} />
      </span>}
      className="tracker-detail" closeLabel="Close tracker details" onClose={onClose}>
      <section aria-label="Location">
        <h3>Location</h3>
        <dl className="detail-grid tracker-location">
          <div>
            <dt>Area</dt>
            <dd>{selected.position?.areaName || 'Unknown area'}</dd>
          </div>
          <div>
            <dt>Coordinates</dt>
            <dd>{coordinates ? <CoordinateCopy key={coordinates} coordinates={coordinates} /> : 'No recorded position'}</dd>
          </div>
          <div>
            <dt>Last GPS</dt>
            <dd>{observationLabel(selected.position?.measuredAt, now)}</dd>
          </div>
          <div>
            <dt>Last Heard</dt>
            <dd>{observationLabel(contactAt, now)}</dd>
          </div>
        </dl>
      </section>
      <section className="tracker-session" aria-label="Latest session">
        <h3>Latest session</h3>
        <dl className="detail-grid session-grid">
          <div><dt>First Seen</dt><dd>{clockTimeLabel(session.firstSeen)}</dd></div>
          <div><dt>Last Heard</dt><dd>{observationLabel(contactAt, now)}</dd></div>
          <div><dt>Time Active</dt><dd>{activeTimeLabel(session.activeSeconds)}</dd></div>
          <div><dt>Distance Travelled</dt><dd title="Estimated distance between recorded GPS points">{session.distanceMiles === null ? 'Unknown' : `${session.distanceMiles.toFixed(1)} mi`}</dd></div>
        </dl>
        <p className="session-source small muted">Based on loaded GPS points</p>
      </section>
      <label className="check trail-control">
        <input type="checkbox" checked={showTrail} onChange={(event) => onTrailChange(event.target.checked)} />
        Show Recorded Trail
      </label>
    </DeviceSheet>
  );
}
