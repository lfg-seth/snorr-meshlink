import assert from 'node:assert/strict';
import test from 'node:test';
import type { Tracker } from './demo.ts';
import { demoStartedAt, demoTrackersAt, initialTrackers } from './demo.ts';
import { clockTimeLabel, minuteAgeLabel, observationLabel, trackerMapLabel, trackerStatus } from './tracker.ts';

const now = Date.parse('2026-10-15T12:00:00Z');
const at = (seconds: number) => new Date(now - seconds * 1000).toISOString();
const tracker: Tracker = { id: 'd1', number: '001', shortName: 'S001', battery: 42,
  position: { latitude: 36.2, longitude: -115.6, measuredAt: at(0), receivedAt: at(0) }, history: [] };

test('Avery stays fully charged with fresh demo GPS after long or interrupted viewing', () => {
  const original = structuredClone(initialTrackers);
  for (const elapsed of [0, 59_999, 120_000, 3 * 60 * 60_000, 24 * 60 * 60_000]) {
    const time = demoStartedAt + elapsed;
    const trackers = demoTrackersAt(time);
    const avery = trackers[0];
    const age = time - Date.parse(avery.position!.measuredAt!);
    assert.equal(avery.battery, 100);
    assert.ok(age >= 0 && age < 120_000);
    assert.equal(trackerStatus(avery, time).label, 'Active');
    assert.equal(avery.lastContactAt, avery.position!.receivedAt);
    assert.deepEqual(trackers.slice(1), original.slice(1));
  }
  assert.deepEqual(initialTrackers, original);
});

test('tracker status is based on GPS time, retains old coordinates and crosses exact boundaries', () => {
  for (const [age, label] of [[0, 'Active'], [119, 'Active'], [120, 'Recent'], [899, 'Recent'],
    [900, 'Stale'], [7200, 'Stale'], [7201, 'No Location']] as const) {
    const device = { ...tracker, position: { ...tracker.position!, measuredAt: at(age) } };
    assert.equal(trackerStatus(device, now).label, label);
    assert.equal(device.position.latitude, 36.2);
  }
  for (const measuredAt of [null, 'invalid', at(-1)])
    assert.equal(trackerStatus({ ...tracker, position: { ...tracker.position!, measuredAt } }, now).label, 'No Location');
  assert.equal(trackerStatus({ ...tracker, position: null }, now).label, 'No Location');
});

test('age labels use whole minutes, cap over two hours and never substitute receipt time', () => {
  for (const [age, label] of [[0, '0 min'], [59, '0 min'], [60, '1 min'], [119, '1 min'],
    [7200, '120 min'], [7201, '+2hrs'], [86400, '+2hrs']] as const)
    assert.equal(minuteAgeLabel(at(age), now), label);
  for (const value of [null, undefined, 'invalid', at(-1)]) {
    assert.equal(minuteAgeLabel(value, now), 'Unknown');
    assert.equal(observationLabel(value, now), 'Unknown');
  }
  assert.match(observationLabel(at(65), now), / · 1 min ago$/);
  assert.match(observationLabel(at(10000), now), / · \+2hrs$/);
});

test('map shortnames follow active assignments without changing radio names', () => {
  const members = [{ id: 'm1', name: 'Demo One', initials: 'DO', shortName: 'ONE' },
    { id: 'm2', name: 'Demo Two', initials: 'DT', shortName: 'TWO' }];
  const assignment = { id: 'a1', deviceId: 'd1', memberId: 'm1', startedAt: at(60), endedAt: null };
  assert.equal(trackerMapLabel(tracker, [assignment], members), 'ONE');
  assert.equal(trackerMapLabel(tracker, [{ ...assignment, memberId: 'm2' }], members), 'TWO');
  assert.equal(trackerMapLabel(tracker, [{ ...assignment, endedAt: at(0) }], members), 'S001');
  assert.equal(trackerMapLabel(tracker, [assignment], [{ ...members[0], shortName: 'TOOLONG' }]), 'TOOLO');
  assert.equal(trackerMapLabel(tracker, [assignment], [{ ...members[0], shortName: '' }]), 'S001');
  assert.equal(tracker.shortName, 'S001');
});

test('clock-only labels omit elapsed age while duration preserves the observed GPS span', () => {
  const label = clockTimeLabel(at(99 * 60));
  assert.equal(label, new Date(at(99 * 60)).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
  assert.doesNotMatch(label, /ago|min|hrs/);
  assert.equal(clockTimeLabel(null), 'Unknown');
  assert.equal(clockTimeLabel('invalid'), 'Unknown');
});
