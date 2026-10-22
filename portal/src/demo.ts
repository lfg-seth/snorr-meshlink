import type { Position } from './position';
import { telemetryTime } from './telemetry-time.ts';

export type Fix = Position & {
  longitude: number;
  latitude: number;
  areaName?: string | null;
  pdop?: number | null;
  satellites?: number | null;
};
export type Tracker = {
  id: string;
  number: string;
  shortName: string;
  deviceType?: string | null;
  battery: number | null;
  batteryVoltage?: number | null;
  batteryMeasuredAt?: string | null;
  batteryReceivedAt?: string | null;
  batteryTimestampQuality?: 'valid' | 'unknown' | 'invalid' | 'future';
  batteryProfile?: string;
  batteryCapacityMah?: number | null;
  position: Fix | null;
  history: Fix[];
  lastContactAt?: string | null;
};
export type Member = { id: string; name: string; initials: string; shortName?: string };
export type Assignment = {
  id: string;
  deviceId: string;
  memberId: string;
  startedAt: string;
  endedAt: string | null;
};
export type NameJob = {
  id?: string;
  assignmentId: string;
  deviceId: string;
  longName: string;
  status: 'pending' | 'confirmed' | 'failed';
};
export type Message = {
  direction?: string;
  authorId?: string;
  id: string;
  author: string;
  text: string;
  at: string;
  evidence: string;
};
export type Infrastructure = {
  id: string;
  name: string;
  role: 'Repeater' | 'Backhaul';
  deploymentStatus?: string;
  lastContactAt?: string | null;
  downlink?: boolean;
  longitude?: number;
  latitude?: number;
  reportedAt: string | null;
  cadenceMinutes: number;
  battery: number | null;
  // Signed battery current: positive charging, negative discharging.
  batteryCurrentMa?: number | null;
  powerReadings?: { metric: string; value: number; measuredAt: string | null;
    receivedAt: string; timestampQuality: string }[];
  temperature: number | null;
  humidity?: number | null;
  solar: number | null;
  intrusion: boolean | null;
  equipped: { solar: boolean; weather: boolean; intrusion: boolean };
  batterySetup: string;
  batteryProfile?: string;
  solarSetup: string;
  antenna: string;
  samples: { at: string; volts: number }[];
  readingTimes?: Record<string, string | null>;
  readingReceivedTimes?: Record<string, string | null>;
  reportCadenceMinutes?: Record<string, number>;
  missingTimeoutMinutes?: Record<string, number>;
  disabledMonitoring?: string[];
};
export type Incident = {
  id: string;
  deviceId: string;
  openedAt: string;
  acknowledgedAt: string | null;
  resolvedAt: string | null;
  note: string;
};
export type AuditEvent = {
  id: string;
  deviceId: string;
  at: string;
  text: string;
};
export type BatteryRule = {
  trigger: number;
  recovery: number;
  enabled?: boolean;
};

