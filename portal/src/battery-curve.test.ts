import assert from 'node:assert/strict';
import test from 'node:test';
import { batteryCurve } from './battery-curve.ts';

test('curves stay within readings and leave telemetry outages disconnected', () => {
  const origin = Date.parse('2026-10-16T12:00:00Z');
  const samples = [[0, 4], [5, 4.2], [6, 3.7], [10, 3.9], [60, 3.6], [65, 3.8]]
    .map(([minute, volts]) => ({ at: new Date(origin + minute * 60000).toISOString(), volts }));
  const path = batteryCurve(samples, origin + 65 * 60000, 15, time => (time - origin) / 60000, v => v * 100);
  assert.equal(path.match(/M/g)?.length, 2, 'outage is a separate subpath');
  const curves = [...path.matchAll(/C([\d., -]+)/g)];
  let index = 0;
  for (const match of curves) {
    const values = match[1].trim().split(/[ ,]+/).map(Number);
    if (index === 3) index++;
    const low = Math.min(samples[index].volts, samples[index + 1].volts) * 100;
    const high = Math.max(samples[index].volts, samples[index + 1].volts) * 100;
    for (const y of [values[1], values[3], values[5]]) assert.ok(y >= low && y <= high);
    index++;
  }
  assert.equal(batteryCurve([samples[0]], origin, 15, x => x, y => y), '', 'single observation cannot invent a line');
});
