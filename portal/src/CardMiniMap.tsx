import { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import type { GeoJSONSource } from 'maplibre-gl';
import './map-runtime';
import { mapStyle } from './map-style';
import { useBasemap } from './MapPreferences';

export type MiniMapNode = {
  id: string;
  label: string;
  markerClassName: string;
  coordinates: [number, number] | null;
};

export default function CardMiniMap({ nodes: suppliedNodes, color }: { nodes: MiniMapNode[]; color?: string }) {
  const nodes = suppliedNodes.map(node => ({ ...node, coordinates: node.coordinates &&
    node.coordinates.every(Number.isFinite) && Math.abs(node.coordinates[0]) <= 180 && Math.abs(node.coordinates[1]) <= 90
    ? node.coordinates : null }));
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [basemap] = useBasemap();
  const [ready, setReady] = useState(0);
  const [error, setError] = useState('');
  const current = useRef(nodes);
  current.current = nodes;
  const nodeKey = JSON.stringify(nodes);
  const coordinatesKey = JSON.stringify(nodes.map(node => node.coordinates));
  const hasLocation = nodes.some(node => node.coordinates !== null);

  function fit(instance: maplibregl.Map) {
    const points = current.current.flatMap(node => node.coordinates ? [node.coordinates] : []);
    if (points.length === 1) instance.easeTo({ center: points[0], zoom: 14, duration: 0 });
    else if (points.length > 1) instance.fitBounds([
      [Math.min(...points.map(p => p[0])), Math.min(...points.map(p => p[1]))],
      [Math.max(...points.map(p => p[0])), Math.max(...points.map(p => p[1]))],
    ], { padding: 55, maxZoom: 14, duration: 0 });
  }

  useEffect(() => {
    if (!container.current || !hasLocation) return;
    setError('');
    let instance: maplibregl.Map;
    try {
      instance = new maplibregl.Map({
        container: container.current,
        style: mapStyle(basemap),
        center: current.current.find(node => node.coordinates)?.coordinates ?? [0, 0],
        zoom: 14,
        maxZoom: 17,
        attributionControl: false,
        scrollZoom: false,
      });
    } catch {
      setError('Map unavailable. Recorded location details remain below.');
      return;
    }
    map.current = instance;
    let active = true;
    instance.on('load', () => { if (active) setReady(value => value + 1); });
    instance.on('error', event => {
      if (active && !(event.error instanceof Error && event.error.name === 'AbortError'))
        setError('Some map tiles could not load. Showing recorded locations.');
    });
    const resize = new ResizeObserver(() => { instance.resize(); fit(instance); });
    resize.observe(container.current);
    return () => {
      active = false;
      resize.disconnect();
      instance.remove();
      map.current = null;
    };
  }, [basemap, hasLocation]);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const visible = nodes.filter(node => node.coordinates !== null);
    const colocated = visible.length === 2 && visible[0].coordinates!.every((value, i) => value === visible[1].coordinates![i]);
    const markers = visible.map((node, index) => {
      const element = document.createElement('div');
      element.className = `mini-map-pin ${node.markerClassName}`;
      element.textContent = node.label;
      element.title = node.label;
      element.setAttribute('aria-label', node.label);
      return new maplibregl.Marker({ element }).setLngLat(node.coordinates!)
        .setOffset(colocated ? [index === 0 ? -30 : 30, 0] : [0, 0]).addTo(instance);
    });
    (instance.getSource('signals') as GeoJSONSource | undefined)?.setData({
      type: 'FeatureCollection',
      features: color && visible.length === 2 ? [{
        type: 'Feature',
        properties: { color, width: 4 },
        geometry: { type: 'LineString', coordinates: visible.map(node => node.coordinates!) },
      }] : [],
    });
    return () => markers.forEach(marker => marker.remove());
  }, [nodeKey, color, ready, basemap, hasLocation]);

  useEffect(() => {
    if (map.current) fit(map.current);
  }, [coordinatesKey, ready, basemap, hasLocation]);

  if (!hasLocation) return <p className="small muted mini-map-missing">No recorded location for this map.</p>;
  return <figure className="card-mini-map" aria-label={`Map of ${nodes.map(node => node.label).join(' and ')}`}>
    <div ref={container} className="mini-map-canvas" />
    <figcaption className="mini-map-attribution"><a href="https://www.usgs.gov/programs/national-geospatial-program/national-map" target="_blank" rel="noreferrer">USGS · The National Map</a></figcaption>
    {error && <p className="mini-map-error" role="status">{error}</p>}
    {nodes.some(node => !node.coordinates) && <p className="mini-map-error">{nodes.filter(node => !node.coordinates).map(node => node.label).join(', ')}: location unknown</p>}
  </figure>;
}
