import assert from 'node:assert/strict';
import test from 'node:test';
import { gpsQuality } from './gps-quality.ts';

test('coarse GPS quality uses explicit boundaries and never treats missing values as good', () => {
  for (const value of [0.01, 1.83, 2.82, 2.99]) assert.equal(gpsQuality(value), 'good');
  for (const value of [3, 4.5, 6]) assert.equal(gpsQuality(value), 'limited');
  for (const value of [6.01, 8, 99]) assert.equal(gpsQuality(value), 'poor');
  for (const value of [null, undefined, 0, -1, NaN, Infinity, -Infinity])
    assert.equal(gpsQuality(value), 'unknown');
  assert.equal(gpsQuality('1.83' as unknown as number), 'unknown');
});