export const demoStartedAt = Date.now();
export function minutesAgo(minutes: number) {
  return new Date(demoStartedAt - minutes * 60_000).toISOString();
}
export const members: Member[] = [
  { id: 'm1', name: 'Demo Avery', initials: 'DA', shortName: 'AVERY' },
  { id: 'm2', name: 'Demo Jordan', initials: 'DJ', shortName: 'JORD' },
  { id: 'm3', name: 'Demo Morgan', initials: 'DM', shortName: 'MORG' },
  { id: 'm4', name: 'Demo Riley', initials: 'DR', shortName: 'RILEY' },
  { id: 'm5', name: 'Demo Casey', initials: 'DC', shortName: 'CASEY' },
];
const coordinates = [
  [-115.633, 36.265],
  [-115.65, 36.274],
  [-115.662, 36.281],
  [-115.684, 36.27],
  [-115.674, 36.293],
];
export const initialTrackers: Tracker[] = [1, 3, 8, 17, null, undefined].map(
  (minutes, i) => {
    const [longitude, latitude] = coordinates[i] ?? [0, 0];
    const history: Fix[] =
      typeof minutes === 'number'
        ? [95, 90, 85, 42, 37, 32, minutes].map((age, j) => ({
            longitude: longitude - 0.002 * (6 - j),
            latitude: latitude - 0.001 * (6 - j),
            measuredAt: minutesAgo(age),
            receivedAt: minutesAgo(Math.max(0, age - 0.1)),
          }))
        : [];
    return {
      id: `d${i + 1}`,
      deviceType: 'Heltec V4',
      number: String(i + 1).padStart(3, '0'),
      shortName: `S${String(i + 1).padStart(3, '0')}`,
      battery: [100, 67, 54, 31, null, null][i],
      history,
      position:
        minutes === undefined
          ? null
          : {
              longitude,
              latitude,
              // Fictional quality examples belong only to the standalone demo.
              pdop: [1.8, 4.5, 8, null, null][i],
              satellites: [9, 7, 5, null, null][i],
              measuredAt: minutes === null ? null : minutesAgo(minutes),
              receivedAt: minutesAgo(0.3),
            },
    };
  },
);
// Keep Avery's standalone demo active with a stationary simulated fix each
// minute. The other fixtures retain their original freshness scenarios.
export function demoTrackersAt(now: number): Tracker[] {
  const at = new Date(Math.floor(now / 60_000) * 60_000).toISOString();
  return initialTrackers.map((tracker) => tracker.id === 'd1' && tracker.position
    ? { ...tracker, position: { ...tracker.position, measuredAt: at, receivedAt: at }, lastContactAt: at }
    : tracker);
}
export const initialAssignments: Assignment[] = [0, 1, 2, 3].map((i) => ({
  id: `a${i}`,
  deviceId: `d${i + 1}`,
  memberId: `m${i + 1}`,
  startedAt: minutesAgo(110),
  endedAt: null,
}));
initialAssignments.unshift({
  id: 'a-old',
  deviceId: 'd1',
  memberId: 'm5',
  startedAt: minutesAgo(230),
  endedAt: minutesAgo(120),
});
export const initialMessages: Message[] = [
  {
    id: 'msg1',
    author: 'Demo Dispatch',
    text: 'Training scenario started. Check your tracker assignment before heading out.',
    at: minutesAgo(15),
    evidence: 'Simulated inbound',
  },
  {
    id: 'msg2',
    author: 'Demo Avery',
    text: 'Team Alpha at the trail junction. Continuing the training route.',
    at: minutesAgo(6),
    evidence: 'Simulated inbound',
  },
  {
    id: 'msg3',
    author: 'Demo Jordan',
    text: 'Copy. Team Bravo holding at the next checkpoint.',
    at: minutesAgo(3),
    evidence: 'Simulated inbound',
  },
];
export const infrastructure: Infrastructure[] = [
  {
    id: 'r1',
    name: 'Demo ridge relay',
    role: 'Repeater',
    longitude: -115.68,
    latitude: 36.31,
    reportedAt: minutesAgo(2),
    cadenceMinutes: 5,
    battery: 3.58,
    temperature: 8.4,
    solar: 1.2,
    intrusion: false,
    equipped: { solar: true, weather: true, intrusion: true },
    batterySetup: 'EVE 26V · 2 × 2550 mAh · 1S2P (demo)',
    batteryProfile: 'eve-26v-1s',
    solarSetup: '6 W panel (demo configuration)',
    antenna: 'Fiberglass (demo)',
    samples: Array.from({ length: 15 }, (_, i) => ({
      at: minutesAgo(72 - i * 5),
      volts: Number((3.72 - i * 0.01).toFixed(3)),
    })),
  },
  {
    id: 'r2',
    name: 'Demo canyon relay',
    role: 'Repeater',
    longitude: -115.617,
    latitude: 36.279,
    reportedAt: minutesAgo(22),
    cadenceMinutes: 5,
    battery: 3.9,
    temperature: null,
    solar: null,
    intrusion: null,
    equipped: { solar: true, weather: false, intrusion: false },
    batterySetup: 'EVE 26V · 4 × 2550 mAh · 1S4P (demo)',
    batteryProfile: 'eve-26v-1s',
    solarSetup: 'Panel configuration unknown',
    antenna: 'Muzi whip (demo)',
    samples: Array.from({ length: 9 }, (_, i) => ({
      at: minutesAgo(62 - i * 5),
      volts: Number((3.82 + i * 0.01).toFixed(3)),
    })),
  },
  {
    id: 'b1',
    name: 'Demo dispatch gateway',
    role: 'Backhaul',
    longitude: -115.64,
    latitude: 36.25,
    reportedAt: minutesAgo(1),
    cadenceMinutes: 2,
    battery: 4.05,
    temperature: null,
    solar: null,
    intrusion: null,
    equipped: { solar: false, weather: false, intrusion: false },
    batterySetup: 'LiPo · 1 cell · 1100 mAh whole pack · 1S (demo)',
    solarSetup: 'Not configured',
    antenna: 'Muzi whip (demo)',
    samples: [15, 10, 5, 1].map((m) => ({ at: minutesAgo(m), volts: 4.05 })),
  },
  {
    id: 'b2',
    name: 'Demo uplink gateway',
    role: 'Backhaul',
    longitude: -115.657,
    latitude: 36.303,
    reportedAt: null,
    cadenceMinutes: 2,
    battery: null,
    temperature: null,
    solar: null,
    intrusion: null,
    equipped: { solar: false, weather: false, intrusion: false },
    batterySetup: 'Battery configuration unknown',
    solarSetup: 'Not configured',
    antenna: 'Unknown / unconfigured',
    samples: [],
  },
];
export const initialIncidents: Incident[] = [
  {
    id: 'incident1',
    deviceId: 'r1',
    openedAt: minutesAgo(12),
    acknowledgedAt: null,
    resolvedAt: null,
    note: '',
  },
];
export const initialEvents: AuditEvent[] = [
  {
    id: 'evt1',
    deviceId: 'r1',
    at: minutesAgo(12),
    text: 'Simulated intrusion report: incident opened.',
  },
  {
    id: 'evt2',
    deviceId: 'r1',
    at: minutesAgo(2),
    text: 'Sensor reported normal. Open intrusion incident remains latched.',
  },
  {
    id: 'evt3',
    deviceId: 'r2',
    at: minutesAgo(22),
    text: 'Last simulated telemetry report received.',
  },
];

