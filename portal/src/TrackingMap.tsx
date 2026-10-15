import { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import type { GeoJSONSource, StyleSpecification } from 'maplibre-gl';
import {
  infrastructure as demoInfrastructure,
} from './demo';
import type { Fix, Tracker, Infrastructure } from './demo';
import { minuteAgeLabel, trackerStatus } from './tracker';
import { infrastructureMarkers } from './infrastructure-map';
import { recordedTrailConnections } from './recorded-session';
import 'maplibre-gl/dist/maplibre-gl.css';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';

// Vite bundles the worker and its shared imports for both dev and production.
maplibregl.setWorkerUrl(workerUrl);

type Props = {
  trackers: Tracker[];
  infrastructureNodes?: Infrastructure[];
  labels: Record<string, string>;
  markerLabels: Record<string, string>;
  selectedId: string;
  now: number;
  online?: boolean;
  trail: Fix[];
  selectedInfrastructureId: string | null;
  onInfrastructureSelect: (id: string) => void;
  onSelect: (id: string) => void;
};
const services = { Topo: 'USGSTopo', 'Aerial imagery': 'USGSImageryOnly' };
function mapStyle(basemap: keyof typeof services): StyleSpecification {
  return {
    version: 8,
    sources: {
      basemap: {
        type: 'raster',
        tiles: [
          `https://basemap.nationalmap.gov/arcgis/rest/services/${services[basemap]}/MapServer/tile/{z}/{y}/{x}`,
        ],
        tileSize: 256,
        maxzoom: 16,
        attribution:
          '<a href="https://www.usgs.gov/programs/national-geospatial-program/national-map">USGS · The National Map</a>',
      },
      trail: {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] },
      },
    },
    layers: [
      {
        id: 'background',
        type: 'background',
        paint: { 'background-color': '#dde1d3' },
      },
      { id: 'basemap', type: 'raster', source: 'basemap' },
      {
        id: 'trail-lines',
        type: 'line',
        source: 'trail',
        paint: {
          'line-color': '#153f49',
          'line-width': 3,
          'line-dasharray': [2, 2],
        },
      },
    ],
  };
}
export default function TrackingMap(props: Props) {
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef(new Map<string, maplibregl.Marker>());
  const current = useRef(props);
  current.current = props;
  const [basemap, setBasemap] = useState<keyof typeof services>('Topo');
  const [retry, setRetry] = useState(0);
  const [ready, setReady] = useState(0);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!container.current) return;
    setError('');
    let instance: maplibregl.Map;
    try {
      instance = new maplibregl.Map({
        container: container.current,
        style: mapStyle(basemap),
        center: [-115.656, 36.278],
        zoom: 12,
        maxZoom: 17,
        attributionControl: false,
      });
    } catch {
      setError(
        'Map rendering unavailable. Your browser may not support WebGL. View trackers and recorded coordinates on the Users page.',
      );
      return;
    }
    let active = true;
    map.current = instance;
    instance.addControl(
      new maplibregl.NavigationControl({ showCompass: false }),
      'top-right',
    );
    instance.addControl(
      new maplibregl.AttributionControl({ compact: false }),
      'bottom-right',
    );
    instance.addControl(
      new maplibregl.ScaleControl({ unit: 'imperial' }),
      'bottom-left',
    );
    instance.on('error', (event) => {
      if (
        !active ||
        (event.error instanceof Error && event.error.name === 'AbortError')
      )
        return;
      setError(
        'Some map tiles could not load. Last recorded positions remain available; retry the basemap.',
      );
    });
    instance.on('load', () => setReady((value) => value + 1));
    const resize = new ResizeObserver(() => instance.resize());
    resize.observe(container.current);
    return () => {
      active = false;
      resize.disconnect();
      markers.current.forEach((marker) => marker.remove());
      markers.current.clear();
      instance.remove();
      map.current = null;
    };
  }, [basemap, retry]);

  useEffect(() => {
    const instance = map.current;
    if (!instance) return;
    const present = new Set<string>();
    function marker(
      id: string,
      coordinates: [number, number],
      className: string,
      text: string,
      label: string,
      action?: () => void,
      offset: [number, number] = [0, 0],
    ) {
      present.add(id);
      let pin = markers.current.get(id);
      if (!pin) {
        const element = document.createElement(action ? 'button' : 'div');
        if (element instanceof HTMLButtonElement) element.type = 'button';
        if (action) element.addEventListener('click', action);
        pin = new maplibregl.Marker({ element })
          .setLngLat(coordinates)
          .addTo(instance!);
        markers.current.set(id, pin);
      }
      const element = pin.getElement();
      element.className = `maplibregl-marker ${className}`;
      element.textContent = text;
      element.setAttribute('aria-label', label);
      element.title = label;
      pin.setLngLat(coordinates);
      pin.setOffset(offset);
    }
    props.trackers.forEach((tracker) => {
      if (!tracker.position) return;
      const status = trackerStatus(tracker, props.now);
      marker(
        tracker.id,
        [tracker.position.longitude, tracker.position.latitude],
        `map-pin ${status.kind} ${props.selectedId === tracker.id ? 'selected-pin' : ''}`,
        props.markerLabels[tracker.id] || tracker.shortName,
        `${props.labels[tracker.id]} · ${tracker.shortName} · ${status.label} · GPS age ${minuteAgeLabel(tracker.position.measuredAt, props.now)}`,
        () => current.current.onSelect(tracker.id),
      );
    });
    infrastructureMarkers(props.infrastructureNodes ?? demoInfrastructure).forEach(({ device, label, offset }) => {
      marker(`infra-${device.id}`, [device.longitude!, device.latitude!],
        `infrastructure-pin ${props.selectedInfrastructureId === device.id ? 'selected-pin' : ''}`,
        label, `${label} · ${device.name} · ${device.role} · select for quick stats`,
        () => current.current.onInfrastructureSelect(device.id), offset);
    });
    props.trail.forEach((fix) => {
      marker(`trail-${fix.measuredAt}`, [fix.longitude, fix.latitude],
        'trail-pin', '', `Recorded trail point ${fix.measuredAt}`);
    });
    markers.current.forEach((pin, id) => {
      if (!present.has(id)) {
        pin.remove();
        markers.current.delete(id);
      }
    });
    const source = instance.getSource('trail') as GeoJSONSource | undefined;
    if (source) {
      source.setData({
        type: 'FeatureCollection',
        features: recordedTrailConnections(props.trail).map(([a, b]) => ({
          type: 'Feature',
          properties: {},
          geometry: {
            type: 'LineString',
            coordinates: [
              [a.longitude, a.latitude],
              [b.longitude, b.latitude],
            ],
          },
        })),
      });
    }
  }, [props, ready]);

  useEffect(() => {
    const tracker = props.trackers.find((t) => t.id === props.selectedId);
    if (tracker?.position)
      map.current?.easeTo({
        center: [tracker.position.longitude, tracker.position.latitude],
        duration: window.matchMedia('(prefers-reduced-motion: reduce)').matches
          ? 0
          : 500,
      });
  }, [props.selectedId, ready]);

  return (
    <div className="map-frame">
      <div
        ref={container}
        className="map-canvas"
        aria-label="Map with recorded tracker positions"
      />
      <div className="map-tools">
        <div className="segmented">
          {(Object.keys(services) as (keyof typeof services)[]).map((name) => (
            <button
              key={name}
              aria-pressed={basemap === name}
              onClick={() => setBasemap(name)}
            >
              {name}
            </button>
          ))}
        </div>
        <button
          onClick={() =>
            map.current?.fitBounds(
              [
                [-115.705, 36.239],
                [-115.6, 36.324],
              ],
              { padding: 45, duration: 0 },
            )
          }
        >
          Fit area
        </button>
      </div>
      {!props.online && <p className="map-feed-status" role="status">Feed offline · showing last recorded positions</p>}
      {error && (
        <div className="map-error" role="status">
          {error}{' '}
          <button onClick={() => setRetry((value) => value + 1)}>
            Retry map
          </button>
        </div>
      )}
    </div>
  );
}
