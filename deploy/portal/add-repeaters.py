"""Add the three owner-authorized planned repeaters after backup and isolated checks."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile

LIVE = Path('/opt/meshlink')
STATE = Path('/var/lib/meshlink/pb_data')
BINARY = '/var/lib/meshlink/bin/pocketbase'


def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def check_migration(source, settings):
    with tempfile.TemporaryDirectory(prefix='meshlink-repeaters-') as directory:
        root = Path(directory)
        data, migrations = root / 'data', root / 'migrations'
        data.mkdir()
        migrations.mkdir()
        with sqlite3.connect(f'file:{STATE / "data.db"}?mode=ro', uri=True) as live:
            with sqlite3.connect(data / 'data.db') as isolated:
                live.backup(isolated)
        def snapshot():
            with sqlite3.connect(data / 'data.db') as db:
                return db.execute('SELECT * FROM devices ORDER BY id').fetchall()
        before = snapshot()
        shutil.copyfile(source / 'deploy/portal/add-repeaters.js', migrations / '1792038000_add_repeaters.js')
        plan = json.loads(settings.read_text())
        invalid = json.loads(settings.read_text())
        invalid['devices'][-1]['kind'] = 'member'
        bad = root / 'invalid.json'
        bad.write_text(json.dumps(invalid))
        command = [BINARY, f'--dir={data}', f'--migrationsDir={migrations}',
                   f'--hooksDir={source / "backend/pb_hooks"}', '--automigrate=false', 'migrate', 'up']
        failed = subprocess.run(command, env={**os.environ, 'MESHLINK_REPEATER_CONFIG': str(bad)},
                                capture_output=True)
        assert failed.returncode != 0 and snapshot() == before, 'Migration rollback failed'
        run(*command, env={**os.environ, 'MESHLINK_REPEATER_CONFIG': str(settings)}, stdout=subprocess.DEVNULL)
        after = snapshot()
        assert all(row in after for row in before), 'Existing device changed'
        with sqlite3.connect(data / 'data.db') as db:
            added = {key: json.loads(config) for key, config in db.execute(
                "SELECT key,configuration FROM devices WHERE key IN ('r001','r002','r003')")}
        assert set(added) == {'r001', 'r002', 'r003'}
        for device in plan['devices']:
            assert added[device['key']] == device['configuration']
    print('Isolated provisioning, rollback and existing-device preservation: PASS', flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--settings', type=Path, required=True)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit('Run as root on the authorized portal host.')
    check_migration(args.source, args.settings)
    if args.check_only:
        return
    assert '<meta name="meshlink-portal-mode" content="live">' in (args.source / 'portal/dist/index.html').read_text(), 'Refusing to deploy a frontend without verified live mode'
    run('python3', str(LIVE / 'deploy/portal/backup.py'))
    run('python3', str(args.source / 'deploy/portal/verify.py'))
    input_path = Path('/etc/meshlink/repeaters.json')
    previous_input = input_path.read_bytes() if input_path.exists() else None
    mqtt_path = Path('/etc/meshlink/mqtt.json')
    previous_mqtt = mqtt_path.read_bytes()
    mqtt_stat = mqtt_path.stat()
    plan = json.loads(args.settings.read_text())
    config = json.loads(previous_mqtt)
    mappings = {d['configuration']['radioNodeId']: d['key'] for d in plan['devices']}
    assert not set(mappings) & (set(config['members']) | set(config['gateways']))
    config['infrastructure'] = {**config.get('infrastructure', {}), **mappings}
    for d in plan['devices']:
        c = d['configuration']
        config['identities'][d['key']] = {'nodeId': c['radioNodeId'], 'hardwareId': c['hardwareId'], 'shortName': d['shortName']}
    run('systemctl', 'stop', 'meshlink-worker', 'meshlink-api')
    migrated = False
    try:
        for folder in ('backend', 'portal/src'):
            shutil.copytree(args.source / folder, LIVE / folder, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__'))
        for filename in ('add-repeaters.js', 'add-repeaters.py', 'verify.py'):
            shutil.copyfile(args.source / 'deploy/portal' / filename, LIVE / 'deploy/portal' / filename)
        input_path.write_text(json.dumps(plan, indent=2))
        input_path.chmod(0o600)
        migrations = Path('/etc/meshlink/repeater-migrations')
        migrations.mkdir(mode=0o700, exist_ok=True)
        shutil.copyfile(LIVE / 'deploy/portal/add-repeaters.js', migrations / '1792038000_add_repeaters.js')
        run(BINARY, f'--dir={STATE}', f'--migrationsDir={migrations}',
            f'--hooksDir={LIVE / "backend/pb_hooks"}', '--automigrate=false', 'migrate', 'up')
        migrated = True
        pending = mqtt_path.with_suffix('.pending')
        pending.write_text(json.dumps(config, indent=2))
        pending.chmod(mqtt_stat.st_mode & 0o777)
        os.chown(pending, mqtt_stat.st_uid, mqtt_stat.st_gid)
        os.replace(pending, mqtt_path)
        shutil.copytree(args.source / 'portal/dist', '/var/www/meshlink', dirs_exist_ok=True)
    except Exception:
        if not migrated:
            if previous_input is None:
                input_path.unlink(missing_ok=True)
            else:
                input_path.write_bytes(previous_input)
        raise
    finally:
        run('chown', '-R', 'meshlink:meshlink', str(STATE))
        run('systemctl', 'start', 'meshlink-api', 'meshlink-worker')
    print('Three repeaters provisioned; live infrastructure telemetry enabled.', flush=True)


if __name__ == '__main__':
    main()
