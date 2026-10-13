import assert from 'node:assert/strict';
import test from 'node:test';
import {
  assignDevice,
  historyConnections,
  historyInRange,
  telemetryState,
} from './demo.ts';
import type { Assignment, Fix } from './demo.ts';
const at = '2026-10-13T12:00:00Z';
const now = Date.parse(at);
const assignments: Assignment[] = [
  {
    id: '1',
    deviceId: 'd1',
    memberId: 'm1',
    startedAt: '2026-10-13T10:00:00Z',
    endedAt: null,
  },
  {
    id: '2',
    deviceId: 'd2',
    memberId: 'm2',
    startedAt: '2026-10-13T10:00:00Z',
    endedAt: null,
  },
];
test('admin transfer closes both conflicting associations and preserves past attribution', () => {
  const result = assignDevice(assignments, 'd1', 'm2', at, true);
  assert.equal(result.filter((a) => !a.endedAt).length, 1);
  assert.equal(result[0].memberId, 'm1');
  assert.equal(result[0].endedAt, at);
  assert.equal(result[1].endedAt, at);
  assert.equal(result[2].deviceId, 'd1');
  assert.equal(assignments[0].endedAt, null);
});
test('member self-claim rejects occupied devices and a second active tracker', () => {
  assert.throws(() => assignDevice(assignments, 'd1', 'm3', at, false));
  assert.throws(() => assignDevice(assignments, 'd3', 'm1', at, false));
  assert.equal(assignDevice(assignments, 'd3', 'm3', at, false).length, 3);
  assert.equal(assignDevice(assignments, 'd1', 'm1', at, false), assignments);
});
function fix(minutes: number): Fix {
  return {
    measuredAt: new Date(now - minutes * 60_000).toISOString(),
    receivedAt: at,
    longitude: -115.6,
    latitude: 36.2,
  };
}
test('history sorts recorded points, filters by measurement time and breaks long gaps', () => {
  const points = historyInRange(
    [
      fix(1),
      fix(35),
      fix(20),
      fix(260),
      { ...fix(4), measuredAt: null },
      fix(-1),
    ],
    now,
    4,
  );
  assert.deepEqual(
    points.map((f) => f.measuredAt),
    [fix(35), fix(20), fix(1)].map((f) => f.measuredAt),
  );
  assert.equal(historyConnections(points).length, 1); // 15 minutes included; 19 minutes excluded.
});
test('infrastructure freshness uses its cadence and preserves never-reported state', () => {
  assert.equal(telemetryState(null, now, 5), 'Awaiting first report');
  assert.equal(telemetryState(fix(14).measuredAt, now, 5), 'Current reading');
  assert.equal(telemetryState(fix(15).measuredAt, now, 5), 'Stale reading');
  assert.equal(telemetryState(fix(7).measuredAt, now, 2), 'Stale reading');
});
