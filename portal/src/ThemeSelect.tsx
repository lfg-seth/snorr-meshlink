import { useEffect, useState } from 'react';

const storageKey = 'meshlink-theme';

function themeChoice(value: string | null | undefined) {
  return value === 'light' || value === 'dark' ? value : 'system';
}

export default function ThemeSelect() {
  const [choice, setChoice] = useState(() => themeChoice(document.documentElement.dataset.theme));

  function apply(value: string | null) {
    const next = themeChoice(value);
    if (next === 'system') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = next;
    setChoice(next);
  }

  useEffect(() => {
    function sync(event: StorageEvent) {
      if (event.key !== storageKey && event.key !== null) return;
      try {
        if (event.storageArea === window.localStorage) apply(window.localStorage.getItem(storageKey));
      } catch { /* Keep the current choice when storage is unavailable. */ }
    }
    window.addEventListener('storage', sync);
    return () => window.removeEventListener('storage', sync);
  }, []);

  return <label className="theme-choice">
    Theme
    <select value={choice} onChange={event => {
      const next = event.target.value;
      apply(next);
      try {
        if (next === 'system') window.localStorage.removeItem(storageKey);
        else window.localStorage.setItem(storageKey, next);
      } catch { /* The choice still applies for this visit when storage is unavailable. */ }
    }}>
      <option value="system">System</option>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  </label>;
}
