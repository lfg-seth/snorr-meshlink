"""Read-only assertions shared by installed backup recovery verifiers."""
from contextlib import closing
from datetime import datetime, timedelta, timezone
import math
from pathlib import Path
import sqlite3

HISTORY_LIMIT = 50000
UTC = timezone.utc
EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


def device_ids(database):
    with closing(sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True)) as db:
        rows = db.execute('SELECT key, kind FROM devices').fetchall()
    return {'trackers': {key for key, kind in rows if kind == 'member'},
            'infrastructure': {key for key, kind in rows if kind != 'member'}}


def assert_device_ids(snapshot, expected):
    for group in ('trackers', 'infrastructure'):
        actual = [device['id'] for device in snapshot[group]]
        assert len(actual) == len(set(actual)), f'Duplicate {group} identities'
        assert set(actual) == expected[group], f'{group} identities differ from provisioned database'


def instant(value):
    at = datetime.fromisoformat(value.replace('Z', '+00:00'))
    assert at.tzinfo is not None, 'History clock must include timezone'
    return at.astimezone(UTC)


def stamp(at):
    return at.isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def assert_history_shape(history):
    samples = history['samples']
    assert isinstance(samples, list) and 0 < len(samples) <= HISTORY_LIMIT, 'Missing or oversized battery history'
    assert type(history['truncated']) is bool, 'Invalid history truncation flag'
    assert not history['truncated'] or len(samples) == HISTORY_LIMIT, 'Truncated history must fill the cap'
    clocks = [instant(s['at']) for s in samples]
    assert clocks == sorted(clocks), 'Battery history is not chronological'
    assert all(isinstance(s['volts'], (int, float)) and not isinstance(s['volts'], bool)
               and math.isfinite(s['volts']) and s['volts'] > 0 for s in samples), 'Invalid saved battery voltage'
    return samples


def assert_saved_history(history, database, device_id, hours, started, finished):
    """Compare exact newest saved rows and flag at a possible API request time.

    The API computes its window internally. A row can enter/leave the window
    while the request runs; check only the finite instants where that window
    changes, rather than guessing its server timestamp or accepting a tolerance.
    The restored database is immutable, so each candidate is an exact comparison.
    """
    samples = assert_history_shape(history)
    modern = any('measuredAt' in sample for sample in samples)
    keys = ('at', 'volts', 'measuredAt', 'receivedAt', 'timestampQuality') if modern else ('at', 'volts')
    actual = [{key: sample[key] for key in keys} for sample in samples]
    clock = "COALESCE(NULLIF(measuredAt, ''), receivedAt)" if modern else 'measuredAt'
    duration = timedelta(hours=hours)
    # API clocks have millisecond precision; keep the entire request interval.
    started = EPOCH + timedelta(milliseconds=(started - EPOCH) // timedelta(milliseconds=1))
    finished = EPOCH + timedelta(milliseconds=(finished - EPOCH) // timedelta(milliseconds=1))
    assert started <= finished
    base = "deviceId = ? AND json_extract(payload, '$.battery') > 0"
    changes = database.execute(
        f'SELECT {clock} FROM observations WHERE {base} AND '
        f'(({clock} >= ? AND {clock} <= ?) OR ({clock} >= ? AND {clock} <= ?))',
        (device_id, stamp(started), stamp(finished), stamp(started-duration), stamp(finished-duration)))
    candidates = {started, finished}
    for (value,) in changes:
        at = instant(value)
        for transition in (at, at + duration + timedelta(milliseconds=1)):
            if started <= transition <= finished:
                candidates.add(transition)
    for end in sorted(candidates):
        params = (device_id, stamp(end-duration), stamp(end))
        where = f'{base} AND {clock} >= ? AND {clock} <= ?'
        total = database.execute(f'SELECT COUNT(*) FROM observations WHERE {where}', params).fetchone()[0]
        # Mirror the stable merge of measured and receipt-fallback rows, including
        # equal-time ties, without loading the full database history into memory.
        rows = database.execute(
            f"SELECT {clock}, json_extract(payload, '$.battery'), measuredAt, receivedAt, timestampQuality "
            f'FROM observations WHERE {where} ORDER BY {clock} DESC, receivedAt DESC, '
            "CASE WHEN COALESCE(measuredAt, '') != '' THEN 0 ELSE 1 END, id DESC LIMIT ?",
            (*params, HISTORY_LIMIT)).fetchall()
        expected = [dict(zip(keys, row if modern else row[:2])) for row in reversed(rows)]
        if modern:
            for row in expected:
                row['measuredAt'] = row['measuredAt'] or None
        if total and actual == expected and history['truncated'] is (total > HISTORY_LIMIT):
            return total
    raise AssertionError(f'Battery history differs from exact saved {hours}-hour window/cap/truncation')
