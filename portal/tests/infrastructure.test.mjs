import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { registerHooks } from 'node:module';
import test from 'node:test';
import { JSDOM } from 'jsdom';
import { act, createElement, useState } from 'react';
import ts from 'typescript';

// Exercise the actual TSX components using the existing Node test runner.
registerHooks({
  resolve(specifier, context, next) {
    if (specifier === 'maplibre-gl')
      return next(
        new URL('./maplibre-stub.mjs', import.meta.url).href,
        context,
      );
    if (specifier.endsWith('.css') || specifier.includes('?worker&url'))
      return {
        url: 'data:text/javascript,export default ""',
        shortCircuit: true,
      };
    try {
      return next(specifier, context);
    } catch (error) {
      if (specifier.startsWith('.')) {
        for (const extension of ['.ts', '.tsx']) {
          const url = new URL(specifier + extension, context.parentURL);
          if (existsSync(url)) return next(url.href, context);
        }
      }
      throw error;
    }
  },
  load(url, context, next) {
    if (!url.endsWith('.tsx')) return next(url, context);
    return {
      format: 'module',
      shortCircuit: true,
      source: ts.transpileModule(readFileSync(new URL(url), 'utf8'), {
        compilerOptions: {
          jsx: ts.JsxEmit.ReactJSX,
          module: ts.ModuleKind.ESNext,
        },
      }).outputText,
    };
  },
});

test('reported RAK current preserves sign and timestamped signal reports preserve hearing age and count', async () => {
  const { renderToStaticMarkup } = await import('react-dom/server');
  const { default: PowerReadings } = await import('../src/PowerReadings.tsx');
  const { default: NeighborTable } = await import('../src/NeighborTable.tsx');
  const { infrastructure } = await import('../src/demo.ts');
  const now = Date.parse('2026-10-16T20:00:00.000Z');
  const device = { ...infrastructure[0], powerReadings: [
    { metric: 'power3CurrentMa', value: -323.1, measuredAt: null, receivedAt: '2026-10-16T19:58:00.000Z', timestampQuality: 'unknown' },
    { metric: 'power1CurrentMa', value: 0, measuredAt: '2026-10-16T18:00:00.000Z', receivedAt: '2026-10-16T19:58:00.000Z', timestampQuality: 'valid' },
  ] };
  const html = renderToStaticMarkup(createElement(PowerReadings, { device, now }));
  assert.match(html, /Power channel 3/);
  assert.match(html, /-323.1 mA/);
  assert.match(html, /0.0 mA/);
  assert.match(html, /Measurement time unknown/);
  assert.match(html, /Stale/);
  assert.match(html, /polarity and calibration are unverified/);
  const table = renderToStaticMarkup(createElement(NeighborTable, { infrastructure: [device], trackers: [], now, online: true,
    links: [{ id: 'one', observerDeviceId: device.id, heardDeviceId: null, heardNodeId: '!00000123',
      originalSourceDeviceId: null, source: 'neighbor', reportType: 'snns-v1', path: 'direct',
      snrDb: 0, rssiDbm: -90, observedAt: '2026-10-16T19:58:48.000Z', receivedAt: '2026-10-16T19:59:00.000Z',
      hearingAgeSeconds: 12, observationCount: 7, subset: true, totalNeighbors: 9, capacityEvicted: true }] }));
  for (const value of ['!00000123', '0 dB', '-90 dBm', '12s', 'Partial', 'capacity eviction', 'RAK signal report'])
    assert.ok(table.includes(value), value);
});

test('neighbor freshness expires map lines, node links, open details and table rows while offline', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.ResizeObserver = class { observe() {} disconnect() {} };
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  const dialog = window.HTMLDialogElement.prototype;
  dialog.show = function () { this.open = true; };
  dialog.close = function () { this.open = false; };
  const { createRoot } = await import('react-dom/client');
  const { default: MapPage } = await import('../src/MapPage.tsx');
  const { default: NeighborTable } = await import('../src/NeighborTable.tsx');
  const { MapPreferences } = await import('../src/MapPreferences.tsx');
  const { initialTrackers, infrastructure } = await import('../src/demo.ts');
  const cutoff = Date.parse('2026-10-21T14:00:00Z');
  const verified = { id: 'verified', observerDeviceId: 'r1', heardDeviceId: 'd1', originalSourceDeviceId: null,
    source: 'neighbor', path: 'direct', snrDb: 8, rssiDbm: -70,
    observedAt: '2026-10-21T12:00:00Z', receivedAt: '2026-10-21T13:59:00Z' };
  const links = [verified,
    { ...verified, id: 'expired', heardDeviceId: 'd2', snrDb: -10, observedAt: '2026-10-21T11:00:00Z' },
    { ...verified, id: 'cached', reportType: 'neighbor-info', observedAt: null, snrDb: -15 },
    { ...verified, id: 'relative-only', reportType: 'snns-v1', observedAt: null, hearingAgeSeconds: 0 }];
  const root = createRoot(document.getElementById('root'));
  const render = (now, rows = links) => act(async () => root.render(createElement(MapPreferences, null,
    createElement(MapPage, { assignments: [], trackers: initialTrackers, infrastructureNodes: infrastructure,
      links: rows, online: false, now, selectedId: '', onSelect() {}, labels: {}, trailId: null, onTrailChange() {} }),
    createElement(NeighborTable, { links: rows, infrastructure, trackers: initialTrackers, online: false, now }))));
  const features = () => JSON.parse(document.querySelector('.map-canvas').dataset.signals).features;
  try {
    await render(cutoff - 1);
    assert.equal(document.querySelectorAll('tbody tr').length, 1);
    assert.doesNotMatch(document.querySelector('tbody').textContent, /-10 dB|-15 dB/);
    await act(async () => document.querySelector('.signal-toggle').click());
    assert.equal(features().length, 1);
    await act(async () => document.querySelector('button.map-pin').click());
    assert.equal(document.querySelectorAll('.node-relationship').length, 1);
    assert.match(document.querySelector('.node-relationship').textContent, /8 dB/);
    await act(async () => document.querySelector('.node-relationship').click());
    assert.equal(document.querySelectorAll('.signal-reading').length, 1);
    // Keep the same links/trackers/infrastructure references: only the clock advances.
    await render(cutoff);
    assert.equal(features().length, 0);
    assert.equal(document.querySelector('.signal-link-detail'), null);
    assert.equal(document.querySelector('.neighbor-table'), null);
    assert.match(document.querySelector('.neighbor-panel').textContent, /two hours|2 hours/);
    await act(async () => document.querySelector('button.map-pin').click());
    assert.equal(document.querySelectorAll('.node-relationship').length, 0);
    assert.match(document.querySelector('.node-relationships').textContent, /No recent neighbors/);
    await render(cutoff, [{ ...verified, id: 'fresh', observedAt: '2026-10-21T13:59:00Z' }]);
    assert.equal(features().length, 1);
    assert.equal(document.querySelectorAll('.node-relationship').length, 1);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    for (const key of ['window', 'document', 'HTMLElement', 'HTMLButtonElement', 'ResizeObserver', 'IS_REACT_ACT_ENVIRONMENT']) delete globalThis[key];
  }
});

