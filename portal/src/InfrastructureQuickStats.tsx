import BatteryCharge from './BatteryCharge';
import DeviceSheet from './DeviceSheet';
import { temperatureLabel } from './temperature';
import type { Infrastructure } from './demo';
import { ageLabel, timeLabel } from './demo';
import { batteryPower } from './battery';
import { infrastructureLabel } from './infrastructure-map';

export default function InfrastructureQuickStats({
  device,
  now,
  online,
  onClose,
}: {
  device: Infrastructure;
  now: number;
  online: boolean;
  onClose: () => void;
}) {
  const power = batteryPower(device, now);
  const freshness = (metric: string) => {
    const at = device.readingTimes
      ? device.readingTimes[metric]
      : device.reportedAt;
    const minutes =
      device.missingTimeoutMinutes?.[metric] ??
      (device.reportCadenceMinutes?.[metric] ?? device.cadenceMinutes) * 3;
    if (!at) return 'measurement time unknown';
    return `${ageLabel(Math.max(0, (now - Date.parse(at)) / 1000))} ago${now - Date.parse(at) >= minutes * 60000 ? ' · stale' : ''}`;
  };
  return (
    <DeviceSheet label={infrastructureLabel(device)} eyebrow={device.role}
      className="infrastructure-quick-stats" closeLabel="Close infrastructure stats" onClose={onClose}>
      <p className="small">{device.name}</p>
      {device.deploymentStatus === 'planned' && (
        <p className="small muted">
          Planned location · installation unverified
        </p>
      )}
      {!online && (
        <p className="small muted">Feed offline · retained readings</p>
      )}
      <dl className="infra-quick-grid">
        <div>
          <dt>Estimated battery percentage</dt>
          <dd><BatteryCharge device={device} now={now} online={online} /></dd>
        </div>
        <div>
          <dt>Battery voltage</dt>
          <dd>
            {device.battery === null
              ? 'Unknown'
              : `${device.battery.toFixed(3)} V`}
            <small>{freshness('battery')}</small>
          </dd>
        </div>
        <div>
          <dt>{power.label}</dt>
          <dd>{power.amount}</dd>
        </div>
        {device.temperature !== null && (
          <div>
            <dt>Temperature</dt>
            <dd>
              {temperatureLabel(device.temperature)}
              <small>{freshness('temperature')}</small>
            </dd>
          </div>
        )}
        {device.humidity != null && (
          <div>
            <dt>Relative humidity</dt>
            <dd>
              {device.humidity.toFixed(1)}% RH
              <small>{freshness('humidity')}</small>
            </dd>
          </div>
        )}
        <div>
          <dt>Last heard</dt>
          <dd>
            {device.lastContactAt
              ? `${ageLabel(Math.max(0, (now - Date.parse(device.lastContactAt)) / 1000))} ago · ${timeLabel(device.lastContactAt)}`
              : 'No receipt time recorded'}
          </dd>
        </div>
      </dl>
    </DeviceSheet>
  );
}
