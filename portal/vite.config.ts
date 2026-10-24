import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { portalBuildMode } from './build-mode.ts';
import { meshlinkBuildMetadata } from './release-metadata.ts';

const proxy = {
  '/api': { target: 'http://127.0.0.1:8090', changeOrigin: false },
  '/demo-api': {
    target: 'http://127.0.0.1:8092', changeOrigin: false,
    rewrite: (path: string) => path.replace(/^\/demo-api/, ''),
  },
};
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd());
  const portalMode = portalBuildMode(command === 'serve', process.env.VITE_PORTAL_MODE ?? env.VITE_PORTAL_MODE);
  const release = meshlinkBuildMetadata();
  return {
    define: { 'import.meta.env.VITE_PORTAL_MODE': JSON.stringify(portalMode) },
    plugins: [react(), {
      name: 'portal-build-mode',
      transformIndexHtml: () => [
        { tag: 'meta', attrs: { name: 'meshlink-portal-mode', content: portalMode }, injectTo: 'head' },
        { tag: 'meta', attrs: { name: 'meshlink-version', content: release.version }, injectTo: 'head' },
        { tag: 'meta', attrs: { name: 'meshlink-source', content: release.sourceCommit }, injectTo: 'head' },
      ],
      generateBundle() {
        this.emitFile({ type: 'asset', fileName: 'version.json',
          source: JSON.stringify({ ...release, portalMode }, null, 2) + '\n' });
      },
    }],
    server: { proxy },
    preview: { proxy },
  };
});
