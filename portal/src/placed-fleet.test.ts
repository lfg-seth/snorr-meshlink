import assert from 'node:assert/strict';
import test from 'node:test';
import { placedInfrastructure, placedLinks } from './placed-fleet.ts';
import { infrastructure } from './demo.ts';
import type { LinkObservation } from './NeighborTable';
import placements from './placements.json' with { type: 'json' };

test('field views match physical radios and keep fixed order, pins and names across registry renames', () => {
  const registry = placements.map((site, index) => ({
    ...infrastructure[0], id: 'registry-' + index, radioNodeId: site.radio,
  }));
  const legacy = { ...registry[0], id: 'r001', radioNodeId: '!00000000' };
  const shown = placedInfrastructure([legacy, ...registry.toReversed()]);
  assert.deepEqual(shown.map(device => [device.shortName, device.name, device.longitude, device.latitude]),
    placements.map(site => [site.shortName, site.name, site.longitude, site.latitude]));
  assert.equal(shown.length, 7);
  assert.equal(shown.at(-1)?.role, 'Offline SD recorder');
  assert.equal(shown.some(device => device.id === 'r001'), false);
  const link = {observerDeviceId: registry[0].id, heardDeviceId: registry[1].id, originalSourceDeviceId: null} as LinkObservation;
  assert.deepEqual(placedLinks([link, {...link, heardDeviceId: legacy.id}, {...link, observerDeviceId: 'b002'}], shown), [link]);
});
