import { useState } from 'react';
import type { Tracker } from './demo';
import { timeLabel } from './demo';
import { memberBatteryState } from './battery-charge';
import { telemetryTime } from './telemetry-time';

export type BatteryConfiguration = {
  batteryProfile: string;
  batteryCapacityMah: number | null;
};

export default function MemberBattery({ device, now, online, onConfigure }: {
  device: Tracker;
  now: number;
  online: boolean;
  onConfigure?: (config: BatteryConfiguration) => Promise<boolean>;
}) {
  const [profile, setProfile] = useState(device.batteryProfile ?? 'unknown');
  const [capacity, setCapacity] = useState(String(device.batteryCapacityMah ?? ''));
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const estimate = memberBatteryState(device, now, online);
  return (
    <section aria-label="Member battery">
      <h3>Battery</h3>
      <dl className="detail-grid">
        <div><dt>Estimated battery percentage</dt><dd>
          {estimate.percent === null ? 'Unknown' : `≈${estimate.percent}%`}
          <small>{estimate.reason}</small>
        </dd></div>
        <div><dt>Battery voltage</dt><dd>
          {device.batteryVoltage == null ? 'Unknown' : `${device.batteryVoltage.toFixed(3)} V`}
          <small>{estimate.status}</small>
        </dd></div>
        <div><dt>Battery measured at</dt><dd>{timeLabel(telemetryTime(device.batteryMeasuredAt, device.batteryReceivedAt, now))}</dd></div>
        <div><dt>Battery received at</dt><dd>{timeLabel(device.batteryReceivedAt ?? null)}</dd></div>
        <div><dt>Configured battery</dt><dd>
          {device.batteryProfile === 'lipo-1s' ? 'LiPo · 1S · 3.7 / 4.2 V'
            : device.batteryProfile === 'eve-26v-1s' ? 'EVE 26V · 1S' : 'Type unknown'}
          <small>{device.batteryCapacityMah ? `${device.batteryCapacityMah} mAh nominal` : 'Capacity unknown'}</small>
        </dd></div>
      </dl>
      <p className="small muted">Approximate voltage estimate, rounded to 5%. Charging, load and temperature affect it. Capacity does not determine charge percentage or remaining runtime. Battery age is independent of GPS age; stale after 15 minutes.</p>
      {onConfigure && <form onSubmit={async (event) => {
        event.preventDefault();
        setSaving(true);
        setMessage('');
        try {
          const saved = await onConfigure({ batteryProfile: profile,
            batteryCapacityMah: capacity === '' ? null : Number(capacity) });
          setMessage(saved ? 'Battery configuration saved.' : 'Could not save battery configuration.');
        } catch {
          setMessage('Could not save battery configuration.');
        } finally {
          setSaving(false);
        }
      }}>
        <fieldset disabled={saving}>
          <legend>Battery configuration</legend>
          <label>Battery type <select value={profile} onChange={(e) => setProfile(e.target.value)}>
            <option value="unknown">Unknown / unconfigured</option>
            <option value="lipo-1s">LiPo 1S · 3.7 V nominal / 4.2 V full</option>
            <option value="eve-26v-1s">EVE 26V 18650 · 1S</option>
          </select></label>
          <label>Nominal capacity (mAh) <input type="number" min="1" max="1000000" step="1"
            list={`battery-capacities-${device.id}`} value={capacity}
            placeholder="Unknown" onChange={(e) => setCapacity(e.target.value)} /></label>
          <datalist id={`battery-capacities-${device.id}`}>
            <option value="1000" /><option value="1100" /><option value="3000" />
          </datalist>
          <button type="submit">{saving ? 'Saving…' : 'Save battery configuration'}</button>
        </fieldset>
        <p role="status">{message}</p>
      </form>}
    </section>
  );
}
