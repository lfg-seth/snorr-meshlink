#!/usr/bin/env python3
"""Guided Windows RAK4631 triage; private backups, no flashing or Bluetooth."""

import argparse
import base64
import contextlib
import copy
from datetime import datetime, timezone
import importlib.util
import json
import logging
import math
import os
from pathlib import Path
import re
import secrets
import sys
import threading
import time

SPEC = importlib.util.spec_from_file_location("rak_updater", Path(__file__).with_name("update-repeater.py"))
updater = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updater)


class PreparationRequired(updater.UpdateError):
    """A captured board needs initialization before reversible diagnostics."""


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def save(path, data):
    """Atomically replace private progress; backups themselves use exclusive creation."""
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.chmod(0o600)
    temporary.replace(path)


def capture(interface, port):
    state = updater.snapshot(interface, port.device, port.serial_number)
    state["selfNodeInfo"] = copy.deepcopy(interface.getMyNodeInfo())
    return state


def assert_identity(state, actual):
    for key in ("usbSerial", "hardwareId"):
        if not state.get(key) or state[key] != actual.get(key):
            raise updater.UpdateError("USB/hardware identity mismatch; refusing configuration writes.")
    if state["user"]["id"] != actual["user"]["id"]:
        raise updater.UpdateError("Node identity mismatch; refusing configuration writes.")


def same_config(before, after):
    assert_identity(before, after)
    updater.assert_preserved(before, after)
    if before["metadata"] != after["metadata"]:
        raise updater.UpdateError("Firmware metadata differs from backup.")
    local, _, _ = load_messages(before)
    position = before.get("selfNodeInfo", {}).get("position", {})
    if local.position.fixed_position and "latitudeI" in position and "longitudeI" in position:
        actual = after.get("selfNodeInfo", {}).get("position", {})
        if any(position.get(key) != actual.get(key) for key in ("latitudeI", "longitudeI", "altitude")):
            raise updater.UpdateError("Saved fixed position differs from backup.")


def load_messages(state):
    from meshtastic.protobuf import channel_pb2, localonly_pb2

    local = localonly_pb2.LocalConfig()
    module = localonly_pb2.LocalModuleConfig()
    local.ParseFromString(base64.b64decode(state["localWire"], validate=True))
    module.ParseFromString(base64.b64decode(state["moduleWire"], validate=True))
    channels = []
    for encoded in state["channelsWire"]:
        channel = channel_pb2.Channel()
        channel.ParseFromString(base64.b64decode(encoded, validate=True))
        channels.append(channel)
    return local, module, channels


def diagnostic_state(before, region, channel_name, key, environment=False, power=False):
    """Only these sections are ever written; identity, security and position stay intact."""
    from meshtastic.protobuf import config_pb2

    local, module, channels = load_messages(before)
    local.device.role = config_pb2.Config.DeviceConfig.CLIENT
    local.device.rebroadcast_mode = config_pb2.Config.DeviceConfig.NONE
    local.lora.Clear()
    local.lora.region = config_pb2.Config.LoRaConfig.RegionCode.Value(region)
    local.lora.use_preset = True
    local.lora.modem_preset = config_pb2.Config.LoRaConfig.LONG_FAST
    # Firmware expands preset defaults on reboot; request the exact LONG_FAST
    # values so full readback comparison does not reject that normalization.
    local.lora.bandwidth = 250
    local.lora.spread_factor = 11
    local.lora.coding_rate = 5
    local.lora.channel_num = 20
    local.lora.tx_enabled = True
    local.lora.tx_power = 10
    local.lora.hop_limit = 0
    # Preserve the board's hardware-specific FEM configuration.
    old_local, _, _ = load_messages(before)
    local.lora.fem_lna_mode = old_local.lora.fem_lna_mode
    module.telemetry.device_telemetry_enabled = True
    module.telemetry.environment_measurement_enabled = environment
    module.telemetry.power_measurement_enabled = power
    for field in ("device_update_interval", "environment_update_interval", "power_update_interval"):
        setattr(module.telemetry, field, 3600)
    for channel in channels:
        index = channel.index
        channel.Clear()
        channel.index = index
        # Firmware fixupChannel materializes empty settings even on disabled slots.
        channel.settings.SetInParent()
        if index == 0:
            channel.role = 1
            channel.settings.name = channel_name
            channel.settings.psk = key
    return local, module, channels


