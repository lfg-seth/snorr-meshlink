import { batterySamples } from './battery.ts';
import type { BatterySample } from './battery.ts';

// Monotone cubic interpolation: round the joins without overshooting readings.
// Missing-report intervals start a new subpath rather than inventing recovery.
export function batteryCurve(samples: BatterySample[], now: number, timeoutMinutes: number,
  x: (time: number) => number, y: (volts: number) => number) {
  const points = batterySamples(samples, now);
  const segments: BatterySample[][] = [];
  for (const point of points) {
    const segment = segments.at(-1);
    if (!segment || Date.parse(point.at) - Date.parse(segment.at(-1)!.at) >= timeoutMinutes * 60000)
      segments.push([point]);
    else segment.push(point);
  }
  return segments.filter(segment => segment.length > 1).map(segment => {
    const p = segment.map(s => ({ x: x(Date.parse(s.at)), y: y(s.volts) }));
    const slopes = p.slice(1).map((v, i) => (v.y - p[i].y) / (v.x - p[i].x));
    const tangents = p.map((_, i) => {
      if (!i) return slopes[0];
      if (i === p.length - 1) return slopes.at(-1)!;
      const a = slopes[i - 1], b = slopes[i];
      return a * b <= 0 ? 0 : 2 * a * b / (a + b);
    });
    const n = (value: number) => value.toFixed(2);
    return `M${n(p[0].x)},${n(p[0].y)}` + p.slice(1).map((v, i) => {
      const prev = p[i], third = (v.x - prev.x) / 3;
      return `C${n(prev.x + third)},${n(prev.y + tangents[i] * third)} ${n(v.x - third)},${n(v.y - tangents[i + 1] * third)} ${n(v.x)},${n(v.y)}`;
    }).join('');
  }).join('');
}
