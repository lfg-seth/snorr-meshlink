#!/usr/bin/env python3
"""Download or verify the pinned RAK prerelease cache; never build or flash."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
TAG = "snorr-rak4631-2.7.26.0b65f2e-pre.1"
sys.path.insert(0, str(ROOT / "firmware" / "bin"))
from verify_snorr_release import download_release, verify_assets


def main():
    manifest_path = ROOT / "firmware" / ".github" / "releases" / f"{TAG}.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    directory = ROOT / "private" / "bench" / "releases" / TAG
    if directory.exists() and any(directory.iterdir()):
        verify_assets(directory, manifest_bytes)
        print("Reusing checksum-verified cached release.")
    else:
        directory.mkdir(parents=True, exist_ok=True)
        download_release(TAG, directory, manifest_bytes)
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
