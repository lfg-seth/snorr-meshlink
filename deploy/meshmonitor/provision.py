#!/usr/bin/env python3
"""Fresh loopback-only install provisioning; reads/writes secrets locally."""

import base64
from http.cookiejar import CookieJar
import json
import os
from pathlib import Path
import secrets
import urllib.error
import urllib.request

os.umask(0o077)
environment = dict(line.split('=', 1) for line in Path('/etc/meshmonitor/meshmonitor.env').read_text().splitlines() if '=' in line)
base = 'http://' + environment.get('MESHLINK_BIND_ADDRESS', '127.0.0.1') + ':3001'


class Client:
    def __init__(self, username, password):
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
        self.csrf = self.call('GET', '/api/csrf-token')['csrfToken']
        self.call('POST', '/api/auth/login', {'username': username, 'password': password})

    def call(self, method, path, data=None):
        headers = {'Content-Type': 'application/json'}
        if hasattr(self, 'csrf'):
            headers['X-CSRF-Token'] = self.csrf
        request = urllib.request.Request(base + path, method=method, headers=headers,
                                        data=None if data is None else json.dumps(data).encode())
        try:
            with self.opener.open(request, timeout=45) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            # Never include submitted credentials/channel keys or response bodies.
            raise RuntimeError(f'{method} {path}: HTTP {error.code}') from None


login_file = Path('/etc/meshmonitor/admin-login.json')
if not login_file.exists():
    client = Client('admin', 'changeme')
    admin = {'username': 'admin', 'password': secrets.token_urlsafe(30)}
    login_file.write_text(json.dumps(admin) + '\n')
    client.call('POST', '/api/auth/change-password',
                {'currentPassword': 'changeme', 'newPassword': admin['password']})
else:
    admin = json.loads(login_file.read_text())
client = Client(**admin)

mqtt = json.loads(Path('/root/meshmonitor-install/mqtt-input.json').read_text())
channel_response = client.call('GET', '/api/channel-database')
channels = channel_response if isinstance(channel_response, list) else channel_response.get('channels', channel_response.get('data', []))
if not any(channel['name'] == mqtt['channel'] for channel in channels):
    client.call('POST', '/api/channel-database', {
        'name': mqtt['channel'], 'psk': mqtt['channelKey'],
        'pskLength': len(base64.b64decode(mqtt['channelKey'])),
        'description': 'Private SNORR pilot channel; read-only monitoring',
        'isEnabled': True, 'enforceNameValidation': True,
    })

source_response = client.call('GET', '/api/sources')
sources = source_response if isinstance(source_response, list) else source_response.get('sources', source_response.get('data', []))
source = next((source for source in sources if source['name'] == 'SNORR Pilot MQTT'), None)
if source is None:
    response = client.call('POST', '/api/sources', {
        'name': 'SNORR Pilot MQTT', 'type': 'mqtt_bridge', 'enabled': True,
        'config': {
            'mode': 'subscribe_only',
            'upstream': {'url': f"mqtts://{mqtt['host']}:{mqtt['port']}",
                         'username': mqtt['username'], 'password': mqtt['password']},
            'subscriptions': [mqtt['root'].rstrip('/') + '/2/e/' + mqtt['channel'] + '/#'],
        },
    })
    source = response.get('source', response.get('data', response))
source_id = source['id']
client.call('POST', '/api/settings', {'mqtt_packet_log_enabled': '1'})
metrics_login = Path('/etc/meshmonitor/metrics-login.json')
if not metrics_login.exists():
    account = {'username': 'prometheus', 'password': secrets.token_urlsafe(30)}
    metrics_login.write_text(json.dumps(account) + '\n')
else:
    account = json.loads(metrics_login.read_text())
users_response = client.call('GET', '/api/users')
users = users_response if isinstance(users_response, list) else users_response.get('users', [])
anonymous = next((user for user in users if user['username'] == 'anonymous'), None)
if anonymous and anonymous.get('isActive'):
    client.call('PUT', f"/api/users/{anonymous['id']}", {'isActive': False})
user = next((user for user in users if user['username'] == account['username']), None)
if user is None:
    user = client.call('POST', '/api/users', {
        **account, 'displayName': 'Prometheus read-only metrics', 'isAdmin': False,
    })['user']
# Replace all per-source grants with only read rights needed for the metric endpoint.
client.call('PUT', f"/api/users/{user['id']}/permissions", {
    'sourceId': source_id,
    'permissions': {
        **{resource: {'read': True, 'write': False, 'delete': False}
           for resource in ['nodes', 'messages', 'packetmonitor']},
        # Upstream MQTT telemetry-only rows can have NULL channel, treated as slot 0.
        # This source is already restricted to the single private project topic.
        'channel_0': {'read': True, 'viewOnMap': True, 'write': False, 'delete': False},
    },
})
# MQTT nodes use virtual channel IDs backed by this separate channel ACL.
# Map visibility permits per-node metrics; key/configuration write access is absent.
channel_response = client.call('GET', '/api/channel-database')
channels = channel_response if isinstance(channel_response, list) else channel_response.get('channels', channel_response.get('data', []))
private_channel = next(channel for channel in channels if channel['name'] == mqtt['channel'])
client.call('PUT', f"/api/channel-database/{private_channel['id']}/permissions/{user['id']}",
            {'canViewOnMap': True, 'canRead': False})
metric_client = Client(**account)
token_file = Path('/etc/meshmonitor/metrics-token')
if not token_file.exists():
    token_file.write_text(metric_client.call('POST', '/api/token/generate', {})['token'] + '\n')
Path('/etc/meshmonitor/source-id').write_text(source_id + '\n')
assert client.call('GET', '/api/auth/check-default-password')['isDefaultPassword'] is False
print('Default admin password disabled; private channel and subscribe-only TLS source provisioned.')
print('Separate non-admin metrics account/token provisioned; packet monitor enabled.')
