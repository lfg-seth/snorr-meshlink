export type ActivitySnapshot = {
  at: string; now: number; status: string; nodes: unknown[];
  packets?: {id: string; radio: string; stream: string; received: number}[];
};
export function mountActivity(root: ShadowRoot): {
  render(data: ActivitySnapshot): void;
  disconnected(): void;
  destroy(): void;
};
