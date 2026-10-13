import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { positionAgeSeconds, positionStatus } from './position';
import type { Position } from './position';
import './style.css';

type Tracker = { device: string; position: Position | null };

const startedAt = Date.now();
const trackers: Tracker[] = [1, 3, 8, 17, null, undefined].map((minutes, index) => ({
  device: `S${String(index + 1).padStart(3, '0')}`,
  position: minutes === undefined ? null : {
    measuredAt: minutes === null ? null : new Date(startedAt - minutes * 60_000).toISOString(),
    receivedAt: new Date(startedAt).toISOString(),
  },
}));

function App() {
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  return <main>
    <p className="eyebrow">SNORR · Search and Rescue</p>
    <h1>MeshLink</h1>
    <p className="intro">Member location awareness, built around the age of each GPS measurement.</p>
    <aside><strong>Development baseline · synthetic data</strong><br />These fictional trackers demonstrate freshness states. No live feed is connected. The four-page portal and map are next.</aside>
    <section aria-labelledby="tracking-title">
      <h2 id="tracking-title">Tracking states</h2>
      <p>Positions become stale at 15 minutes. A recent receipt does not make an old fix fresh.</p>
      <div className="trackers">{trackers.map(tracker => {
        const age = tracker.position ? positionAgeSeconds(tracker.position, now) : null;
        const status = positionStatus(age);
        return <article key={tracker.device}>
          <h3>{tracker.device}</h3>
          <span className={`status ${status}`}>{tracker.position ? status : 'Never seen'}</span>
          <p>GPS age: {age === null ? 'Unknown' : `${Math.floor(age / 60)}m ${Math.floor(age % 60)}s`}</p>
          <p>Last contact: {tracker.position ? `${Math.floor((now - Date.parse(tracker.position.receivedAt)) / 1000)}s ago` : 'None'}</p>
        </article>;
      })}</div>
    </section>
  </main>;
}

const root = document.getElementById('root');
if (!root) throw new Error('Portal root element is missing');
createRoot(root).render(<StrictMode><App /></StrictMode>);