test('neighbor minimap icons select device identities without separate open buttons', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.ResizeObserver = class { observe() {} disconnect() {} };
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  const dialog = window.HTMLDialogElement.prototype;
  dialog.show = function () { this.open = true; };
  dialog.close = function () { this.open = false; };
  const { createRoot } = await import('react-dom/client');
  const { default: SignalLinkDetail } = await import('../src/SignalLinkDetail.tsx');
  const { MapPreferences } = await import('../src/MapPreferences.tsx');
  const nodes = [
    { id: 'member', label: 'B001', coordinates: [-115.6, 36.3], markerClassName: 'map-pin' },
    { id: 'repeater', label: 'R001', coordinates: [-115.6, 36.3], markerClassName: 'infrastructure-pin' },
  ];
  const connection = { nodes, color: '#237346', snrDb: 4, latest: [], observations: [] };
  const selected = [];
  const root = createRoot(document.getElementById('root'));
  const render = (nextNodes = nodes, onNodeSelect = id => selected.push(id)) => act(async () => root.render(
    createElement(MapPreferences, null, createElement(SignalLinkDetail, {
      connection: { ...connection, nodes: nextNodes }, labels: {}, markerLabels: { member: 'ALIAS' },
      markerClasses: { member: 'map-pin', repeater: 'infrastructure-pin' },
      now: Date.now(), online: true, onClose() {}, onNodeSelect,
    })),
  ));
  try {
    await render();
    assert.equal(document.querySelector('.signal-node-buttons'), null);
    const pins = [...document.querySelectorAll('button.mini-map-pin')];
    assert.deepEqual(pins.map(pin => pin.textContent), ['ALIAS', 'R001']);
    assert.deepEqual(pins.map(pin => pin.getAttribute('aria-label')), ['Open ALIAS node card', 'Open R001 node card']);
    assert.ok(pins.every(pin => pin.type === 'button' && pin.tabIndex === 0));
    assert.deepEqual(pins.map(pin => pin.dataset.offset), ['-30,0', '30,0'], 'colocated icons remain separately accessible');
    let bubbled = 0;
    document.querySelector('.mini-map-canvas').addEventListener('click', () => { bubbled++; });
    await act(async () => pins.forEach(pin => pin.click()));
    assert.deepEqual(selected, ['member', 'repeater'], 'labels do not replace device identities');
    assert.equal(bubbled, 0);
    await render(nodes, id => selected.push(`updated:${id}`));
    await act(async () => document.querySelector('button.mini-map-pin').click());
    assert.equal(selected.at(-1), 'updated:member', 'icons use the current selection callback');
    await render([{ ...nodes[0], coordinates: null }, nodes[1]]);
    assert.equal(document.querySelectorAll('button.mini-map-pin').length, 1);
    assert.match(document.querySelector('.card-mini-map').textContent, /ALIAS: location unknown/);
    await act(async () => document.querySelector('button.mini-map-pin').click());
    assert.equal(selected.at(-1), 'repeater');
    await render(nodes.map(node => ({ ...node, coordinates: null })));
    assert.equal(document.querySelectorAll('.mini-map-pin').length, 0);
    assert.match(document.querySelector('.mini-map-missing').textContent, /No recorded location/);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    for (const key of ['window', 'document', 'HTMLElement', 'HTMLButtonElement', 'ResizeObserver', 'IS_REACT_ACT_ENVIRONMENT']) delete globalThis[key];
  }
});

