import { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import type { GeoJSONSource } from 'maplibre-gl';
import type { Fix, Tracker, Infrastructure } from './demo';
import { minuteAgeLabel, trackerStatus } from './tracker';
import { infrastructureMarkers } from './infrastructure-map';
import { recordedTrailConnections } from './recorded-session';
import type { MappedSignalConnection } from './signal-links';
import './map-runtime';
import { mapStyle, services } from './map-style';
import { useBasemap } from './MapPreferences';
import { trackerMarkerClass, infrastructureMarkerClass } from './map-markers';

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
  signalConnections: MappedSignalConnection[];
  omittedSignals: number;
  showSignals: boolean;
  onSignalsChange: (visible: boolean) => void;
  selectedSignalId: string | null;
  onSignalSelect: (id: string) => void;
};
export default function TrackingMap(props: Props) {
  const container = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markers = useRef(new Map<string, maplibregl.Marker>());
  const current = useRef(props);
  current.current = props;
  const [basemap, setBasemap] = useBasemap();
  const [retry, setRetry] = useState(0);
  const [ready, setReady] = useState(0);
  const [error, setError] = useState('');
  const [signalInfo, setSignalInfo] = useState(false);

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
    instance.on('click', 'signal-hit-area', (event) => {
      const target = event.originalEvent?.target;
      if (target instanceof HTMLElement && target.closest('.map-pin, .infrastructure-pin')) return;
      const id = event.features?.[0]?.properties?.id;
      if (current.current.showSignals && typeof id === 'string') current.current.onSignalSelect(id);
    });
    instance.on('mouseenter', 'signal-hit-area', () => { instance.getCanvas().style.cursor = 'pointer'; });
    instance.on('mouseleave', 'signal-hit-area', () => { instance.getCanvas().style.cursor = ''; });
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
        if (action) element.addEventListener('click', (event) => {
          event.stopPropagation();
          action();
        });
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
        trackerMarkerClass(tracker, props.now, props.selectedId === tracker.id),
        props.markerLabels[tracker.id] || tracker.shortName,
        `${props.labels[tracker.id]} · ${tracker.shortName} · ${status.label} · GPS age ${minuteAgeLabel(tracker.position.measuredAt, props.now)}`,
        () => current.current.onSelect(tracker.id),
      );
    });
    infrastructureMarkers(props.infrastructureNodes ?? []).forEach(({ device, label, offset }) => {
      marker(`infra-${device.id}`, [device.longitude!, device.latitude!],
        infrastructureMarkerClass(props.selectedInfrastructureId === device.id),
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
    // Missing sources are populated on load, including after basemap changes.
    const signals = instance.getSource('signals') as GeoJSONSource | undefined;
    signals?.setData({
      type: 'FeatureCollection',
      features: props.showSignals ? props.signalConnections.map(connection => ({
        type: 'Feature',
        properties: { id: connection.id, color: connection.color, width: props.selectedSignalId === connection.id ? 6 : 4 },
        geometry: { type: 'LineString', coordinates: connection.nodes.map(node => node.coordinates) },
      })) : [],
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
        <button className="signal-toggle" aria-pressed={props.showSignals}
          onClick={() => props.onSignalsChange(!props.showSignals)}>
          {props.showSignals ? 'Hide signal strength' : 'Show signal strength'}
        </button>
        {props.showSignals && <div className="signal-legend" aria-label="Signal strength legend">
          <strong>Recorded SNR</strong>
          <span><i style={{ background: '#237346' }} /> ≥5 dB</span>
          <span><i style={{ background: '#a15c00' }} /> 0–&lt;5 dB</span>
          <span><i style={{ background: '#b42318' }} /> &lt;0 dB</span>
          <span><i style={{ background: '#6b756f' }} /> Unknown</span>
          <button className="signal-info-button" aria-label="About signal strength" aria-expanded={signalInfo}
            aria-controls="signal-legend-help" onClick={() => setSignalInfo(!signalInfo)}>i</button>
          {signalInfo && <small id="signal-legend-help">{props.signalConnections.length ? 'Weakest known latest reading · tap a line or a relationship in a node card for details' : 'No neighbor connections with known endpoints and locations'}
            {props.omittedSignals > 0 && ` · ${props.omittedSignals} observations without distinct mapped endpoints omitted`}</small>}
        </div>}
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
