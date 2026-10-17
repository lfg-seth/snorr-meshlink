import type { Infrastructure } from './demo';
import { ageLabel } from './demo';

export default function PowerReadings({ device, now }: { device: Infrastructure; now: number }) {
  const readings = device.powerReadings ?? [];
  return <section className="power-readings" aria-label="Reported sensor power">
    <h3>Sensor voltage &amp; current</h3>
    <p className="small muted">Reported current keeps the sensor’s sign. Wiring, polarity and calibration are unverified; these readings do not establish charging, discharging or solar input.</p>
    {readings.length ? <dl className="detail-grid">{readings.toSorted((a, b) => a.metric.localeCompare(b.metric)).map(reading => {
      const current = reading.metric.endsWith('CurrentMa');
      const channel = reading.metric.match(/^power([1-8])/);
      const label = channel ? `Power channel ${channel[1]}` : 'Environment sensor';
      const cadence = device.reportCadenceMinutes?.[reading.metric] ?? device.cadenceMinutes;
      const stale = reading.measuredAt && now - Date.parse(reading.measuredAt) >= cadence * 3 * 60000;
      return <div key={reading.metric}>
        <dt>{label} · {current ? 'current' : 'bus voltage'}</dt>
        <dd>{Number.isFinite(reading.value) ? `${reading.value.toFixed(current ? 1 : 3)} ${current ? 'mA' : 'V'}` : 'Unknown'}
          <small>{reading.measuredAt
            ? `${stale ? 'Stale' : 'Measured'} ${ageLabel((now - Date.parse(reading.measuredAt)) / 1000)} ago`
            : 'Measurement time unknown'} · received {ageLabel((now - Date.parse(reading.receivedAt)) / 1000)} ago</small>
        </dd>
      </div>;
    })}</dl> : <p className="small muted">Awaiting sensor power readings.</p>}
  </section>;
}