test('unlabelled signal lines, independent legend help and node relationships preserve node selection', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.ResizeObserver = class { observe() {} disconnect() {} };
  const stylesheet = document.createElement('style');
  stylesheet.textContent = readFileSync(new URL('../src/style.css', import.meta.url), 'utf8');
  document.head.append(stylesheet);
  let mobile = false;
  window.matchMedia = () => ({ matches: mobile, addEventListener() {}, removeEventListener() {} });
  const dialog = window.HTMLDialogElement.prototype;
  dialog.showModal = function () { this.open = true; this.dataset.mode = 'modal'; };
  dialog.show = function () { this.open = true; this.dataset.mode = 'panel'; };
  dialog.close = function () { this.open = false; };
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: MapPage } = await import('../src/MapPage.tsx');
  const { MapPreferences } = await import('../src/MapPreferences.tsx');
  const { infrastructure, initialTrackers } = await import('../src/demo.ts');
  const now = Date.now();
  const at = new Date(now - 120000).toISOString();
  const links = [{ id: 'forward', observerDeviceId: 'r1', heardDeviceId: 'd1', originalSourceDeviceId: 'd2',
    path: 'relayed', source: 'gateway', snrDb: 0, rssiDbm: -112, observedAt: at, receivedAt: at },
  { id: 'reverse', observerDeviceId: 'd1', heardDeviceId: 'r1', originalSourceDeviceId: null,
    path: 'direct', source: 'neighbor', snrDb: -2, rssiDbm: null, observedAt: at, receivedAt: at },
  { id: 'unknown', observerDeviceId: 'r1', heardDeviceId: null, originalSourceDeviceId: 'd3',
    path: 'unknown', source: 'gateway', snrDb: 9, rssiDbm: -80, observedAt: at, receivedAt: at }];
  const root = createRoot(document.getElementById('root'));
  const render = (rows = links, online = true, trackers = initialTrackers, assignments = [], members = []) => act(async () => root.render(createElement(MapPreferences, null, createElement(MapPage, {
    trackers, infrastructureNodes: infrastructure, links: rows, online, now, assignments, members,
    labels: Object.fromEntries(initialTrackers.map(t => [t.id, t.shortName])), selectedId: '', onSelect() {}, trailId: null, onTrailChange() {},
  }))));
  const toggle = () => document.querySelector('.signal-toggle');
  const canvas = () => document.querySelector('.map-canvas');
  const features = () => JSON.parse(canvas().dataset.signals).features;
  try {
    await render();
    assert.equal(toggle().previousElementSibling.textContent.trim(), 'Fit area');
    assert.equal(toggle().getAttribute('aria-pressed'), 'false');
    assert.equal(features().length, 0);
    assert.equal(document.querySelector('.signal-map-label'), null);
    await act(async () => document.querySelector('button.map-pin').click());
    const mini = () => document.querySelector('.mini-map-canvas');
    const miniPins = () => [...mini().querySelectorAll('.mini-map-pin')];
    const miniLines = () => JSON.parse(mini().dataset.signals).features;
    const assertMarkerStyle = (main, preview) => {
      // Compare the recorded state after moving the pointer off the clicked marker.
      document.body.dispatchEvent(new window.MouseEvent('mouseover', { bubbles: true }));
      const classes = element => [...element.classList].filter(name => !['maplibregl-marker', 'mini-map-pin'].includes(name)).sort();
      assert.deepEqual(classes(preview), classes(main), 'mini map shares node type, status and selection state');
      const mainStyle = window.getComputedStyle(main);
      const previewStyle = window.getComputedStyle(preview);
      for (const property of ['backgroundColor', 'color', 'height', 'minWidth', 'borderRadius', 'borderColor', 'boxShadow', 'outline', 'outlineOffset'])
        assert.equal(previewStyle[property], mainStyle[property], `mini marker matches main ${property}`);
    };
    assert.equal(miniPins().length, 1, 'node card shows only its node');
    assert.equal(miniPins()[0].textContent, 'S001');
    assertMarkerStyle(canvas().querySelector('button.map-pin'), miniPins()[0]);
    assert.equal(miniLines().length, 0, 'node mini map has no trails or relationships');
    assert.deepEqual(JSON.parse(mini().dataset.camera).center, [initialTrackers[0].position.longitude, initialTrackers[0].position.latitude]);
    assert.equal(mini().dataset.controls, '0', 'no map controls are added');
    assert.equal(document.querySelector('.card-mini-map button'), null, 'pins and attribution add no buttons');
    assert.match(JSON.parse(mini().dataset.style).sources.basemap.tiles[0], /USGSTopo/);
    assert.match(document.querySelector('.node-relationship').textContent, /S001 ↔ R001.*-2 dB/);
    assert.equal(document.querySelectorAll('.node-relationship').length, 1);
    assert.equal(document.querySelector('.node-relationship').children.length, 2, 'relationship and pill only');
    assert.equal(document.querySelectorAll('.signal-reading').length, 0, 'readings stay in the relationship card');
    await act(async () => document.querySelector('.node-relationship').click());
    assert.ok(document.querySelector('.signal-link-detail'), 'relationship works with the overlay off');
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['S001', 'R001']);
    assertMarkerStyle(canvas().querySelector('button.map-pin'), miniPins()[0]);
    assertMarkerStyle(canvas().querySelector('button.infrastructure-pin'), miniPins()[1]);
    assert.equal(miniLines().length, 1);
    assert.equal(miniLines()[0].properties.color, '#b42318');
    assert.deepEqual(miniLines()[0].geometry.coordinates, miniPins().map(pin => JSON.parse(pin.dataset.coordinates)));
    const points = miniPins().map(pin => JSON.parse(pin.dataset.coordinates));
    assert.deepEqual(JSON.parse(mini().dataset.camera).bounds, [
      [Math.min(...points.map(p => p[0])), Math.min(...points.map(p => p[1]))],
      [Math.max(...points.map(p => p[0])), Math.max(...points.map(p => p[1]))],
    ]);
    assert.equal(JSON.parse(mini().dataset.camera).maxZoom, 14);
    assert.equal(features().length, 0);
    assert.equal(document.querySelector('.signal-node-buttons'), null, 'no separate open-device buttons');
    assert.deepEqual([...mini().querySelectorAll('button')].map(button => button.getAttribute('aria-label')),
      ['Open S001 node card', 'Open R001 node card'], 'endpoint icons are named native buttons');
    assert.ok(miniPins().every(pin => pin.type === 'button' && pin.tabIndex === 0), 'icons support keyboard activation');
    await act(async () => document.querySelector('[aria-label="Open S001 node card"]').click());
    assert.ok(document.querySelector('.tracker-detail'));
    assert.equal(document.querySelectorAll('.device-sheet').length, 1, 'endpoint replaces the relationship card');
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => document.querySelector('[aria-label="Open R001 node card"]').click());
    assert.ok(document.querySelector('.infrastructure-quick-stats'));
    assert.ok(document.querySelector('.infrastructure-quick-stats .battery-mini-chart path'));
    assert.equal(document.querySelector('.battery-mini-chart circle'), null);
    assert.equal(document.querySelector('.device-sheet h2').textContent, 'R001');
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['R001']);
    assertMarkerStyle(canvas().querySelector('button.infrastructure-pin'), miniPins()[0]);
    assert.equal(miniLines().length, 0);
    assert.deepEqual(JSON.parse(mini().dataset.camera).center, [infrastructure[0].longitude, infrastructure[0].latitude]);
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => document.querySelector('.device-sheet-header button').click());
    await act(async () => toggle().click());
    assert.equal(toggle().getAttribute('aria-pressed'), 'true');
    assert.equal(features().length, 1, 'reverse observations share one geographic line');
    assert.equal(document.querySelectorAll('.signal-map-label').length, 0);
    const legend = document.querySelector('.signal-legend');
    const info = document.querySelector('.signal-info-button');
    assert.equal(legend.querySelector('small'), null, 'explanation starts hidden');
    assert.equal(window.getComputedStyle(legend).position, 'absolute', 'legend expansion is outside button layout');
    assert.equal(window.getComputedStyle(document.querySelector('.map-tools')).alignItems, 'flex-start');
    const fitStyle = window.getComputedStyle(toggle().previousElementSibling).cssText;
    assert.equal(info.getAttribute('aria-expanded'), 'false');
    await act(async () => info.click());
    assert.equal(info.getAttribute('aria-expanded'), 'true');
    assert.match(legend.querySelector('small').textContent, /1 observations.*omitted/);
    assert.equal(window.getComputedStyle(toggle().previousElementSibling).cssText, fitStyle);
    await act(async () => info.click());
    assert.equal(legend.querySelector('small'), null);
    const line = features()[0];
    assert.equal(line.properties.color, '#b42318');
    const style = JSON.parse(canvas().dataset.style);
    assert.ok(style.layers.find(layer => layer.id === 'signal-hit-area').paint['line-width'] >= 20);
    await act(async () => canvas().dispatchEvent(new window.CustomEvent('test-map-click', {
      detail: { layer: 'signal-hit-area', id: line.properties.id },
    })));
    let sheet = document.querySelector('.signal-link-detail');
    assert.equal(sheet.dataset.mode, 'panel');
    assert.ok(sheet.querySelector('.signal-location-details'), 'neighbor cards retain endpoint location context');
    assert.match(sheet.textContent, /Endpoint locations/);
    assert.equal(document.querySelectorAll('.signal-reading').length, 2);
    assert.match(sheet.textContent, /0 dB/);
    assert.match(sheet.textContent, /-112 dBm/);
    assert.match(sheet.textContent, /S001 → R001/);
    assert.match(sheet.textContent, /R001 → S001/);
    assert.match(sheet.textContent, /Delivery time does not refresh signal age/);
    assert.match(sheet.textContent, /Original packet sourceS002/);
    assert.equal(sheet.querySelector('time').dateTime, at);
    assert.equal(features()[0].properties.width, 6);
    await render(links, false);
    assert.match(document.querySelector('.signal-link-detail').textContent, /Feed offline/);
    const updated = [{ ...links[0], id: 'new-forward', snrDb: 10,
      observedAt: new Date(now - 60000).toISOString(), receivedAt: new Date(now - 60000).toISOString() }, links[0]];
    await render(updated);
    assert.equal(document.querySelectorAll('.signal-reading').length, 1);
    assert.equal(document.querySelector('.signal-map-label'), null);
    assert.equal(features()[0].properties.color, '#237346');
    assert.equal(miniLines()[0].properties.color, '#237346', 'card line follows updated signal readings');
    await act(async () => [...document.querySelectorAll('.segmented button')].find(b => b.textContent === 'Aerial imagery').click());
    assert.equal(features().length, 1, 'signal source survives basemap recreation');
    assert.match(JSON.parse(mini().dataset.style).sources.basemap.tiles[0], /USGSImageryOnly/);
    assert.equal(miniPins().length, 2, 'basemap change retains both endpoints');
    assert.equal(miniLines().length, 1, 'basemap change retains the card line');
    assert.equal(document.querySelector('.signal-map-label'), null);
    let bubbled = 0;
    const onCanvasClick = () => { bubbled++; };
    canvas().addEventListener('click', onCanvasClick);
    const trackerPin = document.querySelector('button.map-pin');
    await act(async () => trackerPin.click());
    assert.equal(bubbled, 0, 'node clicks do not bubble into map line selection');
    canvas().removeEventListener('click', onCanvasClick);
    await act(async () => canvas().dispatchEvent(new window.CustomEvent('test-map-click', {
      detail: { layer: 'signal-hit-area', id: line.properties.id, target: trackerPin },
    })));
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    assert.ok(document.querySelector('.tracker-detail'));
    assert.match(JSON.parse(mini().dataset.style).sources.basemap.tiles[0], /USGSImageryOnly/, 'new cards inherit main map selection');
    assert.match(document.querySelector('.node-relationship').textContent, /S001 → R001.*10 dB/);
    await act(async () => document.querySelector('button.infrastructure-pin').click());
    const infraPin = document.querySelector('button.infrastructure-pin');
    await act(async () => canvas().dispatchEvent(new window.CustomEvent('test-map-click', {
      detail: { layer: 'signal-hit-area', id: line.properties.id, target: infraPin },
    })));
    assert.ok(document.querySelector('.infrastructure-quick-stats'), 'infrastructure marker wins over overlapping line');
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    assert.match(document.querySelector('.node-relationship').textContent, /S001 → R001.*10 dB/);
    await act(async () => document.querySelector('.node-relationship').click());
    assert.ok(document.querySelector('.signal-link-detail'));
    await act(async () => trackerPin.click());
    await act(async () => toggle().click());
    assert.ok(document.querySelector('.tracker-detail'), 'hiding signals preserves a tracker selection');
    assert.equal(features().length, 0);
    assert.equal(document.querySelector('.signal-map-label'), null);
    mobile = true;
    await act(async () => document.querySelector('.node-relationship').click());
    assert.equal(document.querySelector('.signal-link-detail').dataset.mode, 'modal');
    await act(async () => document.querySelector('[aria-label="Open S001 node card"]').click());
    assert.equal(document.querySelector('.tracker-detail').dataset.mode, 'modal');
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => document.querySelector('[aria-label="Open R001 node card"]').click());
    assert.equal(document.querySelector('.infrastructure-quick-stats').dataset.mode, 'modal');
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => document.querySelector('.device-sheet').dispatchEvent(new window.Event('cancel', { cancelable: true })));
    assert.equal(document.querySelector('.device-sheet'), null);
    await act(async () => infraPin.click());
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => toggle().click());
    await act(async () => toggle().click());
    assert.ok(document.querySelector('.signal-link-detail'), 'hiding the layer preserves relationship details');
    await act(async () => toggle().click());
    await render(updated, true, initialTrackers.map(t => ({ ...t, position: null })));
    assert.equal(features().length, 0);
    assert.ok(document.querySelector('.signal-link-detail'), 'missing GPS does not hide the recorded relationship');
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['R001']);
    assert.equal(miniLines().length, 0, 'missing coordinates never invent a line');
    assert.match(document.querySelector('.card-mini-map').textContent, /S001: location unknown/);
    await act(async () => infraPin.click());
    assert.equal(document.querySelectorAll('.node-relationship').length, 1);
    await act(async () => document.querySelector('.node-relationship').click());
    await act(async () => document.querySelector('.signal-location-details summary').click());
    assert.match(document.querySelector('.signal-location-details').textContent, /Location unknown/);
    await act(async () => document.querySelector('.signal-info-button').click());
    assert.match(document.querySelector('#signal-legend-help').textContent, /No neighbor connections/);
    await render([]);
    assert.equal(document.querySelector('.signal-map-label'), null, 'empty live data never creates fixture lines');
    await act(async () => document.querySelector('button.infrastructure-pin').click());
    assert.equal(document.querySelector('.node-relationship'), null);
    assert.match(document.querySelector('.node-relationships').textContent, /No recent neighbors/);
    const assigned = [{ id: 'assigned', deviceId: 'd1', memberId: 'm1', startedAt: at, endedAt: null }];
    const members = [{ id: 'm1', name: 'Demo Member', initials: 'DM', shortName: 'ALIAS' }];
    await render(links, true, initialTrackers, assigned, members);
    await act(async () => document.querySelector('button.map-pin').click());
    assert.equal(document.querySelector('button.map-pin').textContent, 'ALIAS');
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['ALIAS'], 'assigned client mini map matches the main marker');
    await act(async () => document.querySelector('.node-relationship').click());
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['ALIAS', 'R001'], 'relationship mini map also uses the assigned member shortname');
    await act(async () => mini().querySelector('[aria-label="Open ALIAS node card"]').click());
    assert.ok(document.querySelector('.tracker-detail'), 'assigned marker opens its device by persistent identity');
    await act(async () => document.querySelector('.node-relationship').click());
    await render();
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['S001', 'R001'], 'releasing an assignment restores the device label');
    for (const [minutes, state] of [[1, 'recent'], [5, 'aging'], [20, 'stale'], [180, 'unknown']]) {
      const trackers = initialTrackers.map((tracker, index) => index ? tracker : { ...tracker,
        position: { ...tracker.position, measuredAt: new Date(now - minutes * 60000).toISOString() } });
      await render(links, true, trackers);
      assert.ok(miniPins()[0].classList.contains(state), `relationship endpoint follows ${state} status`);
      assertMarkerStyle(canvas().querySelector('button.map-pin'), miniPins()[0]);
      await act(async () => canvas().querySelector('button.map-pin').click());
      assertMarkerStyle(canvas().querySelector('button.map-pin'), miniPins()[0]);
      assert.ok(miniPins()[0].classList.contains('selected-pin'), 'node card preserves the selected outline');
      await act(async () => document.querySelector('.node-relationship').click());
    }
    const { default: UsersPage } = await import('../src/UsersPage.tsx');
    await act(async () => root.render(createElement(MapPreferences, null, createElement(UsersPage, {
      trackers: initialTrackers, now, assignments: assigned, members, nameJobs: [], admin: true,
      online: true, trailId: null, onTrailChange() {}, onAssign() {}, onRelease() {}, onJob() {},
    }))));
    await act(async () => document.querySelector('.users-trackers .tracker-row').click());
    assert.match(JSON.parse(mini().dataset.style).sources.basemap.tiles[0], /USGSImageryOnly/, 'main map selection survives navigation to Users');
    assert.deepEqual(miniPins().map(pin => pin.textContent), ['ALIAS'], 'Users card uses the assigned member shortname');
    assert.ok(miniPins()[0].classList.contains('map-pin'));
    assert.ok(miniPins()[0].classList.contains('recent'));
    assert.ok(miniPins()[0].classList.contains('selected-pin'));
    await act(async () => document.querySelector('.device-sheet-header button').click());
    const userRows = document.querySelectorAll('.users-trackers .tracker-row');
    await act(async () => userRows[userRows.length - 1].click());
    assert.equal(mini(), null, 'never-seen nodes do not show a fabricated location');
    assert.match(document.querySelector('.mini-map-missing').textContent, /No recorded location/);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    for (const key of ['window', 'document', 'HTMLElement', 'HTMLButtonElement', 'ResizeObserver', 'IS_REACT_ACT_ENVIRONMENT']) delete globalThis[key];
  }
});