def write_settings(interface, messages):
    local, module, channels = messages
    node = interface.localNode
    node.beginSettingsTransaction()
    for name in ("device", "lora"):
        getattr(node.localConfig, name).CopyFrom(getattr(local, name))
        node.writeConfig(name)
        time.sleep(0.15)
    node.moduleConfig.telemetry.CopyFrom(module.telemetry)
    node.writeConfig("telemetry")
    for channel in channels:
        node.channels[channel.index].CopyFrom(channel)
        node.writeChannel(channel.index)
        time.sleep(0.15)
    node.commitSettingsTransaction()


def restore_role_defaults(interface, expected, actual):
    """Reapply only observed role-default side effects after the role is stable."""
    saved_local, saved_module, _ = load_messages(expected)
    local, module, _ = load_messages(actual)
    if saved_local.device.role != local.device.role:
        raise updater.UpdateError("Role readback differs; refusing dependent-setting repair.")
    sections = []
    for saved, observed, allowed in (
            (saved_local, local, {"device", "position", "power", "display"}),
            (saved_module, module, {"telemetry", "neighbor_info"})):
        for field in saved.DESCRIPTOR.fields:
            name = field.name
            wanted, current = getattr(saved, name), getattr(observed, name)
            if wanted == current:
                continue
            if name not in allowed:
                raise updater.UpdateError("Unexpected profile difference; refusing automatic dependent-setting repair.")
            current.CopyFrom(wanted)
            sections.append((name, wanted, saved is saved_local))
    user = copy.deepcopy(actual["user"])
    repair_flag = user.get("isUnmessagable") != expected["user"].get("isUnmessagable")
    if repair_flag:
        if "isUnmessagable" not in expected["user"]:
            raise updater.UpdateError("Cannot restore absent owner flag presence; inspect private readback.")
        user["isUnmessagable"] = expected["user"]["isUnmessagable"]
    candidate = dict(actual, user=user, localWire=updater.wire(local), moduleWire=updater.wire(module))
    # Validate every remaining field, identity, key and channel before any write.
    same_config(expected, candidate)
    if not sections and not repair_flag:
        return False
    node = interface.localNode
    node.beginSettingsTransaction()
    for name, wanted, is_local in sections:
        cache = node.localConfig if is_local else node.moduleConfig
        getattr(cache, name).CopyFrom(wanted)
        node.writeConfig(name)
        time.sleep(0.15)
    if repair_flag:
        from meshtastic.protobuf import admin_pb2

        request = admin_pb2.AdminMessage()
        request.set_owner.is_licensed = expected["user"].get("isLicensed", False)
        request.set_owner.is_unmessagable = expected["user"]["isUnmessagable"]
        node._sendAdmin(request)
    node.commitSettingsTransaction()
    return True


