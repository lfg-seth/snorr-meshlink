import type { ReactNode } from 'react';
import type { Infrastructure, Tracker } from './demo';
import { ageLabel } from './demo';
import { batteryPower } from './battery';
import { batteryChargeEstimate, memberBatteryState } from './battery-charge';
import { metricTime, telemetryTime } from './telemetry-time';

type Props = ({ member: Tracker; infrastructure?: never } | { infrastructure: Infrastructure; member?: never }) & {
  now: number;
  online: boolean;
  gpsQuality?: ReactNode;
};

export default function BatterySummary({ member, infrastructure, now, online, gpsQuality }: Props) {
  const voltage = member ? member.batteryVoltage : infrastructure!.battery;
  const memberState = member ? memberBatteryState(member, now, online) : null;
  const estimate = memberState ?? batteryChargeEstimate(infrastructure!);
  const batteryAt = member ? telemetryTime(member.batteryMeasuredAt, member.batteryReceivedAt, now)
    : metricTime(infrastructure!, 'battery', now);
  const timeout = member ? 15 : infrastructure!.missingTimeoutMinutes?.battery ??
    (infrastructure!.reportCadenceMinutes?.battery ?? infrastructure!.cadenceMinutes) * 3;
  const freshness = (at: string | null, minutes: number) => {
    const age = at ? `${ageLabel(Math.max(0, (now - Date.parse(at)) / 1000))} ago` : 'Awaiting first reading';
    const status = !at ? '' : minutes <= 0 ? ' · freshness unknown'
      : now - Date.parse(at) >= minutes * 60000 ? ' · stale' : '';
    return `${age}${status}${!online ? ' · Feed offline · historical reading' : ''}`;
  };
  const power = infrastructure ? batteryPower(infrastructure, now) : null;
  const current = power?.reading;
  const currentAt = current ? telemetryTime(current.measuredAt, current.receivedAt, now) : null;
  const currentTimeout = infrastructure && current ? infrastructure.missingTimeoutMinutes?.[current.metric] ??
    (infrastructure.reportCadenceMinutes?.[current.metric] ?? infrastructure.cadenceMinutes) * 3 : 0;
  const currentSource = current?.metric === 'sensorCurrentMa' ? 'Environment sensor' : 'Power channel 1';
  return <section className="battery-summary" aria-label="Battery summary">
    <h3>Battery</h3>
    <dl className="battery-summary-grid">
      <div><dt>Estimated battery percentage</dt><dd>{estimate.percent === null ? 'Unknown' : `≈${estimate.percent}%`}
        <small>{estimate.reason}</small></dd></div>
      {gpsQuality && <div className="tracker-gps-quality"><dt>GPS quality</dt><dd>{gpsQuality}</dd></div>}
      <div><dt>Battery voltage</dt><dd>{voltage != null && Number.isFinite(voltage) && voltage > 0 ? `${voltage.toFixed(3)} V` : 'Unknown'}
        {infrastructure?.disabledMonitoring?.includes('battery') && <small>Monitoring disabled</small>}
        {memberState && <small>{memberState.status}</small>}
        <small>{freshness(batteryAt, timeout)}</small></dd></div>
      <div><dt>Charging/discharging</dt><dd>{power?.label ?? 'Unknown'}
        <small>{power && !power.trend ? freshness(currentAt, currentTimeout)
          : power?.label.includes('voltage estimate') ? freshness(power.trendAt, timeout)
          : 'Battery flow unverified'}</small></dd></div>
      <div><dt>Current</dt><dd>{power?.amount ?? 'Unknown'}
        <small>{current ? `Measured · ${currentSource} · battery flow/calibration unverified` : 'No unambiguous current source'}</small>
        {current && <small>{freshness(currentAt, currentTimeout)}</small>}</dd></div>
    </dl>
  </section>;
}