test('switching repeaters and backhauls retains exactly one selected device detail', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: InfrastructurePage } =
    await import('../src/InfrastructurePage.tsx');
  const { infrastructure } = await import('../src/demo.ts');
  const root = createRoot(document.getElementById('root'));
  try {
    await act(async () =>
      root.render(
        createElement(InfrastructurePage, {
          now: Date.now(),
          infrastructureNodes: infrastructure,
          online: true,
          admin: true,
          incidents: [],
          events: [],
          rules: {},
          onRule() {},
          onIncident() {},
        }),
      ),
    );
    const cards = document.querySelectorAll('.infra-card');
    assert.equal(cards.length, 4);
    assert.match(document.querySelector('.detail-grid').textContent, /47.1 °F/);
    for (const index of [0, 2, 3, 1, 0, 2, 3, 0]) {
      await act(async () => cards[index].click());
      assert.equal(
        document.querySelectorAll('.battery-history').length,
        1,
        'one battery detail after every device switch',
      );
      assert.equal(
        document.querySelectorAll('.rule-section').length,
        1,
        'one battery rule form',
      );
      assert.equal(
        document.querySelectorAll('.panel:not(.neighbor-panel)').length,
        2,
        'one device panel and one audit panel',
      );
      assert.equal(
        document.querySelector('.panel:not(.neighbor-panel) h2').textContent,
        cards[index].querySelector('strong').textContent,
      );
    }
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});

