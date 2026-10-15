import { lazy, Suspense, useState } from 'react';
import {
  infrastructure as demoInfrastructure,
  initialTrackers as demoTrackers,
  members as demoMembers,
} from './demo';
import type { Assignment, Tracker, Member, Infrastructure } from './demo';
import InfrastructureQuickStats from './InfrastructureQuickStats';
import TrackerDetail from './TrackerDetail';
import { trackerMapLabel } from './tracker';
import { latestRecordedSession } from './recorded-session';
const TrackingMap = lazy(() => import('./TrackingMap'));
export default function MapPage({
  online = true,
  assignments,
  trackers = demoTrackers,
  members = demoMembers,
  infrastructureNodes = demoInfrastructure,
  now,
  selectedId,
  onSelect,
  labels,
  trailId,
  onTrailChange,
}: {
  online?: boolean;
  assignments: Assignment[];
  trackers?: Tracker[];
  members?: Member[];
  infrastructureNodes?: Infrastructure[];
  now: number;
  selectedId: string;
  onSelect: (id: string) => void;
  labels: Record<string, string>;
  trailId: string | null;
  onTrailChange: (id: string | null) => void;
}) {
  const [selection, setSelection] = useState<{
    kind: 'tracker' | 'infrastructure';
    id: string;
  } | null>(null);
  const selectedTracker = selection?.kind === 'tracker'
    ? trackers.find((t) => t.id === selection.id) : undefined;
  const selectedInfrastructure = selection?.kind === 'infrastructure'
    ? infrastructureNodes.find((d) => d.id === selection.id) : undefined;
  const trailDevice = trackers.find((device) => device.id === trailId);
  const trail = trailDevice ? latestRecordedSession(trailDevice, now).points : [];
  return (
    <div className="map-page">
      <Suspense fallback={<div className="map-loading">Loading map renderer…</div>}>
        <TrackingMap online={online} trackers={trackers} infrastructureNodes={infrastructureNodes}
          markerLabels={Object.fromEntries(trackers.map((tracker) => [tracker.id, trackerMapLabel(tracker, assignments, members)]))}
          labels={labels} selectedId={selection?.kind === 'tracker' ? selection.id : ''} now={now}
          trail={trail}
          selectedInfrastructureId={selection?.kind === 'infrastructure' ? selection.id : null}
          onInfrastructureSelect={(id) => setSelection({ kind: 'infrastructure', id })}
          onSelect={(id) => {
            onSelect(id);
            setSelection({ kind: 'tracker', id });
            if (trailId && trailId !== id) onTrailChange(null);
          }}
          />
      </Suspense>
      {selectedTracker && <TrackerDetail key={selectedTracker.id} selected={selectedTracker}
        now={now}
        label={labels[selectedTracker.id] ?? selectedTracker.shortName}
        showTrail={trailId === selectedTracker.id}
        onTrailChange={(visible) => onTrailChange(visible ? selectedTracker.id : null)}
        onClose={() => setSelection(null)} />}
      {selectedInfrastructure && <InfrastructureQuickStats key={selectedInfrastructure.id}
        device={selectedInfrastructure} now={now} online={online} onClose={() => setSelection(null)} />}
    </div>
  );
}
