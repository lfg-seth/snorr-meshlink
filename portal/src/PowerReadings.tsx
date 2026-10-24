import type { Infrastructure } from './demo';
import { ageLabel } from './demo';
import { telemetryTime } from './telemetry-time';

export default function PowerReadings({ device, now }: { device: Infrastructure; now: number }) {
  const readings = device.powerReadings ?? [];
  return <section className="power-readings" aria-label="Reported sensor power">
    <h3>Sensor voltage &amp; current</h3>
    <p className="small muted">Positive current means charging; negative means discharging, using the confirmed fleet wiring. Current measures the sensor path; accuracy and calibration remain unverified.</p>
    {readings.length ? <dl className="detail-grid">{readings.toSorted((a, b) => a.metric.localeCompare(b.metric)).map(reading => {
      const current = reading.metric.endsWith('CurrentMa');
      const channel = reading.metric.match(/^power([1-8])/);
      const label = channel ? `Power channel ${channel[1]}` : 'Environment sensor';
      const cadence = device.reportCadenceMinutes?.[reading.metric] ?? device.cadenceMinutes;
      const at = telemetryTime(reading.measuredAt, reading.receivedAt, now);
      const timeout = device.missingTimeoutMinutes?.[reading.metric] ?? cadence * 3;
      const stale = at && now - Date.parse(at) >= timeout * 60000;
      return <div key={reading.metric}>
        <dt>{label} · {current ? 'current' : 'bus voltage'}</dt>
        <dd>{Number.isFinite(reading.value) ? `${current && reading.value > 0 ? '+' : ''}${reading.value.toFixed(current ? 1 : 3)} ${current ? 'mA' : 'V'}` : 'Unknown'}
          <small>{at
            ? `${stale ? 'Stale' : 'Measured'} ${ageLabel((now - Date.parse(at)) / 1000)} ago`
            : 'Awaiting first reading'}</small>
        </dd>
      </div>;
    })}</dl> : <p className="small muted">Awaiting sensor power readings.</p>}
  </section>;
}
