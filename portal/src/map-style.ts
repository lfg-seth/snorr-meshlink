import type { StyleSpecification } from 'maplibre-gl';

export type Basemap = 'Topo' | 'Aerial imagery';

export const services = { Topo: 'USGSTopo', 'Aerial imagery': 'USGSImageryOnly' };
export function mapStyle(basemap: Basemap): StyleSpecification {
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
      signals: {
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
        id: 'signal-casing', type: 'line', source: 'signals',
        layout: { 'line-cap': 'round' },
        paint: { 'line-color': '#ffffff', 'line-width': ['+', ['get', 'width'], 3], 'line-opacity': 0.9 },
      },
      {
        id: 'signal-lines', type: 'line', source: 'signals',
        layout: { 'line-cap': 'round' },
        paint: { 'line-color': ['get', 'color'], 'line-width': ['get', 'width'], 'line-opacity': 0.9 },
      },
      {
        id: 'signal-hit-area', type: 'line', source: 'signals',
        paint: { 'line-color': '#ffffff', 'line-width': 22, 'line-opacity': 0 },
      },
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
