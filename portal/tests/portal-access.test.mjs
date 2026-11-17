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
    if (specifier.endsWith('.html?raw')) {
      const content = readFileSync(new URL(specifier.split('?')[0], context.parentURL), 'utf8');
      return { url: 'data:text/javascript,' + encodeURIComponent('export default ' + JSON.stringify(content)), shortCircuit: true };
    }
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

test('theme selector and first paint agree across visits, tabs and unavailable storage', async () => {
  const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
  const dom = new JSDOM(html, { url: 'https://portal.test', runScripts: 'outside-only' });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: ThemeSelect } = await import('../src/ThemeSelect.tsx');
  const root = createRoot(document.querySelector('#root'));
  const select = () => document.querySelector('select');
  const storage = window.localStorage;
  const bootstrap = document.querySelector('head script').textContent;
  const reload = async (key) => {
    delete document.documentElement.dataset.theme;
    window.eval(bootstrap);
    const beforeMount = document.documentElement.dataset.theme ?? 'system';
    await act(async () => root.render(createElement(ThemeSelect, { key })));
    assert.equal(select().value, beforeMount);
    return beforeMount;
  };
  const choose = async value => act(async () => {
    select().value = value;
    select().dispatchEvent(new window.Event('change', { bubbles: true }));
  });
  const storageEvent = async key => act(async () => {
    window.dispatchEvent(new window.StorageEvent('storage', { key, storageArea: storage }));
  });
  try {
    assert.equal(await reload('first'), 'system');
    for (const choice of ['dark', 'light']) {
      await choose(choice);
      assert.equal(document.documentElement.dataset.theme, choice);
      assert.equal(storage.getItem('meshlink-theme'), choice);
      assert.equal(await reload(choice), choice);
    }
    storage.setItem('meshlink-theme', 'dark');
    await storageEvent('meshlink-theme');
    assert.equal(select().value, 'dark');
    await choose('system');
    assert.equal(storage.getItem('meshlink-theme'), null);
    assert.equal(document.documentElement.dataset.theme, undefined);
    await choose('dark');
    storage.clear();
    await storageEvent(null);
    assert.equal(select().value, 'system');
    storage.setItem('meshlink-theme', 'invalid');
    assert.equal(await reload('invalid'), 'system');
    Object.defineProperty(window, 'localStorage', { get() { throw new Error('Storage disabled'); } });
    assert.equal(await reload('blocked'), 'system');
    await choose('light');
    assert.equal(document.documentElement.dataset.theme, 'light');
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});

test('Activity switches views and preserves ordered readings and value bars on refresh', async () => {
  const { mountActivity } = await import('../src/activity/view.js');
  const dom = new JSDOM('<div id="host"></div>');
  globalThis.document = dom.window.document;
  try {
    const root = document.querySelector('#host').attachShadow({ mode: 'open' });
    const view = mountActivity(root);
    const reading = (value, age=0) => ({ value, state:'fresh', age });
    const data = {
      voltage:reading('4.200'), busy:reading('1.0'), temperature:reading('6'),
      inaCurrent:reading('-10',15), envCurrent:reading('-15',5),
      inaVoltage:reading('3.700',8), envVoltage:reading('3.800',20),
      charge:reading('30%'), uptime:{ ...reading('2m'), seconds:120 },
      gateway:reading({ wifiConnected:false, mqttConnected:true }), sd:reading({ usedBytes:0,totalBytes:100,dropped:1 }),
    };
    const render = readings => view.render({ at:'2026-11-16T12:00:00Z', now:Date.parse('2026-11-16T12:00:00Z')/1000, status:'Live',
      nodes:[{ radio:'!00000001', label:'R001', name:'Test node', seen:'2026-11-16T11:45:00Z', heardThrough:'Seth Mobile', health:'reporting', readings,
        timers:[{stream:'power',age:30,period:180,due:150,state:'fresh',missed:0}] }] });
    render(data);
    assert.match(root.querySelector('.heard').textContent,/Last heard 15m ago through Seth Mobile/);
    const [readings, timers] = root.querySelectorAll('.controls button');
    assert.deepEqual([readings.textContent, timers.textContent], ['Readings', 'Timers']);
    assert.equal(readings.getAttribute('aria-pressed'), 'true');
    assert.ok(root.querySelector('.tiles .metric'));
    timers.click();
    render(data);
    assert.equal(timers.getAttribute('aria-pressed'), 'true');
    assert.match(root.querySelector('.timer').textContent,/Power.*2m 30s left.*every 3m/);
    readings.click();
    const tiles = () => [...root.querySelectorAll('.metric')];
    const labels = () => tiles().map(tile=>tile.firstChild.textContent);
    const tile = label => tiles().find(t=>t.firstChild.textContent===label);
    assert.deepEqual(labels().slice(0,4),['Device voltage','Channel use','MQTT','Battery current']);
    assert.equal(tile('Battery current').querySelector('b').textContent,'-15mA');
    assert.equal(tile('Battery voltage').querySelector('b').textContent,'3.700V');
    assert.equal(tile('Device voltage').querySelector('.track i').style.width,'100%');
    assert.equal(tile('Wi-Fi').querySelector('.track i').style.width,'100%');
    assert.ok(tile('Wi-Fi').classList.contains('down'));
    assert.ok(tile('Uptime').classList.contains('down'));
    assert.ok(tile('Battery').classList.contains('aging'));
    const initial = labels();
    for (const [pct,tone,seconds,upTone] of [[29,'down',121,'aging'],[60,'aging',3599,'aging'],[61,'fresh',3600,'fresh']]) {
      render({ uptime:{...reading('1h'),seconds}, ...Object.fromEntries(Object.entries(data).filter(([k])=>k!=='uptime').reverse()),
        charge:reading(pct+'%') });
      assert.deepEqual(labels(),initial);
      assert.ok(tile('Battery').classList.contains(tone));
      assert.ok(tile('Uptime').classList.contains(upTone));
    }
    assert.equal(tile('Uptime').querySelector('.track i').style.width,'100%');
    assert.equal(labels().filter(label=>label==='Battery voltage').length,1);
    assert.ok(!labels().includes('SD drops'));
  } finally {
    dom.window.close();
    delete globalThis.document;
  }
});

