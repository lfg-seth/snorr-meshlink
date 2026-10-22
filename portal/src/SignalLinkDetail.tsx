import DeviceSheet from './DeviceSheet';
import { ageLabel } from './demo';
import { signalValue } from './signal-links';
import type { SignalConnection } from './signal-links';

function SignalTime({ at, now }: { at: string | null; now: number }) {
  if (!at || !Number.isFinite(Date.parse(at)) || Date.parse(at) > now) return <>Unknown</>;
  return <time dateTime={at}>{ageLabel((now - Date.parse(at)) / 1000)} ago<small>{new Date(at).toLocaleString()}</small></time>;
}

export default function SignalLinkDetail({ connection, labels, markerLabels = {}, markerClasses, now, online, onClose, onNodeSelect }: {
  connection: SignalConnection;
  labels: Record<string, string>;
  markerLabels?: Record<string, string>;
  markerClasses: Record<string, string>;
  now: number;
  online: boolean;
  onClose: () => void;
  onNodeSelect: (id: string) => void;
}) {
  const label = (id: string | null) => id
    ? connection.nodes.find(node => node.id === id)?.label || labels[id] || id.toUpperCase() : 'Unknown';
  return <DeviceSheet label={connection.nodes.map(node => node.label).join(' / ')}
    eyebrow="Neighbor signal" className="signal-link-detail" closeLabel="Close signal details" onClose={onClose}
    mapNodes={connection.nodes.map(node => ({ ...node, label: markerLabels[node.id] ?? node.label,
      markerClassName: markerClasses[node.id] }))} mapColor={connection.color} onMapNodeSelect={onNodeSelect}>
    {!online && <p className="small muted">Feed offline · showing saved observations</p>}
    <p className="signal-summary" style={{ borderColor: connection.color }}>
      <strong>{signalValue(connection.snrDb, 'dB SNR')}</strong>
      <span>Weakest known SNR across the latest readings below</span>
    </p>
    <p className="small muted">Arrows show heard node → receiver. A reading in one direction does not establish the reverse link. Colors describe recorded SNR, not delivery reliability.</p>
    {connection.latest.map(row => <section className="signal-reading" key={`${row.observerDeviceId}-${row.source}`}>
      <h3>{label(row.heardDeviceId)} → {label(row.observerDeviceId)}</h3>
      <p className="small muted">{row.source === 'gateway' ? 'Gateway receipt · final radio hop' : 'Neighbor report'}</p>
      <dl className="detail-grid">
        <div><dt>Signal quality (SNR)</dt><dd>{signalValue(row.snrDb, 'dB')}</dd></div>
        <div><dt>Signal strength (RSSI)</dt><dd>{signalValue(row.rssiDbm, 'dBm')}</dd></div>
        <div><dt>Last heard / measured</dt><dd><SignalTime at={row.observedAt} now={now} />
          {!row.observedAt && <small>No hearing timestamp supplied</small>}</dd></div>
        <div><dt>Report delivered</dt><dd><SignalTime at={row.receivedAt} now={now} /><small>Delivery time does not refresh signal age</small></dd></div>
        <div><dt>Packet path</dt><dd>{row.path === 'direct' ? 'Direct' : row.path === 'relayed' ? 'Relayed' : 'Unknown'}</dd></div>
        <div><dt>Original packet source</dt><dd>{label(row.originalSourceDeviceId)}</dd></div>
        {row.reportType === 'snns-v1' && <>
          <div><dt>Hearing age at report</dt><dd>{row.hearingAgeSeconds}s<small>Excludes transport delay; absolute hearing time unknown</small></dd></div>
          <div><dt>Accepted observations</dt><dd>{row.observationCount}<small>Count since collector entry began; delivery reliability unmeasured</small></dd></div>
          <div><dt>Report coverage</dt><dd>{row.subset ? 'Partial table' : 'Complete current table'} · {row.totalNeighbors} neighbors{row.capacityEvicted && <small>Earlier capacity eviction reported</small>}</dd></div>
          <div><dt>Report identity</dt><dd>Boot {row.bootId} · sequence {row.sequence}<small>Reporter uptime {row.reportUptimeSeconds}s · via {label(row.transportGatewayId ?? null)}</small></dd></div>
        </>}
      </dl>
    </section>)}
    <p className="small muted">{connection.observations.length} saved observation{connection.observations.length === 1 ? '' : 's'} in the loaded records. Latest reading per direction and report source shown; missing values stay Unknown.</p>
    <details className="signal-location-details"><summary>Endpoint locations</summary>
      <p className="small muted">Lines join displayed locations; they do not trace a radio path or positions at measurement time.</p>
      <dl>{connection.nodes.map(node => <div key={node.id}><dt>{node.label}</dt>
        <dd>{node.location}{node.location === 'Last recorded GPS' && <small><SignalTime at={node.measuredAt} now={now} /></small>}</dd></div>)}</dl>
    </details>
  </DeviceSheet>;
}
