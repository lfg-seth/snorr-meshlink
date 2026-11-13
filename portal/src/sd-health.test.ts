import test from 'node:test';
import assert from 'node:assert/strict';
import { sdHealthLabel } from './sd-health.ts';

test('daily cadence, full rotating storage, unknown capacity and feed outage', () => {
  const t = Date.parse('2026-11-12T20:00:00Z');
  const data = {flags:15,usedBytes:'32000000000',totalBytes:'32000000000',dropped:0,
    measuredAt:new Date(t).toISOString(),receivedAt:new Date(t).toISOString(),intervalSeconds:86400};
  assert.match(sdHealthLabel(data,t+86400000,true), /^Logging · 100.0% used/);
  assert.match(sdHealthLabel(data,t+3*86400000,true), /^Last known/);
  assert.match(sdHealthLabel(data,t,false), /^Last known/);
  assert.match(sdHealthLabel({...data,flags:3,usedBytes:null,totalBytes:null},t,true), /Write failed · capacity unknown/);
  assert.match(sdHealthLabel({...data,measuredAt:null},t,true), /source time unknown/);
  assert.match(sdHealthLabel(null,t,true), /awaiting daily report/);
});
