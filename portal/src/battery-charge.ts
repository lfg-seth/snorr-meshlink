// Approximate readings of EVE's 0.2C / 77°F discharge plot, not an OCV curve.
// Source, lookup points and scope: docs/research/member-battery-charge.md.
const eve26vCurve = [
  [2.5, 0],
  [3.23, 5],
  [3.38, 10],
  [3.47, 20],
  [3.53, 30],
  [3.56, 40],
  [3.61, 50],
  [3.69, 60],
  [3.78, 70],
  [3.87, 80],
  [3.99, 90],
  [4.2, 100],
];

// Generic Meshtastic 1S Li-ion/LiPo OCV lookup, pinned source power.h.
// An approximate starting profile, not calibration of the purchased packs.
const lipoCurve = [
  [3.1, 0], [3.3, 10], [3.42, 20], [3.53, 30], [3.63, 40],
  [3.72, 50], [3.8, 60], [3.89, 70], [3.99, 80], [4.05, 90], [4.19, 100],
];

export function batteryChargeEstimate(device: {
  id: string;
  battery: number | null;
  batteryProfile?: string;
}) {
  // Owner-confirmed project repeaters only; do not infer chemistry from voltage.
  const profile =
    device.batteryProfile ??
    (['r001', 'r002', 'r003'].includes(device.id.toLowerCase())
      ? 'eve-26v-1s'
      : undefined);
  if (profile !== 'eve-26v-1s' && profile !== 'lipo-1s')
    return { percent: null, reason: 'Battery profile unconfigured' };
  const curve = profile === 'lipo-1s' ? lipoCurve : eve26vCurve;
  const reason = profile === 'lipo-1s' ? 'Voltage estimate · generic 1S LiPo' : 'Voltage estimate · EVE 26V';
  const volts = device.battery;
  if (volts === null || !Number.isFinite(volts) || volts <= 0)
    return { percent: null, reason: 'Awaiting valid battery voltage' };
  if (volts > 4.25)
    return { percent: null, reason: 'Voltage outside the 1S profile' };
  if (volts <= curve[0][0])
    return { percent: 0, reason: profile === 'lipo-1s' ? reason : 'At or below specified cell cutoff' };
  if (volts >= curve[curve.length - 1][0])
    return { percent: 100, reason };
  for (let i = 1; i < curve.length; i++) {
    const [upperVolts, upperPercent] = curve[i];
    const [lowerVolts, lowerPercent] = curve[i - 1];
    if (volts <= upperVolts) {
      const percent =
        lowerPercent +
        ((volts - lowerVolts) / (upperVolts - lowerVolts)) *
          (upperPercent - lowerPercent);
      return {
        percent: Math.round(percent / 5) * 5,
        reason,
      };
    }
  }
  return { percent: null, reason: 'Voltage outside the 1S profile' };
}

export function memberBatteryState(device: {
  id: string;
  batteryVoltage?: number | null;
  batteryProfile?: string;
  batteryMeasuredAt?: string | null;
}, now: number, online: boolean) {
  const estimate = batteryChargeEstimate({
    id: device.id, battery: device.batteryVoltage ?? null,
    batteryProfile: device.batteryProfile ?? 'unknown',
  });
  const measured = Date.parse(device.batteryMeasuredAt ?? '');
  const status = !online ? 'Feed offline · historical reading'
    : !Number.isFinite(measured) ? 'Measurement time unknown'
    : measured > now ? 'Invalid future measurement time'
    : now - measured >= 15 * 60000 ? 'Stale battery reading' : 'Recorded voltage';
  return { ...estimate, status };
}
