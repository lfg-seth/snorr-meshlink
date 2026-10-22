import type { LinkObservation } from './NeighborTable';

export const SIGNAL_MAX_AGE_SECONDS = 2 * 60 * 60;

// Radio hearing evidence needs an explicit zone; local/date-only strings are ambiguous.
function timestamp(value: unknown): number | null {
  if (typeof value !== 'string') return null;
  const parts = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.exec(value);
  if (!parts) return null;
  const [, year, month, day, hour, minute, second] = parts.map(Number);
  if (month < 1 || month > 12 || day < 1 || day > new Date(Date.UTC(year, month, 0)).getUTCDate() ||
      hour > 23 || minute > 59 || second > 59) return null;
  const parsed = Date.parse(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function signalFreshness(link: LinkObservation, now: number): {
  basis: 'measured' | 'relative'; ageSeconds: number;
} | null {
  // Standard NeighborInfo is a cached table without evidence of a new hearing.
  if (link.reportType === 'neighbor-info' || !Number.isFinite(now)) return null;
  const received = timestamp(link.receivedAt);
  if (received === null || received > now) return null;
  const observed = timestamp(link.observedAt);
  if (observed !== null && observed <= received) {
    const ageSeconds = (now - observed) / 1000;
    return ageSeconds < SIGNAL_MAX_AGE_SECONDS ? { basis: 'measured', ageSeconds } : null;
  }
  const freshness = link.freshness;
  if (link.reportType !== 'snns-v1' || freshness?.basis !== 'relative' ||
      !Number.isInteger(freshness.ageAtAnchorSeconds) || freshness.ageAtAnchorSeconds < 0 ||
      freshness.ageAtAnchorSeconds >= 1800) return null;
  const anchor = timestamp(freshness.anchorReceivedAt);
  if (anchor === null || anchor > received) return null;
  const ageSeconds = freshness.ageAtAnchorSeconds + (now - anchor) / 1000;
  return ageSeconds < SIGNAL_MAX_AGE_SECONDS ? { basis: 'relative', ageSeconds } : null;
}

export function currentSignalRows(state: { currentLinks?: LinkObservation[]; links: LinkObservation[] }): LinkObservation[] {
  // A server's intentionally empty current state must not revive historical rows.
  // Older servers supply only history: retain explicit measurement evidence alone.
  return state.currentLinks ?? state.links.filter(link => link.observedAt != null);
}
