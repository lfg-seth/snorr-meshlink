import type {
  Assignment,
  AuditEvent,
  BatteryRule,
  Incident,
  Infrastructure,
  Member,
  Message,
  NameJob,
  Tracker,
} from './demo';
import type { LinkObservation } from './NeighborTable';
export type BackendAccount = {
  id: string;
  name: string;
  role: 'admin' | 'member';
  memberId: string;
};
export type BackendState = {
  account: BackendAccount;
  simulation: boolean;
  feedOnline: boolean;
  channel?: { connected: boolean; ready: boolean; until: number; author: string } | null;
  trackers: Tracker[];
  members: Member[];
  assignments: Assignment[];
  nameJobs: NameJob[];
  messages: Message[];
  infrastructure: Infrastructure[];
  fieldRoster?: import('./placed-fleet').FieldPlacement[];
  links: LinkObservation[];
  currentLinks?: LinkObservation[];
  incidents: Incident[];
  warnings: {
    id: string;
    deviceId: string;
    kind: string;
    recoveredAt: string | null;
    acknowledgedAt: string | null;
  }[];
  rules: Record<string, BatteryRule>;
  events: AuditEvent[];
};
export type BackendSession = { token: string; account: BackendAccount; demo?: boolean };
export const sessionKey = 'meshlink-session-token';
function tokenStorage(remember: boolean): Storage | undefined {
  try { return remember ? window.localStorage : window.sessionStorage; }
  catch { return undefined; }
}
function readToken(remember: boolean): string {
  try { return tokenStorage(remember)?.getItem(sessionKey) ?? ''; }
  catch { return ''; }
}
export function savedToken(): string {
  return readToken(false) || readToken(true);
}
function removeToken(remember: boolean): void {
  try { tokenStorage(remember)?.removeItem(sessionKey); }
  catch { /* Storage can be blocked. */ }
}
export function forgetToken(token: string): void {
  for (const remember of [false, true]) {
    if (token && token === readToken(remember)) removeToken(remember);
  }
}
export function saveToken(token: string, remember: boolean): void {
  removeToken(!remember);
  try {
    const storage = tokenStorage(remember);
    if (storage) { storage.setItem(sessionKey, token); return; }
  } catch { /* Try tab storage if durable storage is full or blocked. */ }
  removeToken(remember);
  if (remember) {
    try { tokenStorage(false)?.setItem(sessionKey, token); }
    catch { /* The current page can still use the in-memory session. */ }
  }
}
export class BackendError extends Error {
  constructor(message: string, public status: number) { super(message); }
}
const origin = (import.meta.env.VITE_BACKEND_URL ?? '').replace(/\/$/, '');
const demoOrigin = (import.meta.env.VITE_DEMO_BACKEND_URL ?? '/demo-api').replace(/\/$/, '');
export async function request<T>(
  path: string,
  token = '',
  body?: object,
  signal?: AbortSignal,
  demo = false,
): Promise<T> {
  const response = await fetch(`${demo ? demoOrigin : origin}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: token } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
    signal,
    cache: 'no-store',
  });
  const data = await response.json();
  if (!response.ok)
    throw new BackendError(
      data.message ||
        data.reason ||
        `Backend request failed (${response.status})`,
      response.status,
    );
  if (demo && path === '/api/meshlink/state' && data.simulation !== true)
    throw new Error('The demo address must point to a separate simulation database.');
  return data as T;
}
export async function login(
  username: string,
  password: string,
  demo = false,
  rememberDevice = false,
): Promise<BackendSession> {
  const result = await request<{ token: string; record: BackendAccount }>(
    '/api/collections/accounts/auth-with-password',
    '',
    { identity: username, password, ...(!demo && rememberDevice && { rememberDevice: true }) },
    undefined,
    demo,
  );
  if (result.record.role !== 'admin' && result.record.role !== 'member')
    throw new Error('Use a portal account, not a worker account.');
  return { token: result.token, account: result.record, ...(demo ? { demo: true } : {}) };
}
