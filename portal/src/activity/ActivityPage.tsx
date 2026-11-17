import { useEffect, useRef } from 'react';
import { request } from '../backend';
import { mountActivity, type ActivitySnapshot } from './view.js';

export default function ActivityPage({ token }: { token: string }) {
  const host = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const element = host.current!;
    const view = mountActivity(element.shadowRoot ?? element.attachShadow({ mode: 'open' }));
    let active = true;
    let next: number;
    let controller: AbortController;
    async function refresh() {
      controller = new AbortController();
      const deadline = window.setTimeout(() => controller.abort(), 6000);
      try {
        const data = await request<ActivitySnapshot>('/api/meshlink/activity', token, undefined, controller.signal);
        if (active) view.render(data);
      } catch {
        if (active) view.disconnected();
      } finally {
        window.clearTimeout(deadline);
        if (active) next = window.setTimeout(refresh, 3000);
      }
    }
    void refresh();
    return () => {
      active = false;
      controller.abort();
      window.clearTimeout(next);
      view.destroy();
    };
  }, [token]);
  return <div ref={host} />;
}
