import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { registerHooks } from 'node:module';
import test from 'node:test';
import { createElement, act } from 'react';
import { JSDOM } from 'jsdom';
import ts from 'typescript';

registerHooks({
  resolve(specifier, context, next) {
    if (specifier.startsWith('.') && !/\.[a-z]+$/i.test(specifier)) {
      for (const ext of ['.tsx', '.ts']) {
        try { return next(specifier + ext, context); } catch {}
      }
    }
    return next(specifier, context);
  },
  load(url, context, next) {
    if (!url.endsWith('.tsx')) return next(url, context);
    return { format: 'module', shortCircuit: true,
      source: ts.transpileModule(readFileSync(new URL(url), 'utf8'), {
        compilerOptions: { jsx: ts.JsxEmit.ReactJSX, module: ts.ModuleKind.ESNext },
      }).outputText };
  },
});

test('INA219 cards show signed current, an independent 30-minute average and every graph range', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const { default: CurrentChart } = await import('../src/CurrentChart.tsx');
  const { infrastructure } = await import('../src/demo.ts');
  const now = Date.parse('2026-10-24T20:00:00Z');
  const at = minutes => new Date(now - minutes * 60000).toISOString();
  const device = { ...infrastructure[0], cadenceMinutes: 3,
    powerReadings: [{ metric: 'power1CurrentMa', value: 20, measuredAt: at(1), receivedAt: at(1),
      currentConvention: 'positive-charging' }] };
  const requests = [];
  const loadHistory = (id, hours, signal) => new Promise(resolve => requests.push({ id, hours, signal, resolve }));
  const response = { samples: [{ at: at(20), milliamps: -40 }, { at: at(17), milliamps: 0 },
    { at: at(1), milliamps: 20 }], truncated: false,
    average30Minutes: { milliamps: -6.6667, count: 3, at: at(1), asOf: at(0), metric: 'power1CurrentMa', truncated: false } };
  const root = createRoot(document.getElementById('root'));
  const render = (value = device, clock = now, online = true) => act(async () => root.render(
    createElement(CurrentChart, { device: value, now: clock, online, loadHistory })));
  const buttons = () => [...document.querySelectorAll('.battery-periods button')];
  try {
    await render({ ...device, powerReadings: [] });
    assert.equal(document.querySelector('.current-history'), null);
    assert.equal(requests.length, 0);
    await render();
    await act(async () => requests[0].resolve(response));
    assert.deepEqual(buttons().map(b => b.textContent), ['30min', '6hr', '24hr', '7day', '30day']);
    assert.match(document.querySelector('.current-average').textContent, /30-minute average: -6.7 mA.*Mean of 3 readings/);
    assert.match(document.querySelector('svg').getAttribute('aria-label'), /-40.0 to 20.0 milliamps/);
    assert.ok(document.querySelector('path').getAttribute('d').includes('C'));
    assert.equal(document.querySelectorAll('circle').length, 1, 'gap retains the isolated latest reading');
    for (const [index, hours] of [[0, .5], [1, 6], [3, 168], [4, 720]]) {
      const previous = requests.at(-1);
      await act(async () => buttons()[index].click());
      assert.equal(previous.signal.aborted, true);
      assert.equal(requests.at(-1).hours, hours);
      await act(async () => requests.at(-1).resolve(response));
      assert.match(document.querySelector('.current-average').textContent, /-6.7 mA/);
    }
    await render(device, now, false);
    assert.match(document.querySelector('.current-average').textContent, /Feed offline/);
    await render(device, now + 31 * 60000, false);
    assert.match(document.querySelector('.current-average').textContent, /Unknown/);
    await render({ ...device, id: 'other-device', powerReadings: [] });
    assert.equal(document.querySelector('.current-history'), null);
    assert.equal(requests.at(-1).signal.aborted, true);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});
