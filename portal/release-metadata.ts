import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

type Release = {
  product: string;
  version: string;
  stage: string;
  components: string[];
  compatibility: Record<string, unknown>;
};

export function validateRelease(release: Release, packageVersions: string[], changelog: string, ref = '') {
  if (release.product !== 'MeshLink' || !/^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/.test(release.version)) {
    throw new Error('MeshLink release requires a numeric major.minor.patch version');
  }
  if (packageVersions.some(version => version !== release.version)) {
    throw new Error('Portal package and lockfile versions must match meshlink-release.json');
  }
  if (!changelog.split(/\r?\n/).some(line => line.startsWith(`## ${release.version} - `))) {
    throw new Error('MeshLink release requires a matching changelog entry');
  }
  if (ref.startsWith('refs/tags/meshlink-v') && ref !== `refs/tags/meshlink-v${release.version}`) {
    throw new Error('MeshLink release tag does not match the declared version');
  }
  return release;
}

export function meshlinkBuildMetadata() {
  const root = new URL('../', import.meta.url);
  const readJson = (path: string) => JSON.parse(readFileSync(new URL(path, root), 'utf8'));
  const pkg = readJson('portal/package.json');
  const lock = readJson('portal/package-lock.json');
  const release = validateRelease(readJson('meshlink-release.json'),
    [pkg.version, lock.version, lock.packages[''].version],
    readFileSync(new URL('CHANGELOG.md', root), 'utf8'), process.env.GITHUB_REF);
  // Fail rather than assign a plausible source identity when Git is unavailable.
  const git = (...args: string[]) => execFileSync('git', args,
    { cwd: fileURLToPath(root), encoding: 'utf8' }).trim();
  return {
    ...release,
    sourceCommit: git('rev-parse', 'HEAD'),
    trackedChanges: git('status', '--porcelain', '--untracked-files=no', '--ignore-submodules=all') !== '',
  };
}
