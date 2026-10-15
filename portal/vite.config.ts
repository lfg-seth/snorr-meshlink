import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { portalBuildMode } from './build-mode.ts';

const proxy = {
  '/api': { target: 'http://127.0.0.1:8090', changeOrigin: false },
};
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd());
  const portalMode = portalBuildMode(command === 'serve', process.env.VITE_PORTAL_MODE ?? env.VITE_PORTAL_MODE);
  return {
    define: { 'import.meta.env.VITE_PORTAL_MODE': JSON.stringify(portalMode) },
    plugins: [react(), {
      name: 'portal-build-mode',
      transformIndexHtml: () => [{ tag: 'meta', attrs: { name: 'meshlink-portal-mode', content: portalMode }, injectTo: 'head' }],
    }],
    server: { proxy },
    preview: { proxy },
  };
});
