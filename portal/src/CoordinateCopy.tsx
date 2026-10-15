import { useEffect, useState } from 'react';

export default function CoordinateCopy({ coordinates }: { coordinates: string }) {
  const [state, setState] = useState<'ready' | 'copied' | 'failed'>('ready');
  useEffect(() => {
    if (state !== 'copied') return;
    const timer = window.setTimeout(() => setState('ready'), 1600);
    return () => window.clearTimeout(timer);
  }, [state]);
  return (
    <>
      <button type="button" className={`coordinate-copy ${state}`}
        aria-label="Copy coordinates" title={state === 'copied' ? 'Copied' : 'Copy coordinates'}
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(coordinates);
            setState('copied');
          } catch {
            setState('failed');
          }
        }}>
        <span>{coordinates}</span>
        <svg key={state} viewBox="0 0 24 24" className="copy-icon" aria-hidden="true"
          fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <rect x="8" y="8" width="13" height="13" rx="2" />
          <path d="M5 16H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1" />
          {state === 'copied' && <path className="copy-check" d="m11 14 2.5 2.5L18 12" />}
        </svg>
      </button>
      <span className={state === 'failed' ? 'copy-error' : 'sr-only'} role="status">
        {state === 'copied' ? 'Coordinates copied.' : state === 'failed'
          ? 'Unable to copy. Select the coordinates to copy manually.' : ''}
      </span>
    </>
  );
}
