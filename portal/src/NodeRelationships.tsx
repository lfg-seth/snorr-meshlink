import type { SignalConnection } from './signal-links';
import { signalValue } from './signal-links';

export default function NodeRelationships({ nodeId, connections, onSelect }: {
  nodeId: string;
  connections: SignalConnection[];
  onSelect: (id: string) => void;
}) {
  const relationships = connections.filter(connection => connection.nodes.some(node => node.id === nodeId));
  return <section className="node-relationships" aria-label="Neighbors">
    <h3>Neighbors</h3>
    {relationships.length ? <ul>{relationships.map(connection => <li key={connection.id}>
      <button className="node-relationship" onClick={() => onSelect(connection.id)}
        aria-label={`${connection.relationship}, ${signalValue(connection.snrDb, 'dB SNR')}, view relationship`}>
        <span>{connection.relationship}</span>
        <span className="signal-pill" style={{ color: connection.color, borderColor: connection.color }}>
          {signalValue(connection.snrDb, 'dB')}
        </span>
      </button>
    </li>)}</ul> : <p className="small muted">No recorded neighbors</p>}
  </section>;
}
