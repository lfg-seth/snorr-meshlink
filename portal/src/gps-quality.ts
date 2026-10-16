export type GPSQuality = 'good' | 'limited' | 'poor' | 'unknown';

// A coarse satellite-geometry indicator, not calibrated location confidence.
// These provisional presentation bands do not measure an error in metres.
export function gpsQuality(pdop: number | null | undefined): GPSQuality {
  if (typeof pdop !== 'number' || !Number.isFinite(pdop) || pdop <= 0) return 'unknown';
  if (pdop < 3) return 'good';
  if (pdop <= 6) return 'limited';
  return 'poor';
}
