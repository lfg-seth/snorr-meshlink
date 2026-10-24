import test from 'node:test';
import assert from 'node:assert/strict';
import { currentSamples } from './current.ts';
import { historyCurve, historySegments } from './battery-curve.ts';

test('current plots retain signed and zero measurements and disconnect missing intervals', () => {
  const now = Date.parse('2026-10-24T20:00:00Z');
  const samples = currentSamples([
    { at: '2026-10-24T19:40:00Z', milliamps: -40 },
    { at: '2026-10-24T19:45:00Z', milliamps: 0 },
    { at: '2026-10-24T19:59:00Z', milliamps: 80 },
    { at: '2026-10-24T19:59:00Z', milliamps: 90 },
    { at: '2026-10-24T20:01:00Z', milliamps: 100 },
    { at: 'unknown', milliamps: 12 },
    { at: '2026-10-24T19:50:00Z', milliamps: NaN },
  ], now);
  assert.deepEqual(samples.map(s => s.milliamps), [-40, 0, 90]);
  assert.deepEqual(historySegments(samples, 9).map(s => s.length), [2, 1]);
  assert.deepEqual(historySegments(samples, 0).map(s => s.length), [1, 1, 1]);
  const path = historyCurve(samples, 9, t => (t - now) / 60000, s => s.milliamps);
  assert.match(path, /^M-20.00,-40.00C/);
  assert.ok(path.endsWith('-15.00,0.00'));
});
