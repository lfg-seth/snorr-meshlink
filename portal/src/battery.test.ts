import assert from 'node:assert/strict';
import test from 'node:test';
import { batterySamples, batteryTrend, batteryPower, batteryCurrent } from './battery.ts';
const now = Date.parse('2026-10-15T12:00:00Z');
const sample = (minutes: number, volts: number) => ({
  at: new Date(now - minutes * 60000).toISOString(),
  volts,
});
test('trend uses elapsed time for irregular reports and both directions', () => {
  for (const sign of [-1, 1]) {
    const samples = [30, 11, 0].map((m) =>
      sample(m, 4 - ((sign * m) / 60) * 0.06),
    );
    const result = batteryTrend(samples.reverse(), now, 45);
    assert.ok(Math.abs(result.rate! - sign * 60) < 0.00001);
    assert.equal(
      result.label,
      sign > 0 ? 'Charging' : 'Discharging',
    );
  }
});
test('flat voltage is steady; sparse history cannot produce a rate', () => {
  assert.equal(
    batteryTrend([sample(20, 4), sample(10, 4), sample(0, 4)], now, 30).label,
    'Steady',
  );
  for (const samples of [
    [],
    [sample(0, 4)],
    [sample(20, 4), sample(0, 3.9)],
    [sample(2, 4), sample(1, 3.9), sample(0, 3.8)],
  ])
    assert.equal(batteryTrend(samples, now, 30).rate, null);
});
test('trend never bridges an outage or uses reports older than one hour', () => {
  const samples = [sample(50, 4.2), sample(40, 4.1), sample(0, 3.9)];
  assert.equal(batteryTrend(samples, now, 30).rate, null);
  assert.equal(
    batteryTrend([sample(90, 4.2), sample(70, 4.1), sample(0, 3.9)], now, 120)
      .rate,
    null,
  );
});
test('invalid, future and duplicate timestamps cannot distort the fit', () => {
  const clean = batterySamples(
    [
      sample(10, 4),
      sample(0, 3.9),
      sample(0, 3.95),
      sample(-1, 4.5),
      sample(20, NaN),
      { at: 'unknown', volts: 4 },
      sample(30, 0),
    ],
    now,
  );
  assert.deepEqual(clean, [sample(10, 4), sample(0, 3.95)]);
});

test('EVE estimate is nonlinear, rounded and restricted to configured 1S batteries', async () => {
  const { batteryChargeEstimate: estimate } = await import('./battery.ts');
  const device = { id: 'r001', battery: 3.58 };
  assert.equal(estimate(device).percent, 45);
  assert.equal(estimate({ ...device, battery: 4.2 }).percent, 100);
  assert.equal(estimate({ ...device, battery: 2.5 }).percent, 0);
  assert.equal(estimate({ ...device, battery: 2.4 }).percent, 0);
  assert.equal(estimate({ ...device, battery: 3.69 }).percent, 60);
  for (const battery of [null, NaN, Infinity, 0, -1, 5, 8.4])
    assert.equal(estimate({ ...device, battery }).percent, null);
  assert.equal(estimate({ ...device, id: 'g001' }).percent, null);
  assert.equal(
    estimate({ ...device, batteryProfile: 'unknown' }).percent,
    null,
  );
  assert.equal(
    estimate({ ...device, id: 'custom', batteryProfile: 'eve-26v-1s' }).percent,
    45,
  );
  let previous = -1;
  for (let battery = 2.5; battery <= 4.2; battery += 0.01) {
    const percent = estimate({ ...device, battery }).percent!;
    assert.ok(percent >= previous && percent >= 0 && percent <= 100);
    assert.equal(percent % 5, 0);
    previous = percent;
  }
});


const reading = (metric: string, value: number, marked = true) => ({
  metric, value, measuredAt: sample(0, 4).at, receivedAt: sample(0, 4).at,
  timestampQuality: 'valid', ...(marked ? { currentConvention: 'positive-charging' as const } : {}),
});

test('current selection uses the INA219 channel or legacy source without arbitrary channel fallback', () => {
  const primary = reading('power1CurrentMa', 0);
  const legacy = reading('sensorCurrentMa', -32);
  assert.equal(batteryCurrent([legacy, primary]), primary);
  assert.equal(batteryCurrent([legacy]), legacy);
  for (const rows of [[], [reading('power3CurrentMa', 10)],
    [primary, reading('power2CurrentMa', 10)], [reading('power1CurrentMa', NaN), legacy],
    [reading('power1CurrentMa', Infinity)], [primary, primary]]) assert.equal(batteryCurrent(rows), null);
});

test('power keeps measured signs/zero but requires confirmed convention for direction', () => {
  const device = { cadenceMinutes: 15, samples: [] };
  for (const [value, label, amount] of [[125.25, 'Charging', '+125.3 mA'],
    [-32, 'Discharging', '-32.0 mA'], [0, 'Steady', '0.0 mA']] as const) {
    const power = batteryPower({ ...device, powerReadings: [reading('power1CurrentMa', value)] }, now);
    assert.equal(power.label, `${label} (sensor path)`);
    assert.equal(power.amount, amount);
    const unmarked = batteryPower({ ...device, powerReadings: [reading('power1CurrentMa', value, false)] }, now);
    assert.equal(unmarked.label, 'Unknown');
    assert.equal(unmarked.amount, amount);
  }
});

test('voltage trend is explicitly an estimate and never supplies mA', () => {
  for (const sign of [-1, 1]) {
    const device = { cadenceMinutes: 15, samples: [20, 10, 0].map(m => sample(m, 4 - sign * m * .001)) };
    const power = batteryPower(device, now);
    assert.equal(power.label, `${sign > 0 ? 'Charging' : 'Discharging'} (voltage estimate)`);
    assert.equal(power.amount, 'Unknown');
    assert.equal(power.trendAt, sample(0, 4).at);
  }
});
