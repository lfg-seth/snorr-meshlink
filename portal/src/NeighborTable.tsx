import { useState } from 'react';
import type { Infrastructure, Tracker } from './demo';

export type LinkObservation = {
  id: string;
  observerDeviceId: string;
  heardDeviceId: string | null;
  originalSourceDeviceId: string | null;
  source: 'gateway' | 'neighbor';
  path: 'direct' | 'relayed' | 'unknown';
  snrDb: number | null;
  rssiDbm: number | null;
  receivedAt: string;
  observedAt: string | null;
};

function age(at: string | null, now: number): string {
  if (!at || !Number.isFinite(Date.parse(at)) || Date.parse(at) > now) return 'Unknown';
  const minutes = Math.floor((now - Date.parse(at)) / 60000);
  if (minutes === 0) return 'Under 1m ago';
  return minutes < 60 ? `${minutes}m ago` : `${Math.floor(minutes / 60)}h ${minutes % 60}m ago`;
}
function signal(value: number | null | undefined, unit: string) {
  return typeof value === 'number' && Number.isFinite(value) ? `${value} ${unit}` : 'Unknown';
}

export default function NeighborTable({ links, infrastructure, trackers, now, online }: {
  links: LinkObservation[];
  infrastructure: Infrastructure[];
  trackers: Tracker[];
  now: number;
  online: boolean;
}) {
  const [observer, setObserver] = useState('all');
  const label = (id: string | null) => {
    if (!id) return 'Unknown';
    const device = infrastructure.find(d => d.id === id);
    return device ? `${id.toUpperCase()} · ${device.name}`
      : trackers.find(t => t.id === id)?.shortName || id.toUpperCase();
  };
  const rows = links.filter(link => observer === 'all' || link.observerDeviceId === observer)
    .toSorted((a, b) => b.receivedAt.localeCompare(a.receivedAt));
  return <section className="panel neighbor-panel" aria-labelledby="neighbor-heading">
    <div className="panel-heading">
      <h2 id="neighbor-heading">Neighbor signals</h2>
      <label>Receiver{' '}
        <select value={observer} onChange={event => setObserver(event.target.value)}>
          <option value="all">All receivers</option>
          {infrastructure.map(device => <option key={device.id} value={device.id}>{label(device.id)}</option>)}
        </select>
      </label>
    </div>
    <p className="small muted">Each row records one direction, as heard by its receiver. Gateway readings describe the final radio hop. Neighbor reports do not supply signal strength or a last-heard time.</p>
    {!online && <p className="small muted" role="status">Feed unavailable · showing saved observations.</p>}
    {rows.length ? <div className="neighbor-table-scroll" tabIndex={0} role="region" aria-label="Neighbor signal observations">
      <table className="neighbor-table">
        <caption className="sr-only">Recorded directional radio observations; report receipt and last heard are separate times.</caption>
        <thead><tr>
          <th scope="col">Receiver</th><th scope="col">Heard node</th><th scope="col">Original source</th>
          <th scope="col"><abbr title="Signal-to-noise ratio; higher is clearer">Signal quality (SNR)</abbr></th>
          <th scope="col"><abbr title="Received signal strength; less negative is stronger">Strength (RSSI)</abbr></th>
          <th scope="col">Path</th><th scope="col">Last heard</th><th scope="col">Report received</th><th scope="col">Source</th>
        </tr></thead>
        <tbody>{rows.map(row => <tr key={row.id}>
          <th scope="row">{label(row.observerDeviceId)}</th>
          <td>{label(row.heardDeviceId)}</td><td>{label(row.originalSourceDeviceId)}</td>
          <td>{signal(row.snrDb, 'dB')}</td><td>{signal(row.rssiDbm, 'dBm')}</td>
          <td>{row.path === 'direct' ? 'Direct' : row.path === 'relayed' ? 'Relayed' : 'Unknown'}</td>
          <td><time dateTime={row.observedAt ?? undefined} title={row.observedAt ?? 'The report supplies no hearing timestamp'}>{age(row.observedAt, now)}</time></td>
          <td><time dateTime={row.receivedAt} title={row.receivedAt}>{age(row.receivedAt, now)}</time></td>
          <td>{row.source === 'gateway' ? 'Gateway receipt' : 'Neighbor report'}</td>
        </tr>)}</tbody>
      </table>
    </div> : <p className="empty">No signal observations recorded for this receiver.</p>}
  </section>;
}
