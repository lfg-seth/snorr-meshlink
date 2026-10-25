#!/usr/bin/env python3
"""Change only one inventoried RAK's role over USB; preserve its full profile."""

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import logging
import os
from pathlib import Path
import sys
import time
import traceback

SPEC = importlib.util.spec_from_file_location(
    "repeater_updater", Path(__file__).with_name("update-repeater.py"))
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


def change_role(interface, port, profile, role, apply, evidence):
    """Validate and back up before the sole configuration write."""
    before = updater.snapshot(interface, port, profile["usbSerial"])
    updater.validate_node(interface, before, profile)
    updater.private_json(evidence / "before.json", before)
    device = interface.localNode.localConfig.device
    roles = device.DESCRIPTOR.fields_by_name["role"].enum_type
    previous = roles.values_by_number[device.role].name
    device.role = roles.values_by_name[role].number
    intended = updater.snapshot(interface, port, profile["usbSerial"])
    updater.private_json(evidence / "intended.json", intended)
    if not apply or previous == role:
        return previous, intended, False
    # No retry: a lost response can follow an executed/rebooting write.
    interface.localNode.writeConfig("device")
    time.sleep(2)
    return previous, intended, True


def verify(profile, intended, evidence, name):
    interface, port = updater.wait_application(profile)
    try:
        actual = updater.snapshot(interface, port, profile["usbSerial"])
        updater.private_json(evidence / name, actual)
        updater.validate_node(interface, actual, profile)
        updater.assert_preserved(intended, actual)
        if intended["metadata"] != actual["metadata"]:
            raise updater.UpdateError("Firmware metadata changed; inspect private evidence.")
    finally:
        interface.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", help="R001 through R006 (one connected RAK)")
    parser.add_argument("--role", choices=("ROUTER", "CLIENT"), default="ROUTER")
    parser.add_argument("--port", help="Optional port; recorded USB serial must still match")
    parser.add_argument("--apply", action="store_true", help="Save role; default only reads/backups")
    args = parser.parse_args(argv)
    evidence = None
    old_umask = os.umask(0o077)
    try:
        number = updater.normalize_number(args.number)
        profile = json.loads(updater.PROFILE_PATH.read_text())["nodes"][number]
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            raise updater.UpdateError("Install scripts/bench/repeater-requirements.txt in a Python virtual environment.") from None
        port = updater.select_port(comports(), profile, args.port)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        evidence = updater.ROOT / "private" / "bench" / f"{number}-role-{stamp}"
        evidence.mkdir(parents=True, mode=0o700)
        print(f"{number} {profile['nodeId']} on {port.device}; private backup: {evidence}", flush=True)
        logging.disable(logging.CRITICAL)
        with (evidence / "serial.log").open("x", encoding="utf-8") as log, updater.quiet_serial(log):
            interface = updater.connect(port.device)
            try:
                previous, intended, changed = change_role(
                    interface, port.device, profile, args.role, args.apply, evidence)
            finally:
                interface.close()
            if changed:
                time.sleep(15)
                verify(profile, intended, evidence, "verified.json")
                # Explicit reboot proves the role persisted, beyond a live config read.
                interface, _ = updater.wait_application(profile)
                try:
                    interface.localNode.reboot(2)
                    time.sleep(1)
                finally:
                    interface.close()
                time.sleep(12)
                verify(profile, intended, evidence, "reboot-verified.json")
        if changed:
            print(f"{number}: {previous} -> {args.role}; full profile verified through reboot.")
        elif args.apply:
            print(f"{number}: already {args.role}; backed up, no write needed.")
        else:
            print(f"READ ONLY: {number} is {previous}; proposed {args.role}. Repeat with --apply to save.")
        return 0
    except Exception as error:
        if evidence:
            with (evidence / "failure.log").open("w", encoding="utf-8") as log:
                traceback.print_exc(file=log)
        print("Role operation failed. No automatic retry or rollback. Inspect private evidence; read saved role over USB before retrying.", file=sys.stderr)
        if isinstance(error, updater.UpdateError):
            print(str(error), file=sys.stderr)
        if evidence:
            print(f"Private evidence: {evidence}", file=sys.stderr)
        return 1
    finally:
        os.umask(old_umask)


if __name__ == "__main__":
    sys.exit(main())
