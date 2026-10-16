import assert from 'node:assert/strict';
import test from 'node:test';
import { portalBuildMode } from '../build-mode.ts';

test('production defaults to live when the deployment omits the mode', () => {
  assert.equal(portalBuildMode(false), 'live');
});
test('build mode selects sign-in backend independently of default demo viewing', () => {
  assert.equal(portalBuildMode(true), 'demo');
  assert.equal(portalBuildMode(true, 'live'), 'live');
  assert.equal(portalBuildMode(false, 'demo'), 'demo');
  assert.throws(() => portalBuildMode(false, 'typo'));
});
