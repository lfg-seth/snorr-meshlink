import assert from 'node:assert/strict';
import test from 'node:test';
import type { Fix, Tracker } from './demo.ts';
import { activeTimeLabel, latestRecordedSession, recordedTrailConnections } from './recorded-session.ts';

const now = Date.parse('2026-10-15T12:00:00Z');
const point = (minutes: number): Fix => ({ latitude: 36.2, longitude: -115.6,
  measuredAt: new Date(now - minutes * 60000).toISOString(), receivedAt: new Date(now).toISOString() });
const device = (history: Fix[], position: Fix | null = null): Tracker => ({
  id: 'd1', number: '001', shortName: 'S001', battery: 42, history, position,
});

test('latest recorded session splits only at gaps greater than two hours', () => {
  const history = [point(500), point(400), point(150), point(30), point(0)];
  const result = latestRecordedSession(device(history.reverse()), now);
  assert.deepEqual(result.points, [point(150), point(30), point(0)]);
  assert.equal(result.firstSeen, point(150).measuredAt);
  assert.equal(result.activeSeconds, 9000);
  assert.equal(activeTimeLabel(result.activeSeconds), '2h 30m');
  assert.equal(recordedTrailConnections(result.points).length, 2);
  assert.equal(recordedTrailConnections([point(150.01), point(30)]).length, 0);
});

test('current position joins loaded history, duplicates collapse, and input order is unchanged', () => {
  const history = [point(30), point(60), point(30)];
  const original = [...history];
  const result = latestRecordedSession(device(history, point(0)), now);
  assert.deepEqual(result.points, [point(60), point(30), point(0)]);
  assert.deepEqual(history, original);
  assert.equal(activeTimeLabel(result.activeSeconds), '1h 0m');
  assert.equal(latestRecordedSession(device([], point(4000)), now).points.length, 1);
});

test('unknown/future clocks and invalid coordinates cannot manufacture a session', () => {
  const invalid = [{ ...point(0), measuredAt: null }, { ...point(0), measuredAt: 'invalid' },
    point(-1), { ...point(0), latitude: NaN }, { ...point(0), longitude: 181 }];
  const result = latestRecordedSession(device(invalid), now);
  assert.deepEqual(result.points, []);
  assert.equal(result.firstSeen, null);
  assert.equal(result.activeSeconds, null);
  assert.equal(result.distanceMiles, null);
  assert.equal(activeTimeLabel(result.activeSeconds), 'Unknown');
  assert.equal(activeTimeLabel(59), '0 min');
  assert.equal(activeTimeLabel(120), '2 min');
});

test('session distance sums geographic legs in miles and excludes earlier sessions', () => {
  const start = { ...point(60), latitude: 0, longitude: 0 };
  const corner = { ...point(30), latitude: 0, longitude: 0.01 };
  const finish = { ...point(0), latitude: 0.01, longitude: 0.01 };
  const previousSession = { ...point(300), latitude: 45, longitude: 45 };
  const result = latestRecordedSession(device([previousSession, finish, start, corner]), now);
  assert.ok(Math.abs(result.distanceMiles! - 1.38187) < 0.0001);
  assert.equal(result.distanceMiles!.toFixed(1), '1.4');
  assert.equal(latestRecordedSession(device([start]), now).distanceMiles, 0);
  assert.equal(latestRecordedSession(device([start, { ...start, measuredAt: point(30).measuredAt }]), now).distanceMiles, 0);
  const acrossDateline = latestRecordedSession(device([
    { ...start, longitude: 179.99 }, { ...finish, latitude: 0, longitude: -179.99 },
  ]), now);
  assert.ok(Math.abs(acrossDateline.distanceMiles! - 1.38187) < 0.0001);
});
