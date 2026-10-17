// Exercise the actual patched cleanup method bodies. Any database access fails.
import assert from 'node:assert/strict';
import fs from 'node:fs';

const root = process.argv[2] || '/opt/meshmonitor';
const targets = [
  ['dist/services/database.js', 'async purgeOldTelemetryAsync(hoursToKeep, favoriteDaysToKeep) {'],
  ['dist/services/database.js', 'async cleanupOldPacketLogsAsync() {'],
  ['dist/server/services/mqttPacketLogService.js', 'async runCleanup() {'],
  ['dist/server/services/coverageRetentionService.js', 'async runCleanup() {'],
  ['dist/server/services/meshcorePositionHistoryService.js', 'async runCleanup() {'],
];
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const forbidden = new Proxy({}, { get() { throw new Error('database access attempted'); } });
process.env.MESHLINK_RETAIN_HISTORY = 'true';
for (const [file, anchor] of targets) {
  const source = fs.readFileSync(`${root}/${file}`, 'utf8');
  const start = source.indexOf(anchor) + anchor.length;
  assert(start >= anchor.length);
  const end = source.indexOf('\n    }', start);
  assert(end > start);
  const run = new AsyncFunction('databaseService', 'hoursToKeep', 'favoriteDaysToKeep', source.slice(start, end));
  assert.equal(await run.call(forbidden, forbidden, 1, 1), 0);
  // Without the policy guard, the same real body must reach its dependencies.
  delete process.env.MESHLINK_RETAIN_HISTORY;
  let accessed = false;
  try { await run.call(forbidden, forbidden, 1, 1); } catch { accessed = true; }
  // Some upstream services catch their error and then need the logger dependency.
  assert(accessed);
  process.env.MESHLINK_RETAIN_HISTORY = 'true';
}
console.log('Five actual cleanup methods skip all DB access under the retention policy.');
