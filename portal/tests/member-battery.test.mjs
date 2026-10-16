import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { registerHooks } from 'node:module';
import test from 'node:test';
import { act, createElement } from 'react';
import { JSDOM } from 'jsdom';
import { renderToStaticMarkup } from 'react-dom/server';
import ts from 'typescript';

registerHooks({
  resolve(specifier, context, next) {
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
    if (!url.endsWith('.tsx')) return next(url, context);
    return { format: 'module', shortCircuit: true, source: ts.transpileModule(
      readFileSync(new URL(url), 'utf8'), { compilerOptions: {
        module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.ReactJSX,
      } }).outputText };
  },
});

const { default: MemberBattery } = await import('../src/MemberBattery.tsx');
const { default: GPSQuality } = await import('../src/GPSQuality.tsx');
const now = Date.parse('2026-10-15T12:00:00Z');
const device = { id: 'b001', battery: 42, batteryVoltage: 3.72,
  batteryProfile: 'lipo-1s', batteryCapacityMah: 3000,
  batteryMeasuredAt: '2026-10-15T11:40:00Z' };

test('member display separates voltage estimate, nominal capacity and measurement age', () => {
  const html = renderToStaticMarkup(createElement(MemberBattery, { device, now, online: true }));
  assert.match(html, /≈50%/);
  assert.match(html, /3\.720 V/);
  assert.match(html, /3000 mAh nominal/);
  assert.match(html, /Stale battery reading/);
  assert.doesNotMatch(html, /Save battery configuration|42%/);
  const offline = renderToStaticMarkup(createElement(MemberBattery, { device, now, online: false }));
  assert.match(offline, /Feed offline/);
});

test('admin configuration offers LiPo and inventory capacities; unknown voltage stays unknown', () => {
  const html = renderToStaticMarkup(createElement(MemberBattery, {
    device: { ...device, batteryVoltage: null }, now, online: true,
    onConfigure: async () => true,
  }));
  assert.match(html, /Save battery configuration/);
  for (const capacity of [1000, 1100, 3000]) assert.match(html, new RegExp(`value="${capacity}"`));
  assert.match(html, /Awaiting valid battery voltage/);
  assert.doesNotMatch(html, /≈50%/);
});

test('GPS pill uses plain language and opens an explanation without revealing technical scores', async () => {
  const dom = new JSDOM('<div id="root"></div>');
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const { createRoot } = await import('react-dom/client');
  const root = createRoot(document.getElementById('root'));
  try {
    const fix = { latitude: 36.2, longitude: -115.6, measuredAt: '2026-10-15T10:00:00Z',
      receivedAt: '2026-10-15T12:00:00Z', satellites: 9 };
    for (const [pdop, label, tone] of [[1.83, 'Good', 'good'], [4.5, 'Limited', 'limited'],
      [8, 'Poor', 'poor'], [undefined, 'Unknown', 'unknown'], [0, 'Unknown', 'unknown']]) {
      await act(async () => root.render(createElement(GPSQuality, { position: { ...fix, pdop } })));
      const pill = document.querySelector('summary');
      assert.match(pill.textContent, new RegExp(label));
      assert.ok(pill.classList.contains(tone));
      assert.match(pill.getAttribute('aria-label'), new RegExp(`GPS quality: ${label}`));
      assert.doesNotMatch(document.body.textContent, /PDOP|HDOP|1\.83|\d+\s*(metres|meters|%)/i);
      assert.match(document.querySelector('.gps-quality-explanation').textContent, /not a measured accuracy or a guarantee/);
      assert.match(document.querySelector('.gps-quality-explanation').textContent, /Check Last GPS for its age/);
    }
    const details = document.querySelector('details');
    assert.equal(details.open, false);
    document.querySelector('summary').click();
    assert.equal(details.open, true);
    assert.match(details.textContent, /Reported satellites: 9/);
    document.querySelector('summary').click();
    assert.equal(details.open, false);
    await act(async () => root.render(createElement(GPSQuality, { position: null })));
    assert.match(document.querySelector('summary').textContent, /Unknown/);
    assert.match(document.querySelector('.gps-quality-explanation').textContent, /No recorded location/);
    assert.doesNotMatch(document.body.textContent, /Reported satellites/);
  } finally {
    await act(async () => root.unmount());
    dom.window.close();
    delete globalThis.window;
    delete globalThis.document;
    delete globalThis.IS_REACT_ACT_ENVIRONMENT;
  }
});
