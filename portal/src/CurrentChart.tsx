import { useState } from 'react';
import { batteryCurrent } from './battery';
import { historyCurve, historySegments } from './battery-curve';
import type { Infrastructure } from './demo';
import { currentLabel, currentSamples, hasCurrentSensor } from './current';
import type { LoadCurrentHistory } from './current';
import { historyPeriods } from './history-periods';
import { telemetryTime } from './telemetry-time';
import { useHistory } from './use-history';

export default function CurrentChart(props: {
  device: Infrastructure; now: number; online: boolean; loadHistory?: LoadCurrentHistory;
}) {
  return hasCurrentSensor(props.device)
    ? <SensorCurrentChart key={`${props.device.id}:${batteryCurrent(props.device.powerReadings)?.metric ?? 'unknown'}`} {...props} /> : null;
}

function SensorCurrentChart({ device, now, online, loadHistory }: {
  device: Infrastructure; now: number; online: boolean; loadHistory?: LoadCurrentHistory;
}) {
  const [hours, setHours] = useState(24);
  const { history, loading, error } = useHistory(device.id, hours, loadHistory);
  const reading = batteryCurrent(device.powerReadings);
  const at = reading ? telemetryTime(reading.measuredAt, reading.receivedAt, now) : null;
  const retained = reading?.currentConvention === 'positive-charging' && at
    ? [{ at, milliamps: reading.value }] : [];
  const start = now - hours * 3600000;
  const samples = currentSamples([...(history?.samples ?? []), ...retained], now)
    .filter(s => Date.parse(s.at) >= start);
  const low = samples.length ? Math.min(...samples.map(s => s.milliamps)) : 0;
  const high = samples.length ? Math.max(...samples.map(s => s.milliamps)) : 0;
  const padding = Math.max(1, (high - low) * .12);
  const bottom = Math.min(0, low - padding), top = Math.max(0, high + padding);
  const x = (time: number) => 48 + (time - start) / (now - start) * 296;
  const y = (milliamps: number) => 98 - (milliamps - bottom) / (top - bottom) * 86;
  const metric = reading?.metric ?? history?.average30Minutes.metric;
  const timeout = metric ? device.missingTimeoutMinutes?.[metric] ??
    (device.reportCadenceMinutes?.[metric] ?? device.cadenceMinutes) * 3 : 0;
  const path = historyCurve(samples, timeout, x, s => y(s.milliamps));
  const isolated = historySegments(samples, timeout).filter(s => s.length === 1).map(s => s[0]);
  const average = history?.average30Minutes;
  // A retained response must age out even if the feed or history request fails.
  const averageAt = Date.parse(average?.at ?? '');
  const averageExpired = !Number.isFinite(averageAt) || averageAt > now || now - averageAt > 1800000 ||
    now - Date.parse(average?.asOf ?? '') > 60000;
  const averageValue = averageExpired ? null : average?.milliamps;
  const stale = timeout > 0 && now - averageAt >= timeout * 60000;
  const timeLabel = (time: number) => new Date(time).toLocaleString([], hours <= 24
    ? { hour: '2-digit', minute: '2-digit' } : { month: 'short', day: 'numeric' });
  return <section className="battery-mini-history current-history" aria-label="Current history">
    <div className="battery-mini-heading">
      <span>Current · mA</span>
      <div className="battery-periods" role="group" aria-label="Current history period">
        {historyPeriods.map(({ hours: value, label }) => <button key={value} type="button"
          aria-pressed={hours === value} onClick={() => setHours(value)}>{label}</button>)}
      </div>
    </div>
    <p className="current-average">30-minute average: <strong>{averageValue != null && Number.isFinite(averageValue)
      ? currentLabel(averageValue) : 'Unknown'}</strong>
      <small>{average && averageValue != null ? `Mean of ${average.count} readings in the latest 30 minutes${stale ? ' · stale' : ''}`
        : average?.truncated ? 'Incomplete history' : loading ? 'Loading current history…' : 'No recent current history'}
        {!online ? ' · Feed offline · historical readings' : error ? ' · History unavailable' : ''}</small>
    </p>
    {samples.length > 0 ? <svg className="battery-mini-chart current-mini-chart" viewBox="0 0 360 122" role="img"
      aria-label={`${device.name}: current over ${historyPeriods.find(p => p.hours === hours)!.description}, ${low.toFixed(1)} to ${high.toFixed(1)} milliamps`}>
      <title>Measured sensor-path current · positive charging · negative discharging · local time</title>
      {[bottom, 0, top].filter((v, i, values) => values.indexOf(v) === i).map(value =>
        <text key={value} x="39" y={y(value) + 3} textAnchor="end">{value.toFixed(1)}</text>)}
      {[0, .5, 1].map(fraction => <text key={fraction} x={48 + fraction * 296} y="118"
        textAnchor={fraction === 0 ? 'start' : fraction === 1 ? 'end' : 'middle'}>
        {timeLabel(start + fraction * (now - start))}</text>)}
      {path && <path d={path} fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />}
      {isolated.map(s => <circle key={s.at} cx={x(Date.parse(s.at))} cy={y(s.milliamps)} r="2.2" fill="currentColor">
        <title>{`${new Date(s.at).toLocaleString()}: ${currentLabel(s.milliamps)}`}</title></circle>)}
    </svg> : <p className="battery-mini-empty small muted">{loading ? 'Loading current history…' : 'Not enough current history in this period.'}</p>}
    <p className="small muted">Measured sensor path · battery flow/calibration unverified</p>
    {error && <p className="small muted" role="status">History unavailable · showing retained readings.</p>}
    {history?.truncated && <p className="small muted">Showing the most recent 50,000 readings.</p>}
  </section>;
}
