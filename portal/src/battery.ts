import type { Infrastructure } from './demo.ts';

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

// Current is a sensor-path measurement, not proof of whole-battery accounting.
// The ordinary INA219 firmware reports channel 1; legacy firmware reports the
// environment metric too. Prefer channel 1 to avoid displaying both copies.
// Other/multiple power channels have no battery-path mapping in this contract.
export function batteryCurrent(readings: Infrastructure['powerReadings'] = []) {
  const channels = readings.filter(r => /^power[1-8]CurrentMa$/.test(r.metric));
  const candidates = channels.length ? channels : readings.filter(r => r.metric === 'sensorCurrentMa');
  if (candidates.length !== 1 || (channels.length && candidates[0].metric !== 'power1CurrentMa')) return null;
  return Number.isFinite(candidates[0].value) ? candidates[0] : null;
}

// Never infer mA from voltage slope or charge direction from an unmarked sign.
export function batteryPower(device: {
  powerReadings?: Infrastructure['powerReadings'];
  samples: BatterySample[];
  cadenceMinutes: number;
  reportCadenceMinutes?: Record<string, number>;
  missingTimeoutMinutes?: Record<string, number>;
}, now: number) {
  const reading = batteryCurrent(device.powerReadings);
  const timeout = device.missingTimeoutMinutes?.battery ??
    (device.reportCadenceMinutes?.battery ?? device.cadenceMinutes) * 3;
  const trend = batteryTrend(device.samples, now, timeout);
  return {
    label: reading?.currentConvention === 'positive-charging'
      ? `${reading.value > 0 ? 'Charging' : reading.value < 0 ? 'Discharging' : 'Steady'} (sensor path)`
      : trend.rate !== null ? `${trend.label} (voltage estimate)` : 'Unknown',
    amount: reading ? `${reading.value > 0 ? '+' : ''}${reading.value.toFixed(1)} mA` : 'Unknown',
    reading,
    trend: !reading || reading.currentConvention !== 'positive-charging',
    trendAt: batterySamples(device.samples, now).at(-1)?.at ?? null,
  };
}
