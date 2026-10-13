import { useState } from 'react';
import Badge from './Badge';
import {
  ageLabel,
  infrastructure as demoInfrastructure,
  telemetryState,
  timeLabel,
} from './demo';
import type { AuditEvent, BatteryRule, Incident } from './demo';
export default function InfrastructurePage({
  now,
  connected = false,
  infrastructureNodes = demoInfrastructure,
  warnings = [],
  onAckWarning,
  online,
  admin,
  incidents,
  events,
  rules,
  onRule,
  onIncident,
}: {
  now: number;
  connected?: boolean;
  infrastructureNodes?: import('./demo').Infrastructure[];
  warnings?: {
    id: string;
    deviceId: string;
    kind: string;
    recoveredAt: string | null;
    acknowledgedAt: string | null;
  }[];
  onAckWarning?: (id: string) => void;
  online: boolean;
  admin: boolean;
  incidents: Incident[];
  events: AuditEvent[];
  rules: Record<string, BatteryRule>;
  onRule: (id: string, rule: BatteryRule) => void;
  onIncident: (id: string, note?: string) => void;
}) {
  const [selectedId, setSelectedId] = useState('r1');
  const [role, setRole] = useState('All');
  const [note, setNote] = useState('');
  const selected =
    infrastructureNodes.find((d) => d.id === selectedId) ??
    infrastructureNodes[0];
  if (!selected)
    return (
      <p className="empty">No infrastructure devices have been provisioned.</p>
    );
  const incident = incidents.find(
    (i) => i.deviceId === selected.id && !i.resolvedAt,
  );
  const metricState = (metric: string) => {
    const time = selected.readingTimes
      ? selected.readingTimes[metric]
      : selected.reportedAt;
    if (selected.readingTimes && metric in selected.readingTimes && !time)
      return 'unknown measurement time';
    const cadence =
      selected.reportCadenceMinutes?.[metric] ?? selected.cadenceMinutes;
    const timeout = selected.missingTimeoutMinutes?.[metric] ?? cadence * 3;
    if (!time) return 'awaiting first report';
    return now - Date.parse(time) >= timeout * 60000
      ? 'stale reading'
      : 'current reading';
  };
  const state = telemetryState(
    selected.reportedAt,
    now,
    selected.cadenceMinutes,
  );
  return (
    <div className="stack">
      <div className="section-toolbar">
        <label>
          Device role{' '}
          <select
            value={role}
            onChange={(event) => setRole(event.target.value)}
          >
            <option>All</option>
            <option>Repeater</option>
            <option>Backhaul</option>
          </select>
        </label>
        <span className="muted small">
          Scenario capabilities and readings · hardware fitment unverified
        </span>
      </div>
      <div className="infrastructure-grid">
        {infrastructureNodes
          .filter((d) => role === 'All' || d.role === role)
          .map((device) => {
            const deviceState = telemetryState(
              device.reportedAt,
              now,
              device.cadenceMinutes,
            );
            const open = incidents.find(
              (i) => i.deviceId === device.id && !i.resolvedAt,
            );
            return (
              <button
                className={`infra-card ${selected.id === device.id ? 'active' : ''}`}
                key={device.id}
                aria-pressed={selected.id === device.id}
                onClick={() => {
                  setSelectedId(device.id);
                  setNote('');
                }}
              >
                <span className="eyebrow">
                  {device.role} · {device.id.toUpperCase()}
                </span>
                <strong>{device.name}</strong>
                <span className="infra-value">
                  {device.battery === null
                    ? '—'
                    : `${device.battery.toFixed(2)} V`}
                  <small>Last recorded battery</small>
                </span>
                <Badge
                  kind={
                    deviceState === 'Current reading' ? 'recent' : 'neutral'
                  }
                >
                  {deviceState}
                </Badge>
                {warnings
                  .filter((w) => w.deviceId === device.id && !w.recoveredAt)
                  .map((w) => (
                    <Badge key={w.id} kind="old">
                      {w.kind === 'battery'
                        ? 'Low battery'
                        : `Missing ${w.kind.split(':')[1]}`}
                      {w.acknowledgedAt ? ' · acknowledged' : ''}
                    </Badge>
                  ))}
                {open && (
                  <Badge kind="old">
                    Intrusion ·{' '}
                    {open.acknowledgedAt ? 'acknowledged, open' : 'open'}
                  </Badge>
                )}
                {!online && (
                  <span className="small muted">
                    Feed outage · health uncertain
                  </span>
                )}
              </button>
            );
          })}
      </div>
      <section className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">{selected.role} detail</p>
            <h2>{selected.name}</h2>
          </div>
          <Badge>{state}</Badge>
        </div>
        <p className="muted small">
          Last report:{' '}
          {selected.reportedAt
            ? `${timeLabel(selected.reportedAt)} · ${ageLabel((now - Date.parse(selected.reportedAt)) / 1000)} ago`
            : 'Never reported'}
          . Demo cadence {selected.cadenceMinutes}m; missing timeout{' '}
          {selected.cadenceMinutes * 3}m (three intervals).{' '}
          {online
            ? 'Fresh evidence is required to recover existing warnings.'
            : 'Outage suppresses new missing incidents and preserves existing warnings. Reconnect grace applies before new missing warnings.'}
        </p>
        <dl className="detail-grid">
          <div>
            <dt>Battery voltage</dt>
            <dd>
              {selected.battery === null
                ? 'Awaiting first reading'
                : `${selected.battery.toFixed(2)} V · ${metricState('battery')}`}
            </dd>
          </div>
          <div>
            <dt>Solar input</dt>
            <dd>
              {!selected.equipped.solar
                ? 'Not equipped'
                : selected.solar === null
                  ? 'Awaiting first reading'
                  : `${selected.solar} W (demo) · ${metricState('solar')}`}
            </dd>
          </div>
          <div>
            <dt>Weather temperature</dt>
            <dd>
              {!selected.equipped.weather
                ? 'Not equipped'
                : selected.temperature === null
                  ? 'Awaiting first reading'
                  : `${selected.temperature} °C (demo) · ${metricState('temperature')}`}
            </dd>
          </div>
          <div>
            <dt>Intrusion sensor state</dt>
            <dd>
              {!selected.equipped.intrusion
                ? 'Not equipped · no all-clear inferred'
                : selected.intrusion === null
                  ? 'Awaiting first reading'
                  : `${selected.intrusion ? 'Triggered' : 'Reported normal'} · ${metricState('intrusion')}`}
            </dd>
          </div>
          <div>
            <dt>Charge / discharge current</dt>
            <dd>Unknown · no measured value</dd>
          </div>
          <div>
            <dt>Gateway direction</dt>
            <dd>
              {selected.id === 'b1'
                ? 'Designated downlink + uplink (demo)'
                : selected.id === 'b2'
                  ? 'Uplink only (demo)'
                  : 'Relay (demo)'}
            </dd>
          </div>
        </dl>
        {warnings
          .filter((w) => w.deviceId === selected.id && !w.recoveredAt)
          .map((w) => (
            <div className="incident" key={w.id}>
              <Badge kind="old">{w.kind} warning</Badge>
              <p className="small">
                {w.acknowledgedAt
                  ? 'Acknowledged · still open'
                  : 'Open · fresh evidence required for recovery'}
              </p>
              {onAckWarning && !w.acknowledgedAt && (
                <button onClick={() => onAckWarning(w.id)}>
                  Acknowledge warning
                </button>
              )}
            </div>
          ))}
        {incident && (
          <div className="incident">
            <div className="panel-heading">
              <h3>Open intrusion incident</h3>
              <Badge kind="old">Latched</Badge>
            </div>
            <p className="small">
              Opened {timeLabel(incident.openedAt)}. A normal sensor reading
              does not resolve this incident. Acknowledgment means seen.
            </p>
            {incident.acknowledgedAt ? (
              <p className="small">
                Acknowledged {timeLabel(incident.acknowledgedAt)} · still open
              </p>
            ) : (
              <button onClick={() => onIncident(incident.id)}>
                Acknowledge incident
              </button>
            )}
            {admin && (
              <form
                className="resolve-form"
                onSubmit={(event) => {
                  event.preventDefault();
                  if (note.trim()) {
                    onIncident(incident.id, note.trim());
                    setNote('');
                  }
                }}
              >
                <label>
                  Admin resolution note
                  <input
                    value={note}
                    onChange={(event) => setNote(event.target.value)}
                    placeholder="Record the reason for resolving…"
                    required
                  />
                </label>
                <button disabled={!note.trim()} type="submit">
                  Resolve demo incident
                </button>
              </form>
            )}
          </div>
        )}
        <div className="infra-detail-columns">
          <div>
            <h3>Recorded battery history</h3>
            <p className="small muted">
              Illustrative voltage observations, not remaining charge or
              runtime.
            </p>
            {selected.samples.length ? (
              <>
                <svg
                  className="telemetry-chart"
                  viewBox="0 0 400 130"
                  role="img"
                  aria-label={`Recorded battery voltages: ${selected.samples.map((s) => `${s.volts} V at ${timeLabel(s.at)}`).join(', ')}`}
                >
                  <path d="M35 10V100H390" fill="none" stroke="#cdd6d2" />
                  <text x="0" y="20">
                    4.2V
                  </text>
                  <text x="0" y="100">
                    3.4V
                  </text>
                  {selected.samples.map((sample, i) => (
                    <circle
                      key={sample.at}
                      cx={
                        45 +
                        (i * 330) / Math.max(1, selected.samples.length - 1)
                      }
                      cy={100 - ((sample.volts - 3.4) / 0.8) * 80}
                      r="5"
                      fill="#287162"
                    />
                  ))}
                </svg>
                <div className="point-buttons">
                  {selected.samples.map((s) => (
                    <span key={s.at}>
                      {timeLabel(s.at)} · {s.volts} V
                    </span>
                  ))}
                </div>
              </>
            ) : (
              <p className="empty">No battery observations.</p>
            )}
          </div>
          <div>
            <h3>Declared hardware configuration</h3>
            <dl className="config-list">
              <dt>Battery</dt>
              <dd>{selected.batterySetup}</dd>
              <dt>Solar</dt>
              <dd>{selected.solarSetup}</dd>
              <dt>Antenna</dt>
              <dd>{selected.antenna}</dd>
            </dl>
            <p className="small muted">
              Configuration does not establish measured capacity, panel output
              or antenna performance.
            </p>
          </div>
        </div>
        <RuleForm
          key={selected.id}
          deviceId={selected.id}
          connected={connected}
          rule={rules[selected.id] ?? rules['*']}
          admin={admin}
          onRule={onRule}
        />
      </section>
      <section className="panel">
        <h2>Event & audit history</h2>
        <p className="small muted">
          Silent persistent infrastructure badges; no infrastructure toasts or
          sound.
        </p>
        <ol className="event-list">
          {[...events]
            .reverse()
            .filter((e) => e.deviceId === selected.id)
            .map((event) => (
              <li key={event.id}>
                <time>{timeLabel(event.at)}</time>
                <span>{event.text}</span>
              </li>
            ))}
        </ol>
        {!events.some((e) => e.deviceId === selected.id) && (
          <p className="empty">No simulated events recorded for this device.</p>
        )}
        {incidents
          .filter((i) => i.deviceId === selected.id && i.resolvedAt)
          .map((i) => (
            <p className="small" key={i.id}>
              Resolved {timeLabel(i.resolvedAt)} · {i.note}
            </p>
          ))}
      </section>
    </div>
  );
}
function RuleForm({
  deviceId,
  connected = false,
  rule,
  admin,
  onRule,
}: {
  deviceId: string;
  connected?: boolean;
  rule?: BatteryRule;
  admin: boolean;
  onRule: (id: string, rule: BatteryRule) => void;
}) {
  const [trigger, setTrigger] = useState(rule ? String(rule.trigger) : '');
  const [recovery, setRecovery] = useState(rule ? String(rule.recovery) : '');
  const [error, setError] = useState('');
  return (
    <div className="rule-section">
      <h3>Battery warning configuration</h3>
      <p className="small muted">
        {rule?.enabled === false
          ? 'Disabled rule · earlier warning history retained.'
          : rule
            ? `Demo rule: below ${rule.trigger} V; recover at ${rule.recovery} V on fresh evidence.`
            : 'Unconfigured · no hardware voltage thresholds selected.'}{' '}
        {connected
          ? 'The server evaluates supported readings and separate recovery thresholds.'
          : 'This prototype records the rule only; automatic warning evaluation comes with ingestion.'}
      </p>
      {admin && (
        <form
          className="assignment-form"
          onSubmit={(event) => {
            event.preventDefault();
            const t = Number(trigger);
            const r = Number(recovery);
            if (!trigger || !recovery || t <= 0 || r <= t) {
              setError(
                'Recovery must be greater than a positive trigger voltage.',
              );
              return;
            }
            setError('');
            onRule(deviceId, { trigger: t, recovery: r });
          }}
        >
          <label>
            Trigger voltage (demo)
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={trigger}
              onChange={(event) => setTrigger(event.target.value)}
              required
            />
          </label>
          <label>
            Recovery voltage (demo)
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={recovery}
              onChange={(event) => setRecovery(event.target.value)}
              required
            />
          </label>
          <button type="submit">Save illustrative rule</button>
        </form>
      )}
      {error && (
        <p role="alert" className="form-error">
          {error}
        </p>
      )}
    </div>
  );
}