class Radio:
    def __init__(self, port, log):
        self.port = port
        self.log = log
        self.interface = None
        self.before = None
        self.dirty = False

    def connect(self, timeout=12):
        from meshtastic.serial_interface import SerialInterface

        interface = SerialInterface(devPath=self.port.device, debugOut=self.log,
                                    connectNow=False, timeout=timeout, noNodes=True)
        try:
            interface.connect()
        except BaseException:
            interface.close()
            raise
        self.interface = interface

    def close(self):
        if self.interface:
            try:
                self.interface.close()
            finally:
                self.interface = None

    def snapshot(self):
        return capture(self.interface, self.port)

    def backup(self, path):
        self.before = self.snapshot()
        updater.private_json(path, self.before)
        if not self.port.serial_number:
            raise updater.UpdateError("USB serial unavailable; backup saved, no changes allowed.")
        if self.before["metadata"].get("hwModel") != "RAK4631":
            raise updater.UpdateError("This tool only changes RAK4631 devices; backup saved.")
        local, module, channels = load_messages(self.before)
        if len(channels) != 8 or [c.index for c in channels] != list(range(8)):
            raise updater.UpdateError("Incomplete channel export; backup saved, no changes allowed.")
        if (len(local.security.private_key) != 32 or not any(local.security.private_key)
                or len(local.security.public_key) != 32 or not any(local.security.public_key)):
            raise PreparationRequired("Security identity is uninitialized; backup saved. Prepare the board separately before reversible triage.")
        if local.lora.region != 1 or module.mqtt.root == "msh":
            raise PreparationRequired("US region/default initialization is incomplete; backup saved. Prepare the board separately before reversible triage.")
        if local.lora.use_preset and not all((local.lora.bandwidth, local.lora.spread_factor, local.lora.coding_rate)):
            raise PreparationRequired("Preset defaults are not initialized; backup saved. Reboot and capture a stable baseline before triage.")

    def reconnect(self):
        from serial.tools.list_ports import comports

        self.close()
        # The pinned firmware schedules commit-triggered reboot seven seconds out.
        # Waiting beyond it avoids accepting a pre-reboot config handshake.
        time.sleep(12)
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            ports = [p for p in comports() if updater.serial_matches(p.serial_number, self.before["usbSerial"])]
            if len(ports) > 1:
                raise updater.UpdateError("Multiple ports match USB identity; no automatic selection.")
            if ports:
                self.port = ports[0]
                try:
                    self.connect(timeout=5)
                    assert_identity(self.before, self.snapshot())
                    return
                except Exception as error:
                    self.close()
                    # Identity failures must never become a reconnect retry on another board.
                    if isinstance(error, updater.UpdateError):
                        raise
            time.sleep(1)
        raise updater.UpdateError("Device did not reconnect within the bounded wait.")

    def apply(self, messages):
        assert_identity(self.before, self.snapshot())
        self.dirty = True  # Set before first write, including an interrupted transaction.
        write_settings(self.interface, messages)
        self.reconnect()
        actual = self.snapshot()
        local, module, channels = messages
        expected = copy.deepcopy(self.before)
        old_local, old_module, _ = load_messages(self.before)
        old_local.device.CopyFrom(local.device)
        old_local.lora.CopyFrom(local.lora)
        old_module.telemetry.CopyFrom(module.telemetry)
        expected.update(localWire=updater.wire(old_local), moduleWire=updater.wire(old_module),
                        channelsWire=[updater.wire(c) for c in channels])
        # User.role reflects the active role and is handled by assert_preserved.
        same_config(expected, actual)

    def restore(self, directory):
        if not self.dirty:
            return
        if self.interface is None:
            self.reconnect()
        assert_identity(self.before, self.snapshot())
        write_settings(self.interface, load_messages(self.before))
        self.reconnect()
        actual = self.snapshot()
        updater.private_json(directory / "restore-role-readback.json", actual)
        if restore_role_defaults(self.interface, self.before, actual):
            self.reconnect()
        # An explicit reboot also verifies persistence if commit did not reboot.
        self.interface.localNode.reboot(1)
        self.reconnect()
        actual = self.snapshot()
        updater.private_json(directory / "restored.json", actual)
        same_config(self.before, actual)
        self.dirty = False


class Inbox:
    """Match actual received protobufs, never SDK enqueue success or generic ACKs."""
    def __init__(self):
        self.rows = []
        self.condition = threading.Condition()

    def receive(self, packet, interface):
        raw = packet.get("raw")
        if raw is not None:
            with self.condition:
                self.rows.append((time.monotonic(), interface, copy.deepcopy(raw)))
                self.rows = self.rows[-2000:]
                self.condition.notify_all()

    def wait(self, interface, since, predicate, timeout):
        deadline = time.monotonic() + timeout
        with self.condition:
            while True:
                for when, received_on, raw in self.rows:
                    if when >= since and received_on is interface and predicate(raw):
                        return raw
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None
                self.condition.wait(remaining)


