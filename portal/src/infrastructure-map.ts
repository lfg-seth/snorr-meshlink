import type { Infrastructure } from './demo';

export function infrastructureLabel(device: Infrastructure) {
  const named = device.name.match(/\b[RGS]\d{3}\b/i)?.[0];
  if (named) return named.toUpperCase();
  const numbered = device.id.match(/^([rgb])(\d+)$/i);
  if (!numbered) return device.name;
  const prefix =
    numbered[1].toUpperCase() === 'B' ? 'G' : numbered[1].toUpperCase();
  return `${prefix}${numbered[2].padStart(3, '0')}`;
}

export function infrastructureMarkers(devices: Infrastructure[]) {
  const sites = new Map<string, Infrastructure[]>();
  devices
    .filter((d) => Number.isFinite(d.longitude) && Number.isFinite(d.latitude))
    .forEach((device) => {
      const key = `${device.longitude},${device.latitude}`;
      sites.set(key, [...(sites.get(key) ?? []), device]);
    });
  return [...sites.values()].flatMap((group) =>
    group.map((device, index) => ({
      device,
      label: infrastructureLabel(device),
      // Keep every colocated device selectable without changing its coordinates.
      offset: [
        ((index % 3) - (Math.min(group.length, 3) - 1) / 2) * 62,
        Math.floor(index / 3) * 38,
      ] as [number, number],
    })),
  );
}
