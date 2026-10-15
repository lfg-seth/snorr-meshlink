import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { registerHooks } from 'node:module';
import test from 'node:test';
import { createElement } from 'react';
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
