#!/usr/bin/env python3
"""Apply the bounded local policy overlay to the checksum-verified 4.17.0 build."""

import json
from pathlib import Path
import sys

root = Path(sys.argv[1])
assert json.loads((root / "package.json").read_text())["version"] == "4.17.0"
targets = {
    "dist/services/database.js": [
        "    async purgeOldTelemetryAsync(hoursToKeep, favoriteDaysToKeep) {",
        "    async cleanupOldPacketLogsAsync() {",
    ],
    "dist/server/services/mqttPacketLogService.js": ["    async runCleanup() {"],
    "dist/server/services/coverageRetentionService.js": ["    async runCleanup() {"],
    "dist/server/services/meshcorePositionHistoryService.js": ["    async runCleanup() {"],
}
guard = '\n        if (process.env.MESHLINK_RETAIN_HISTORY === "true") return 0;'
changes = {}
for name, anchors in targets.items():
    path = root / name
    source = path.read_text()
    for anchor in anchors:
        if anchor + guard in source:
            continue
        if source.count(anchor) != 1:
            raise RuntimeError(f"Unexpected upstream cleanup seam: {name}")
        source = source.replace(anchor, anchor + guard)
    changes[path] = source
path = root / "dist/server/server.js"
source = path.read_text()
before = "server = app.listen(PORT, () => {"
after = "server = app.listen(PORT, process.env.MESHLINK_BIND_ADDRESS || '127.0.0.1', () => {"
if after not in source:
    if source.count(before) != 1:
        raise RuntimeError("Unexpected upstream HTTP listen seam")
    source = source.replace(before, after)
changes[path] = source
# Validate all seams before writing any file. Refuse a new release until reviewed.
for path, content in changes.items():
    path.write_text(content)
print("4.17.0 policy overlay: five cleanup guards and explicit HTTP bind")
