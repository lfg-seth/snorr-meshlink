#!/usr/bin/env python3
"""Add the authorized scrape without rewriting existing jobs; validate before reload."""

from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import subprocess

path = Path('/etc/prometheus/prometheus.yml')
source = path.read_text()
backup = Path('/root/meshmonitor-integration-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
backup.mkdir(mode=0o700)
shutil.copy2(path, backup / 'prometheus.yml')
job = '''
  # SNORR MeshMonitor: internal, authenticated, read-only metrics.
  - job_name: snorr-meshmonitor
    scrape_interval: 30s
    scrape_timeout: 10s
    metrics_path: /api/v1/metrics
    authorization:
      credentials_file: /etc/prometheus/meshmonitor-secrets/metrics-token
    static_configs:
      - targets: ['meshmonitor.int.spp.lol:3001']
'''
if not re.search(r'job_name:\s*[\x27\x22]?snorr-meshmonitor\b', source):
    lines = source.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if re.match(r'^scrape_configs:\s*(#.*)?$', line.rstrip()))
    end = next((i for i in range(start + 1, len(lines)) if re.match(r'^[A-Za-z_]', lines[i])), len(lines))
    lines.insert(end, job + '\n')
    candidate = path.with_suffix('.meshmonitor-candidate.yml')
    candidate.write_text(''.join(lines))
    try:
        subprocess.run(['/usr/local/bin/promtool', 'check', 'config', str(candidate)], check=True)
        shutil.copymode(path, candidate)
        shutil.chown(candidate, user='root', group='root')
        candidate.replace(path)
    finally:
        candidate.unlink(missing_ok=True)
# Retention is global. This extends the existing default 15d to the owner's 30d.
# Preserve the exact existing start command and all its existing options.
command = subprocess.check_output(['systemctl', 'show', 'prometheus', '-p', 'ExecStart', '--value'], text=True)
match = re.search(r'argv\[\]=(.*?) ;', command)
if not match:
    raise RuntimeError('Cannot determine existing Prometheus start command')
argv = match.group(1)
argv = re.sub(r'\s+--storage\.tsdb\.retention\.time(?:=|\s+)\S+', '', argv)
dropin = Path('/etc/systemd/system/prometheus.service.d/30-snorr-retention.conf')
dropin.parent.mkdir(parents=True, exist_ok=True)
if dropin.exists():
    shutil.copy2(dropin, backup / dropin.name)
dropin.write_text('[Service]\nExecStart=\nExecStart=' + argv + ' --storage.tsdb.retention.time=30d\n')
subprocess.run(['systemctl', 'daemon-reload'], check=True)
subprocess.run(['systemctl', 'restart', 'prometheus'], check=True)
print('Existing jobs preserved; authenticated MeshMonitor scrape added; global retention 30d.')
