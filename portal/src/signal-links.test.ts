import assert from 'node:assert/strict';
import test from 'node:test';
import type { Infrastructure, Tracker } from './demo.ts';
import type { LinkObservation } from './NeighborTable.tsx';
import { signalColor, signalConnections, signalValue } from './signal-links.ts';

test('late timestamped SNNS delivery keeps the later report sequence', () => {
  const early = row({ id: 'early', source: 'neighbor', reportType: 'snns-v1', bootId: 10,
    sequence: 1, observedAt: '2026-10-16T20:01:00.000Z', receivedAt: '2026-10-16T20:05:00.000Z', snrDb: 10 });
  const late = row({ id: 'late', source: 'neighbor', reportType: 'snns-v1', bootId: 10,
    sequence: 2, observedAt: '2026-10-16T20:00:00.000Z', receivedAt: '2026-10-16T20:00:00.000Z', snrDb: 0 });
  const result = signalConnections([early, late], [tracker], [receiver], Date.parse('2026-10-16T20:15:00Z'));
  assert.equal(result.connections[0].snrDb, 0);
  assert.equal(result.connections[0].latest[0].observedAt, late.observedAt);
});

const tracker: Tracker = { id: 'd1', number: '001', shortName: 'S001', battery: null, history: [],
  position: { longitude: -115.65, latitude: 36.27, measuredAt: null, receivedAt: '2026-10-16T12:00:00Z' } };
const receiver = { id: 'r1', name: 'R001', longitude: -115.66, latitude: 36.28, deploymentStatus: 'planned' } as Infrastructure;
const now = Date.parse('2026-10-16T12:15:00Z');
const row = (changes: Partial<LinkObservation> = {}): LinkObservation => ({ id: 'one',
  observerDeviceId: 'r1', heardDeviceId: 'd1', originalSourceDeviceId: 'd1',
  source: 'gateway', path: 'direct', snrDb: 8, rssiDbm: -88,
  observedAt: '2026-10-16T12:00:00Z', receivedAt: '2026-10-16T12:01:00Z', ...changes });

test('one line per pair preserves direction, report sources and weaker reverse SNR', () => {
  const rows = [row(), row({ id: 'neighbor', source: 'neighbor', snrDb: 5 }),
    row({ id: 'reverse', observerDeviceId: 'd1', heardDeviceId: 'r1', source: 'neighbor', snrDb: -2, rssiDbm: null })];
  const { connections, omitted } = signalConnections(rows, [tracker], [receiver], now);
  assert.equal(omitted, 0);
  assert.equal(connections.length, 1);
  const connection = connections[0];
  assert.equal(connection.latest.length, 3);
  assert.equal(connection.snrDb, -2);
  assert.equal(connection.color, signalColor(-2));
  assert.equal(connection.relationship, 'S001 ↔ R001');
  assert.equal(signalConnections([...rows].reverse(), [tracker], [receiver], now).connections[0].id, connection.id);
  assert.equal(connection.nodes[1].location, 'Planned location · installation unverified');
  assert.equal(connection.nodes[0].measuredAt, null);
});

test('late delivery does not replace a newer hearing; latest missing signal never borrows old strength', () => {
  const older = row({ id: 'late', receivedAt: '2026-10-16T12:10:00Z' });
  const newer = row({ id: 'new', observedAt: '2026-10-16T12:02:00Z', receivedAt: '2026-10-16T12:03:00Z', snrDb: null });
  const { connections } = signalConnections([older, newer], [tracker], [receiver], now);
  assert.equal(connections[0].latest[0].id, 'new');
  assert.equal(connections[0].observations.length, 2);
  assert.equal(connections[0].snrDb, null);
  assert.equal(connections[0].relationship, 'S001 → R001');
  assert.equal(connections[0].color, signalColor(null));
});

test('unknown radio endpoints do not become original-source links; invalid or absent coordinates are omitted', () => {
  const rows = [row({ heardDeviceId: null }), row({ id: 'unknown', heardDeviceId: 'other' }),
    row({ id: 'self', heardDeviceId: 'r1' })];
  assert.deepEqual(signalConnections(rows, [tracker], [receiver], now), { connections: [], relationships: [], omitted: 3 });
  for (const position of [null, { ...tracker.position!, longitude: NaN }, { ...tracker.position!, latitude: 91 }]) {
    const result = signalConnections([row()], [{ ...tracker, position }], [receiver], now);
    assert.equal(result.omitted, 1);
    assert.equal(result.connections.length, 0);
    assert.equal(result.relationships.length, 1, 'known relationships remain available without a mapped endpoint');
    assert.equal(result.relationships[0].nodes[0].coordinates, null);
    assert.equal(result.relationships[0].nodes[0].location, 'Location unknown');
  }
  assert.equal(signalConnections([row()], [tracker], [{ ...receiver, latitude: undefined }], now).omitted, 1);
  const relayed = signalConnections([row({ path: 'relayed', originalSourceDeviceId: 'd2' })], [tracker], [receiver], now);
  assert.deepEqual(relayed.connections[0].nodes.map(node => node.id), ['d1', 'r1']);
});

