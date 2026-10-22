import type { LinkObservation } from './NeighborTable';

const MAX_SIGNAL_AGE_MS = 2 * 60 * 60 * 1000;
export const signalFreshnessHelp = 'Only signals with a known hearing time in the past two hours are shown. Reports without a hearing time are hidden.';

function timestamp(at: string | null): number {
  // A local clock string must not change meaning with the browser's time zone.
  return at && /(Z|[+-]\d\d:\d\d)$/.test(at) ? Date.parse(at) : NaN;
}

export function recentSignals(links: LinkObservation[], now: number): LinkObservation[] {
  return links.filter(link => {
    const heard = timestamp(link.observedAt);
    const received = timestamp(link.receivedAt);
    // Receipt is delivery evidence, never hearing evidence. SNNS hearing age
    // excludes unknown transport delay, so it cannot certify a two-hour limit.
    return Number.isFinite(now) && Number.isFinite(heard) && Number.isFinite(received) &&
      heard <= received && received <= now && now - heard < MAX_SIGNAL_AGE_MS;
  });
}