def telemetry(inbox, sender, destination, variant, timeout=4):
    from google.protobuf.json_format import MessageToDict
    from meshtastic.protobuf import portnums_pb2, telemetry_pb2

    request = telemetry_pb2.Telemetry()
    getattr(request, variant).SetInParent()
    start = time.monotonic()
    sent = sender.sendData(request, destinationId=destination, portNum=portnums_pb2.TELEMETRY_APP,
                           wantAck=False, wantResponse=True, hopLimit=0)

    def match(raw):
        if (getattr(raw, "from") != destination or raw.decoded.request_id != sent.id
                or raw.decoded.portnum != portnums_pb2.TELEMETRY_APP):
            return False
        data = telemetry_pb2.Telemetry()
        try:
            data.ParseFromString(raw.decoded.payload)
        except Exception:
            return False
        return data.WhichOneof("variant") == variant

    raw = inbox.wait(sender, start, match, timeout)
    if raw is None:
        return None
    data = telemetry_pb2.Telemetry()
    data.ParseFromString(raw.decoded.payload)
    return MessageToDict(data)


def probe_matches(raw, sent, source, destination, payload):
    from meshtastic.protobuf import portnums_pb2

    return (getattr(raw, "from") == source and raw.to == destination and raw.id == sent.id
            and raw.decoded.portnum == portnums_pb2.PRIVATE_APP and raw.decoded.payload == payload
            and raw.hop_start == 0 and raw.hop_limit == 0)


def probe(inbox, sender, receiver, attempts=3):
    from meshtastic.protobuf import portnums_pb2

    results = []
    for attempt in range(attempts):
        payload = b"RAKCHECK1:" + secrets.token_bytes(12)
        start = time.monotonic()
        sent = sender.sendData(payload, destinationId=receiver.localNode.nodeNum,
                               portNum=portnums_pb2.PRIVATE_APP, wantAck=False, hopLimit=0)
        raw = inbox.wait(receiver, start, lambda packet: probe_matches(
            packet, sent, sender.localNode.nodeNum, receiver.localNode.nodeNum, payload), 4)
        results.append({"attempt": attempt + 1, "packetId": sent.id, "received": raw is not None,
                        "rssi": raw.rx_rssi if raw else None, "snr": raw.rx_snr if raw else None})
        time.sleep(0.3)
    return results


class UI:
    def __init__(self, console):
        self.console = console

    def say(self, text):
        print(text, file=self.console, flush=True)

    def ask(self, text):
        self.say(text)
        return input().strip()

    def yes(self, text):
        return self.ask(text + " [y/N]").lower() in ("y", "yes")

    def number(self, text):
        while True:
            answer = self.ask(text + " (blank = not measured)")
            if not answer:
                return None
            try:
                value = float(answer)
                if not math.isfinite(value) or value < 0:
                    raise ValueError()
                return value
            except ValueError:
                self.say("Enter a finite nonnegative number, or leave blank.")


def add(report, name, status, detail):
    report["checks"][name] = {"status": status, "detail": detail}


def sensor_check(report, name, sample, variant, required_fields):
    if sample is None:
        add(report, name, "INCONCLUSIVE", "No requested response: firmware support, detection, wiring or hardware unresolved.")
    else:
        metrics = sample.get(variant, {})
        present = any(isinstance(metrics.get(field), (int, float)) and math.isfinite(metrics[field])
                      for field in required_fields)
        add(report, name, "PASS" if present else "INCONCLUSIVE",
            "Requested sensor data returned; accuracy unverified." if present else "Response lacks expected measurements.")


