// These types describe the data shape. They do not validate incoming radio data.
export type Position = {
  measuredAt: string | null;
  receivedAt: string;
};

export type PositionStatus = 'recent' | 'aging' | 'old' | 'stale' | 'unknown';

// Receipt time never substitutes for GPS measurement time.
export function positionAgeSeconds(position: Position, now: number): number | null {
  if (!position.measuredAt) return null;
  const measuredAt = Date.parse(position.measuredAt);
  if (!Number.isFinite(measuredAt) || measuredAt > now) return null;
  return (now - measuredAt) / 1000;
}

export function positionStatus(ageSeconds: number | null): PositionStatus {
  if (ageSeconds === null || !Number.isFinite(ageSeconds) || ageSeconds < 0) return 'unknown';
  if (ageSeconds < 120) return 'recent';
  if (ageSeconds < 300) return 'aging';
  if (ageSeconds < 900) return 'old';
  return 'stale';
}