// End both sides of a transfer before creating its new dated association.
export function assignDevice(
  assignments: Assignment[],
  deviceId: string,
  memberId: string,
  at: string,
  admin: boolean,
): Assignment[] {
  if (
    assignments.some(
      (a) => !a.endedAt && a.deviceId === deviceId && a.memberId === memberId,
    )
  )
    return assignments;
  if (
    !admin &&
    assignments.some(
      (a) => !a.endedAt && (a.deviceId === deviceId || a.memberId === memberId),
    )
  )
    throw new Error(
      'Release your current tracker and choose an unassigned device.',
    );
  return [
    ...assignments.map((a) =>
      !a.endedAt && (a.deviceId === deviceId || a.memberId === memberId)
        ? { ...a, endedAt: at }
        : a,
    ),
    {
      id: `assignment-${deviceId}-${at}`,
      deviceId,
      memberId,
      startedAt: at,
      endedAt: null,
    },
  ];
}
export function historyInRange(fixes: Fix[], now: number, hours: number) {
  return fixes
    .filter(
      (f) =>
        f.measuredAt &&
        Date.parse(f.measuredAt) >= now - hours * 3_600_000 &&
        Date.parse(f.measuredAt) <= now,
    )
    .sort((a, b) => Date.parse(a.measuredAt!) - Date.parse(b.measuredAt!));
}
export function historyConnections(fixes: Fix[]): [Fix, Fix][] {
  return fixes.slice(1).flatMap((fix, i) => {
    const previous = fixes[i];
    if (!previous.measuredAt || !fix.measuredAt) return [];
    const gap = Date.parse(fix.measuredAt) - Date.parse(previous.measuredAt);
    return gap > 0 && gap <= 900_000 ? [[previous, fix] as [Fix, Fix]] : [];
  });
}
export function telemetryState(
  at: string | null,
  now: number,
  cadenceMinutes: number,
  receivedAt?: string | null,
) {
  const time = telemetryTime(at, receivedAt, now);
  if (!time) return 'Awaiting first report';
  return now - Date.parse(time) >= cadenceMinutes * 3 * 60_000
    ? 'Stale reading'
    : 'Current reading';
}
export function timeLabel(at: string | null) {
  return at
    ? new Date(at).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      })
    : 'Unknown';
}
export function ageLabel(seconds: number | null) {
  if (seconds === null) return 'Unknown';
  if (seconds < 60) return `${Math.floor(seconds)}s`;
  if (seconds < 3600)
    return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
}
