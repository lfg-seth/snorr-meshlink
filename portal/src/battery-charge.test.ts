import test from 'node:test';
import assert from 'node:assert/strict';
import { batteryChargeEstimate, memberBatteryState } from './battery-charge.ts';

test('LiPo estimate is explicit, bounded, nonlinear and rounded', () => {
  const device = { id: 'b001', battery: 3.72, batteryProfile: 'lipo-1s' };
  assert.equal(batteryChargeEstimate(device).percent, 50);
  assert.equal(batteryChargeEstimate({ ...device, battery: 4.2 }).percent, 100);
  assert.equal(batteryChargeEstimate({ ...device, battery: 3.1 }).percent, 0);
  assert.equal(batteryChargeEstimate({ ...device, battery: 3.76 }).percent, 55);
  assert.equal(batteryChargeEstimate({ ...device, batteryProfile: 'unknown' }).percent, null);
  for (const battery of [null, NaN, Infinity, 0, -1, 5, 8.4])
    assert.equal(batteryChargeEstimate({ ...device, battery }).percent, null);
  let previous = -1;
  for (let battery = 3.1; battery <= 4.2; battery += 0.01) {
    const percent = batteryChargeEstimate({ ...device, battery }).percent!;
    assert.ok(percent >= previous && percent >= 0 && percent <= 100);
    assert.equal(percent % 5, 0);
    previous = percent;
  }
  assert.equal(batteryChargeEstimate({ id: 'r001', battery: 3.58 }).percent, 45);
});

test('battery freshness prefers its measurement clock and falls back to its own receipt', () => {
  const now = Date.parse('2026-10-15T12:00:00Z');
  const device = { id: 'b001', batteryVoltage: 3.72, batteryProfile: 'lipo-1s',
    batteryMeasuredAt: '2026-10-15T11:45:00Z' };
  assert.equal(memberBatteryState(device, now, true).status, 'Stale battery reading');
  assert.match(memberBatteryState(device, now, false).status, /offline/);
  assert.match(memberBatteryState({ ...device, batteryMeasuredAt: null }, now, true).status, /Awaiting/);
  assert.match(memberBatteryState({ ...device, batteryMeasuredAt: '2026-10-15T12:01:00Z' }, now, true).status, /Awaiting/);
  const received = { ...device, batteryReceivedAt: '2026-10-15T11:59:00Z' };
  assert.equal(memberBatteryState(received, now, true).status, 'Stale battery reading');
  for (const batteryMeasuredAt of [null, 'bad', '2026-10-15T12:01:00Z'])
    assert.equal(memberBatteryState({ ...received, batteryMeasuredAt }, now, true).status, 'Recorded voltage');
  assert.equal(memberBatteryState({ ...device, batteryProfile: undefined }, now, true).percent, null);
});