test('production opens the isolated demo by default and live sign-in survives refresh', async () => {
  const dom = new JSDOM('<div id="root"></div>', { url: 'https://portal.example.test/' });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.HTMLButtonElement = dom.window.HTMLButtonElement;
  globalThis.FormData = dom.window.FormData;
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
      originalSourceDeviceId: 'db-tracker', source: 'gateway', path: 'direct', snrDb: -20, rssiDbm: -101,
      receivedAt: new Date().toISOString(), observedAt: new Date().toISOString() }],
    currentLinks: [{ id: 'db-current-link', observerDeviceId: 'db-gateway', heardDeviceId: 'db-tracker',
      originalSourceDeviceId: 'db-tracker', source: 'gateway', path: 'direct', snrDb: 0, rssiDbm: -101,
      observedAt: new Date().toISOString(), receivedAt: new Date().toISOString() }],
  };
  globalThis.fetch = async (url, options) => {
    requests.push({ url, options });
    const demo = url.startsWith('/demo-api/');
    if (demo && demoGate) await demoGate;
    if (demo && demoFailure) throw new Error('Demo PocketBase unavailable');
    if (url.endsWith('/auth-with-password'))
      return { ok: true, json: async () => ({ token: demo ? 'demo-token' : 'test-token', record: demo ? demoAccount : account }) };
    assert.equal(options.headers.Authorization, demo ? 'demo-token' : 'test-token');
    if (url.endsWith('/api/meshlink/activity')) {
      assert.equal(demo, false);
      return {ok: true, json: async () => ({at: new Date().toISOString(), now: Date.now()/1000, status: 'Live',
        nodes: [{radio:'!f95b5501', label:'R001', name:'Cathedral Rock', health:'silent', kind:'repeater',
          readings:{}, timers:[], seen:null, contact:'stale'}]})};
    }
    if (url.endsWith('/api/meshlink/accounts')) {
      const body = JSON.parse(options.body);
      assert.equal(body.createMember, true);
      assert.equal(body.role, 'member');
      assert.equal(body.memberId, undefined, 'the user never supplies an internal key');
      if (body.username === 'taken') return { ok: false, status: 400,
        json: async () => ({ message: 'Username is already in use.' }) };
      emptyState.members.push({ id: 'generated-member', name: body.name, initials: 'NP' });
      return { ok: true, json: async () => ({ memberId: 'generated-member' }) };
    }
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
    assert.equal(document.querySelector('nav a[href="#activity"]'), null);
    assert.equal(document.querySelector('.demo-banner'), null, 'map remains banner-free');
    await navigate('#users');
    assert.match(document.querySelector('.users-trackers').textContent, /Demo Database Person/);
    assert.ok(document.querySelectorAll('.tracker-row').length > 0);
    assert.ok(requests.length >= 2, 'demo authenticates and reads its PocketBase');
    assert.ok(requests.every(r => r.url.startsWith('/demo-api/')), 'demo cannot use production routes');
    assert.equal(window.sessionStorage.length, 0, 'demo tokens cannot become saved production sign-ins');
    assert.equal(window.localStorage.length, 0);
    await navigate('#infrastructure');
    assert.match(document.querySelector('.neighbor-table').textContent, /DB901/);
    assert.match(document.querySelector('.neighbor-table').textContent, /0 dB/);
    demoState.currentLinks[0].snrDb = 8.5;
    await navigate('#users');
    await navigate('#infrastructure');
    assert.match(document.querySelector('.neighbor-table').textContent, /8.5 dB/, 'table reflects backend changes');
    demoState.currentLinks = [];
    await navigate('#users');
    await navigate('#infrastructure');
    assert.equal(document.querySelector('.neighbor-table'), null, 'empty current state never revives history');
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
    window.sessionStorage.clear(); // Closing the browser discards tab storage.
    await act(async () => root.render(createElement(App, { key: 'browser-restart' })));
    assert.ok(button('Sign out'), 'reopening this browser restores the live account');
    assert.equal(window.localStorage.getItem('meshlink-session-token'), 'test-token');
    assert.ok(requests.some(r => !r.url.startsWith('/demo-api/') && r.url.endsWith('/auth-with-password')
      && JSON.parse(r.options.body).rememberDevice === true));
    await navigate('#activity');
    const activity = document.querySelector('#page-content > div').shadowRoot;
    assert.equal(activity.querySelector('article h2').textContent, 'Cathedral Rock');
    assert.match(activity.querySelector('article').textContent, /R001/);
    activity.querySelector('button.reporting').click();
    assert.equal(activity.querySelector('article').hidden, true);
    activity.querySelector('button.silent').click();
    assert.equal(activity.querySelector('article').hidden, false);
    await navigate('#users');
    const addForm = document.querySelector('.add-member-fields').closest('form');
    addForm.elements.name.value = 'New Person';
    addForm.elements.username.value = 'taken';
    addForm.elements.password.value = 'fictional-test-password';
    await act(async () => addForm.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true })));
    assert.match(document.querySelector('[role="alert"]').textContent, /already in use/);
    assert.equal(addForm.elements.name.value, 'New Person', 'failure preserves the draft');
    addForm.elements.username.value = 'new-person';
    await act(async () => addForm.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true })));
    assert.match(document.querySelector('[role="status"]').textContent, /New Person added/);
    assert.equal(addForm.elements.password.value, '', 'success clears the password');
    const memberSelect = [...document.querySelectorAll('select')].find(select =>
      [...select.options].some(option => option.value === 'generated-member'));
    assert.equal(memberSelect.value, 'generated-member', 'new member is selected for assignment');
    account.role = 'member';
    await act(async () => root.render(createElement(App, { key: 'member-view' })));
    assert.equal(document.querySelector('.add-member-fields'), null, 'ordinary members cannot create accounts');
    account.role = 'admin';
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
    assert.equal(window.localStorage.length, 0);
    await act(async () => document.querySelector('.remember-device input').click());
    await act(async () => document.querySelector('form').dispatchEvent(
      new window.Event('submit', { bubbles: true, cancelable: true }),
    ));
    assert.equal(window.localStorage.length, 0, 'a shared browser does not remember the account');
    assert.equal(window.sessionStorage.getItem('meshlink-session-token'), 'test-token');
    assert.equal(JSON.parse(requests.filter(r => r.url.endsWith('/auth-with-password')).at(-1).options.body).rememberDevice, undefined);
    window.sessionStorage.clear();
    await act(async () => root.render(createElement(App, { key: 'signed-out-reload' })));
    assert.equal(document.querySelector('.demo-mode-label').textContent, 'Demo', 'signed-out refresh returns to the demo');
    assert.equal(window.sessionStorage.length, 0, 'refresh cannot restore the signed-out live account');

    window.localStorage.setItem('meshlink-session-token', 'test-token');
    stateFailure = 503;
    await act(async () => root.render(createElement(App, { key: 'offline-reload' })));
    assert.match(document.querySelector('[role="status"]').textContent, /sign-in is saved/);
    assert.equal(document.querySelector('.app-shell'), null, 'records wait for server validation');
    assert.equal(window.localStorage.getItem('meshlink-session-token'), 'test-token');
    stateFailure = 0;
    await act(async () => button('Try again').click());
    assert.ok(document.querySelector('.app-shell'), 'reconnect restores the account without a password');

    window.localStorage.removeItem('meshlink-session-token');
    await act(async () => window.dispatchEvent(new window.StorageEvent('storage', {
      key: 'meshlink-session-token', oldValue: 'test-token', storageArea: window.localStorage,
    })));
    assert.ok(button('View demo'), 'sign-out in another tab closes this remembered workspace');
    window.localStorage.setItem('meshlink-session-token', 'test-token');
    await act(async () => root.render(createElement(App, { key: 'active-account' })));
    stateFailure = 403;
    await navigate('#messages'); // Navigation starts a fresh state poll.
    assert.ok(button('View demo'), 'losing access closes an already-open live workspace');
    assert.equal(window.localStorage.length, 0);
    window.localStorage.setItem('meshlink-session-token', 'test-token');

    for (const status of [401, 403]) {
      stateFailure = status;
      await act(async () => root.render(createElement(App, { key: `rejected-${status}` })));
      assert.ok(button('View demo'), 'rejected sign-in returns to login');
      assert.equal(window.localStorage.length, 0, 'rejected token is removed');
      window.localStorage.setItem('meshlink-session-token', 'test-token');
    }
    window.localStorage.clear();
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
    Object.defineProperty(window, 'localStorage', { configurable: true,
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
    delete globalThis.FormData;
    delete globalThis.ResizeObserver;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});
