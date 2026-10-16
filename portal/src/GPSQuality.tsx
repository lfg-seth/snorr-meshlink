import type { Fix } from './demo';
import { gpsQuality } from './gps-quality';

const descriptions = {
  good: { label: 'Good', text: 'Satellite conditions looked good for this recorded location.' },
  limited: { label: 'Limited', text: 'Satellite conditions were less favorable. Treat this recorded location with extra caution.' },
  poor: { label: 'Poor', text: 'Satellite conditions were poor. This recorded location may be unreliable.' },
  unknown: { label: 'Unknown', text: 'This recorded location has no usable GPS quality report.' },
};

export default function GPSQuality({ position }: { position: Fix | null }) {
  const quality = gpsQuality(position?.pdop);
  const { label, text } = descriptions[quality];
  const bars = { good: 3, limited: 2, poor: 1, unknown: 0 }[quality];
  const satellites = position?.satellites;
  const hasSatellites = typeof satellites === 'number' && Number.isInteger(satellites) && satellites > 0;
  return (
    <details className="gps-quality">
      <summary className={`gps-quality-pill ${quality}`} aria-label={`GPS quality: ${label}. Show explanation`}>
        <svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">
          {[0, 1, 2].map((bar) => <rect key={bar} x={1 + bar * 5} y={10 - bar * 4}
            width="4" height={5 + bar * 4} rx="1" fill="currentColor" opacity={bar < bars ? 1 : 0.2} />)}
        </svg>
        {label}
        <span className="gps-quality-info" aria-hidden="true">ⓘ</span>
      </summary>
      <p className="gps-quality-explanation">
        {position ? text : 'No recorded location is available.'}
        {' '}This describes the satellite layout, not a measured accuracy or a guarantee.
        {' '}Trees, cliffs and reflected signals can still affect the location. Check Last GPS for its age.
        {hasSatellites && <> Reported satellites: {satellites}.</>}
      </p>
    </details>
  );
}
