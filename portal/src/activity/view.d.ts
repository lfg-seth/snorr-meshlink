export type ActivityRoute = {
  reception: "local" | "direct" | "relayed" | "unknown";
  reportedHops?: number; lastRelayCandidate?: string; lastRelayRadio?: string;
};
export type ActivitySnapshot = {
  at: string; now: number; status: string; nodes: unknown[];
  packets?: {
    id: string; radio: string; stream: string; received: number;
    heardThrough?: string; heardThroughRadio?: string; route?: ActivityRoute | null;
  }[];
};
export function mountActivity(root: ShadowRoot): {
  render(data: ActivitySnapshot): void;
  disconnected(): void;
  destroy(): void;
};