test('zero and negative signals survive; colors are display bands and unknown stays neutral', () => {
  for (const snr of [0, -4.5, 5]) {
    assert.equal(signalConnections([row({ snrDb: snr })], [tracker], [receiver], now).connections[0].snrDb, snr);
  }
  assert.equal(signalValue(0, 'dB'), '0 dB');
  assert.equal(signalValue(null, 'dB'), 'Unknown');
  assert.equal(signalValue(NaN, 'dBm'), 'Unknown');
  assert.equal(signalConnections([row({ snrDb: Infinity })], [tracker], [receiver], now).connections[0].snrDb, null);
  assert.equal(new Set([signalColor(null), signalColor(-1), signalColor(0), signalColor(5)]).size, 4);
});

test('cached B002/G001 reports cannot refresh hearing freshness', () => {
  const now = Date.parse('2026-10-21T21:22:49.434Z');
  const b002 = { ...tracker, id: 'b002', shortName: 'B002' };
  const g001 = { ...receiver, id: 'g001', name: 'G001' };
  const cached = row({ id: 'standard', observerDeviceId: 'g001', heardDeviceId: 'b002',
    source: 'neighbor', reportType: 'neighbor-info', observedAt: null,
    receivedAt: '2026-10-21T20:46:49.434Z', snrDb: 6.25, rssiDbm: null });
  const richer = { ...cached, id: 'richer', reportType: 'snns-v1' as const,
    receivedAt: '2026-10-21T13:44:52.671Z', hearingAgeSeconds: 1772,
    observationCount: 314, bootId: 380571083, sequence: 524, reportUptimeSeconds: 39486 };
  assert.deepEqual(signalConnections([cached, richer], [b002], [g001], now),
    { connections: [], relationships: [], omitted: 0 });
});

test('two-hour cutoff uses hearing time and expires without another report', () => {
  const heard = Date.parse('2026-10-21T12:00:00Z');
  const rows = [row({ observedAt: new Date(heard).toISOString(),
    receivedAt: '2026-10-21T13:59:59Z' })];
  assert.equal(signalConnections(rows, [tracker], [receiver], heard + 7200000 - 1).relationships.length, 1);
  assert.equal(signalConnections(rows, [tracker], [receiver], heard + 7200000).relationships.length, 0);
  assert.equal(signalConnections(rows, [tracker], [receiver], heard + 7200001).connections.length, 0);
});

test('unknown, invalid, future and inconsistent clocks never become current signals', () => {
  const now = Date.parse('2026-10-21T14:00:00Z');
  for (const changes of [
    { observedAt: null },
    { observedAt: '' },
    { observedAt: 'invalid' },
    { observedAt: '2026-10-21T13:00:00' },
    { observedAt: '2026-10-21T14:01:00Z', receivedAt: '2026-10-21T14:01:00Z' },
    { observedAt: '2026-10-21T13:59:30Z', receivedAt: '2026-10-21T13:59:00Z' },
    { receivedAt: 'invalid' },
    { receivedAt: '2026-10-21T14:01:00Z' },
    // Even a zero hearing age cannot bound an unknown transport delay.
    { observedAt: null, source: 'neighbor' as const, reportType: 'snns-v1' as const,
      hearingAgeSeconds: 0, bootId: 1, sequence: 1, reportUptimeSeconds: 60 },
  ]) {
    const result = signalConnections([row({ observedAt: '2026-10-21T13:00:00Z',
      receivedAt: '2026-10-21T13:59:00Z', ...changes })], [tracker], [receiver], now);
    assert.equal(result.relationships.length, 0, JSON.stringify(changes));
  }
});

test('fresh table delivery cannot displace a verified signal or preserve an expired reverse direction', () => {
  const now = Date.parse('2026-10-21T14:00:00Z');
  const verified = row({ id: 'verified', source: 'neighbor', snrDb: 8,
    observedAt: '2026-10-21T13:00:00Z', receivedAt: '2026-10-21T13:01:00Z' });
  const rows = [verified, { ...verified, id: 'cached', reportType: 'neighbor-info' as const,
    snrDb: -10, observedAt: null, receivedAt: '2026-10-21T13:59:00Z' },
  { ...verified, id: 'reverse', observerDeviceId: 'd1', heardDeviceId: 'r1',
    snrDb: -20, observedAt: '2026-10-21T12:00:00Z', receivedAt: '2026-10-21T13:58:00Z' }];
  for (const input of [rows, [...rows].reverse()]) {
    const [connection] = signalConnections(input, [tracker], [receiver], now).connections;
    assert.deepEqual(connection.latest.map(link => link.id), ['verified']);
    assert.equal(connection.snrDb, 8);
    assert.equal(connection.relationship, 'S001 → R001');
    assert.equal(connection.observations.length, 1);
  }
});
