#!/usr/bin/env python3
"""Download or verify the pinned RAK prerelease cache; never build or flash."""

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "firmware" / "bin"))
from verify_snorr_release import download_release, verify_assets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Explicit historical release; default is the current repeater profile pin")
    args = parser.parse_args()
    tag = args.tag or json.loads(Path(__file__).with_name("repeater-profiles.json").read_text())["releaseTag"]
    if not isinstance(tag, str) or not re.fullmatch(r"snorr-rak4631-\d+\.\d+\.\d+\.[0-9a-f]{7}-pre\.\d+", tag):
        parser.error("No supported RAK release is pinned; use --tag only for an explicit known release")
    manifest_path = ROOT / "firmware" / ".github" / "releases" / f"{tag}.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest.get("schemaVersion") != 1 or manifest.get("repository") != "lfg-seth/firmware" or manifest.get("target") != "rak4631" or manifest.get("tag") != tag:
        parser.error("Expected a tracked RAK4631 manifest with this exact tag")
    directory = ROOT / "private" / "bench" / "releases" / tag
    if directory.exists() and any(directory.iterdir()):
        verify_assets(directory, manifest_bytes)
        print("Reusing checksum-verified cached release.")
    else:
        directory.mkdir(parents=True, exist_ok=True)
        download_release(tag, directory, manifest_bytes)
        verify_assets(directory, manifest_bytes)
        print("Downloaded and checksum-verified the pinned release.")
    print(f"Target: {manifest['target']}; binary version: {manifest['version']}")
    print(f"Binary source: {manifest['source']}")
    print(f"Cache: {directory}")
    print(
        "No build or flash performed. Identify the board before choosing its update method."
    )


if __name__ == "__main__":
    main()