test('map selections and device sheets keep infrastructure always visible without a dashboard', async () => {
  const dom = new JSDOM('<div id="root"></div>', { url: 'https://portal.example.test/' });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.ResizeObserver = class { observe() {} disconnect() {} };
  let mobile = true;
  window.matchMedia = () => ({ matches: mobile, addEventListener() {}, removeEventListener() {} });
  // jsdom has no native dialog behavior. Verify which browser API we request;
  // focus containment, visual placement and gestures still require a browser.
  const dialog = window.HTMLDialogElement.prototype;
  dialog.showModal = function () { this.open = true; this.dataset.mode = 'modal'; };
  dialog.show = function () { this.open = true; this.dataset.mode = 'panel'; };
  dialog.close = function () { this.open = false; };
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: MapPage } = await import('../src/MapPage.tsx');
  const { default: UsersPage } = await import('../src/UsersPage.tsx');
  const { infrastructure, initialTrackers } = await import('../src/demo.ts');
  const now = Date.now();
  const devices = [
    { ...infrastructure[0], id: 'r001', name: 'R001',
      lastContactAt: new Date(now - 60000).toISOString(), humidity: 42.3 },
    { ...infrastructure[1], id: 'g001', name: 'G001', role: 'Backhaul',
      longitude: infrastructure[0].longitude, latitude: infrastructure[0].latitude },
  ];
  const root = createRoot(document.getElementById('root'));
  function MapHarness({ online, trackers, assigned }) {
    const [selectedId, select] = useState('');
    const [trailId, onTrailChange] = useState(null);
    return createElement(MapPage, { trackers,
      assignments: assigned ? [{ id: 'a1', deviceId: 'd1', memberId: 'm1', startedAt: new Date(now - 3600000).toISOString(), endedAt: null }] : [],
      members: [{ id: 'm1', name: 'Demo Member', initials: 'DM', shortName: 'ALIAS' }],
      infrastructureNodes: devices, labels: Object.fromEntries(trackers.map(t => [t.id, t.shortName])),
      selectedId, onSelect: select, now, online, trailId, onTrailChange });
  }
  const render = (online = true, trackers = initialTrackers, assigned = true) => act(async () => {
    root.render(createElement(MapHarness, { online, trackers, assigned }));
  });
  const closeSheet = async () => act(async () => {
    document.querySelector('.device-sheet button').click();
  });
  try {
    // Old saved preferences must not hide infrastructure after the toggle removal.
    document.cookie = 'meshlink-map-infrastructure=off; Path=/';
    await render();
    assert.equal(document.querySelectorAll('.summary-card, .tracker-panel, .detail-panel').length, 0);
    assert.equal(document.querySelector('.device-sheet'), null, 'nothing opens before a marker click');
    assert.equal(document.querySelector('.map-infrastructure-toggle'), null);
    let markers = document.querySelectorAll('button.infrastructure-pin');
    assert.deepEqual([...markers].map(m => m.textContent), ['R001', 'G001']);
    assert.notEqual(markers[0].dataset.offset, markers[1].dataset.offset);
    assert.equal(document.querySelectorAll('.map-pin')[0].textContent, 'ALIAS');
    assert.equal(document.querySelectorAll('.map-pin')[1].textContent, 'S002');
    await act(async () => markers[0].click());
    let detail = document.querySelector('.infrastructure-quick-stats');
    assert.equal(detail.dataset.mode, 'modal');
    assert.match(detail.textContent, /Discharging/);
    assert.match(detail.textContent, /— mA/);
    assert.match(detail.textContent, /Estimated battery percentage/);
    assert.doesNotMatch(detail.textContent, /trend|mV\/h|overstate|cutoff|load and temperature/i);
    assert.match(detail.textContent, /42.3% RH/);
    assert.match(detail.textContent, /47.1 °F/);
    assert.match(detail.textContent, /Last heard/);
    assert.match(detail.textContent, /≈45%/);
    await act(async () => markers[1].click());
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    assert.equal(document.querySelector('.device-sheet h2').textContent, 'G001');
    assert.deepEqual([...document.querySelectorAll('.mini-map-pin')].map(pin => pin.textContent), ['G001'], 'gateway card shows only the gateway');
    assert.ok(document.querySelector('.mini-map-pin').classList.contains('infrastructure-pin'));
    assert.ok(document.querySelector('.mini-map-pin').classList.contains('selected-pin'));
    assert.doesNotMatch(document.querySelector('.device-sheet').textContent, /Relative humidity/);
    await render(false);
    assert.match(document.querySelector('.device-sheet').textContent, /Feed offline/);
    assert.match(document.querySelector('.map-feed-status').textContent, /Feed offline/);
    await closeSheet();
    assert.equal(document.querySelector('.device-sheet'), null);

    const tracker = document.querySelector('button.map-pin');
    tracker.focus();
    await act(async () => tracker.click());
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    assert.equal(document.querySelector('.tracker-detail').dataset.mode, 'modal');
    assert.match(document.querySelector('.tracker-detail').textContent, /Location/);
    assert.match(document.querySelector('.device-sheet-header').textContent, /Heltec V4 - S001/);
    assert.equal(document.querySelector('.tracker-detail .sheet-title .badge').textContent, 'Active');
    assert.doesNotMatch(document.querySelector('.tracker-detail').textContent, /Older fix|Reported battery|Battery voltage|Save battery configuration|Estimated battery percentage/);
    assert.ok(document.querySelector('.sheet-title .badge').nextElementSibling.matches('.tracker-battery-icon'));
    assert.equal(document.querySelector('.tracker-battery-icon text'), null);
    assert.equal(document.querySelector('.tracker-battery-icon').getAttribute('aria-label'), 'Battery 100%');
    assert.equal(document.querySelector('.tracker-battery-icon rect').getAttribute('fill'), 'currentColor');
    assert.match(document.querySelector('.tracker-battery-icon').getAttribute('class'), /green/);
    assert.equal(document.querySelector('.tracker-battery'), null);
    assert.match(document.querySelector('[aria-label="Latest session"]').textContent, /First Seen.*Last Heard.*Time Active/s);
    const sessionFields = [...document.querySelectorAll('.session-grid > div')];
    assert.doesNotMatch(sessionFields[0].querySelector('dd').textContent, /ago|min|hrs/);
    assert.equal(sessionFields[2].querySelector('dt').textContent, 'Time Active');
    assert.equal(sessionFields[3].querySelector('dt').textContent, 'Distance Travelled');
    assert.match(sessionFields[3].querySelector('dd').textContent, /^\d+\.\d mi$/);
    const beforeTrail = document.querySelector('.tracker-detail').textContent;
    const trailToggle = document.querySelector('.trail-control input');
    await act(async () => trailToggle.click());
    assert.ok(document.querySelectorAll('.trail-pin').length > 0);
    assert.equal(document.querySelector('.tracker-detail').textContent, beforeTrail, 'checking the box adds no card UI or copy');
    assert.equal(document.querySelectorAll('.history-detail, .point-buttons, .history-controls, .tracker-detail select').length, 0);
    assert.match(document.querySelector('.trail-control').textContent, /Show Recorded Trail/);
    assert.match(document.querySelector('.tracker-gps-quality').textContent, /GPS quality/);
    assert.match(document.querySelector('.gps-quality-pill').textContent, /Good/);
    const trail = JSON.parse(document.querySelector('.map-canvas').dataset.trail);
    assert.equal(trail.features.length, document.querySelectorAll('.trail-pin').length - 1);
    await closeSheet();
    assert.equal(document.activeElement, tracker, 'closing restores marker focus');
    assert.ok(document.querySelectorAll('.trail-pin').length > 0, 'trail stays visible when sheet closes');
    assert.equal(document.querySelectorAll('button.trail-pin').length, 0, 'trail dots do not open more detail UI');
    await act(async () => tracker.click());
    await act(async () => document.querySelector('.trail-control input').click());
    assert.equal(document.querySelectorAll('.trail-pin').length, 0);
    await act(async () => document.querySelector('.device-sheet').dispatchEvent(new window.Event('cancel', { cancelable: true })));
    assert.equal(document.querySelector('.device-sheet'), null, 'native Escape/cancel closes');

    // Desktop remains a compact nonmodal overlay and selection stays exclusive.
    mobile = false;
    await act(async () => markers[0].click());
    assert.equal(document.querySelector('.device-sheet').dataset.mode, 'panel');
    await act(async () => tracker.click());
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    assert.ok(document.querySelector('.tracker-detail'));
    await act(async () => document.querySelector('.device-sheet').dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true })));
    assert.equal(document.querySelector('.device-sheet'), null);
    await act(async () => root.render(null));
    await render();
    assert.equal(document.querySelector('.map-infrastructure-toggle'), null);
    assert.equal(document.querySelectorAll('.infrastructure-pin').length, 2, 'infrastructure stays visible after remount despite old off cookie');
    await render(true, initialTrackers, false);
    assert.equal(document.querySelector('.map-pin').textContent, 'S001', 'release restores the radio label');
    const old = { ...initialTrackers[0], lastContactAt: new Date(now - 3 * 3600000).toISOString(),
      position: { ...initialTrackers[0].position, measuredAt: new Date(now - 3 * 3600000).toISOString(), areaName: 'Demo area' } };
    await render(true, [old]);
    assert.equal(document.querySelectorAll('.map-pin').length, 1, 'No Location keeps its last pin');
    await act(async () => document.querySelector('.map-pin').click());
    assert.equal(document.querySelector('.sheet-title .badge').textContent, 'No Location');
    assert.match(document.querySelector('.gps-quality-pill').textContent, /Good/,
      'quality describes the saved fix independently of its age');
    assert.match(document.querySelector('.tracker-detail').textContent, /Demo area/);
    assert.equal((document.querySelector('[aria-label="Location"]').textContent.match(/\+2hrs/g) || []).length, 2);
    const originalNavigator = Object.getOwnPropertyDescriptor(globalThis, 'navigator');
    let copied = '';
    Object.defineProperty(globalThis, 'navigator', { configurable: true, value: { clipboard: {
      writeText: async (text) => { copied = text; },
    } } });
    try {
      await act(async () => document.querySelector('[aria-label="Copy coordinates"]').click());
      assert.equal(copied, `${old.position.latitude.toFixed(5)}, ${old.position.longitude.toFixed(5)}`);
      assert.match(document.querySelector('.tracker-detail').textContent, /Coordinates copied/);
      assert.ok(document.querySelector('.copy-check'));
      assert.equal(document.querySelector('[aria-label="Copy coordinates"]').title, 'Copied');
      await act(async () => document.querySelector('.coordinate-copy span').click());
      assert.equal(copied, `${old.position.latitude.toFixed(5)}, ${old.position.longitude.toFixed(5)}`);
      navigator.clipboard.writeText = async () => { throw new Error('Clipboard unavailable'); };
      await act(async () => document.querySelector('[aria-label="Copy coordinates"]').click());
      assert.match(document.querySelector('.tracker-detail').textContent, /Unable to copy/);
    } finally {
      if (originalNavigator) Object.defineProperty(globalThis, 'navigator', originalNavigator);
      else delete globalThis.navigator;
    }
    await closeSheet();
    await render(true, []);
    assert.equal(document.querySelectorAll('.map-pin').length, 0);
    await act(async () => document.querySelector('.infrastructure-pin').click());
    assert.ok(document.querySelector('.infrastructure-quick-stats'), 'infrastructure works with zero member trackers');

    await act(async () => root.render(createElement(UsersPage, { trackers: initialTrackers, now,
      assignments: [], members: [], nameJobs: [], admin: true, online: false, trailId: null, onTrailChange() {},
      onAssign() {}, onRelease() {}, onJob() {} })));
    assert.equal(document.querySelectorAll('.summary-card').length, 4);
    assert.match(document.querySelector('.summary-grid').textContent, /Member trackers|Within 15 minutes|Stale positions|Unknown \/ never seen/);
    const userTrackers = document.querySelectorAll('.users-trackers .tracker-row');
    assert.equal(userTrackers.length, initialTrackers.length);
    await act(async () => userTrackers[userTrackers.length - 1].click());
    assert.match(document.querySelector('.tracker-detail').textContent, /No recorded position/);
    assert.match(document.querySelector('.gps-quality-pill').textContent, /Unknown/);
    assert.doesNotMatch(document.querySelector('.tracker-detail').textContent, /Save battery configuration/);
    await closeSheet();
    await act(async () => userTrackers[0].click());
    assert.match(document.querySelector('.tracker-detail').textContent, /Coordinates/);
    assert.match(document.querySelector('.gps-quality-pill').textContent, /Good/);
    assert.equal(document.querySelectorAll('.device-sheet').length, 1);
    const { default: TrackerBatteryIcon } = await import('../src/TrackerBatteryIcon.tsx');
    for (const [battery, tone, digits] of [[0, 'red', '00'], [9, 'red', '09'], [19, 'red', '19'],
      [20, 'amber', '20'], [39, 'amber', '39'], [40, 'green', '40'], [99, 'green', '99'],
      [100, 'green', null], [null, 'unknown', '—'], [NaN, 'unknown', '—']]) {
      await act(async () => root.render(createElement(TrackerBatteryIcon, { battery })));
      const icon = document.querySelector('.tracker-battery-icon');
      assert.ok(icon.classList.contains(tone));
      assert.equal(icon.querySelector('text')?.textContent ?? null, digits);
      assert.equal(icon.querySelector('rect').getAttribute('fill'), battery === 100 ? 'currentColor' : 'none');
    }
    const { default: MapShortName } = await import('../src/MapShortName.tsx');
    let savedShortName = '';
    await act(async () => root.render(createElement(MapShortName, { shortName: 'CJ_5',
      onSave: async (value) => { savedShortName = value; return true; } })));
    const shortnameInput = document.querySelector('input[name="shortName"]');
    assert.equal(shortnameInput.maxLength, 5);
    assert.equal(shortnameInput.required, true);
    await act(async () => document.querySelector('.map-shortname-form').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true })));
    assert.equal(savedShortName, 'CJ_5');
    assert.match(document.querySelector('[role="status"]').textContent, /Map shortname saved/);

  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    for (const key of ['window', 'document', 'HTMLElement', 'HTMLButtonElement', 'ResizeObserver', 'IS_REACT_ACT_ENVIRONMENT']) delete globalThis[key];
  }
});

