import type { Infrastructure } from './demo.ts';

export type CurrentSample = { at: string; milliamps: number };
export type CurrentHistoryResult = {
  samples: CurrentSample[];
  truncated: boolean;
  average30Minutes: { milliamps: number | null; count: number; at: string | null;
    asOf: string; metric: string | null; truncated: boolean };
};
export type LoadCurrentHistory = (id: string, hours: number, signal: AbortSignal) => Promise<CurrentHistoryResult>;

export function hasCurrentSensor(device: Infrastructure) {
  return device.powerReadings?.some(r => r.metric === 'sensorCurrentMa' || r.metric === 'power1CurrentMa') ||
    ['sensorCurrentMa', 'power1CurrentMa'].some(metric => metric in (device.reportCadenceMinutes ?? {}));
}

export function currentSamples(samples: CurrentSample[], now: number) {
  const byTime = new Map<number, CurrentSample>();
  for (const sample of samples) {
    const time = Date.parse(sample.at);
    if (Number.isFinite(time) && time <= now && Number.isFinite(sample.milliamps)) byTime.set(time, sample);
  }
  return [...byTime.values()].sort((a, b) => Date.parse(a.at) - Date.parse(b.at));
}

export const currentLabel = (milliamps: number) => `${milliamps > 0 ? '+' : ''}${milliamps.toFixed(1)} mA`;
