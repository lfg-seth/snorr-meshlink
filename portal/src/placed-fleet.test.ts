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
  assert.equal(shown.length, 10);
  assert.equal(shown.find(device => device.shortName === 'G002')?.role, 'Offline SD recorder');
  assert.equal(shown.some(device => device.id === 'r001'), false);
  const link = {observerDeviceId: registry[0].id, heardDeviceId: registry[1].id, originalSourceDeviceId: null} as LinkObservation;
  assert.deepEqual(placedLinks([link, {...link, heardDeviceId: legacy.id}, {...link, observerDeviceId: 'b002'}], shown), [link]);
});

test('Terry Home uses the approved public pin and keeps its own power and gateway health', () => {
  const gateway = {...infrastructure[0], radioNodeId: '!b03d6790', latitude: 0, longitude: 0,
    antenna: 'Muzi', batterySetup: '1,000 mAh', externalPower: 'AC power planned', solarSetup: 'Unconfigured',
    gatewayHealth: {state: 'offline', label: 'Offline'}};
  const [station] = placedInfrastructure([gateway]);
  assert.deepEqual([station.shortName, station.name, station.role], ['G006', 'Terry Home', 'Backhaul']);
  assert.deepEqual([station.latitude, station.longitude], [36.26153180096932, -115.18904437592454]);
  assert.equal(station.externalPower, gateway.externalPower);
  assert.equal(station.solarSetup, gateway.solarSetup);
  assert.equal(station.gatewayHealth, gateway.gatewayHealth);
});

test('Lee Fire Station retains gateway health and uses its owner-supplied deployment pin only', () => {
  const gateway = {...infrastructure[0], id: 'g001', radioNodeId: '!1bbf0638',
    batterySetup: 'Verified pack', antenna: 'Verified antenna', longitude: -115, latitude: 36,
    locationLabel: 'Lee Fire Station', locationSource: 'owner-deployment-pin',
    gatewayHealth: {state: 'online', label: 'Online'}};
  const [station] = placedInfrastructure([gateway]);
  assert.equal(station.role, 'Backhaul');
  assert.equal(station.shortName, 'G001');
  assert.equal(station.name, gateway.locationLabel);
  assert.deepEqual([station.longitude, station.latitude], [-115, 36]);
  assert.equal(station.batterySetup, gateway.batterySetup);
  assert.equal(station.antenna, gateway.antenna);
  assert.equal(station.gatewayHealth, gateway.gatewayHealth);
  for (const stale of [{...gateway, locationLabel:'Former bench'}, {...gateway, locationSource:'old'}]) {
    assert.equal(placedInfrastructure([stale])[0].longitude, undefined);
  }
});