test('neighbor rows preserve direction, zero readings, known hearing times and receiver filtering', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: NeighborTable } = await import('../src/NeighborTable.tsx');
  const root = createRoot(document.getElementById('root'));
  const now = Date.now();
  const at = new Date(now - 5 * 60000).toISOString();
  const links = [
    { id: 'n', observerDeviceId: 'r1', heardDeviceId: 'r2', originalSourceDeviceId: null,
      source: 'neighbor', path: 'direct', snrDb: 0, rssiDbm: null, receivedAt: at, observedAt: at },
    { id: 'g', observerDeviceId: 'g1', heardDeviceId: null, originalSourceDeviceId: 'd1',
      source: 'gateway', path: 'relayed', snrDb: -3.5, rssiDbm: -118, receivedAt: at, observedAt: at },
  ];
  try {
    await act(async () => root.render(createElement(NeighborTable, {
      links, now, online: false, trackers: [{ id: 'd1', shortName: 'S001' }],
      infrastructure: [{ id: 'r1', name: 'Demo repeater' }, { id: 'r2', name: 'Demo other repeater' }, { id: 'g1', name: 'Demo gateway' }],
    })));
    assert.equal(document.querySelectorAll('tbody tr').length, 2);
    assert.match(document.querySelector('tbody').textContent, /0 dB/);
    assert.match(document.querySelector('tbody').textContent, /-118 dBm/);
    assert.match(document.querySelector('tbody').textContent, /S001/);
    assert.match(document.querySelector('[role="status"]').textContent, /saved observations/);
    const neighbor = document.querySelector('tbody tr');
    assert.equal(neighbor.querySelectorAll('time')[0].textContent, '5m ago');
    assert.equal(neighbor.querySelectorAll('time')[1].textContent, '5m ago');
    const select = document.querySelector('select');
    await act(async () => { select.value = 'g1'; select.dispatchEvent(new window.Event('change', { bubbles: true })); });
    assert.equal(document.querySelectorAll('tbody tr').length, 1);
    assert.match(document.querySelector('tbody').textContent, /Relayed/);
    assert.doesNotMatch(document.querySelector('tbody').textContent, /Demo other repeater/);
    await act(async () => { select.value = 'r2'; select.dispatchEvent(new window.Event('change', { bubbles: true })); });
    assert.equal(document.querySelector('table'), null);
    assert.match(document.querySelector('.empty').textContent, /No recent neighbor signals/);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});


