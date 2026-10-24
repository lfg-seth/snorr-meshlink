import type { Infrastructure } from './demo';

export function gatewayHealthLabel(report: Infrastructure['gatewayHealth'], now: number, online: boolean) {
  if (!report?.measuredAt || !report.intervalSeconds) return { label: 'Awaiting gateway health report', kind: 'neutral' as const };
  const age = now - Date.parse(report.measuredAt);
  if (!Number.isFinite(age) || age < 0 || age >= report.intervalSeconds * 3000)
    return { label: 'Gateway health stale', kind: 'neutral' as const };
  if (!online) return { label: 'Feed outage · gateway health uncertain', kind: 'neutral' as const };
  return { label: report.label + (report.radioAlive ? ` · radio alive via ${report.transportGatewayId?.toUpperCase()}` : ''),
    kind: report.state === 'online' ? 'recent' as const : report.state.endsWith('lost') ? 'old' as const : 'neutral' as const };
}
