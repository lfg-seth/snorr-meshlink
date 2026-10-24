import assert from 'node:assert/strict';
import test from 'node:test';
import { gatewayHealthLabel } from './gateway-health.ts';

test('gateway badges expire retained snapshots and distinguish feed loss from radio receipt', () => {
  const now = Date.now();
  const report = { state: 'online', label: 'Wi-Fi and MQTT connected', radioAlive: true,
    transportGatewayId: 'g002', intervalSeconds: 180, measuredAt: new Date(now).toISOString() };
  assert.equal(gatewayHealthLabel(report, now, true).kind, 'recent');
  assert.match(gatewayHealthLabel(report, now, true).label, /radio alive via G002/);
  assert.equal(gatewayHealthLabel(report, now + 540000, true).label, 'Gateway health stale');
  assert.match(gatewayHealthLabel(report, now, false).label, /uncertain/);
  assert.equal(gatewayHealthLabel(report, now - 1, true).kind, 'neutral');
  assert.equal(gatewayHealthLabel(null, now, true).kind, 'neutral');
  assert.equal(gatewayHealthLabel({ ...report, state: 'wifi-lost', label: 'Wi-Fi disconnected' }, now, true).kind, 'old');
});
