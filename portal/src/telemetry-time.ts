import type { Infrastructure } from './demo';

export function telemetryTime(measuredAt: string | null | undefined,
  receivedAt: string | null | undefined, now: number) {
  for (const at of [measuredAt, receivedAt]) {
    const value = Date.parse(at ?? '');
    if (Number.isFinite(value) && value <= now) return at!;
  }
  return null;
}

export function metricTime(device: Pick<Infrastructure, 'readingTimes' | 'readingReceivedTimes' | 'reportedAt'>,
  metric: string, now: number) {
  if (device.readingTimes || device.readingReceivedTimes)
    return telemetryTime(device.readingTimes?.[metric], device.readingReceivedTimes?.[metric], now);
  return telemetryTime(device.reportedAt, null, now);
}
