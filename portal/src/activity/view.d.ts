export type ActivitySnapshot = {at: string; now: number; status: string; nodes: unknown[]};
export function mountActivity(root: ShadowRoot): {
  render(data: ActivitySnapshot): void;
  disconnected(): void;
};
