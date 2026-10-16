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
  trackers: Tracker[];
  members: Member[];
  assignments: Assignment[];
  nameJobs: NameJob[];
  messages: Message[];
  infrastructure: Infrastructure[];
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
export type BackendSession = { token: string; account: BackendAccount };
const sessionKey = 'meshlink-session-token';
export function savedToken(): string {
  try { return window.sessionStorage.getItem(sessionKey) ?? ''; }
  catch { return ''; }
}
export function saveToken(token: string): void {
  try {
    if (token) window.sessionStorage.setItem(sessionKey, token);
    else window.sessionStorage.removeItem(sessionKey);
  } catch { /* Sign-in still works when browser storage is unavailable. */ }
}
export class BackendError extends Error {
  constructor(message: string, public status: number) { super(message); }
}
const origin = (import.meta.env.VITE_BACKEND_URL ?? '').replace(/\/$/, '');
export async function request<T>(
  path: string,
  token = '',
  body?: object,
  signal?: AbortSignal,
): Promise<T> {
  const response = await fetch(`${origin}${path}`, {
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
  return data as T;
}
export async function login(
  username: string,
  password: string,
): Promise<BackendSession> {
  const result = await request<{ token: string; record: BackendAccount }>(
    '/api/collections/accounts/auth-with-password',
    '',
    { identity: username, password },
  );
  if (result.record.role !== 'admin' && result.record.role !== 'member')
    throw new Error('Use a portal account, not a worker account.');
  return { token: result.token, account: result.record };
}
