import type { Infrastructure } from './demo';
import { batteryChargeEstimate } from './battery';
import { metricTime } from './telemetry-time';

export default function BatteryCharge({
  device,
  now,
  online,
}: {
  device: Infrastructure;
  now: number;
  online: boolean;
}) {
  const estimate = batteryChargeEstimate(device);
  const at = metricTime(device, 'battery', now);
  const timeout =
    device.missingTimeoutMinutes?.battery ??
    (device.reportCadenceMinutes?.battery ?? device.cadenceMinutes) * 3;
  const stale = !at || now - Date.parse(at) >= timeout * 60000;
  return (
    <>
      <strong>
        {estimate.percent === null ? 'Unknown' : `≈${estimate.percent}%`}
      </strong>
      {estimate.percent === null && <small>{estimate.reason}</small>}
      {estimate.percent !== null && (!online || stale) && <small>Historical reading</small>}
    </>
  );
}
