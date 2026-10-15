import BatteryCharge from './BatteryCharge';
import { useState } from 'react';
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
const clock = (time: number) =>
  new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
export default function BatteryHistory({
  device,
  now,
  online,
  connected,
}: {
  device: Infrastructure;
  now: number;
  online: boolean;
  connected: boolean;
}) {
  const [range, setRange] = useState(6);
  const [active, setActive] = useState<string | null>(null);
  const all = batterySamples(device.samples, now);
  const samples = all.filter(
    (s) => !range || Date.parse(s.at) >= now - range * 3600000,
  );
  const cadence = device.reportCadenceMinutes?.battery ?? device.cadenceMinutes;
  const timeout = device.missingTimeoutMinutes?.battery ?? cadence * 3;
  const power = batteryPower(device, now);
  const latest = all.at(-1);
  const readingAt = device.readingTimes
    ? device.readingTimes.battery
    : device.reportedAt;
  const stale = !readingAt || now - Date.parse(readingAt) >= timeout * 60000;
  const point = samples.find((s) => s.at === active) ?? samples.at(-1);
  const low = samples.length ? Math.min(...samples.map((s) => s.volts)) : 0;
  const high = samples.length ? Math.max(...samples.map((s) => s.volts)) : 0;
  const padding = Math.max(0.015, (high - low) * 0.15);
  const bottom = Math.max(0, low - padding);
  const top = high + padding;
  const start = range
    ? now - range * 3600000
    : latest
      ? Date.parse(all[0].at)
      : now - 3600000;
  const x = (at: string) =>
    66 + ((Date.parse(at) - start) / Math.max(60000, now - start)) * 620;
  const y = (volts: number) => 195 - ((volts - bottom) / (top - bottom)) * 170;
  const delta =
    samples.length > 1 ? samples.at(-1)!.volts - samples[0].volts : null;
  return (
    <section className="battery-history" aria-label="Battery detail">
      <div className="panel-heading">
        <div>
          <h3>Battery & power</h3>
          <p className="small muted">Voltage history · local time</p>
        </div>
        <label className="battery-range">
          History
          <select
            value={range}
            onChange={(e) => {
              setRange(Number(e.target.value));
              setActive(null);
            }}
          >
            <option value={1}>Last hour</option>
            <option value={6}>Last 6 hours</option>
            <option value={24}>Last 24 hours</option>
            <option value={0}>All loaded</option>
          </select>
        </label>
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
      {samples.length ? (
        <>
          <svg
            className="battery-chart"
            viewBox="0 0 720 240"
            role="group"
            aria-label="Battery voltage history; select a reading for details"
          >
            {[0, 1, 2, 3, 4].map((i) => {
              const volts = bottom + ((top - bottom) * i) / 4;
              return (
                <g key={i}>
                  <line
                    x1="66"
                    x2="686"
                    y1={y(volts)}
                    y2={y(volts)}
                    stroke="#dce5df"
                  />
                  <text x="56" y={y(volts) + 4} textAnchor="end">
                    {volts.toFixed(3)} V
                  </text>
                </g>
              );
            })}
            {[0, 1, 2, 3, 4].map((i) => {
              const time = start + ((now - start) * i) / 4;
              return (
                <text key={i} x={66 + i * 155} y="222" textAnchor="middle">
                  {clock(time)}
                </text>
              );
            })}
            {samples
              .slice(1)
              .map(
                (s, i) =>
                  Date.parse(s.at) - Date.parse(samples[i].at) <
                    timeout * 60000 && (
                    <line
                      key={s.at}
                      x1={x(samples[i].at)}
                      y1={y(samples[i].volts)}
                      x2={x(s.at)}
                      y2={y(s.volts)}
                      stroke="#287162"
                      strokeWidth="2"
                    />
                  ),
              )}
            {point && (
              <line
                x1={x(point.at)}
                x2={x(point.at)}
                y1="25"
                y2="195"
                stroke="#8a9c91"
                strokeDasharray="3 4"
              />
            )}
            {samples.map((s) => (
              <g
                key={s.at}
                role="button"
                tabIndex={0}
                aria-label={`${stamp(s.at)}: ${s.volts.toFixed(3)} V`}
                aria-pressed={point?.at === s.at}
                onFocus={() => setActive(s.at)}
                onMouseEnter={() => setActive(s.at)}
                onClick={() => setActive(s.at)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    setActive(s.at);
                  }
                }}
              >
                <title>
                  {stamp(s.at)} · {s.volts.toFixed(3)} V
                </title>
                <circle
                  cx={x(s.at)}
                  cy={y(s.volts)}
                  r="11"
                  fill="transparent"
                />
                <circle
                  cx={x(s.at)}
                  cy={y(s.volts)}
                  r={point?.at === s.at ? 5 : 3}
                  fill="#287162"
                />
              </g>
            ))}
          </svg>
          <p className="battery-readout" aria-live="polite">
            {point && `${stamp(point.at)} · ${point.volts.toFixed(3)} V`}
          </p>
          <p className="small">
            Range {low.toFixed(3)}–{high.toFixed(3)} V · Net change{' '}
            {delta === null
              ? '—'
              : `${delta > 0 ? '+' : ''}${(delta * 1000).toFixed(1)} mV`}{' '}
            · {samples.length} readings
          </p>
          <details>
            <summary>Exact readings</summary>
            <div className="battery-table">
              <table>
                <thead>
                  <tr>
                    <th>Measured (local time)</th>
                    <th>Voltage</th>
                    <th>Change</th>
                    <th>Interval</th>
                  </tr>
                </thead>
                <tbody>
                  {samples.map((s, i) => (
                    <tr key={s.at}>
                      <td>{stamp(s.at)}</td>
                      <td>{s.volts.toFixed(3)} V</td>
                      <td>
                        {i
                          ? `${((s.volts - samples[i - 1].volts) * 1000).toFixed(1)} mV`
                          : '—'}
                      </td>
                      <td>
                        {i
                          ? `${((Date.parse(s.at) - Date.parse(samples[i - 1].at)) / 60000).toFixed(1)} min`
                          : '—'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      ) : (
        <p className="empty">
          No timed battery observations in this range. Try All loaded; readings
          with unknown measurement times cannot be plotted.
        </p>
      )}
      <p className="small muted">
        Adaptive voltage scale; gaps of {timeout} minutes or more are left
        disconnected.{' '}
        {connected
          ? 'Live snapshot includes up to 40 recent infrastructure observations, so the selected period may be incomplete.'
          : 'Fictional demo readings.'}{' '}
      </p>
    </section>
  );
}
