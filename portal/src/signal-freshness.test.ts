import assert from 'node:assert/strict';
import test from 'node:test';
import type { LinkObservation } from './NeighborTable.tsx';
import { currentSignalRows, signalFreshness } from './signal-freshness.ts';

const anchor = '2026-10-21T20:00:00Z';
const anchorMs = Date.parse(anchor);
const row: LinkObservation = { id: 'hearing', observerDeviceId: 'r1', heardDeviceId: 'd1',
  originalSourceDeviceId: null, source: 'neighbor', reportType: 'snns-v1', path: 'direct',
  snrDb: 0, rssiDbm: -90, observedAt: null, receivedAt: anchor,
  freshness: { basis: 'relative', anchorReceivedAt: anchor, ageAtAnchorSeconds: 30 } };

test('relative hearing age advances from the accepted anchor, never from the latest report receipt', () => {
  assert.deepEqual(signalFreshness(row, anchorMs), { basis: 'relative', ageSeconds: 30 });
  const redelivered = { ...row, receivedAt: '2026-10-21T21:00:00Z' };
  assert.deepEqual(signalFreshness(redelivered, anchorMs + 3600000), { basis: 'relative', ageSeconds: 3630 });
  assert.deepEqual(signalFreshness(redelivered, anchorMs + 7169999), { basis: 'relative', ageSeconds: 7199.999 });
  assert.equal(signalFreshness(redelivered, anchorMs + 7170000), null);
});

test('malformed, unanchored, future or standard cached reports cannot become current hearing evidence', () => {
  const bad: Partial<LinkObservation>[] = [
    { freshness: undefined },
    { reportType: 'neighbor-info', observedAt: anchor },
    { reportType: undefined },
    { receivedAt: '2026-10-21T21:00:01Z' },
    { receivedAt: '2026-10-21T20:00:00' },
    { freshness: { ...row.freshness!, anchorReceivedAt: '2026-10-21T20:00:01Z' } },
    { freshness: { ...row.freshness!, anchorReceivedAt: '2026-02-30T20:00:00Z' } },
    ...[-1, 0.5, 1800, Infinity, NaN].map(ageAtAnchorSeconds => ({
      freshness: { ...row.freshness!, ageAtAnchorSeconds },
    })),
  ];
  for (const change of bad) assert.equal(signalFreshness({ ...row, ...change }, anchorMs + 3600000), null,
    `invalid evidence: ${JSON.stringify(change)}`);
  assert.equal(signalFreshness(row, NaN), null);
  assert.equal(signalFreshness(row, anchorMs - 1), null);
});

test('explicit measurement evidence needs a valid zoned hearing at or before receipt and expires at two hours', () => {
  const measured = { ...row, source: 'gateway' as const, reportType: undefined, freshness: undefined,
    observedAt: '2026-10-21T13:00:00-07:00' };
  assert.deepEqual(signalFreshness(measured, anchorMs + 7199999), { basis: 'measured', ageSeconds: 7199.999 });
  assert.equal(signalFreshness(measured, anchorMs + 7200000), null);
  for (const observedAt of [null, '', 'invalid', '2026-10-21', '2026-10-21T20:00:00',
    '2026-02-30T20:00:00Z', '2026-10-21T20:00:01Z'])
    assert.equal(signalFreshness({ ...measured, observedAt }, anchorMs + 3600000), null, `${observedAt}`);
  assert.equal(signalFreshness({ ...measured, reportType: 'neighbor-info' }, anchorMs), null);
});

test('current state stays distinct from history, including an intentionally empty current set', () => {
  const links = [row, { ...row, id: 'measured', observedAt: anchor, freshness: undefined }];
  const currentLinks = [row];
  assert.equal(currentSignalRows({ links, currentLinks }), currentLinks);
  assert.deepEqual(currentSignalRows({ links, currentLinks: [] }), []);
  assert.deepEqual(currentSignalRows({ links }).map(link => link.id), ['measured'],
    'legacy history fallback does not turn raw relative reports into accepted current state');
});
