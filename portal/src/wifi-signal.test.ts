import test from 'node:test';
import assert from 'node:assert/strict';
import { wifiSignalLabel } from './wifi-signal.ts';
import { sdHealthLabel } from './sd-health.ts';

test('gateway card distinguishes small SD use, measured signal, outage and stale observations', () => {
  const now = Date.now(), t = new Date(now).toISOString();
  assert.match(sdHealthLabel({flags:15,dropped:0,usedBytes:'393216',totalBytes:'31902400512',
    measuredAt:t,receivedAt:t,intervalSeconds:86400},now,true), /<0.1% used \(384 KiB of 29.7 GiB\)/);
  const signal = {state:'measured' as const,rssiDbm:-62,channel:11,measuredAt:t,receivedAt:t,intervalSeconds:300};
  assert.match(wifiSignalLabel(signal,now,true), /^Wi-Fi signal · -62 dBm · channel 11/);
  assert.match(wifiSignalLabel(signal,now+900000,true), /^Last known/);
  assert.match(wifiSignalLabel({...signal,state:'disconnected',rssiDbm:null,channel:null},now,true), /disconnected/);
  assert.match(wifiSignalLabel({...signal,measuredAt:null},now,true), /Last known.*source time unknown/);
});
