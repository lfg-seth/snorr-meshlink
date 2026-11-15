# Field Survey

Field Survey records direct-hop vehicle surveys on a Windows desktop or headless Linux laptop. Start the **simulation** to test the map, recording, fault handling and replay. The simulator uses generated positions and repeater IDs. The [v1 contract](../docs/operations/survey-interface-v1.md) defines the separate live client, host and browser responsibilities.

## Desktop and phone

From the root of this checkout with Python 3.10+ on PATH, start the hidden Windows process.

~~~powershell
.\survey-app\preview.ps1 start -Port 5187
.\survey-app\preview.ps1 status -Port 5187
~~~

Open the loopback service on port 5187. To use an iPhone or iPad, connect it to the owner's tailnet. On the authorized desktop the private HTTPS Serve listener uses 9447. For a new installation, inspect existing mappings and add the survey's mapping on an unused port.

~~~powershell
tailscale serve status
tailscale serve --bg --https=9447 http://127.0.0.1:5187
~~~

The owner's desktop also has another service on 8443. To remove only the survey mapping and stop its recorder, finish the run first, then use the two commands below. Closing the web page leaves the host running. A manual process restart opens a new host epoch and preserves recorded sessions on disk.

~~~powershell
tailscale serve --https=9447 off
.\survey-app\preview.ps1 stop -Port 5187
~~~

On a Linux laptop the server needs only Python's standard library for simulation. Run from the checkout root. Ctrl+C stops the foreground server. For a detached session under an existing user service manager, use the second command with systemd and stop it with the third.

~~~sh
python3 survey-app/server.py --source simulation --port 5187
systemd-run --user --unit=meshlink-survey --working-directory="$PWD" "$(command -v python3)" "$PWD/survey-app/server.py" --source simulation --port 5187
systemctl --user stop meshlink-survey
~~~

The host binds to 127.0.0.1. HTTPS on the private tailnet uses Tailscale Serve. The app serves its own scripts, styles and offline area. [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve).

## Run a survey

On the commissioned Fedora field laptop, plug in the GPS Heltec and open **MeshLink Field Survey** from Applications, or open `http://127.0.0.1:5187/` in the laptop browser. The system service `meshlink-survey.service` is enabled for that USB device's stable by-ID path and runs as the operator with serial access. `systemctl status meshlink-survey.service` shows service health. Use `sudo systemctl restart meshlink-survey.service` to reconnect after a fault. The offline area and private live recordings are under `/var/lib/meshlink-survey/`. Each `--known-target '!xxxxxxxx'` in the service adds a commissioned RAK ID to the selector independently of the radio's current selection. The operator starts the survey explicitly.

1. Select the target and **Survey** or **Bench**, then tap **Start survey**. Survey requires a fresh Heltec fix. Bench can continue through missing GPS and leaves those coordinates empty. The first browser to issue a command owns the controls. **Take controls** explicitly moves them to another browser while the run continues.
2. **Open map** fills the browser viewport. Drag with one finger, pinch with two, double-tap or use the zoom buttons. A mouse wheel zooms around the pointer. Pan or pinch releases Follow. Tap **Follow** to center on the client again. The top pills show target, run state, selected signal measurement, GPS and recorder health. **Layers** changes direction, metric and target filter. Pause and Stop stay on the map. **← Survey** returns to instruments.
3. A triangle marks a fixed repeater, a blue dot marks the latest valid client fix, and a circle shows a successful attempt. A cross means round-trip timeout. A square marks another recorded outcome. The dashed path estimates travel between nearby fixes. Missing fixes and gaps break it. Map color interpolates between the displayed limits for the selected metric. Choose the radio profile and inspect both directions before interpreting a result.
4. **Readout** shows both directions, successes and attempts, GPS age, pacing, quiet, heartbeat and capture health. Wide views display it next to the map. Under **Simulation scenario**, test asymmetric links, timeouts, backlog, stale or absent GPS, USB or heartbeat loss and map outages. Restore a working scenario before explicitly resuming a faulted run.
5. Pause before editing **Setup** or fixed-site records. The settings form is generated from adapter-advertised limits. Acknowledge a configuration change against its actual applied values. Firmware can require profile changes to be submitted separately. Fixed-site import accepts a JSON array of objects with `id`, `lat_deg` and `lon_deg`. Enter the actual repeater's fixed location privately. Use **Lock target** in live setup when the device has no configured target list.
6. **Run log** selects a session, pages through attempts and faults, and opens the original envelope on tap. **Replay on map** plays by host receipt time or advances one event at a time. The replay bar identifies the historic map. The run controls and instrument panel continue to describe the current host. Export CSV for analysis or JSONL for every event in the selected recording.

