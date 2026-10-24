#!/usr/bin/env python3
"""Add one private gateway uplink account while preserving working accounts."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import stat
import struct
import subprocess
import tempfile


def atomic(path, data, original):
    fd, name = tempfile.mkstemp(prefix=".meshlink-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
            os.fchmod(stream.fileno(), stat.S_IMODE(original.st_mode))
            os.fchown(stream.fileno(), original.st_uid, original.st_gid)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def authenticate(host, port, username, password):
    def string(value):
        data = value.encode()
        return struct.pack("!H", len(data)) + data

    payload = (
        b"\x00\x04MQTT\x04\xc2\x00\x14"
        + string("meshlink-account-check")
        + string(username)
        + string(password)
    )
    length, encoded = len(payload), bytearray()
    while True:
        byte, length = length % 128, length // 128
        encoded.append(byte | (128 if length else 0))
        if not length:
            break
    with socket.create_connection((host, port), timeout=5) as connection:
        connection.sendall(b"\x10" + encoded + payload)
        reply = b""
        while len(reply) < 4:
            part = connection.recv(4 - len(reply))
            if not part:
                break
            reply += part
        if reply != b"\x20\x02\x00\x00":
            raise RuntimeError("Gateway MQTT authentication failed")


def install(settings, credentials, passwords, acl, backup_parent, reload_broker, verify):
    username, password = settings["username"], settings["password"]
    node, channel = settings["nodeId"], settings["channel"]
    if (
        username != "pilot-v3-uplink-3"
        or node != "!9e9f167c"
        or not isinstance(password, str)
        or not 24 <= len(password.encode()) <= 31
        or not channel
        or any(c in channel for c in "/+#\n\r")
        or any(c in password for c in "\n\r:")
    ):
        raise ValueError("Invalid verified G003 account input")
    old = {p: p.read_bytes() for p in (credentials, passwords, acl)}
    state = json.loads(old[credentials])
    if (state["host"], state["port"], state["root"], state["tls"]) != (
        "mqtt.snorr.org",
        8883,
        "snorr/pilot",
        True,
    ):
        raise ValueError("Unexpected broker configuration")
    stanza = f"\nuser {username}\ntopic write snorr/pilot/2/e/{channel}/{node}\n".encode()
    users = state["accounts"]
    if username in users:
        if users[username] != password or stanza not in old[acl]:
            raise RuntimeError("Existing account differs; refusing rotation")
        verify(username, password)
        return {"created": False, "verified": True}
    if (
        any(line.split(b":", 1)[0] == username.encode() for line in old[passwords].splitlines())
        or f"user {username}" in old[acl].decode()
    ):
        raise RuntimeError("Partial or conflicting account exists; inspect before retry")
    backup = backup_parent / (
        "g003-account-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    )
    backup.mkdir(parents=True, mode=0o700)
    for path, data in old.items():
        target = backup / path.name
        target.write_bytes(data)
        target.chmod(0o600)
    hashed = backup / "new-account-hash"
    hashed.write_text(f"{username}:{password}\n")
    hashed.chmod(0o600)
    subprocess.run(["mosquitto_passwd", "-U", str(hashed)], check=True, capture_output=True)
    new_hash = hashed.read_bytes()
    state["accounts"] = {**users, username: password}
    try:
        atomic(passwords, old[passwords].rstrip(b"\n") + b"\n" + new_hash, passwords.stat())
        atomic(acl, old[acl] + stanza, acl.stat())
        atomic(credentials, (json.dumps(state, indent=2) + "\n").encode(), credentials.stat())
        reload_broker()
        verify(username, password)
        assert passwords.read_bytes().startswith(old[passwords].rstrip(b"\n") + b"\n")
        assert acl.read_bytes().startswith(old[acl])
    except BaseException:
        for path, data in old.items():
            atomic(path, data, path.stat())
        reload_broker()
        raise
    return {"created": True, "verified": True, "privateBackup": str(backup)}


def listener_address(configuration):
    candidates = []
    for line in configuration.splitlines():
        parts = line.split("#", 1)[0].split()
        if len(parts) in (2, 3) and parts[0] == "listener" and parts[1] == "1883":
            address = parts[2] if len(parts) == 3 else "127.0.0.1"
            candidates.append(("127.0.0.1" if address in ("0.0.0.0", "::") else address, 1883))
    if ("127.0.0.1", 1883) in candidates:
        return "127.0.0.1", 1883
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError("No unambiguous MQTT authentication listener")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", required=True, type=Path)
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit("Run through sudo on the authorized broker.")
    os.umask(0o077)
    settings = json.loads(args.settings.read_text())
    address, port = listener_address(Path("/etc/mosquitto/conf.d/pilot.conf").read_text())
    result = install(
        settings,
        Path("/root/meshlink-private/mqtt-credentials.json"),
        Path("/etc/mosquitto/passwd"),
        Path("/etc/mosquitto/acl"),
        Path("/root/meshlink-maintenance"),
        lambda: subprocess.run(["systemctl", "reload", "mosquitto"], check=True),
        lambda username, password: authenticate(address, int(port), username, password),
    )
    print(json.dumps({"account": "pilot-v3-uplink-3", "gateway": "G003", **result}))


if __name__ == "__main__":
    main()
