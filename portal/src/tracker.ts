import type { Assignment, Member, Tracker } from './demo';
import { positionAgeSeconds } from './position.ts';
export function statusText(tracker: Tracker, now: number) {
  return trackerStatus(tracker, now).label;
}

export function trackerStatus(tracker: Tracker, now: number) {
  const age = tracker.position ? positionAgeSeconds(tracker.position, now) : null;
  if (age === null || age > 7200) return { label: 'No Location', kind: 'unknown' };
  if (age < 120) return { label: 'Active', kind: 'recent' };
  if (age < 900) return { label: 'Recent', kind: 'aging' };
  return { label: 'Stale', kind: 'stale' };
}

export function minuteAgeLabel(at: string | null | undefined, now: number) {
  const time = at ? Date.parse(at) : NaN;
  if (!Number.isFinite(time) || time > now) return 'Unknown';
  const seconds = (now - time) / 1000;
  return seconds > 7200 ? '+2hrs' : `${Math.floor(seconds / 60)} min`;
}

export function observationLabel(at: string | null | undefined, now: number) {
  const age = minuteAgeLabel(at, now);
  if (age === 'Unknown') return age;
  return `${clockTimeLabel(at)} · ${age}${age === '+2hrs' ? '' : ' ago'}`;
}

export function clockTimeLabel(at: string | null | undefined) {
  const time = at ? Date.parse(at) : NaN;
  return Number.isFinite(time)
    ? new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : 'Unknown';
}

export function trackerMapLabel(tracker: Tracker, assignments: Assignment[], members: Member[]) {
  const assignment = assignments.find((item) => item.deviceId === tracker.id && !item.endedAt);
  const shortName = members.find((member) => member.id === assignment?.memberId)?.shortName?.trim();
  return shortName ? Array.from(shortName).slice(0, 5).join('') : tracker.shortName;
}
