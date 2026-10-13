import type { Tracker } from './demo';
import { positionAgeSeconds, positionStatus } from './position';
export function statusText(tracker: Tracker, now: number) {
  if (!tracker.position)
    return tracker.lastContactAt ? 'No GPS position' : 'Never seen';
  return {
    recent: 'Recent',
    aging: 'Aging',
    old: 'Older fix',
    stale: 'Stale',
    unknown: 'Unknown age',
  }[positionStatus(positionAgeSeconds(tracker.position, now))];
}