def current_response(report):
    """A changing measurement is functional evidence, not a current calibration."""
    charging = (report["samples"].get("charging_power") or {}).get("powerMetrics", {})
    battery = (report["samples"].get("battery_power") or {}).get("powerMetrics", {})
    comparisons = []
    for channel in (1, 2, 3):
        key = f"ch{channel}Current"
        left, right = charging.get(key), battery.get(key)
        if all(isinstance(x, (float, int)) and math.isfinite(x) for x in (left, right)):
            comparisons.append({"channel": channel, "usbConnected_mA": left, "batteryOnly_mA": right,
                                "change_mA": right - left})
    report["samples"]["ina219CurrentComparison"] = comparisons
    changed = any(abs(row["change_mA"]) >= 1 for row in comparisons)
    add(report, "ina219_response", "PASS" if changed else "INCONCLUSIVE",
        "Current changed by at least 1 mA between power states; wiring, sign and calibration unverified." if changed else
        "No matched changing current samples; firmware, wiring, load or sensor cause unresolved.")


def choose_port(ui, explicit=None, exclude=None):
    from serial.tools.list_ports import comports

    ports = [p for p in comports() if p.device.casefold() != (exclude or "").casefold()]
    if explicit:
        matches = [p for p in ports if p.device.casefold() == explicit.casefold()]
        if len(matches) == 1:
            return matches[0]
        raise updater.UpdateError("Selected port is absent or is the reference port.")
    for port in ports:
        ui.say(f"  {port.device}: {port.description}; USB serial {port.serial_number or 'unavailable'}")
    answer = ui.ask("Connect the next RAK; enter its COM port (blank = finish" +
                    "; skip = no usable USB port" * bool(exclude) + "):")
    # Refresh after operator attaches a board; never open a port just to identify it.
    if not answer:
        return None
    if exclude and answer.lower() == "skip":
        return "skip"
    try:
        return choose_port(ui, answer, exclude)
    except updater.UpdateError as error:
        ui.say(str(error))
        return choose_port(ui, exclude=exclude)


