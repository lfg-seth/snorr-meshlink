import type { Fix, Tracker } from './demo.ts';

const sessionGapMs = 2 * 60 * 60 * 1000;

// This is the latest session visible in the loaded GPS observations, not a
// persisted session record. A gap of exactly two hours still belongs together.
export function latestRecordedSession(tracker: Tracker, now: number) {
  const byTime = new Map<number, Fix>();
  for (const point of [...tracker.history, ...(tracker.position ? [tracker.position] : [])]) {
    const time = point.measuredAt ? Date.parse(point.measuredAt) : NaN;
    if (Number.isFinite(time) && time <= now &&
        Number.isFinite(point.latitude) && Math.abs(point.latitude) <= 90 &&
        Number.isFinite(point.longitude) && Math.abs(point.longitude) <= 180)
      byTime.set(time, point);
  }
  const points = [...byTime.values()].sort(
    (a, b) => Date.parse(a.measuredAt!) - Date.parse(b.measuredAt!),
  );
  let start = points.length - 1;
  while (start > 0 && Date.parse(points[start].measuredAt!) -
      Date.parse(points[start - 1].measuredAt!) <= sessionGapMs) start--;
  const latest = points.slice(Math.max(0, start));
  const firstSeen = latest[0]?.measuredAt ?? null;
  const lastGPS = latest.at(-1)?.measuredAt ?? null;
  return {
    points: latest,
    firstSeen,
    lastGPS,
    // Only count the observed GPS span; silence does not add active time.
    activeSeconds: firstSeen && lastGPS
      ? (Date.parse(lastGPS) - Date.parse(firstSeen)) / 1000 : null,
    distanceMiles: latest.length ? recordedTrailConnections(latest).reduce(
      (total, [a, b]) => total + pointDistanceMiles(a, b), 0,
    ) : null,
  };
}

// Great-circle segments estimate travel between reported fixes; they do not
// measure the path between samples, elevation gain, or movement within a gap.
function pointDistanceMiles(a: Fix, b: Fix) {
  const radians = (degrees: number) => degrees * Math.PI / 180;
  const latitude = radians(b.latitude - a.latitude);
  const longitude = radians(b.longitude - a.longitude);
  const haversine = Math.sin(latitude / 2) ** 2 +
    Math.cos(radians(a.latitude)) * Math.cos(radians(b.latitude)) * Math.sin(longitude / 2) ** 2;
  const bounded = Math.max(0, Math.min(1, haversine));
  const angle = 2 * Math.atan2(Math.sqrt(bounded), Math.sqrt(1 - bounded));
  return (6371008.8 / 1609.344) * angle;
}

export function activeTimeLabel(seconds: number | null) {
  if (seconds === null) return 'Unknown';
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  return hours ? `${hours}h ${minutes % 60}m` : `${minutes} min`;
}

export function recordedTrailConnections(points: Fix[]) {
  const connections: [Fix, Fix][] = [];
  for (let i = 1; i < points.length; i++) {
    const gap = Date.parse(points[i].measuredAt!) - Date.parse(points[i - 1].measuredAt!);
    if (gap > 0 && gap <= sessionGapMs) connections.push([points[i - 1], points[i]]);
  }
  return connections;
}
