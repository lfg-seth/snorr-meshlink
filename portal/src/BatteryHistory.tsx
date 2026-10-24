import BatteryChart from './BatteryChart';
import type { LoadBatteryHistory } from './BatteryChart';
import type { Infrastructure } from './demo';
import { batterySamples } from './battery';

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
  loadHistory,
}: {
  device: Infrastructure;
  now: number;
  loadHistory?: LoadBatteryHistory;
}) {
  const all = batterySamples(device.samples, now);
  return (
    <section className="battery-history" aria-label="Battery detail">
      <div className="panel-heading">
        <div>
          <h3>Battery history</h3>
          <p className="small muted">Voltage history · local time</p>
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
