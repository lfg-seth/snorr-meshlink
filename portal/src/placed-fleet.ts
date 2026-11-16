import placements from './placements.json' with { type: 'json' };
import type { Infrastructure } from './demo';
import type { LinkObservation } from './NeighborTable';

export function placedInfrastructure(devices: Infrastructure[]): Infrastructure[] {
  const byRadio = new Map(devices.map(device => [device.radioNodeId, device]));
  return placements.flatMap(site => {
    const device = byRadio.get(site.radio);
    if (!device) return [];
    return [{
      ...device, name: site.name, shortName: site.shortName, latitude: site.latitude, longitude: site.longitude,
      role: site.offlineRecorder ? 'Offline SD recorder' : 'Repeater', deploymentStatus: 'placed',
      batterySetup: 'Eight cells', antenna: 'Muzi',
    }];
  });
}

export function placedLinks(links: LinkObservation[], devices: Infrastructure[]) {
  const ids = new Set(devices.map(device => device.id));
  return links.filter(link => ids.has(link.observerDeviceId) && link.heardDeviceId && ids.has(link.heardDeviceId)
    && (!link.originalSourceDeviceId || ids.has(link.originalSourceDeviceId)));
}
