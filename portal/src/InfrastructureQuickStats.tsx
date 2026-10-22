import BatteryCharge from './BatteryCharge';
import PowerReadings from './PowerReadings';
import BatteryChart from './BatteryChart';
import type { LoadBatteryHistory } from './BatteryChart';
import DeviceSheet from './DeviceSheet';
import { temperatureLabel } from './temperature';
import type { Infrastructure } from './demo';
import { ageLabel, timeLabel } from './demo';
import { batteryPower } from './battery';
import { metricTime } from './telemetry-time';
import { infrastructureLabel } from './infrastructure-map';
import type { ReactNode } from 'react';
import { infrastructureMarkerClass } from './map-markers';

export default function InfrastructureQuickStats({
  device,
  now,
  online,
  onClose,
  relationships,
  loadBatteryHistory,
}: {
  device: Infrastructure;
  now: number;
  online: boolean;
  onClose: () => void;
  relationships?: ReactNode;
  loadBatteryHistory?: LoadBatteryHistory;
}) {
  const power = batteryPower(device, now);
  const freshness = (metric: string) => {
    const at = metricTime(device, metric, now);
    const minutes =
      device.missingTimeoutMinutes?.[metric] ??
      (device.reportCadenceMinutes?.[metric] ?? device.cadenceMinutes) * 3;
    if (!at) return 'Awaiting first reading';
    return `${ageLabel(Math.max(0, (now - Date.parse(at)) / 1000))} ago${now - Date.parse(at) >= minutes * 60000 ? ' · stale' : ''}`;
  };
  return (
    <DeviceSheet label={infrastructureLabel(device)} eyebrow={device.role}
      className="infrastructure-quick-stats" closeLabel="Close infrastructure stats" onClose={onClose}
      mapNodes={[{ id: device.id, label: infrastructureLabel(device), markerClassName: infrastructureMarkerClass(true),
        coordinates: device.longitude != null && device.latitude != null ? [device.longitude, device.latitude] : null }]}>
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
      <BatteryChart device={device} now={now} loadHistory={loadBatteryHistory} />
      <PowerReadings device={device} now={now} />
      {relationships}
    </DeviceSheet>
  );
}
