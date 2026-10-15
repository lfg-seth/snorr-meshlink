import type { Infrastructure } from './demo';
import { batteryChargeEstimate } from './battery';

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
  const at = device.readingTimes
    ? device.readingTimes.battery
    : device.reportedAt;
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
