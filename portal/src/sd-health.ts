import { ageLabel } from './demo.ts';

export type SdHealth = {
  flags: number; usedBytes: string | null; totalBytes: string | null;
  dropped: number; measuredAt: string | null; receivedAt: string; intervalSeconds: number;
};

export function sdHealthLabel(report: SdHealth | null | undefined, now: number, online: boolean) {
  if (!report) return 'SD logging unknown · awaiting daily report';
  const age = report.measuredAt ? (now - Date.parse(report.measuredAt)) / 1000 : null;
  const storage = report.usedBytes !== null && report.totalBytes !== null && Number(report.totalBytes) > 0
    ? `${(Number(report.usedBytes) / Number(report.totalBytes) * 100).toFixed(1)}% used (${report.usedBytes} / ${report.totalBytes} bytes)`
    : 'capacity unknown';
  const status = report.flags & 4 ? 'Logging' : report.flags & 2 ? 'Write failed' :
    report.flags & 1 ? 'Mount failed' : 'Card unavailable';
  const freshness = age === null ? 'source time unknown' : `reported ${ageLabel(age)} ago`;
  const lastKnown = !online || age === null || age < 0 || age >= report.intervalSeconds * 3;
  return `${lastKnown ? 'Last known · ' : ''}${status} · ${storage} · ${report.dropped} dropped this boot · ${freshness}`;
}
