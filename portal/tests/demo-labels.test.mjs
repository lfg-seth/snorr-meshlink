import assert from 'node:assert/strict';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { trackerMapLabel } from '../src/tracker.ts';

test('database demo preserves assigned member map shortnames', () => {
  const database = new DatabaseSync(fileURLToPath(new URL('../../backend/demo/data.db', import.meta.url)), { readOnly: true });
  try {
    const members = database.prepare('SELECT key AS id, name, initials, shortName FROM members').all();
    const assignments = database.prepare('SELECT deviceId, memberId, endedAt FROM assignments').all();
    const trackers = database.prepare("SELECT key AS id, shortName FROM devices WHERE kind = 'member' ORDER BY number").all();
    assert.deepEqual(trackers.map(tracker => trackerMapLabel(tracker, assignments, members)),
      ['AVERY', 'JORD', 'MORG', 'RILEY', 'S005', 'S006']);
  } finally {
    database.close();
  }
});
