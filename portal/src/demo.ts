import type { Position } from './position';

export type Fix = Position & { longitude: number; latitude: number };
export type Tracker = {
  id: string;
  number: string;
  shortName: string;
  battery: number | null;
  position: Fix | null;
  history: Fix[];
};
export type Member = { id: string; name: string; initials: string };
export type Assignment = {
  id: string;
  deviceId: string;
  memberId: string;
  startedAt: string;
  endedAt: string | null;
};
export type NameJob = {
  assignmentId: string;
  deviceId: string;
  longName: string;
  status: 'pending' | 'confirmed' | 'failed';
};
export type Message = {
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
  longitude: number;
  latitude: number;
  reportedAt: string | null;
  cadenceMinutes: number;
  battery: number | null;
  temperature: number | null;
  solar: number | null;
  intrusion: boolean | null;
  equipped: { solar: boolean; weather: boolean; intrusion: boolean };
  batterySetup: string;
  solarSetup: string;
  antenna: string;
  samples: { at: string; volts: number }[];
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
export type BatteryRule = { trigger: number; recovery: number };

export const demoStartedAt = Date.now();
export function minutesAgo(minutes: number) {
  return new Date(demoStartedAt - minutes * 60_000).toISOString();
}
export const members: Member[] = [
  { id: 'm1', name: 'Demo Avery', initials: 'DA' },
  { id: 'm2', name: 'Demo Jordan', initials: 'DJ' },
  { id: 'm3', name: 'Demo Morgan', initials: 'DM' },
  { id: 'm4', name: 'Demo Riley', initials: 'DR' },
  { id: 'm5', name: 'Demo Casey', initials: 'DC' },
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
      number: String(i + 1).padStart(3, '0'),
      shortName: `S${String(i + 1).padStart(3, '0')}`,
      battery: [82, 67, 54, 31, null, null][i],
      history,
      position:
        minutes === undefined
          ? null
          : {
              longitude,
              latitude,
              measuredAt: minutes === null ? null : minutesAgo(minutes),
              receivedAt: minutesAgo(0.3),
            },
    };
  },
);
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
    batterySetup: '18650 Li-ion · 2 cells · 3000 mAh per cell · 1S2P (demo)',
    solarSetup: '6 W panel (demo configuration)',
    antenna: 'Fiberglass (demo)',
    samples: [70, 50, 30, 10, 2].map((m, i) => ({
      at: minutesAgo(m),
      volts: [3.95, 3.88, 3.72, 3.61, 3.58][i],
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
    batterySetup: 'Battery chemistry / cell count / capacity unknown',
    solarSetup: 'Panel configuration unknown',
    antenna: 'Muzi whip (demo)',
    samples: [{ at: minutesAgo(22), volts: 3.9 }],
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
) {
  if (!at) return 'Awaiting first report';
  return now - Date.parse(at) >= cadenceMinutes * 3 * 60_000
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
