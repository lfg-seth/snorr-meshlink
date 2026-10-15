"""Apply owner-supplied Wi-Fi only; privately preserve and verify radio/MQTT state."""
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
    parser.add_argument('--wifi', type=Path, required=True)
    parser.add_argument('--private-dir', type=Path, required=True)
    parser.add_argument('ports', nargs='+')
    args = parser.parse_args()
    wifi = json.loads(args.wifi.read_text())
    args.private_dir.mkdir(parents=True, exist_ok=True)
    logging.disable(logging.CRITICAL)
    with open(os.devnull, 'w') as log:
        for port in args.ports:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                interface = SerialInterface(devPath=port)
                try:
                    node_id = interface.getMyNodeInfo()['user']['id']
                    if node_id not in ('!9ea13cc0', '!849ad7a0'):
                        raise RuntimeError('Port is not a verified bench gateway.')
                    node = interface.localNode
                    mqtt_before = node.moduleConfig.mqtt.SerializeToString()
                    lora_before = node.localConfig.lora.SerializeToString()
                    if node.localConfig.lora.tx_enabled:
                        raise RuntimeError('Expected receive-only gateway.')
                    backup = args.private_dir / f'{node_id[1:]}-before-wifi.json'
                    if not backup.exists():
                        backup.write_text(json.dumps({
                            'localConfig': base64.b64encode(node.localConfig.SerializeToString()).decode(),
                            'moduleConfig': base64.b64encode(node.moduleConfig.SerializeToString()).decode()}))
                    node.localConfig.network.wifi_ssid = wifi['ssid']
                    node.localConfig.network.wifi_psk = wifi['password']
                    node.localConfig.network.wifi_enabled = True
                    node.writeConfig('network')
                    time.sleep(4)
                finally:
                    interface.close()
                time.sleep(12)
                verify = SerialInterface(devPath=port)
                try:
                    node = verify.localNode
                    if verify.getMyNodeInfo()['user']['id'] != node_id:
                        raise RuntimeError('Device identity changed during verification.')
                    network = node.localConfig.network
                    if not (network.wifi_enabled and network.wifi_ssid == wifi['ssid']
                            and network.wifi_psk == wifi['password']):
                        raise RuntimeError('Saved Wi-Fi does not match.')
                    if node.moduleConfig.mqtt.SerializeToString() != mqtt_before:
                        raise RuntimeError('MQTT configuration changed unexpectedly.')
                    if node.localConfig.lora.SerializeToString() != lora_before:
                        raise RuntimeError('LoRa configuration changed unexpectedly.')
                finally:
                    verify.close()
            print(port, node_id, 'saved Wi-Fi verified; MQTT/LoRa configuration preserved', flush=True)


if __name__ == '__main__':
    main()
