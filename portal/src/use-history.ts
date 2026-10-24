import { useEffect, useState } from 'react';

export type LoadHistory<T> = (id: string, hours: number, signal: AbortSignal) => Promise<T>;

export function useHistory<T>(id: string, hours: number, loadHistory?: LoadHistory<T>) {
  const [state, setState] = useState<{ id: string; hours: number; history: T | null; loading: boolean; error: boolean }>(
    { id, hours, history: null, loading: false, error: false });
  useEffect(() => {
    setState({ id, hours, history: null, loading: Boolean(loadHistory), error: false });
    if (!loadHistory) return;
    let active = true;
    let abort: AbortController;
    const refresh = async () => {
      abort?.abort();
      const controller = new AbortController();
      abort = controller;
      setState(s => ({ ...s, loading: true }));
      try {
        const result = await loadHistory(id, hours, controller.signal);
        if (active && !controller.signal.aborted)
          setState({ id, hours, history: result, error: false, loading: false });
      } catch {
        if (active && !controller.signal.aborted) setState(s => ({ ...s, error: true, loading: false }));
      }
    };
    void refresh();
    const timer = window.setInterval(() => void refresh(), 60000);
    return () => { active = false; abort?.abort(); window.clearInterval(timer); };
  }, [id, hours, loadHistory]);
  return state.id === id && state.hours === hours ? state : { history: null, loading: Boolean(loadHistory), error: false };
}
