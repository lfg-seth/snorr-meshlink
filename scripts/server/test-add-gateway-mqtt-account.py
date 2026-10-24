#!/usr/bin/env python3
"""Check real isolated-broker account creation, preservation and rollback."""

import importlib.util
import json
import os
from pathlib import Path
import secrets
import select
import signal
import socket
import subprocess
import tempfile
import time

spec = importlib.util.spec_from_file_location(
    "account", Path(__file__).with_name("add-gateway-mqtt-account.py")
)
account = importlib.util.module_from_spec(spec)
spec.loader.exec_module(account)
helper_spec = importlib.util.spec_from_file_location(
    "mqtt_helpers", Path(__file__).with_name("reset-mqtt-pilot.py")
)
helpers = importlib.util.module_from_spec(helper_spec)
helper_spec.loader.exec_module(helpers)


def main():
    assert account.listener_address("listener 1883 127.0.0.1\nlistener 1883 192.168.12.51\n") == (
        "127.0.0.1",
        1883,
    )
    assert account.listener_address("  listener 1883 # local default\n") == ("127.0.0.1", 1883)
    assert account.listener_address("listener 1883 192.168.12.51\n") == ("192.168.12.51", 1883)
    assert os.geteuid() != 0, "Use an unprivileged account for isolated checks"
    with tempfile.TemporaryDirectory(prefix="g003-account-") as directory:
        root = Path(directory)
        credentials, passwords, acl = (
            root / name for name in ("credentials.json", "passwd", "acl")
        )
        existing = {
            name: secrets.token_urlsafe(22)
            for name in ("pilot-worker", "pilot-v3-uplink-1", "pilot-v3-uplink-2")
        }
        credentials.write_text(
            json.dumps(
                dict(
                    host="mqtt.snorr.org",
                    port=8883,
                    root="snorr/pilot",
                    tls=True,
                    accounts=existing,
                )
            )
        )
        passwords.write_text("".join(f"{k}:{v}\n" for k, v in existing.items()))
        subprocess.run(["mosquitto_passwd", "-U", str(passwords)], check=True, capture_output=True)
        acl.write_text("user pilot-worker\ntopic read snorr/pilot/2/e/#\n")
        originals = {p: p.read_bytes() for p in (credentials, passwords, acl)}
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            port = reservation.getsockname()[1]
        config = root / "broker.conf"
        config.write_text(
            f"listener {port} 127.0.0.1\nallow_anonymous false\npassword_file {passwords}\nacl_file {acl}\npersistence false\n"
        )
        with (root / "broker.log").open("w") as log:
            broker = subprocess.Popen(["mosquitto", "-c", str(config)], stdout=log, stderr=log)
            try:

                def verify(username, password):
                    account.authenticate("127.0.0.1", port, username, password)

                def reload():
                    broker.send_signal(signal.SIGHUP)
                    time.sleep(0.3)

                for attempt in range(40):
                    try:
                        verify("pilot-worker", existing["pilot-worker"])
                        break
                    except (OSError, RuntimeError):
                        time.sleep(0.1)
                else:
                    raise RuntimeError("Isolated broker did not become ready")
                settings = dict(
                    username="pilot-v3-uplink-3",
                    password=secrets.token_urlsafe(22),
                    nodeId="!9e9f167c",
                    channel="testbench",
                )

                def fail(*args):
                    raise RuntimeError("Injected verification failure")

                try:
                    account.install(
                        settings, credentials, passwords, acl, root / "backups", reload, fail
                    )
                except RuntimeError as error:
                    assert str(error) == "Injected verification failure"
                else:
                    raise AssertionError("Failure injection unexpectedly succeeded")
                assert all(p.read_bytes() == data for p, data in originals.items())
                result = account.install(
                    settings, credentials, passwords, acl, root / "backups", reload, verify
                )
                assert result["created"] and result["verified"]
                updated = json.loads(credentials.read_text())["accounts"]
                assert {k: updated[k] for k in existing} == existing
                assert passwords.read_bytes().startswith(originals[passwords])
                assert (
                    acl.read_bytes()
                    == originals[acl]
                    + b"\nuser pilot-v3-uplink-3\ntopic write snorr/pilot/2/e/testbench/!9e9f167c\n"
                )
                helpers.BACKEND_ADDRESS, helpers.BACKEND_PORT = "127.0.0.1", port
                connection, code = helpers.connect(settings["username"], settings["password"])
                assert code == 0
                with connection:
                    topic = "snorr/pilot/2/e/testbench/!9e9f167c"
                    connection.sendall(
                        helpers.packet(0x82, b"\x00\x01\x00" + helpers.field(topic) + b"\x00")
                    )
                    kind, body = helpers.receive(connection)
                    assert kind == 0x90
                    connection.sendall(
                        helpers.packet(
                            0x32, helpers.field(topic) + b"\x00\x02\x00synthetic-acl-check"
                        )
                    )
                    kind, body = helpers.receive(connection)
                    assert kind == 0x40 and (len(body) == 2 or body[2] in (0, 0x10))
                    assert not select.select([connection], [], [], 0.2)[
                        0
                    ], "Write-only account received a publication"
                    for denied in (
                        "snorr/pilot/2/e/testbench/!849ad7a0",
                        "snorr/pilot/2/json/test",
                        "unrelated/test",
                    ):
                        connection.sendall(
                            helpers.packet(
                                0x32, helpers.field(denied) + b"\x00\x03\x00synthetic-denied"
                            )
                        )
                        kind, body = helpers.receive(connection)
                        assert kind == 0x40 and len(body) >= 3 and body[2] == 0x87
                for username, password in existing.items():
                    verify(username, password)
                unchanged = {p: p.read_bytes() for p in originals}
                assert not account.install(
                    settings, credentials, passwords, acl, root / "backups", reload, verify
                )["created"]
                assert all(p.read_bytes() == data for p, data in unchanged.items())
                conflict = {**settings, "password": secrets.token_urlsafe(22)}
                try:
                    account.install(
                        conflict, credentials, passwords, acl, root / "backups", reload, verify
                    )
                except RuntimeError:
                    pass
                else:
                    raise AssertionError("Existing account rotation was allowed")
                assert all(p.read_bytes() == data for p, data in unchanged.items())
                print(
                    "PASS: listener parsing, real broker auth, own-topic-only writes/no reads, existing-account preservation, rollback, idempotence and conflicting-rotation refusal"
                )
            finally:
                broker.terminate()
                broker.wait(timeout=10)


if __name__ == "__main__":
    main()
