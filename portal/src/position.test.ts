import assert from 'node:assert/strict';
import test from 'node:test';
import { positionAgeSeconds, positionStatus } from './position.ts';

const now = Date.parse('2026-10-13T12:00:00Z');

test('a newly received old GPS measurement remains stale', () => {
  const age = positionAgeSeconds({ measuredAt: '2026-10-13T11:40:00Z', receivedAt: '2026-10-13T12:00:00Z' }, now);
  assert.equal(age, 1200);
  assert.equal(positionStatus(age), 'stale');
});

test('measurement age bands include the exact stale boundary', () => {
  for (const [age, expected] of [[0, 'recent'], [119, 'recent'], [120, 'aging'], [299, 'aging'], [300, 'old'], [899, 'old'], [900, 'stale']] as const) {
    assert.equal(positionStatus(age), expected);
  }
});

test('missing, invalid and future GPS times remain unknown', () => {
  for (const measuredAt of [null, '', 'invalid', '2026-10-13T12:01:00Z']) {
    const age = positionAgeSeconds({ measuredAt, receivedAt: '2026-10-13T12:00:00Z' }, now);
    assert.equal(age, null);
    assert.equal(positionStatus(age), 'unknown');
  }
});

test('the same position becomes stale as time passes without another packet', () => {
  const position = { measuredAt: '2026-10-13T11:50:00Z', receivedAt: '2026-10-13T11:50:02Z' };
  assert.equal(positionStatus(positionAgeSeconds(position, now)), 'old');
  assert.equal(positionStatus(positionAgeSeconds(position, now + 300_000)), 'stale');
});
