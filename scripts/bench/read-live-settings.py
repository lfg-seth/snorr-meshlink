"""Read existing radio settings privately; never write radio configuration."""
import argparse
import base64
import contextlib
import json
import logging
import os
from pathlib import Path
import time

from meshtastic.serial_interface import SerialInterface


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ports', nargs='+')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    logging.disable(logging.CRITICAL)
    rows = []
    # Library output may include private configuration; keep it out of terminal logs.
    with open(os.devnull, 'w') as log:
        for port in args.ports:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                interface = SerialInterface(devPath=port, noProto=False)
                try:
                    node = interface.getMyNodeInfo()
                    channel = interface.localNode.channels[0].settings
                    mqtt = interface.localNode.moduleConfig.mqtt
                    position = node.get('position', {})
                    rows.append({
                        'port': port, 'nodeId': node['user']['id'],
                        'shortName': node['user']['shortName'],
                        'hardwareId': interface.myInfo.device_id.hex(),
                        'channel': channel.name,
                        'channelKey': base64.b64encode(channel.psk).decode(),
                        'mqttUsername': mqtt.username, 'mqttPassword': mqtt.password,
                        'mqttEnabled': mqtt.enabled, 'tlsEnabled': mqtt.tls_enabled,
                        'endpointMatches': mqtt.address == 'mqtt.snorr.org:8883',
                        'rootMatches': mqtt.root == 'snorr/pilot',
                        'wifiEnabled': interface.localNode.localConfig.network.wifi_enabled,
                        'positionBroadcastSeconds': interface.localNode.localConfig.position.position_broadcast_secs,
                        'smartBroadcastEnabled': interface.localNode.localConfig.position.position_broadcast_smart_enabled,
                        'gpsUpdateSeconds': interface.localNode.localConfig.position.gps_update_interval,
                        'gpsAgeSeconds': round(time.time() - position['timestamp'], 1) if position.get('timestamp') else None,
                        'satellites': position.get('satsInView'),
                    })
                finally:
                    interface.close()
    args.output.write_text(json.dumps(rows))
    for row in rows:
        print(row['port'], row['nodeId'], row['shortName'], 'identity/settings saved privately')
        print({key: row[key] for key in ('mqttEnabled', 'tlsEnabled', 'endpointMatches',
               'rootMatches', 'wifiEnabled', 'gpsAgeSeconds', 'satellites',
               'positionBroadcastSeconds', 'smartBroadcastEnabled', 'gpsUpdateSeconds')})


if __name__ == '__main__':
    main()
