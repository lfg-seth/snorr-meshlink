import assert from 'node:assert/strict';
import test from 'node:test';
import type { Infrastructure, Tracker } from './demo.ts';
import type { LinkObservation } from './NeighborTable.tsx';
import { signalColor, signalConnections, signalValue } from './signal-links.ts';

test('late SNNS delivery keeps the later report sequence without inventing a hearing time', () => {
  const early = row({ id: 'early', source: 'neighbor', reportType: 'snns-v1', bootId: 10,
    sequence: 1, observedAt: null, receivedAt: '2026-10-16T20:05:00.000Z', snrDb: 10 });
  const late = row({ id: 'late', source: 'neighbor', reportType: 'snns-v1', bootId: 10,
    sequence: 2, observedAt: null, receivedAt: '2026-10-16T20:00:00.000Z', snrDb: 0 });
  const result = signalConnections([early, late], [tracker], [receiver]);
  assert.equal(result.connections[0].snrDb, 0);
  assert.equal(result.connections[0].latest[0].observedAt, null);
});

const tracker: Tracker = { id: 'd1', number: '001', shortName: 'S001', battery: null, history: [],
  position: { longitude: -115.65, latitude: 36.27, measuredAt: null, receivedAt: '2026-10-16T12:00:00Z' } };
const receiver = { id: 'r1', name: 'R001', longitude: -115.66, latitude: 36.28, deploymentStatus: 'planned' } as Infrastructure;
const row = (changes: Partial<LinkObservation> = {}): LinkObservation => ({ id: 'one',
  observerDeviceId: 'r1', heardDeviceId: 'd1', originalSourceDeviceId: 'd1',
  source: 'gateway', path: 'direct', snrDb: 8, rssiDbm: -88,
  observedAt: '2026-10-16T12:00:00Z', receivedAt: '2026-10-16T12:01:00Z', ...changes });

test('one line per pair preserves direction, report sources and weaker reverse SNR', () => {
  const rows = [row(), row({ id: 'neighbor', source: 'neighbor', snrDb: 5, observedAt: null }),
    row({ id: 'reverse', observerDeviceId: 'd1', heardDeviceId: 'r1', source: 'neighbor', snrDb: -2, rssiDbm: null })];
  const { connections, omitted } = signalConnections(rows, [tracker], [receiver]);
  assert.equal(omitted, 0);
  assert.equal(connections.length, 1);
  const connection = connections[0];
  assert.equal(connection.latest.length, 3);
  assert.equal(connection.snrDb, -2);
  assert.equal(connection.color, signalColor(-2));
  assert.equal(connection.relationship, 'S001 ↔ R001');
  assert.equal(signalConnections([...rows].reverse(), [tracker], [receiver]).connections[0].id, connection.id);
  assert.equal(connection.nodes[1].location, 'Planned location · installation unverified');
  assert.equal(connection.nodes[0].measuredAt, null);
});

test('late delivery does not replace a newer hearing; latest missing signal never borrows old strength', () => {
  const older = row({ id: 'late', receivedAt: '2026-10-16T12:10:00Z' });
  const newer = row({ id: 'new', observedAt: '2026-10-16T12:02:00Z', receivedAt: '2026-10-16T12:03:00Z', snrDb: null });
  const { connections } = signalConnections([older, newer], [tracker], [receiver]);
  assert.equal(connections[0].latest[0].id, 'new');
  assert.equal(connections[0].observations.length, 2);
  assert.equal(connections[0].snrDb, null);
  assert.equal(connections[0].relationship, 'S001 → R001');
  assert.equal(connections[0].color, signalColor(null));
});

test('unknown radio endpoints do not become original-source links; invalid or absent coordinates are omitted', () => {
  const rows = [row({ heardDeviceId: null }), row({ id: 'unknown', heardDeviceId: 'other' }),
    row({ id: 'self', heardDeviceId: 'r1' })];
  assert.deepEqual(signalConnections(rows, [tracker], [receiver]), { connections: [], relationships: [], omitted: 3 });
  for (const position of [null, { ...tracker.position!, longitude: NaN }, { ...tracker.position!, latitude: 91 }]) {
    const result = signalConnections([row()], [{ ...tracker, position }], [receiver]);
    assert.equal(result.omitted, 1);
    assert.equal(result.connections.length, 0);
    assert.equal(result.relationships.length, 1, 'known relationships remain available without a mapped endpoint');
    assert.equal(result.relationships[0].nodes[0].coordinates, null);
    assert.equal(result.relationships[0].nodes[0].location, 'Location unknown');
  }
  assert.equal(signalConnections([row()], [tracker], [{ ...receiver, latitude: undefined }]).omitted, 1);
  const relayed = signalConnections([row({ path: 'relayed', originalSourceDeviceId: 'd2' })], [tracker], [receiver]);
  assert.deepEqual(relayed.connections[0].nodes.map(node => node.id), ['d1', 'r1']);
});

test('zero and negative signals survive; colors are display bands and unknown stays neutral', () => {
  for (const snr of [0, -4.5, 5]) {
    assert.equal(signalConnections([row({ snrDb: snr })], [tracker], [receiver]).connections[0].snrDb, snr);
  }
  assert.equal(signalValue(0, 'dB'), '0 dB');
  assert.equal(signalValue(null, 'dB'), 'Unknown');
  assert.equal(signalValue(NaN, 'dBm'), 'Unknown');
  assert.equal(signalConnections([row({ snrDb: Infinity })], [tracker], [receiver]).connections[0].snrDb, null);
  assert.equal(new Set([signalColor(null), signalColor(-1), signalColor(0), signalColor(5)]).size, 4);
});
