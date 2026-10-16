import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { registerHooks } from 'node:module';
import test from 'node:test';
import { act, createElement } from 'react';
import { JSDOM } from 'jsdom';
import ts from 'typescript';

// Run the real application in live-build mode; replace only browser assets and
// WebGL, as in the device interaction tests.
registerHooks({
  resolve(specifier, context, next) {
    if (specifier === 'maplibre-gl')
      return next(new URL('./maplibre-stub.mjs', import.meta.url).href, context);
    if (specifier.endsWith('.png'))
      return { url: 'data:text/javascript,export default "/test-logo.png"', shortCircuit: true };
    if (specifier.endsWith('.css') || specifier.includes('?worker&url'))
      return { url: 'data:text/javascript,export default ""', shortCircuit: true };
    try { return next(specifier, context); }
    catch (error) {
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
    if (!url.endsWith('.tsx') && !url.endsWith('.ts')) return next(url, context);
    const source = readFileSync(new URL(url), 'utf8').replaceAll(
      'import.meta.env', '({ VITE_PORTAL_MODE: "live" })',
    );
    return { format: 'module', shortCircuit: true, source: ts.transpileModule(source, {
      compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.ReactJSX },
    }).outputText };
  },
});

test('production opens the isolated demo by default and live sign-in survives refresh', async () => {
  const dom = new JSDOM('<div id="root"></div>', { url: 'https://portal.example.test/' });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.ResizeObserver = class { observe() {} disconnect() {} };
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  window.matchMedia = () => ({ matches: false, addEventListener() {}, removeEventListener() {} });
  const originalFetch = globalThis.fetch;
  const requests = [];
  let stateFailure = 0;
  let demoFailure = false;
  let demoGate;
  let stateGate;
  const account = { id: 'admin', name: 'Test Admin', role: 'admin', memberId: '' };
  const emptyState = { account, simulation: false, feedOnline: true,
    trackers: [], members: [], assignments: [], nameJobs: [], messages: [],
    infrastructure: [], links: [], incidents: [], warnings: [], rules: {}, events: [] };
  const demoAccount = { ...account, id: 'demo-admin', name: 'Demo Dispatch' };
  const demoState = { ...emptyState, account: demoAccount, simulation: true,
    trackers: [{ id: 'db-tracker', number: '901', shortName: 'DB901', battery: 100, position: null, history: [] }],
    members: [{ id: 'db-member', name: 'Demo Database Person', initials: 'DP' }],
    assignments: [{ id: 'db-assignment', deviceId: 'db-tracker', memberId: 'db-member',
      startedAt: new Date().toISOString(), endedAt: null }],
    infrastructure: [{ id: 'db-gateway', name: 'Demo database gateway', role: 'Backhaul',
      reportedAt: null, cadenceMinutes: 2, battery: null, temperature: null, solar: null, intrusion: null,
      equipped: { solar: false, weather: false, intrusion: false }, batterySetup: 'Unknown', solarSetup: 'Unknown', antenna: 'Unknown', samples: [] }],
    links: [{ id: 'db-link', observerDeviceId: 'db-gateway', heardDeviceId: 'db-tracker',
      originalSourceDeviceId: 'db-tracker', source: 'gateway', path: 'direct', snrDb: 0, rssiDbm: -101,
      receivedAt: new Date().toISOString(), observedAt: null }],
  };
  globalThis.fetch = async (url, options) => {
    requests.push({ url, options });
    const demo = url.startsWith('/demo-api/');
    if (demo && demoGate) await demoGate;
    if (demo && demoFailure) throw new Error('Demo PocketBase unavailable');
    if (url.endsWith('/auth-with-password'))
      return { ok: true, json: async () => ({ token: demo ? 'demo-token' : 'test-token', record: demo ? demoAccount : account }) };
    assert.equal(options.headers.Authorization, demo ? 'demo-token' : 'test-token');
    if (!demo && stateGate) await stateGate;
    if (!demo && stateFailure) return { ok: false, status: stateFailure,
      json: async () => ({ message: 'Test backend failure' }) };
    return { ok: true, json: async () => demo ? demoState : emptyState };
  };
  const { createRoot } = await import('react-dom/client');
  const { default: App } = await import('../src/App.tsx');
  const root = createRoot(document.getElementById('root'));
  const button = (label) => [...document.querySelectorAll('button')].find(b => b.textContent === label);
  const navigate = async (hash) => act(async () => {
    window.location.hash = hash;
    window.dispatchEvent(new window.HashChangeEvent('hashchange'));
  });
  try {
    await act(async () => root.render(createElement(App)));
    assert.ok(document.querySelector('.app-shell'));
    assert.ok(document.querySelector('.brand-row .access-button'));
    assert.equal(document.querySelector('.brand-row .access-button').textContent, 'Sign in');
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo');
    assert.equal(document.querySelector('.demo-banner'), null, 'map remains banner-free');
    await navigate('#users');
    assert.match(document.querySelector('.users-trackers').textContent, /Demo Database Person/);
    assert.ok(document.querySelectorAll('.tracker-row').length > 0);
    assert.ok(requests.length >= 2, 'demo authenticates and reads its PocketBase');
    assert.ok(requests.every(r => r.url.startsWith('/demo-api/')), 'demo cannot use production routes');
    assert.equal(window.sessionStorage.length, 0, 'demo tokens cannot become saved production sign-ins');
    await navigate('#infrastructure');
    assert.match(document.querySelector('.neighbor-table').textContent, /DB901/);
    assert.match(document.querySelector('.neighbor-table').textContent, /0 dB/);
    demoState.links[0].snrDb = 8.5;
    await navigate('#users');
    await navigate('#infrastructure');
    assert.match(document.querySelector('.neighbor-table').textContent, /8.5 dB/, 'table reflects backend changes');
    await act(async () => button('Simulate outage').click());
    assert.ok(requests.some(r => r.url === '/demo-api/api/meshlink/demo/feed' && r.options.method === 'POST'));
    assert.ok(requests.every(r => r.url.startsWith('/demo-api/')), 'demo mutations also stay isolated');
    await act(async () => button('Sign in').click());
    assert.equal(document.querySelector('.app-shell'), null);
    assert.ok(document.querySelector('form input[type="password"]'));
    assert.ok(button('View demo'));

    // Anonymous refresh opens the database demo in production too.
    await act(async () => button('View demo').click());
    await act(async () => root.render(createElement(App, { key: 'reload' })));
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo');
    assert.ok(button('Sign in'));

    demoFailure = true;
    await act(async () => root.render(createElement(App, { key: 'unavailable-demo' })));
    assert.equal(document.querySelector('.app-shell'), null, 'unavailable DB cannot fall back to browser fixtures');
    assert.match(document.querySelector('[role="status"]').textContent, /unavailable/);
    assert.ok(document.querySelector('form input[type="password"]'), 'live sign-in remains available during demo failure');
    demoFailure = false;
    demoState.simulation = false;
    await act(async () => button('View demo').click());
    assert.equal(document.querySelector('.app-shell'), null, 'demo rejects a live database response');
    assert.match(document.querySelector('[role="status"]').textContent, /separate simulation database/);
    demoState.simulation = true;

    let releaseDemo;
    demoGate = new Promise(resolve => { releaseDemo = resolve; });
    await act(async () => root.render(createElement(App, { key: 'pending-demo' })));
    assert.match(document.querySelector('[role="status"]').textContent, /Opening/);
    await act(async () => button('Sign in').click());
    await act(async () => { demoGate = undefined; releaseDemo(); });
    assert.ok(document.querySelector('form input[type="password"]'), 'a late demo response cannot undo opening sign-in');

    await act(async () => document.querySelector('form').dispatchEvent(
      new window.Event('submit', { bubbles: true, cancelable: true }),
    ));
    assert.ok(requests.some(r => r.url.endsWith('/api/meshlink/state')));
    assert.equal(document.querySelector('.demo-mode-label'), null);
    assert.equal(document.querySelectorAll('.tracker-row').length, 0, 'authenticated empty state cannot show demos');
    assert.doesNotMatch(document.querySelector('.workspace').textContent, /Demo Avery/);
    assert.equal(window.sessionStorage.getItem('meshlink-session-token'), 'test-token');
    assert.equal(window.localStorage.length, 0, 'sign-in is scoped to this tab');
    const beforeReload = requests.length;
    await act(async () => root.render(createElement(App, { key: 'authenticated-reload' })));
    assert.ok(document.querySelector('.app-shell'), 'refresh keeps the signed-in workspace');
    assert.ok(button('Sign out'), 'refresh keeps the account signed in');
    assert.ok(requests.slice(beforeReload).some(r => r.url.endsWith('/api/meshlink/state')),
      'the backend validates the saved token on reload');
    await act(async () => button('Sign out').click());
    assert.equal(document.querySelector('.app-shell'), null);
    assert.ok(button('View demo'));
    assert.equal(window.sessionStorage.length, 0);
    await act(async () => root.render(createElement(App, { key: 'signed-out-reload' })));
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo', 'signed-out refresh returns to the demo');
    assert.equal(window.sessionStorage.length, 0, 'refresh cannot restore the signed-out live account');

    window.sessionStorage.setItem('meshlink-session-token', 'test-token');
    stateFailure = 503;
    await act(async () => root.render(createElement(App, { key: 'offline-reload' })));
    assert.match(document.querySelector('[role="status"]').textContent, /sign-in is saved/);
    assert.equal(document.querySelector('.app-shell'), null, 'records wait for server validation');
    assert.equal(window.sessionStorage.getItem('meshlink-session-token'), 'test-token');
    stateFailure = 0;
    await act(async () => button('Try again').click());
    assert.ok(document.querySelector('.app-shell'), 'reconnect restores the account without a password');

    for (const status of [401, 403]) {
      stateFailure = status;
      await act(async () => root.render(createElement(App, { key: `rejected-${status}` })));
      assert.ok(button('View demo'), 'rejected sign-in returns to login');
      assert.equal(window.sessionStorage.length, 0, 'rejected token is removed');
      window.sessionStorage.setItem('meshlink-session-token', 'test-token');
    }
    window.sessionStorage.clear();
    stateFailure = 0;
    let releaseState;
    stateGate = new Promise(resolve => { releaseState = resolve; });
    window.sessionStorage.setItem('meshlink-session-token', 'test-token');
    await act(async () => root.render(createElement(App, { key: 'pending-restore' })));
    assert.match(document.querySelector('[role="status"]').textContent, /Restoring/);
    await act(async () => button('Sign out').click());
    await act(async () => { stateGate = undefined; releaseState(); });
    assert.ok(button('View demo'), 'a late restore response cannot undo sign-out');
    assert.equal(window.sessionStorage.length, 0);
    Object.defineProperty(window, 'sessionStorage', { configurable: true,
      get() { throw new Error('Storage disabled'); } });
    await act(async () => root.render(createElement(App, { key: 'storage-disabled' })));
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo');
    await act(async () => button('Sign in').click());
    await act(async () => document.querySelector('form').dispatchEvent(
      new window.Event('submit', { bubbles: true, cancelable: true }),
    ));
    assert.ok(document.querySelector('.app-shell'), 'storage restrictions do not break sign-in');
    await act(async () => button('Sign out').click());
    assert.ok(button('View demo'));
  } finally {
    await act(async () => root.unmount());
    globalThis.fetch = originalFetch;
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.HTMLElement;
    delete globalThis.HTMLButtonElement;
    delete globalThis.ResizeObserver;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});
