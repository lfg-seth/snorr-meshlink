import type { Infrastructure } from './demo';
import type { LinkObservation } from './NeighborTable';

export type FieldPlacement = {
  radio: string; shortName: string; name: string;
  kind: string; latitude?: number; longitude?: number; solarSetup?: string;
  batterySetup?: string; antenna?: string;
};

export function placedInfrastructure(devices: Infrastructure[], placements: FieldPlacement[]): Infrastructure[] {
  const byRadio = new Map(devices.map(device => [device.radioNodeId, device]));
  return placements.flatMap<Infrastructure>(site => {
    const device = byRadio.get(site.radio);
    if (!device || site.kind === 'mobileGateway') return [];
    const equipment = {
      batterySetup: site.batterySetup || device.batterySetup || 'Unverified',
      antenna: site.antenna || device.antenna || 'Unverified',
      solarSetup: site.solarSetup || device.solarSetup,
    };
    if (site.kind === 'stationBackhaul') {
      const stationPin = device.locationSource === 'owner-deployment-pin' && device.locationLabel === site.name;
      return [{
        ...device, name: site.name, shortName: site.shortName, role: 'Backhaul',
        deploymentStatus: 'station', latitude: site.latitude ?? (stationPin ? device.latitude : undefined),
        longitude: site.longitude ?? (stationPin ? device.longitude : undefined),
        ...equipment,
      }];
    }
    return [{
      ...device, name: site.name, shortName: site.shortName, latitude: site.latitude, longitude: site.longitude,
      role: site.kind === 'offlineRecorder' ? 'Offline SD recorder' : 'Repeater', deploymentStatus: 'placed',
      ...equipment,
    }];
  });
}

export function placedLinks(links: LinkObservation[], devices: Infrastructure[]) {
  const ids = new Set(devices.map(device => device.id));
  return links.filter(link => ids.has(link.observerDeviceId) && link.heardDeviceId && ids.has(link.heardDeviceId)
    && (!link.originalSourceDeviceId || ids.has(link.originalSourceDeviceId)));
}
