import test from 'node:test';
import assert from 'node:assert/strict';
import { telemetryTime, metricTime } from './telemetry-time.ts';

test('telemetry uses valid calendar time before receipt, with no node-contact fallback', () => {
  const now = Date.parse('2026-10-21T22:00:00Z');
  const measured = '2026-10-21T20:00:00Z';
  const received = '2026-10-21T21:59:00Z';
  assert.equal(telemetryTime(measured, received, now), measured);
  for (const clock of [null, undefined, 'bad', '2026-10-21T22:01:00Z'])
    assert.equal(telemetryTime(clock, received, now), received);
  assert.equal(telemetryTime(null, '2026-10-21T22:01:00Z', now), null);
  const device = { reportedAt: received, readingTimes: { battery: null, temperature: measured },
    readingReceivedTimes: { battery: received, temperature: received } };
  assert.equal(metricTime(device, 'battery', now), received);
  assert.equal(metricTime(device, 'temperature', now), measured);
  assert.equal(metricTime(device, 'humidity', now), null);
  assert.equal(metricTime({ reportedAt: received }, 'battery', now), received);
});
