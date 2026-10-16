import BatteryCharge from './BatteryCharge';
import BatteryChart from './BatteryChart';
import type { LoadBatteryHistory } from './BatteryChart';
import type { Infrastructure } from './demo';
import { ageLabel } from './demo';
import { batterySamples, batteryPower } from './battery';

const stamp = (at: string) =>
  new Date(at).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
export default function BatteryHistory({
  device,
  now,
  online,
  loadHistory,
}: {
  device: Infrastructure;
  now: number;
  online: boolean;
  loadHistory?: LoadBatteryHistory;
}) {
  const all = batterySamples(device.samples, now);
  const cadence = device.reportCadenceMinutes?.battery ?? device.cadenceMinutes;
  const timeout = device.missingTimeoutMinutes?.battery ?? cadence * 3;
  const power = batteryPower(device, now);
  const readingAt = device.readingTimes
    ? device.readingTimes.battery
    : device.reportedAt;
  const stale = !readingAt || now - Date.parse(readingAt) >= timeout * 60000;
  return (
    <section className="battery-history" aria-label="Battery detail">
      <div className="panel-heading">
        <div>
          <h3>Battery & power</h3>
          <p className="small muted">Voltage history · local time</p>
        </div>
      </div>
      <div className="battery-stats">
        <div><span>Estimated battery percentage</span><BatteryCharge device={device} now={now} online={online} /></div>
        <div>
          <span>Last voltage</span>
          <strong>
            {device.battery === null ? '—' : `${device.battery.toFixed(3)} V`}
          </strong>
          <small>
            {readingAt
              ? `${ageLabel(Math.max(0, (now - Date.parse(readingAt)) / 1000))} ago`
              : 'Measurement time unknown'}
          </small>
        </div>
        <div>
          <span>{power.label}</span>
          <strong>{power.amount}</strong>
          {(!online || stale) && <small>Historical reading</small>}
        </div>
      </div>
      <BatteryChart device={device} now={now} loadHistory={loadHistory} />
      <details>
        <summary>Recent exact readings</summary>
        <div className="battery-table">
          <table>
            <thead><tr><th>Measured (local time)</th><th>Voltage</th></tr></thead>
            <tbody>{all.map(s => <tr key={s.at}><td>{stamp(s.at)}</td><td>{s.volts.toFixed(3)} V</td></tr>)}</tbody>
          </table>
        </div>
      </details>
    </section>
  );
}
