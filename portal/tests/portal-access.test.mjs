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

test('live sign-in survives refresh, validates saved tokens, and keeps demo access separate', async () => {
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
  let stateGate;
  const account = { id: 'admin', name: 'Test Admin', role: 'admin', memberId: '' };
  globalThis.fetch = async (url, options) => {
    requests.push({ url, options });
    if (url.endsWith('/auth-with-password'))
      return { ok: true, json: async () => ({ token: 'test-token', record: account }) };
    assert.equal(options.headers.Authorization, 'test-token');
    if (stateGate) await stateGate;
    if (stateFailure) return { ok: false, status: stateFailure,
      json: async () => ({ message: 'Test backend failure' }) };
    return { ok: true, json: async () => ({ account, simulation: false, feedOnline: true,
      trackers: [], members: [], assignments: [], nameJobs: [], messages: [],
      infrastructure: [], incidents: [], warnings: [], rules: {}, events: [] }) };
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
    assert.ok(document.querySelector('form input[type="password"]'));
    assert.equal(document.querySelector('.app-shell'), null);
    assert.ok(button('View demo'));
    assert.equal(requests.length, 0);

    await act(async () => button('View demo').click());
    assert.ok(document.querySelector('.app-shell'));
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo');
    assert.equal(document.querySelector('.demo-banner'), null, 'map remains banner-free');
    await navigate('#users');
    assert.match(document.querySelector('.users-trackers').textContent, /Demo Avery/);
    assert.ok(document.querySelectorAll('.tracker-row').length > 0);
    assert.equal(requests.length, 0, 'demo viewing never requests backend records');
    await act(async () => button('Exit demo').click());
    assert.equal(document.querySelector('.app-shell'), null);
    assert.ok(button('View demo'));

    // A refresh/remount starts signed out rather than persisting demo mode.
    await act(async () => button('View demo').click());
    await act(async () => root.render(createElement(App, { key: 'reload' })));
    assert.equal(document.querySelector('.app-shell'), null);
    assert.ok(button('View demo'));

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
    assert.ok(button('View demo'), 'sign-out persists through refresh');

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