test('gateway voltage samples remain visible without a configured reporting cadence', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: BatteryChart } = await import('../src/BatteryChart.tsx');
  const { infrastructure } = await import('../src/demo.ts');
  const now = Date.parse('2026-10-21T18:00:00Z');
  const samples = [
    { at: '2026-10-21T17:50:00Z', volts: 4.25 },
    { at: '2026-10-21T17:55:00Z', volts: 4.24 },
  ];
  const device = { ...infrastructure[0], id: 'g002', name: 'G002', cadenceMinutes: 0,
    reportCadenceMinutes: {}, missingTimeoutMinutes: {}, samples: [], battery: 4.24 };
  const loadHistory = async () => ({ samples, truncated: false });
  const root = createRoot(document.getElementById('root'));
  try {
    await act(async () => root.render(createElement(BatteryChart, {
      device: { ...device, cadenceMinutes: 5, batteryProfile: 'unknown' }, now, loadHistory,
    })));
    assert.ok(document.querySelector('path'), 'same loader and readings work with positive cadence, without pack metadata');
    await act(async () => root.render(createElement(BatteryChart, { device, now, loadHistory })));
    assert.ok(document.querySelector('svg'), 'received gateway history must populate the graph');
    assert.equal(document.querySelectorAll('circle').length, 2, 'show exact readings with unknown cadence');
    assert.equal(document.querySelector('path'), null, 'unknown cadence must not imply continuity');
    assert.equal(document.querySelector('.battery-mini-empty'), null);
    await act(async () => root.render(createElement(BatteryChart, {
      device: { ...device, id: 'g001', cadenceMinutes: 5, samples: [samples[0]] }, now,
    })));
    assert.equal(document.querySelectorAll('circle').length, 1, 'first reading is visible before a second arrives');
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});

