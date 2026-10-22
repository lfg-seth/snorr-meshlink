import { useEffect, useState } from 'react';
import { batterySamples } from './battery';
import type { BatterySample } from './battery';
import { batteryCurve, batterySegments } from './battery-curve';
import type { Infrastructure } from './demo';

export type BatteryHistoryResult = { samples: BatterySample[]; truncated: boolean };
export type LoadBatteryHistory = (id: string, hours: number, signal: AbortSignal) => Promise<BatteryHistoryResult>;

export default function BatteryChart({ device, now, loadHistory }: {
  device: Infrastructure;
  now: number;
  loadHistory?: LoadBatteryHistory;
}) {
  const [hours, setHours] = useState(24);
  const [history, setHistory] = useState<BatteryHistoryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  useEffect(() => {
    setHistory(null);
    setError(false);
    if (!loadHistory) return;
    let active = true;
    let abort: AbortController;
    const refresh = async () => {
      abort?.abort();
      const controller = new AbortController();
      abort = controller;
      setLoading(true);
      try {
        const result = await loadHistory(device.id, hours, controller.signal);
        if (active && !controller.signal.aborted) { setHistory(result); setError(false); }
      } catch {
        if (active && !controller.signal.aborted) setError(true);
      } finally {
        if (active && !controller.signal.aborted) setLoading(false);
      }
    };
    void refresh();
    const timer = window.setInterval(() => void refresh(), 60000);
    return () => { active = false; abort?.abort(); window.clearInterval(timer); };
  }, [device.id, hours, loadHistory]);

  const start = now - hours * 3600000;
  const samples = batterySamples([...(history?.samples ?? []), ...device.samples], now)
    .filter(s => Date.parse(s.at) >= start);
  const low = samples.length ? Math.min(...samples.map(s => s.volts)) : 0;
  const high = samples.length ? Math.max(...samples.map(s => s.volts)) : 0;
  const padding = Math.max(.025, (high - low) * .12);
  const bottom = Math.max(0, low - padding), top = high + padding;
  const x = (time: number) => 43 + (time - start) / (now - start) * 301;
  const y = (volts: number) => 98 - (volts - bottom) / (top - bottom) * 86;
  const timeout = device.missingTimeoutMinutes?.battery ??
    (device.reportCadenceMinutes?.battery ?? device.cadenceMinutes) * 3;
  const path = batteryCurve(samples, now, timeout, x, y);
  const isolated = batterySegments(samples, now, timeout)
    .filter(segment => segment.length === 1).map(segment => segment[0]);
  const timeLabel = (time: number) => new Date(time).toLocaleString([], hours === 24
    ? { hour: '2-digit', minute: '2-digit' } : { month: 'short', day: 'numeric' });
  return (
    <section className="battery-mini-history" aria-label="Battery voltage history">
      <div className="battery-mini-heading">
        <span>Battery · V</span>
        <div className="battery-periods" role="group" aria-label="Battery history period">
          {[[24, '24hr'], [168, '7day'], [720, '30day']].map(([value, label]) => (
            <button key={value} type="button" aria-pressed={hours === value}
              onClick={() => setHours(Number(value))}>{label}</button>
          ))}
        </div>
      </div>
      {samples.length > 0 ? (
        <svg className="battery-mini-chart" viewBox="0 0 360 122" role="img"
          aria-label={`${device.name}: battery voltage over ${hours === 24 ? '24 hours' : `${hours / 24} days`}, ${low.toFixed(2)} to ${high.toFixed(2)} volts`}>
          <title>Battery voltage · curved interpolation · local time</title>
          {[bottom, (bottom + top) / 2, top].map(volts => (
            <text key={volts} x="34" y={y(volts) + 3} textAnchor="end">{volts.toFixed(2)}</text>
          ))}
          {[0, .5, 1].map(fraction => (
            <text key={fraction} x={43 + fraction * 301} y="118"
              textAnchor={fraction === 0 ? 'start' : fraction === 1 ? 'end' : 'middle'}>
              {timeLabel(start + fraction * (now - start))}
            </text>
          ))}
          {path && <path d={path} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />}
          {isolated.map(sample => <circle key={sample.at} cx={x(Date.parse(sample.at))}
            cy={y(sample.volts)} r="2.2" fill="currentColor">
            <title>{`${new Date(sample.at).toLocaleString()}: ${sample.volts.toFixed(3)} V`}</title>
          </circle>)}
        </svg>
      ) : <p className="battery-mini-empty small muted">{loading ? 'Loading battery history…' : 'Not enough battery history in this period.'}</p>}
      {error && <p className="small muted" role="status">History unavailable · showing retained readings.</p>}
      {history?.truncated && <p className="small muted">Showing the most recent 50,000 readings.</p>}
    </section>
  );
}