def finish_report(directory, report, ui):
    report["finishedAt"] = datetime.now(timezone.utc).isoformat()
    statuses = [value["status"] for value in report["checks"].values()]
    report["verdict"] = "FAIL" if "FAIL" in statuses else "INCONCLUSIVE" if "INCONCLUSIVE" in statuses else "PASS"
    save(directory / "report.json", report)
    lines = [f"# {report['label']} — {report['verdict']}", "", "Quick triage only; no calibrated RF/sensor or runtime acceptance.", ""]
    for name, result in report["checks"].items():
        lines.append(f"- {name}: **{result['status']}** — {result['detail']}")
    lines.extend(["", "## Measurements", "", "Raw firmware current is in mA; USB meter current is in A.", "",
                  "```json", json.dumps({key: report.get(key) for key in (
                      "nodeId", "usbSerial", "firmware", "inspectionNotes", "modules", "ina219Path",
                      "usbMeter", "chargingIndicator", "ledButtonNotes", "elapsedSeconds", "samples")}, indent=2), "```"])
    (directory / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    ui.say(f"{report['label']}: {report['verdict']} | {directory / 'report.md'}")
    for name, result in report["checks"].items():
        ui.say(f"  {name}: {result['status']} — {result['detail']}")


def record_missing(ui, root):
    directory = root / ("board-" + stamp())
    directory.mkdir(mode=0o700)
    report = {"schemaVersion": 1, "label": ui.ask("Label for unresponsive/unpowered board:") or "unlabelled",
              "startedAt": datetime.now(timezone.utc).isoformat(), "checks": {}, "samples": {},
              "inspectionNotes": ui.ask("Damage/power/cable observations:")}
    add(report, "usb_connection", "FAIL", "Operator reports no usable USB port; board/cable/power/firmware cause unresolved.")
    add(report, "config_backup", "NOT_TESTED", "No API connection: configuration could not be captured; no changes attempted.")
    finish_report(directory, report, ui)
    return report


def run_board(ui, peer, inbox, port, root, bench, log, usb_only=False):
    start = time.monotonic()
    directory = root / ("board-" + stamp())
    directory.mkdir(mode=0o700)
    report = {"schemaVersion": 1, "startedAt": datetime.now(timezone.utc).isoformat(),
              "label": ui.ask("Test label (e.g. rak01; separate from saved radio name):") or "unlabelled",
              "port": port.device, "usbSerial": port.serial_number, "checks": {}, "samples": {}}
    report["inspectionNotes"] = ui.ask("Inspection notes (smoke/flex/pins/corrosion; blank = none recorded):")
    if not ui.yes("Inspection complete, safe to power, correct battery polarity, and included test antenna attached?"):
        add(report, "inspection", "FAIL", "Operator did not approve powering this board; no serial connection or changes.")
        finish_report(directory, report, ui)
        return report
    environment = ui.yes("Temperature/humidity sensor physically fitted?")
    power = ui.yes("INA219 physically fitted?")
    report["modules"] = {"temperatureHumidity": environment, "ina219": power}
    report["ina219Path"] = ui.ask("INA219 wiring/shunt marking (blank = unknown):") if power else None
    radio = Radio(port, log)
    log.flush()
    log_start = log.tell()
    add(report, "inspection", "PASS", "Operator approved inspection and antenna/battery setup.")
    try:
        radio.connect()
        radio.backup(directory / "original.json")
        report["nodeId"] = radio.before["user"]["id"]
        report["firmware"] = radio.before["metadata"].get("firmwareVersion")
        if radio.before["hardwareId"] == peer.before["hardwareId"]:
            raise updater.UpdateError("Reference and board have the same hardware identity.")
        if radio.before["user"]["id"] == peer.before["user"]["id"]:
            raise updater.UpdateError("Reference and board have the same node ID; resolve identity before testing.")
        add(report, "usb_config_backup", "PASS", "API-visible configuration and identity saved before writes.")
        save(directory / "report.json", report)
        radio.apply(diagnostic_state(radio.before, *bench, environment, power))
        updater.private_json(directory / "diagnostic.json", radio.snapshot())
        add(report, "diagnostic_profile", "PASS", "Complete intended profile read back after reconnect.")
        destination = radio.interface.localNode.nodeNum
        for variant in ("device_metrics", "local_stats", "environment_metrics", "power_metrics"):
            if variant == "environment_metrics" and not environment or variant == "power_metrics" and not power:
                continue
            report["samples"][variant] = telemetry(inbox, radio.interface, destination, variant)
        add(report, "device_telemetry", "PASS" if report["samples"]["device_metrics"] else "INCONCLUSIVE",
            "Requested device metrics response recorded." if report["samples"]["device_metrics"] else "No matching device response.")
        if environment:
            sensor_check(report, "temperature_humidity", report["samples"].get("environment_metrics"),
                         "environmentMetrics", ("temperature", "relativeHumidity"))
        else:
            add(report, "temperature_humidity", "NOT_FITTED", "Operator reports no sensor.")
        if power:
            sensor_check(report, "ina219_data", report["samples"].get("power_metrics"), "powerMetrics",
                         ("ch1Voltage", "ch1Current", "ch2Voltage", "ch2Current", "ch3Voltage", "ch3Current"))
        else:
            add(report, "ina219_data", "NOT_FITTED", "Operator reports no INA219.")
        for name, sender, receiver in (("radio_tx", radio.interface, peer.interface),
                                        ("radio_rx", peer.interface, radio.interface)):
            attempts = probe(inbox, sender, receiver)
            report["samples"][name] = attempts
            count = sum(row["received"] for row in attempts)
            add(report, name, "PASS" if count == len(attempts) else "FAIL",
                f"{count}/{len(attempts)} direct packets observed on the opposite USB radio; RF output/sensitivity unverified.")
        if usb_only:
            report["powerMode"] = "usb_only"
            report["usbMeter"] = {"volts": None, "amps": None}
            add(report, "battery_operation", "NOT_TESTED", "USB-only run; no battery connected or USB-disconnect test performed.")
            add(report, "charging_activity", "NOT_TESTED", "USB-only run; no battery charging test performed.")
            add(report, "ina219_accuracy", "NOT_TESTED", "No reference current measurement; calibration remains unverified.")
        else:
            report["powerMode"] = "usb_and_battery"
            ui.say("Power step: attach a healthy partially discharged battery in its normal circuit; leave USB connected.")
            report["usbMeter"] = {"volts": ui.number("USB meter voltage (V)"),
                                  "amps": ui.number("USB meter current (A)")}
            charging = ui.ask("Charging LED/indicator: on, off, or unknown?").lower()
            report["chargingIndicator"] = charging
            report["samples"]["charging_device"] = telemetry(inbox, radio.interface, destination, "device_metrics")
            if power:
                report["samples"]["charging_power"] = telemetry(inbox, radio.interface, destination, "power_metrics")
            radio.close()
            ui.ask("Unplug ONLY the test board's USB; keep battery and reference radio connected. Press Enter.")
            report["samples"]["battery_device"] = telemetry(inbox, peer.interface, destination, "device_metrics", 6)
            if power:
                report["samples"]["battery_power"] = telemetry(inbox, peer.interface, destination, "power_metrics", 6)
                current_response(report)
            battery_alive = report["samples"]["battery_device"] is not None
            add(report, "battery_operation", "PASS" if battery_alive else "INCONCLUSIVE",
                "Fresh telemetry response received over RF with USB unplugged." if battery_alive else "No battery-only response; power and RF causes unresolved.")
            add(report, "charging_activity", "PASS" if charging == "on" else "INCONCLUSIVE",
                "Operator observed charging indicator; termination/current accuracy unverified." if charging == "on" else "Charging activity not positively observed.")
            add(report, "ina219_accuracy", "NOT_TESTED", "Raw firmware polarity retained; USB input current is not battery-branch calibration.")
        report["ledButtonNotes"] = ui.ask("Other LED/button observations (blank = not checked):")
    except (Exception, KeyboardInterrupt, SystemExit) as error:
        if isinstance(error, PreparationRequired):
            add(report, "preparation", "INCONCLUSIVE", str(error))
        else:
            add(report, "run", "FAIL", f"Run interrupted or operation failed ({type(error).__name__}); inspect private sdk.log.")
        import traceback
        traceback.print_exc(file=log)
    finally:
        if radio.dirty:
            try:
                if usb_only:
                    ui.say("USB-only run: restoring and reboot-verifying original configuration.")
                else:
                    ui.ask("Reconnect test board USB now for configuration restoration. Press Enter.")
                radio.restore(directory)
                add(report, "restore_reboot", "PASS", "Original complete config, channels, identity and firmware verified after explicit reboot.")
            except (Exception, KeyboardInterrupt, SystemExit):
                add(report, "restore_reboot", "FAIL", "RESTORATION UNVERIFIED. Keep original.json; use --recover before reuse.")
                import traceback
                traceback.print_exc(file=log)
        try:
            radio.close()
        except Exception:
            add(report, "serial_close", "FAIL", "Serial close raised an error; close other tools before the next run.")
        log.flush()
        with Path(log.name).open(encoding="utf-8", errors="replace") as reader:
            reader.seek(log_start)
            lines = reader.read().splitlines()
        report["criticalErrorLines"] = [line for line in lines if re.search(
            r"critical\s+error|SX1262Failure|TransmitFailed|RadioSpiBug|NO_RADIO", line, re.I)]
        add(report, "firmware_errors", "FAIL" if report["criticalErrorLines"] else "NOT_TESTED",
            "Critical/error signature observed in private serial log." if report["criticalErrorLines"] else
            "No recognized critical signature captured; absence of logs is not an exhaustive self-test.")
        report["elapsedSeconds"] = round(time.monotonic() - start, 1)
        report["overFiveMinuteTarget"] = report["elapsedSeconds"] > 300
        finish_report(directory, report, ui)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-ports", action="store_true", help="List serial ports without opening them")
    parser.add_argument("--peer", help="Reference RAK COM port, e.g. COM5")
    parser.add_argument("--port", help="Test one board on this COM port; otherwise prompt for a batch")
    parser.add_argument("--usb-only", action="store_true", help="Skip battery/charging/meter steps; record those checks as not tested")
    parser.add_argument("--recover", type=Path, help="Restore one original.json or reference/original.json; requires --port")
    parser.add_argument("--region", choices=("US",), default="US", help="US/915 MHz bench hardware only")
    args = parser.parse_args(argv)
    ui = UI(sys.stdout)
    if args.list_ports:
        from serial.tools.list_ports import comports
        for port in comports():
            ui.say(f"{port.device}: {port.description}; USB serial {port.serial_number or 'unavailable'}")
        return 0
    if args.recover and not args.port or not args.recover and not args.peer:
        parser.error("Use --peer COMx, or --recover backup.json --port COMy.")
    if args.peer and args.port and args.peer.casefold() == args.port.casefold():
        parser.error("Reference and test board ports must differ.")
    old_umask = os.umask(0o077)
    directory = updater.ROOT / "private" / "bench" / ("rak-check-" + stamp())
    directory.mkdir(parents=True, mode=0o700)
    ui.say(f"Private evidence: {directory}")
    log = (directory / "sdk.log").open("x", encoding="utf-8")
    previous_logging = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    radio = None
    inbox = Inbox()
    from pubsub import pub
    pub.subscribe(inbox.receive, "meshtastic.receive")
    try:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            if args.recover:
                radio = Radio(choose_port(ui, args.port), log)
                radio.before = json.loads(args.recover.read_text(encoding="utf-8"))
                radio.connect()
                radio.dirty = True
                radio.restore(directory)
                ui.say("Original configuration restored and verified after reboot.")
                return 0
            reference_dir = directory / "reference"
            reference_dir.mkdir(mode=0o700)
            ui.say("Use two 915 MHz included RAK antennas, upright at fixed marked positions several metres apart. No Muzi comparison in this run.")
            if not ui.yes("Reference antenna attached, board inspected, and US/915 MHz hardware confirmed?"):
                return 1
            radio = Radio(choose_port(ui, args.peer), log)
            radio.connect()
            radio.backup(reference_dir / "original.json")
            bench = (args.region, "B" + secrets.token_hex(3), secrets.token_bytes(32))
            save(reference_dir / "status.json", {"state": "temporary-profile-may-be-applied", "restoreRequired": True})
            radio.apply(diagnostic_state(radio.before, *bench))
            updater.private_json(reference_dir / "diagnostic.json", radio.snapshot())
            ui.say("Reference prepared. It is a comparison peer, not a calibrated RF instrument.")
            reports = []
            while True:
                port = choose_port(ui, args.port, radio.port.device)
                if port is None:
                    break
                report = record_missing(ui, directory) if port == "skip" else run_board(
                    ui, radio, inbox, port, directory, bench, log, usb_only=args.usb_only)
                reports.append({"label": report["label"], "verdict": report["verdict"], "usbSerial": report.get("usbSerial")})
                save(directory / "batch.json", reports)
                if args.port:
                    break
            return 1 if any(row["verdict"] == "FAIL" for row in reports) else 2 if any(row["verdict"] == "INCONCLUSIVE" for row in reports) else 0
    except (Exception, KeyboardInterrupt, SystemExit):
        import traceback
        traceback.print_exc(file=log)
        ui.say("Setup/recovery failed; inspect private sdk.log. No automatic flashing or retry.")
        return 1
    finally:
        try:
            if radio and radio.dirty and not args.recover:
                with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                    try:
                        radio.restore(directory / "reference")
                        save(directory / "reference" / "status.json", {"state": "restored-and-verified", "restoreRequired": False})
                        ui.say("Reference original configuration restored and verified.")
                    except (Exception, KeyboardInterrupt, SystemExit):
                        save(directory / "reference" / "status.json", {"state": "restoration-unverified", "restoreRequired": True})
                        ui.say("REFERENCE RESTORATION UNVERIFIED: recover from reference/original.json before reuse.")
                        # A failed cleanup must override any otherwise successful batch exit.
                        raise SystemExit(1)
        finally:
            if radio:
                with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                    radio.close()
            pub.unsubscribe(inbox.receive, "meshtastic.receive")
            logging.disable(previous_logging)
            log.close()
            os.umask(old_umask)


if __name__ == "__main__":
    sys.exit(main())
