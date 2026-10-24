import { lazy, Suspense, useMemo, useState } from 'react';
import type { Assignment, Tracker, Member, Infrastructure } from './demo';
import InfrastructureQuickStats from './InfrastructureQuickStats';
import type { LoadBatteryHistory } from './BatteryChart';
import TrackerDetail from './TrackerDetail';
import { trackerMapLabel } from './tracker';
import { latestRecordedSession } from './recorded-session';
import type { LinkObservation } from './NeighborTable';
import { signalConnections } from './signal-links';
import SignalLinkDetail from './SignalLinkDetail';
import NodeRelationships from './NodeRelationships';
import { trackerMarkerClass, infrastructureMarkerClass } from './map-markers';
const TrackingMap = lazy(() => import('./TrackingMap'));
export default function MapPage({
  online = true,
  assignments,
  trackers = [],
  members = [],
  infrastructureNodes = [],
  links = [],
  now,
  selectedId,
  onSelect,
  labels,
  trailId,
  onTrailChange,
  loadBatteryHistory,
}: {
  online?: boolean;
  loadBatteryHistory?: LoadBatteryHistory;
  assignments: Assignment[];
  trackers?: Tracker[];
  members?: Member[];
  infrastructureNodes?: Infrastructure[];
  links?: LinkObservation[];
  now: number;
  selectedId: string;
  onSelect: (id: string) => void;
  labels: Record<string, string>;
  trailId: string | null;
  onTrailChange: (id: string | null) => void;
}) {
  const [selection, setSelection] = useState<{
    kind: 'tracker' | 'infrastructure' | 'signal';
    id: string;
  } | null>(null);
  const [showSignals, setShowSignals] = useState(false);
  const markerLabels = Object.fromEntries(trackers.map(tracker => [tracker.id, trackerMapLabel(tracker, assignments, members)]));
  const markerClasses = Object.fromEntries([
    ...trackers.map(tracker => [tracker.id, trackerMarkerClass(tracker, now)]),
    ...infrastructureNodes.map(device => [device.id, infrastructureMarkerClass()]),
  ]);
  const signalMap = useMemo(() => signalConnections(links, trackers, infrastructureNodes, now), [links, trackers, infrastructureNodes, now]);
  const selectedSignal = selection?.kind === 'signal'
    ? signalMap.relationships.find(connection => connection.id === selection.id) : undefined;
  const selectedTracker = selection?.kind === 'tracker'
    ? trackers.find((t) => t.id === selection.id) : undefined;
  const selectedInfrastructure = selection?.kind === 'infrastructure'
    ? infrastructureNodes.find((d) => d.id === selection.id) : undefined;
  const trailDevice = trackers.find((device) => device.id === trailId);
  const trail = trailDevice ? latestRecordedSession(trailDevice, now).points : [];
  const relationships = (nodeId: string) => <NodeRelationships nodeId={nodeId}
    connections={signalMap.relationships} onSelect={(id) => setSelection({ kind: 'signal', id })} />;
  const selectTracker = (id: string) => {
    onSelect(id);
    setSelection({ kind: 'tracker', id });
    if (trailId && trailId !== id) onTrailChange(null);
  };
  return (
    <div className="map-page">
      <Suspense fallback={<div className="map-loading">Loading map renderer…</div>}>
        <TrackingMap online={online} trackers={trackers} infrastructureNodes={infrastructureNodes}
          signalConnections={signalMap.connections} omittedSignals={signalMap.omitted}
          showSignals={showSignals} onSignalsChange={setShowSignals}
          selectedSignalId={selection?.kind === 'signal' ? selection.id : null}
          onSignalSelect={(id) => setSelection({ kind: 'signal', id })}
          markerLabels={markerLabels}
          labels={labels} selectedId={selection?.kind === 'tracker' ? selection.id : ''} now={now}
          trail={trail}
          selectedInfrastructureId={selection?.kind === 'infrastructure' ? selection.id : null}
          onInfrastructureSelect={(id) => setSelection({ kind: 'infrastructure', id })}
          onSelect={selectTracker}
          />
      </Suspense>
      {selectedTracker && <TrackerDetail key={selectedTracker.id} selected={selectedTracker}
        now={now} online={online}
        label={labels[selectedTracker.id] ?? selectedTracker.shortName}
        mapLabel={markerLabels[selectedTracker.id]}
        showTrail={trailId === selectedTracker.id}
        relationships={relationships(selectedTracker.id)}
        onTrailChange={(visible) => onTrailChange(visible ? selectedTracker.id : null)}
        onClose={() => setSelection(null)} />}
      {selectedInfrastructure && <InfrastructureQuickStats key={selectedInfrastructure.id}
        loadBatteryHistory={loadBatteryHistory}
        device={selectedInfrastructure} now={now} online={online} onClose={() => setSelection(null)}
        relationships={relationships(selectedInfrastructure.id)} />}
      {selectedSignal && <SignalLinkDetail key={selectedSignal.id} connection={selectedSignal}
        markerLabels={markerLabels}
        markerClasses={markerClasses}
        labels={{ ...labels, ...Object.fromEntries(infrastructureNodes.map(d => [d.id, d.name])) }}
        onNodeSelect={(id) => {
          if (trackers.some(tracker => tracker.id === id)) selectTracker(id);
          else if (infrastructureNodes.some(device => device.id === id)) setSelection({ kind: 'infrastructure', id });
        }}
        now={now} online={online} onClose={() => setSelection(null)} />}
    </div>
  );
}
