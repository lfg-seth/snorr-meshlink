import type { Infrastructure, Tracker } from './demo';
import type { LinkObservation } from './NeighborTable';
import { infrastructureLabel } from './infrastructure-map.ts';

export type SignalNode = {
  id: string;
  label: string;
  coordinates: [number, number] | null;
  location: string;
  measuredAt: string | null;
};
export type SignalConnection = {
  id: string;
  nodes: [SignalNode, SignalNode];
  observations: LinkObservation[];
  latest: LinkObservation[];
  snrDb: number | null;
  color: string;
  relationship: string;
};
export type MappedSignalConnection = SignalConnection & {
  nodes: [SignalNode & { coordinates: [number, number] }, SignalNode & { coordinates: [number, number] }];
};

export function signalValue(value: number | null | undefined, unit: string) {
  return typeof value === 'number' && Number.isFinite(value) ? `${value} ${unit}` : 'Unknown';
}

// Display bands only; these are not receiver sensitivity or reliability limits.
export function signalColor(snr: number | null): string {
  return snr === null ? '#6b756f' : snr >= 5 ? '#237346' : snr >= 0 ? '#a15c00' : '#b42318';
}

function validCoordinates(longitude: number | undefined, latitude: number | undefined) {
  return typeof longitude === 'number' && Number.isFinite(longitude) && Math.abs(longitude) <= 180 &&
    typeof latitude === 'number' && Number.isFinite(latitude) && Math.abs(latitude) <= 90;
}

function time(at: string | null) {
  return at ? Date.parse(at) || 0 : 0;
}

export function signalConnections(links: LinkObservation[], trackers: Tracker[], infrastructure: Infrastructure[]) {
  const nodes = new Map<string, SignalNode>();
  trackers.forEach(device => {
    const position = device.position;
    nodes.set(device.id, { id: device.id, label: device.shortName,
      coordinates: position && validCoordinates(position.longitude, position.latitude) ? [position.longitude, position.latitude] : null,
      location: position && validCoordinates(position.longitude, position.latitude) ? 'Last recorded GPS' : 'Location unknown',
      measuredAt: position?.measuredAt ?? null });
  });
  infrastructure.forEach(device => {
    nodes.set(device.id, { id: device.id, label: infrastructureLabel(device),
      coordinates: validCoordinates(device.longitude, device.latitude) ? [device.longitude!, device.latitude!] : null, measuredAt: null,
      location: !validCoordinates(device.longitude, device.latitude) ? 'Location unknown'
        : device.deploymentStatus === 'planned' ? 'Planned location · installation unverified' : 'Configured location' });
  });
  const groups = new Map<string, SignalConnection>();
  let omitted = 0;
  links.forEach(link => {
    // The packet's original source is not necessarily the radio neighbor.
    const heard = link.heardDeviceId && nodes.get(link.heardDeviceId);
    const observer = nodes.get(link.observerDeviceId);
    if (!heard || !observer || heard.id === observer.id) { omitted++; return; }
    const pair = [heard, observer].sort((a, b) => a.id.localeCompare(b.id)) as [SignalNode, SignalNode];
    const id = JSON.stringify(pair.map(node => node.id));
    let connection = groups.get(id);
    if (!connection) {
      connection = { id, nodes: pair, observations: [], latest: [], snrDb: null, color: signalColor(null), relationship: '' };
      groups.set(id, connection);
    }
    connection.observations.push(link);
  });
  const relationships = [...groups.values()].sort((a, b) => a.id.localeCompare(b.id));
  relationships.forEach(connection => {
    const chronological = (a: LinkObservation, b: LinkObservation) =>
      time(b.observedAt ?? b.receivedAt) - time(a.observedAt ?? a.receivedAt) ||
      time(b.receivedAt) - time(a.receivedAt) || a.id.localeCompare(b.id);
    connection.observations.sort(chronological);
    const latest = new Map<string, LinkObservation>();
    connection.observations.forEach(row => {
      const key = JSON.stringify([row.observerDeviceId, row.heardDeviceId, row.source]);
      const previous = latest.get(key);
      // Compare sequences only within the same direction and boot. Sorting a
      // mixed list by sequence/time could produce a non-transitive comparator.
      const sameBoot = previous && row.reportType === 'snns-v1' && previous.reportType === 'snns-v1' &&
        row.bootId === previous.bootId && row.sequence != null && previous.sequence != null;
      if (!previous || (sameBoot ? row.sequence! > previous.sequence! : chronological(row, previous) < 0))
        latest.set(key, row);
    });
    connection.latest = [...latest.values()];
    const snrs = connection.latest.flatMap(row => typeof row.snrDb === 'number' && Number.isFinite(row.snrDb) ? [row.snrDb] : []);
    connection.snrDb = snrs.length ? Math.min(...snrs) : null;
    connection.color = signalColor(connection.snrDb);
    const receivers = new Set(connection.latest.map(row => row.observerDeviceId));
    const [a, b] = connection.nodes;
    connection.relationship = receivers.size > 1 ? `${a.label} ↔ ${b.label}`
      : receivers.has(b.id) ? `${a.label} → ${b.label}` : `${b.label} → ${a.label}`;
  });
  const connections = relationships.filter((connection): connection is MappedSignalConnection =>
    connection.nodes.every(node => node.coordinates !== null));
  omitted += relationships.filter(connection => !connection.nodes.every(node => node.coordinates !== null))
    .reduce((count, connection) => count + connection.observations.length, 0);
  return { connections, relationships, omitted };
}
