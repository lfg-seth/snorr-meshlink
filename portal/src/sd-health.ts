import { ageLabel } from './demo.ts';

export type SdHealth = {
  flags: number; usedBytes: string | null; totalBytes: string | null;
  dropped: number; measuredAt: string | null; receivedAt: string; intervalSeconds: number;
};

function size(bytes: bigint) {
  const units = ['B','KiB','MiB','GiB','TiB','PiB','EiB'];
  let unit = 0, divisor = 1n;
  while (unit < units.length - 1 && bytes >= divisor*1024n) { divisor *= 1024n; unit++; }
  const tenths = (bytes*10n + divisor/2n)/divisor;
  return `${tenths/10n}${tenths%10n ? '.'+String(tenths%10n) : ''} ${units[unit]}`;
}

export function sdHealthLabel(report: SdHealth | null | undefined, now: number, online: boolean) {
  if (!report) return 'SD logging unknown · awaiting report';
  const age = report.measuredAt ? (now - Date.parse(report.measuredAt)) / 1000 : null;
  let storage = 'capacity unknown';
  if (report.usedBytes !== null && report.totalBytes !== null && BigInt(report.totalBytes) > 0n) {
    const used = BigInt(report.usedBytes), total = BigInt(report.totalBytes);
    const pct = used > 0n && used*1000n < total ? '<0.1' : (Number(used)/Number(total)*100).toFixed(1);
    storage = `${pct}% used (${size(used)} of ${size(total)})`;
  }
  const status = report.flags & 4 ? 'Logging' : report.flags & 2 ? 'Write failed' :
    report.flags & 1 ? 'Mount failed' : 'Card unavailable';
  const receiptAge = (now - Date.parse(report.receivedAt)) / 1000;
  const freshness = age === null ? `source time unknown · received ${ageLabel(receiptAge)} ago` : `reported ${ageLabel(age)} ago`;
  const lastKnown = !online || age === null || age < 0 || age >= report.intervalSeconds * 3;
  return `${lastKnown ? 'Last known · ' : ''}${status} · ${storage} · ${report.dropped} dropped this boot · ${freshness}`;
}