test('minimal battery charts load each period, retain outages, and reject obsolete requests', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: BatteryChart } = await import('../src/BatteryChart.tsx');
  const { infrastructure } = await import('../src/demo.ts');
  const now = Date.now();
  const requests = [];
  const loadHistory = (id, hours, signal) => new Promise(resolve => requests.push({ id, hours, signal, resolve }));
  const root = createRoot(document.getElementById('root'));
  const device = { ...infrastructure[0], samples: [] };
  const render = (value = device) => act(async () => root.render(createElement(BatteryChart, { device: value, now, loadHistory })));
  const series = (hours) => Array.from({ length: hours * 6 + 1 }, (_, i) => ({
    at: new Date(now - (hours * 6 - i) * 600000).toISOString(), volts: 3.9 + .2 * Math.sin(i * Math.PI / 72),
  }));
  const buttons = () => [...document.querySelectorAll('.battery-periods button')];
  try {
    await render();
    assert.deepEqual(buttons().map(b => b.textContent), ['24hr', '7day', '30day']);
    assert.equal(requests[0].hours, 24);
    await act(async () => requests[0].resolve({ samples: series(24), truncated: false }));
    let path = document.querySelector('.battery-mini-chart path').getAttribute('d');
    assert.ok(path.includes('C'));
    assert.equal(document.querySelectorAll('.battery-mini-chart circle, .battery-mini-chart line, .battery-mini-chart polyline').length, 0);
    assert.equal(document.querySelectorAll('.battery-mini-chart text').length, 6, 'only small axis values');
    await act(async () => buttons()[1].click());
    assert.equal(requests[1].hours, 168);
    assert.equal(requests[0].signal.aborted, true);
    await act(async () => buttons()[2].click());
    assert.equal(requests[2].hours, 720);
    assert.equal(requests[1].signal.aborted, true);
    await act(async () => requests[2].resolve({ samples: series(720), truncated: false }));
    path = document.querySelector('.battery-mini-chart path').getAttribute('d');
    assert.ok(path.length > 100000, 'full month of cycles is plotted');
    assert.match(document.querySelector('svg').getAttribute('aria-label'), /30 days/);
    await act(async () => requests[1].resolve({ samples: [], truncated: false }));
    assert.equal(document.querySelector('.battery-mini-chart path').getAttribute('d'), path, 'stale range response is ignored');
    await render({ ...device, id: 'b1', name: 'Gateway' });
    assert.equal(requests.at(-1).id, 'b1');
    await act(async () => requests.at(-1).resolve({ samples: [], truncated: false }));
    assert.equal(document.querySelector('svg'), null, 'empty history never fabricates readings');
    assert.match(document.querySelector('.battery-mini-empty').textContent, /Not enough battery history/);
  } finally {
    await act(async () => root.unmount());
    assert.equal(requests.at(-1).signal.aborted, true);
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});
