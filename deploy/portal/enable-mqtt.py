"""Owner-authorized real-device cutover after verified backup and live preflight."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/opt/meshlink')


def run(*args):
    subprocess.run(args, check=True)


def main():
    if os.geteuid() != 0:
        raise SystemExit('Run as root on the MeshLink LXC.')
    config = Path('/etc/meshlink/mqtt.json')
    if not config.is_file() or config.stat().st_mode & 0o007:
        raise SystemExit('Private MQTT configuration required before cutover.')
    # Validate TLS/auth and real decoding before any hosted data/service changes.
    preflight = ['/opt/meshlink-mqtt-venv/bin/python', str(ROOT / 'backend/mqtt_probe.py'),
                 '--config', str(config), '--seconds', '300']
    run(*preflight)
    run(sys.executable, str(ROOT / 'deploy/portal/backup.py'))
    run(sys.executable, str(ROOT / 'deploy/portal/verify.py'))
    run('systemctl', 'stop', 'meshlink-worker', 'meshlink-api')
    # Any migration failure leaves the original database intact; restore normal
    # service operation. Later failures retain the backup and require inspection.
    migrated, live_ready = False, False
    try:
        stage = Path('/etc/meshlink/cutover-migrations')
        stage.mkdir(mode=0o700, exist_ok=True)
        shutil.copyfile(ROOT / 'deploy/portal/live-cutover.js', stage / '1792010000_live_cutover.js')
        run('/var/lib/meshlink/bin/pocketbase', '--dir=/var/lib/meshlink/pb_data',
            f'--migrationsDir={stage}', '--hooksDir=/opt/meshlink/backend/pb_hooks',
            '--automigrate=false', 'migrate', 'up')
        migrated = True
        # Override simulation explicitly; keep every existing API sandbox setting.
        override = Path('/etc/systemd/system/meshlink-api.service.d')
        override.mkdir(exist_ok=True)
        (override / 'live.conf').write_text('[Service]\nEnvironment=MESHLINK_SIMULATION=0\n')
        shutil.copyfile(ROOT / 'deploy/portal/meshlink-mqtt-worker.service',
                        '/etc/systemd/system/meshlink-worker.service')
        shutil.copyfile(ROOT / 'deploy/portal/backup.py', '/usr/local/sbin/meshlink-backup')
        Path('/usr/local/sbin/meshlink-backup').chmod(0o755)
        run('systemctl', 'daemon-reload')
        live_ready = True
    finally:
        run('chown', '-R', 'meshlink:meshlink', '/var/lib/meshlink/pb_data')
        run('systemctl', 'start', 'meshlink-api')
        if not migrated or live_ready:
            run('systemctl', 'start', 'meshlink-worker')
    print('Live GPS worker enabled; verify actual portal observations next.')


if __name__ == '__main__':
    main()
