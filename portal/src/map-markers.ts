import type { Tracker } from './demo';
import { trackerStatus } from './tracker';

export function trackerMarkerClass(tracker: Tracker, now: number, selected = false) {
  return `map-pin ${trackerStatus(tracker, now).kind}${selected ? ' selected-pin' : ''}`;
}

export function infrastructureMarkerClass(selected = false) {
  return `infrastructure-pin${selected ? ' selected-pin' : ''}`;
}
