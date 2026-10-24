import assert from 'node:assert/strict';
import test from 'node:test';
import { validateRelease } from '../release-metadata.ts';

const release = { product: 'MeshLink', version: '0.1.0', stage: 'development', components: ['portal', 'backend'], compatibility: {} };
const changelog = '# Changes\n\n## 0.1.0 - 2026-10-23\nInitial release.\n';

test('release rejects mismatched package, lockfile, changelog and tag identities', () => {
  assert.equal(validateRelease(release, ['0.1.0', '0.1.0', '0.1.0'], changelog, 'refs/tags/meshlink-v0.1.0'), release);
  for (let index = 0; index < 3; index++) {
    const versions = ['0.1.0', '0.1.0', '0.1.0'];
    versions[index] = '0.2.0';
    assert.throws(() => validateRelease(release, versions, changelog), /must match/);
  }
  assert.throws(() => validateRelease(release, ['0.1.0'], '# No release'), /changelog/);
  assert.throws(() => validateRelease(release, ['0.1.0'], changelog, 'refs/tags/meshlink-v0.2.0'), /tag/);
  assert.throws(() => validateRelease({ ...release, version: '0.01.0' }, [], changelog), /numeric/);
  assert.equal(validateRelease(release, ['0.1.0'], changelog, 'refs/heads/main'), release);
});
