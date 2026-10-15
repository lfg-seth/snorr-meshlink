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

test('switching repeaters and backhauls retains exactly one selected device detail', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: InfrastructurePage } =
    await import('../src/InfrastructurePage.tsx');
  const root = createRoot(document.getElementById('root'));
  try {
    await act(async () =>
      root.render(
        createElement(InfrastructurePage, {
          now: Date.now(),
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
        document.querySelectorAll('.panel').length,
        2,
        'one device panel and one audit panel',
      );
      assert.equal(
        document.querySelector('.panel h2').textContent,
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
    assert.doesNotMatch(document.querySelector('.tracker-detail').textContent, /Save battery configuration/);
    await closeSheet();
    await act(async () => userTrackers[0].click());
    assert.match(document.querySelector('.tracker-detail').textContent, /Coordinates/);
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
