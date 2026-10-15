export type BatterySample = { at: string; volts: number };

export function batterySamples(samples: BatterySample[], now: number) {
  const byTime = new Map<number, BatterySample>();
  for (const sample of samples) {
    const time = Date.parse(sample.at);
    if (
      Number.isFinite(time) &&
      time <= now &&
      Number.isFinite(sample.volts) &&
      sample.volts > 0
    )
      byTime.set(time, sample);
  }
  return [...byTime.values()].sort(
    (a, b) => Date.parse(a.at) - Date.parse(b.at),
  );
}

// Fit actual elapsed time, using only the latest uninterrupted hour of reports.
// Voltage direction estimates charging behavior; it does not measure current.
export function batteryTrend(
  samples: BatterySample[],
  now: number,
  timeoutMinutes: number,
) {
  const sorted = batterySamples(samples, now);
  const latest = sorted.at(-1);
  if (!latest) return { label: 'Unknown', rate: null, count: 0, minutes: 0 };
  const latestTime = Date.parse(latest.at);
  const recent = [latest];
  for (let i = sorted.length - 2; i >= 0; i--) {
    const time = Date.parse(sorted[i].at);
    if (
      latestTime - time > 3600000 ||
      Date.parse(recent[0].at) - time >= timeoutMinutes * 60000
    )
      break;
    recent.unshift(sorted[i]);
  }
  const minutes = (latestTime - Date.parse(recent[0].at)) / 60000;
  if (recent.length < 3 || minutes < 10)
    return {
      label: 'Insufficient history',
      rate: null,
      count: recent.length,
      minutes,
    };
  const hours = recent.map((s) => (Date.parse(s.at) - latestTime) / 3600000);
  const meanTime = hours.reduce((a, b) => a + b, 0) / hours.length;
  const meanVolts = recent.reduce((a, b) => a + b.volts, 0) / recent.length;
  const slope =
    recent.reduce(
      (sum, s, i) => sum + (hours[i] - meanTime) * (s.volts - meanVolts),
      0,
    ) / hours.reduce((sum, h) => sum + (h - meanTime) ** 2, 0);
  const rate = slope * 1000;
  return {
    label:
      Math.abs(rate) < 5
        ? 'Steady'
        : rate > 0
          ? 'Charging'
          : 'Discharging',
    rate,
    count: recent.length,
    minutes,
  };
}

export { batteryChargeEstimate } from './battery-charge.ts';

// Positive battery current means charging; negative means discharging.
// A voltage slope supplies direction only and must never be relabelled as mA.
export function batteryPower(device: {
  batteryCurrentMa?: number | null;
  samples: BatterySample[];
  cadenceMinutes: number;
  reportCadenceMinutes?: Record<string, number>;
  missingTimeoutMinutes?: Record<string, number>;
}, now: number) {
  const current = device.batteryCurrentMa;
  const timeout = device.missingTimeoutMinutes?.battery ??
    (device.reportCadenceMinutes?.battery ?? device.cadenceMinutes) * 3;
  const measured = current != null && Number.isFinite(current);
  return {
    label: measured ? (current > 0 ? 'Charging' : current < 0 ? 'Discharging' : 'Steady')
      : batteryTrend(device.samples, now, timeout).label,
    amount: measured ? `${Math.abs(current).toFixed(1)} mA` : '— mA',
  };
}
