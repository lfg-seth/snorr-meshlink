import { ageLabel } from './demo.ts';

export type WifiSignal = {
  state: 'measured'|'disconnected'|'unavailable'; rssiDbm: number|null; channel: number|null;
  measuredAt: string|null; receivedAt: string; intervalSeconds: number;
};

export function wifiSignalLabel(s: WifiSignal|null|undefined, now: number, online: boolean) {
  if (!s) return 'Wi-Fi signal · awaiting report';
  const age = s.measuredAt ? (now - Date.parse(s.measuredAt))/1000 : null;
  const value = s.state === 'measured' ? `${s.rssiDbm} dBm · channel ${s.channel}` :
    s.state === 'disconnected' ? 'disconnected' : 'reading unavailable';
  const old = !online || age === null || age < 0 || age >= s.intervalSeconds*3;
  const when = age === null ? 'source time unknown' : `reported ${ageLabel(age)} ago`;
  return `${old ? 'Last known · ' : ''}Wi-Fi signal · ${value} · ${when}`;
}
