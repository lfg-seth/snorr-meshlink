import type { LinkObservation } from './NeighborTable';
import { ageLabel } from './demo';
import { signalFreshness } from './signal-freshness';

export default function SignalHearingAge({ row, now }: { row: LinkObservation; now: number }) {
  const freshness = signalFreshness(row, now);
  if (!freshness) return <>Unknown</>;
  if (freshness.basis === 'relative') return <span title="Hearing age at report plus elapsed server receipt time; excludes upstream delivery delay. Absolute hearing time unknown.">
    Estimated {ageLabel(freshness.ageSeconds)} ago<small>Excludes upstream delivery delay</small>
  </span>;
  return <time dateTime={row.observedAt!} title={row.observedAt!}>{ageLabel(freshness.ageSeconds)} ago</time>;
}