The baseline uses four-edge safe areas, viewport-relative sizing and container resize observation. It preserves state across layout changes and uses Pointer Events for map gestures. [WebKit Duo viewport guidance](https://webkit.org/blog/18486/webkit-features-for-safari-27-1/). [WebKit safe areas](https://webkit.org/blog/7929/designing-websites-for-iphone-x/).

### Reading the target on the map

The amber ring and **TARGET** label identify the repeater selected by the client. **Show target** brings its fixed site into view along with the vehicle when GPS is available. The dotted line shows the geographic bearing to the selected site. The reply or timeout time comes from the most recent completed result matching that target, session and configuration segment. **Samples for** filters historical measurements and leaves the selected repeater in view.

The simulation supplies two preset repeater IDs and coordinates. A saved site record for the same ID takes precedence on the map. In live mode, the client reports the target node ID through the firmware USB adapter. Enter or import its fixed coordinates under **Setup → Fixed repeater locations**. A target with unknown coordinates still shows its ID and results. Replay uses the site positions stored with the recording.

## Recording and recovery

The host ticks independently of HTTP clients. The firmware owns RF scheduling, GPS gating and the heartbeat interlock. The simulator models those responsibilities inside its adapter. Each source has a separate SQLite database below ignored `local-data/direct-hop-survey/{simulation,live}/`. A source lease prevents concurrent hosts from opening the same source directory. Keep the same data directory for reconnect and replay. To move a recording, stop the host before copying its data directory, or use SQLite's online backup API.

Each raw event gets a host cursor and receipt timestamp. The recorder uses append-only event rows, WAL and FULL synchronous commits. The command ledger reserves each ID before dispatch. An ambiguous prior outcome stays unknown. The browser issues each operator command once and polls by cursor. Refreshing or reconnecting retrieves authoritative state and recent history. A display catch-up message identifies a skipped screen window. All committed events remain available through export.

The host records boot/sequence gaps, duplicate deliveries, adapter queue drops, firmware errors and fixed-site edits. Raw JSONL export includes source, clock and adapter fields. The firmware adapter also retains its original private JSONL evidence. CSV adds separate uplink/downlink fields and fixed-target coordinates. SQL readers page recordings while the recorder writes. The live map retains at most 600 recent GPS/results and the journal renders at most 60 operator-facing rows per page.

A disk failure latches a recording error, counts affected events, attempts Stop and suspends host heartbeats. Restore writable disk space and restart explicitly. A transport exception is shown as an adapter fault. On a physical disconnect, inspect the recorded evidence and restart the live process with the same client identity after the device is available. It requires a fresh handshake and explicit start/resume. The simulation offers a switchable USB-loss scenario.

## Offline Mount Charleston map

The prepared desktop map uses the existing private AO polygon, cached OSM road geometry and local USGS 3DEP elevation raster. The installer clips roads to the polygon, shades a bounded elevation image in Web Mercator and atomically replaces a single local package. It requires no network transfer. The surveyed desktop package has 892 road segments and 1600 × 1419 relief, occupying 681,288 bytes. The display zoom range is 9–16. Zooming in magnifies the fixed-resolution terrain and redraws the vector roads. Outside this area the map uses a coordinate grid. Bounds and installed bytes appear under Setup.

Copy the prepared `map/area.json` into the same ignored data directory on the field laptop. To rebuild it at home, use a Python environment with NumPy, rasterio, Shapely and Pillow. Supply a WGS84 polygon FeatureCollection, a WGS84 OSM FeatureCollection with highway tags, and a georeferenced DEM. The command reports bounds, zooms, size estimate, clipping progress and final bytes. Ctrl+C cancels. Free space and final file size are checked against the budget before installation.

~~~sh
python3 survey-app/prepare_area.py --boundary /private/ao.geojson --roads /private/local-osm.geojson --dem /private/terrain-local.tif --out local-data/direct-hop-survey/map --size 1600 --budget-mib 16
~~~

The road data is © OpenStreetMap contributors under ODbL. USGS 3DEP elevation products are public domain. The software repository carries the renderer and builder. AO bounds, extracted data, rendered package and survey tracks stay private. [OSM copyright and license](https://www.openstreetmap.org/copyright). [USGS 3DEP data catalog](https://data.usgs.gov/datacatalog/data/USGS%3A3a81321b-c153-416f-98b7-cc8e5f0e17c3).

## Firmware adapter

After the firmware worker hands off the client, use its documented installed Python environment and an explicit device and expected node ID. Pass the path to the worker's version of `scripts/survey/adapter.py`. The GUI worktree can point to a separate firmware worktree. The command below is a template for the bench owner.

~~~sh
python3 survey-app/server.py --source live --adapter /path/to/scripts/survey/adapter.py --device /dev/serial/by-id/CLIENT --expected-id '!xxxxxxxx' --port 5187
~~~

`firmware_bridge.py` uses the worker's `SurveyAdapter(port, expected_id, log_path)` context, `command(envelope)`, `read_event(timeout=0)` and `close()`. The firmware adapter verifies the physical node ID and the bridge checks the client role. Only the adapter handles USB framing. Its separate automatic heartbeat is disabled so recording health gates the laptop heartbeat. A bounded command worker delivers ACKs asynchronously. Protocol/USB failure never selects simulation.

The bridge translates advertised numeric limits and profiles, separate device/adapter-host sequence streams, independent local GNSS, quiet time, queue capacity/drops, timing and directional measurements. Live session keys include the firmware boot ID. Original firmware fields remain in `adapter_data`. Completed live round trips use successes and timeouts reported by the device. Unsupported or missing readings remain unknown. Another normalized adapter can provide `open_adapter()` returning an object with `source="live"`, nonblocking `send(command)`, `poll(monotonic_ms)` returning a bounded batch of v1 events, and optional `close()`.

## Verification

~~~sh
python3 -m unittest discover -s survey-app -v
node survey-app/check-browser.cjs
python3 scripts/check-project.py docs --base codex/survey-assignments
~~~

The optional browser suite uses Playwright and Chromium. Set `PLAYWRIGHT_MODULE` or install Playwright in the test environment, set `CHROMIUM_PATH` for an existing browser, and set `PYTHON` if your interpreter is named python3. It launches a disposable simulator on a free loopback port. Set `SURVEY_PRIVATE_URL` to include a read-only TLS preview check. Screenshots and mock recordings stay under ignored `local-data/survey-qa/`. Set `SURVEY_FIRMWARE_MODULE` to include the real adapter API signature/import check with serial opening disabled.

Desktop tests cover stale GPS, bench mode without a fix, USB and heartbeat faults, idempotent commands, independent recording, queue/disk errors, restart recovery, segment changes, duplicate/late events and a 10,000-event archive. Chromium tests cover 14 viewport sizes including both WebKit toolbar heights for each Duo layout, iPad mini widths and narrow multitasking; trusted simulated touch pan/pinch, compact keyboard viewport, full-page map, replay, exports, control transfer and map outage. Owner feedback on the first private preview led to the dedicated map view and gesture changes. Native Safari folding, the physical iOS keyboard, Linux service execution, live USB/RF measurements and field coverage remain separate acceptance checks.
