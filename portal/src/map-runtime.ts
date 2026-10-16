import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import workerUrl from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';

// Vite bundles the worker and its shared imports for both dev and production.
maplibregl.setWorkerUrl(workerUrl);
