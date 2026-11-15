import { SurveyMap, hasPosition } from "./map.js";
const $ = (id) => document.getElementById(id);
const uid = () =>
  Array.from(crypto.getRandomValues(new Uint32Array(4)), (x) =>
    x.toString(16).padStart(8, "0"),
  ).join("");
let token = sessionStorage.getItem("survey.controller");
if (!token) {
  token = uid();
  sessionStorage.setItem("survey.controller", token);
}
let host = null,
  rows = [],
  cursor = 0,
  connected = false,
  busy = false,
  view = "field",
  lastSetup = "",
  lastEvents = "",
  page = [],
  frozen = false;
let logSerial = 0,
  sessionsAt = 0,
  notice = "",
  viewGap = "",
  lastSession,
  latestResult = null;
let playback = null,
  replayVersion = 0,
  playTimer = null;
let pendingAck = null;
const options = (sel, values, chosen) => {
  const keys = values.map((v) => (Array.isArray(v) ? v : [v, v]));
  if (JSON.stringify(keys) !== sel.dataset.keys) {
    sel.replaceChildren(
      ...keys.map(([value, label]) => new Option(label, value)),
    );
    sel.dataset.keys = JSON.stringify(keys);
  }
  if (chosen != null) sel.value = chosen;
};
function message(s) {
  notice = s;
  alerts();
}
function alerts() {
  const s = host?.state || {};
  const lines = [
    !connected && "Browser disconnected · last received values",
    host?.record_error,
    host?.adapter_error,
    s.fault,
    s.mode === "bench" && "Bench mode · coverage acceptance disabled",
    viewGap,
    notice,
  ].filter(Boolean);
  $("alert").textContent = lines.join(" · ");
  $("alert").hidden = !lines.length;
}
async function api(url, payload) {
  const opts = {
    cache: "no-store",
    headers: { "X-Survey-Controller": token },
    signal: AbortSignal.timeout(8000),
  };
  if (payload !== undefined) {
    opts.method = "POST";
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(payload);
  }
  const r = await fetch(url, opts);
  const body = await r.json();
  if (!r.ok || body.ok === false) throw Error(body.error || "Request failed");
  return body;
}
function runAction(fn) {
  if (busy) return;
  busy = true;
  renderRun();
  (async () => {
    try {
      await fn();
      await sync();
    } catch (e) {
      message(e.message);
    } finally {
      busy = false;
      renderRun();
    }
  })();
}
async function send(name, params = {}) {
  const ack = await api("/api/command", {
    revision: host.revision,
    command: { v: 1, kind: "command", id: uid(), name, params },
  });
  pendingAck = ack.ok === null ? ack.command_id : null;
  message(
    ack.ok === null
      ? ack.error
      : name === "configure"
        ? "Settings applied · " + JSON.stringify(ack.applied)
        : "",
  );
}
function selectView(v) {
  view = v;
  document.querySelectorAll("nav button").forEach((b) => {
    const active = b.dataset.view === v;
    b.classList.toggle("active", active);
    b.setAttribute("aria-current", active ? "page" : "false");
  });
  $("field").hidden = !["field", "readout"].includes(v);
  $("field").classList.toggle("readout", v === "readout");
  $("journal").hidden = v !== "journal";
  $("setup").hidden = v !== "setup";
  if (v === "journal")
    refreshSessions()
      .then(showPage)
      .catch((e) => message(e.message));
  fieldMap.draw();
}
document
  .querySelectorAll("nav button")
  .forEach((b) => (b.onclick = () => selectView(b.dataset.view)));
const unit = (v, s) => (Number.isFinite(v) ? v + " " + s : "—");
const readings = (d) =>
  d ? unit(d.rssi_dbm, "dBm") + " / " + unit(d.snr_db, "dB") : "—";
const describe = (r) => {
  const d = r.event.data;
  return [
    d.target_id,
    d.status,
    d.reason,
    d.uplink && "↑ " + readings(d.uplink),
    d.downlink && "↓ " + readings(d.downlink),
    d.rtt_ms != null && unit(d.rtt_ms, "ms"),
    d.gps && !d.gps.valid && "No fix",
    d.gps?.fix_age_ms != null && "GPS " + unit(d.gps.fix_age_ms, "ms"),
  ]
    .filter(Boolean)
    .join(" · ");
};
const fieldMap = new SurveyMap((r) => {
  $("pick").hidden = false;
  $("pick").textContent =
    new Date(r.received_ms).toLocaleTimeString() + " · " + describe(r);
});
const mapDialog = $("mapdialog"),
  stage = document.querySelector(".mapstage");
function openMap() {
  if (mapDialog.open) return;
  $("mapmount").append(stage);
  $("targetMount").append($("mapTarget"));
  $("optionmount").append($("mapsettings"));
  $("pickmount").append($("pick"));
  document.body.classList.add("map-open");
  mapDialog.showModal();
  history.pushState({ surveyMap: true }, "", "#map");
  fieldMap.draw();
}
function closeMap() {
  if (!mapDialog.open) return;
  mapDialog.close();
  $("maphome").append(stage);
  $("targetHome").append($("mapTarget"));
  $("optionshome").append($("mapsettings"));
  $("pickhome").append($("pick"));
  $("maplayers").open = false;
  document.body.classList.remove("map-open");
  fieldMap.draw();
  $("openMap").focus({ preventScroll: true });
}
function leaveMap() {
  closeMap();
  if (history.state?.surveyMap) history.back();
}
$("openMap").onclick = openMap;
$("closeMap").onclick = leaveMap;
mapDialog.addEventListener("cancel", (e) => {
  e.preventDefault();
  leaveMap();
});
window.addEventListener("popstate", () => {
  if (!history.state?.surveyMap) closeMap();
  else if (!mapDialog.open) {
    history.replaceState(null, "", location.pathname + location.search);
  }
});
$("mapAction").onclick = () => $("go").click();
$("mapStop").onclick = () => $("stop").click();
function renderRun() {
  if (!host) return;
  const s = host.state,
    cmds = host.hello.commands || [];
  const action =
    s.run_state === "running"
      ? "pause"
      : s.run_state === "paused"
        ? "resume"
        : "start";
  $("go").textContent = {
    pause: "Pause survey",
    resume: "Resume survey",
    start: "Start survey",
  }[action];
  $("go").disabled =
    busy ||
    !connected ||
    !host.has_control ||
    !cmds.includes(action) ||
    !host.recording ||
    !!host.adapter_error ||
    s.transport === "disconnected";
  $("stop").disabled =
    busy || !connected || !host.has_control || !cmds.includes("stop");
  $("mapAction").textContent = $("go").textContent;
  $("mapAction").disabled = $("go").disabled;
  $("mapStop").disabled = $("stop").disabled;
  $("control").hidden = host.has_control;
  $("target").disabled =
    busy ||
    !connected ||
    !host.has_control ||
    !cmds.includes("set_target") ||
    s.run_state === "running";
  $("mode").disabled = busy || ["running", "paused"].includes(s.run_state);
  if (["running", "paused"].includes(s.run_state) && s.mode)
    $("mode").value = s.mode;
  $("go").onclick = () =>
    runAction(() =>
      send(
        action,
        action === "start"
          ? { mode: $("mode").value, target_id: $("target").value }
          : {},
      ),
    );
}
$("stop").onclick = () => runAction(() => send("stop"));
$("control").onclick = () => runAction(() => api("/api/control", {}));
$("target").onchange = () =>
  runAction(() => send("set_target", { target_id: $("target").value }));
$("scenario").onchange = () =>
  runAction(() => api("/api/simulation", { scenario: $("scenario").value }));
function isTargetResult(row, state) {
  const data = row?.event.data;
  return (
    !!state.session_id &&
    row?.event.name === "result" &&
    data.target_id === state.target_id &&
    data.session_id === state.session_id &&
    data.segment_id === state.segment_id &&
    data.status !== "late" &&
    !data.duplicate
  );
}
function targetSummary(state, site, result, isReplay) {
  const id = state.target_id;
  $("mapTargetId").textContent = id || "Unselected";
  $("locateTarget").disabled = !hasPosition(site);
  if (!id) {
    $("siteOrigin").textContent = "";
  } else if (!hasPosition(site)) {
    $("siteOrigin").textContent = "Site position unknown";
  } else if (isReplay) {
    $("siteOrigin").textContent = "Recorded site position";
  } else {
    const preset = host.hello.targets?.[id];
    const matches =
      preset?.lat_deg === site.lat_deg && preset?.lon_deg === site.lon_deg;
    $("siteOrigin").textContent = matches
      ? host.source === "simulation"
        ? "Simulator coordinates"
        : "Adapter coordinates"
      : "Saved site coordinates";
  }
  const status = result?.event.data.status;
  const when = result ? new Date(result.received_ms).toLocaleTimeString() : "";
  $("mapReply").textContent = !id
    ? "No target selected"
    : !result
      ? state.session_id
        ? "No result this segment"
        : "No survey result"
      : (status === "success"
          ? "Replied"
          : status === "timeout"
            ? "Timed out"
            : status || "Result") +
        " · " +
        when;
}
function render() {
  const s = host.state,
    caps = host.hello,
    counts = s.counts || {};
  $("source").textContent =
    host.source === "simulation" ? "Simulation" : "Live adapter";
  $("connection").textContent = !connected
    ? "Browser offline"
    : host.adapter_error || s.transport === "disconnected"
      ? "Adapter offline"
      : "Host connected";
  $("connection").className =
    connected && !host.adapter_error && s.transport === "connected"
      ? "good"
      : "bad";
  $("recording").textContent = !connected
    ? "Recorder unknown"
    : host.recording
      ? "Recording to disk"
      : "Recording failed";
  $("recording").className = connected && host.recording ? "good" : "bad";
  $("run").textContent = s.run_state || "Awaiting state";
  const targets = [
    ...new Set([...Object.keys(caps.targets || {}), ...(s.target_ids || [])]),
  ];
  if (s.target_id && !targets.includes(s.target_id)) targets.push(s.target_id);
  options($("target"), targets, s.target_id);
  options($("filter"), [
    ["", "All targets"],
    ...new Set([...targets, ...Object.keys(host.sites || {})]),
  ]);
  $("simlabel").hidden = host.source !== "simulation";
  options($("scenario"), caps.scenarios || [], s.scenario);
  $("scenario").disabled = !connected || !host.has_control || busy;
  const newest = rows.findLast((r) => isTargetResult(r, s));
  if (newest) latestResult = newest;
  const result = isTargetResult(latestResult, s)
    ? latestResult.event.data
    : null;
  $("up").textContent = readings(result?.uplink);
  $("down").textContent = readings(result?.downlink);
  const gps = s.gps || {};
  const mapState = playback?.state || s;
  const mapGps = mapState.gps || {};
  const mapResult = playback
    ? playback.rows.findLast((r) => isTargetResult(r, mapState))?.event.data
    : result;
  $("fullSource").textContent = playback
    ? host.source === "simulation"
      ? "Simulation · replay"
      : "Live recording · replay"
    : host.source === "simulation"
      ? "Simulation"
      : "Live";
  $("pillRun").textContent = mapState.run_state || "Awaiting state";
  if (!playback)
    targetSummary(
      s,
      host.sites?.[s.target_id],
      result ? latestResult : null,
      false,
    );
  const mapDir = $("direction").value,
    mapMetric = $("metric").value;
  $("pillSignal").textContent =
    (mapDir === "uplink" ? "↑ " : "↓ ") +
    (mapMetric === "snr_db" ? "SNR " : "RSSI ") +
    unit(
      mapResult?.[mapDir]?.[mapMetric],
      mapMetric === "snr_db" ? "dB" : "dBm",
    );
  $("pillGps").textContent = mapGps.valid
    ? "GPS " + unit(mapGps.fix_age_ms, "ms")
    : "GPS · no fix";
  $("pillRecord").textContent = !connected
    ? "Host offline"
    : host.recording
      ? playback
        ? "● Host recording"
        : "● Recording"
      : "Recording fault";
  const facts = [
    ["Selected repeater", s.target_id],
    ["Last round trip", result?.status || "No result"],
    [
      s.round_trip_basis === "completed"
        ? "Completed round trips"
        : "Round trips",
      counts.attempts == null
        ? "—"
        : counts.success +
          " / " +
          counts.attempts +
          (counts.attempts
            ? " · " + Math.round((100 * counts.success) / counts.attempts) + "%"
            : ""),
    ],
    [
      "Heltec GPS",
      gps.valid
        ? "Fix · " + unit(gps.fix_age_ms, "ms")
        : "No fresh fix" +
          (gps.fix_age_ms != null ? " · " + unit(gps.fix_age_ms, "ms") : ""),
    ],
    ["Measured interval", unit(s.measured_interval_ms, "ms")],
    [
      "Scheduled interval",
      unit(s.cadence_ms, "ms") + (s.backdown ? " · backed down" : ""),
    ],
    ["Quiet remaining", unit(s.quiet_remaining_s, "s")],
    [
      "Radio profile",
      s.settings?.profile ||
        s.settings?.radio_profile ||
        (s.radio_profile?.modem_preset != null
          ? "Preset " + s.radio_profile.modem_preset
          : "—"),
    ],
    ["Heartbeat", s.heartbeat_ok ? "Healthy" : "Missing"],
    [
      "Adapter queue",
      s.queue_depth == null
        ? "Unknown"
        : s.queue_depth + " / " + (s.queue_capacity ?? "—"),
    ],
    [
      "Capture gaps / drops",
      host.gaps + " / " + (host.dropped + (s.queue_dropped || 0)),
    ],
    ["Session segment", s.session_id ? String(s.segment_id) : "—"],
  ];
  $("facts").replaceChildren(
    ...facts.map(([k, v]) => {
      const div = document.createElement("div"),
        dt = document.createElement("dt"),
        dd = document.createElement("dd");
      dt.textContent = k;
      dd.textContent = v ?? "—";
      div.append(dt, dd);
      return div;
    }),
  );
  if (!playback) fieldMap.update(rows, host);
  renderRun();
  alerts();
  renderSettings();
}
function renderSettings() {
  const caps = host.hello,
    s = host.state,
    signature = JSON.stringify([
      caps.settings,
      s.settings,
      host.host_id,
      s.segment_id,
    ]);
  $("build").textContent = [
    caps.hardware,
    caps.build,
    "Protocol " + (caps.protocol ?? "—"),
    ...(Array.isArray(caps.capabilities)
      ? caps.capabilities
      : Object.entries(caps.capabilities || {}).map(
          ([k, v]) => k + " " + JSON.stringify(v),
        )),
  ]
    .filter(Boolean)
    .join(" · ");
  $("lockTarget").hidden =
    host.source !== "live" || !caps.commands?.includes("set_target");
  [...$("lockTarget").elements].forEach(
    (e) =>
      (e.disabled =
        !connected || !host.has_control || s.run_state === "running"),
  );
  if (signature !== lastSetup) {
    lastSetup = signature;
    const grid = document.querySelector(".settingsgrid");
    grid.replaceChildren(
      ...Object.entries(caps.settings || {}).map(([key, spec]) => {
        const label = document.createElement("label"),
          v = s.settings?.[key] ?? spec.default;
        label.textContent =
          key.replaceAll("_", " ") + (spec.unit ? " (" + spec.unit + ")" : "");
        let input;
        if (spec.type === "enum" || spec.type === "boolean") {
          input = document.createElement("select");
          options(input, spec.choices || ["true", "false"], String(v));
        } else {
          input = document.createElement("input");
          input.type = "number";
          input.inputMode = "numeric";
          input.required = true;
          input.min = spec.min;
          input.max = spec.max;
          input.step = spec.type === "integer" ? 1 : "any";
          input.value = v;
        }
        input.name = key;
        label.append(input);
        return label;
      }),
    );
  }
  const disabled =
    !connected ||
    !host.has_control ||
    s.run_state === "running" ||
    !caps.commands?.includes("configure");
  [...$("settings").elements].forEach((e) => (e.disabled = disabled));
}
$("settings").onsubmit = (e) => {
  e.preventDefault();
  const p = {};
  for (const [k, v] of new FormData(e.target)) {
    const spec = host.hello.settings[k];
    const value =
      spec.type === "enum"
        ? v
        : spec.type === "boolean"
          ? v === "true"
          : Number(v);
    if (value !== (host.state.settings?.[k] ?? spec.default)) p[k] = value;
  }
  if (!Object.keys(p).length) {
    message("Settings already applied");
    return;
  }
  if ("radio_profile" in p && Object.keys(p).length > 1) {
    message("Apply radio profile separately from timing changes");
    return;
  }
  runAction(() => send("configure", p));
};
$("lockTarget").onsubmit = (e) => {
  e.preventDefault();
  const target_id = new FormData(e.target).get("node");
  runAction(() => send("set_target", { target_id }));
};
$("site").onsubmit = (e) => {
  e.preventDefault();
  const row = Object.fromEntries(new FormData(e.target));
  runAction(async () => {
    await api("/api/sites", { sites: [row] });
    message("Fixed site saved");
  });
};
$("sitefile").onchange = () =>
  runAction(async () => {
    const f = $("sitefile").files[0];
    if (f.size > 30000) throw Error("Site file exceeds 30 KB");
    await api("/api/sites", { sites: JSON.parse(await f.text()) });
    message("Fixed sites imported");
  });
async function refreshSessions() {
  const sessions = await api("/api/sessions"),
    selected = $("session").value;
  options(
    $("session"),
    [
      ["", "Current session"],
      ...sessions.map((s) => [s.id, s.id + " · " + s.events + " events"]),
    ],
    selected,
  );
  sessionsAt = Date.now();
}
const logNames =
  "result,attempt,fault,gap,transport_lost,duplicate_delivery,adapter_error,site_record,host_command";
async function showPage(move) {
  if (!host) return;
  const serial = ++logSerial,
    session = $("session").value || host.state.session_id;
  let q = new URLSearchParams({ limit: "60", names: logNames });
  if (session) q.set("session", session);
  if (move === "older" && page.length) q.set("before", page[0].cursor);
  if (move === "newer" && page.length) q.set("after", page.at(-1).cursor);
  const data = await api("/api/events?" + q);
  if (serial !== logSerial) return;
  if (move && !data.length) {
    message("End of recorded window");
    return;
  }
  page = data;
  const fragment = document.createDocumentFragment();
  for (const r of page.slice().reverse()) {
    const b = document.createElement("button"),
      d = r.event.data;
    b.textContent =
      new Date(r.received_ms).toLocaleTimeString() +
      " · " +
      r.event.name +
      " · " +
      (describe(r) || d.command?.name || d.reason || "");
    b.onclick = () => {
      $("detail").hidden = false;
      $("detail").textContent = JSON.stringify(r, null, 2);
    };
    fragment.append(b);
  }
  $("events").replaceChildren(fragment);
  $("windowInfo").textContent = page.length
    ? String(page.length) +
      " events · cursors " +
      page[0].cursor +
      "–" +
      page.at(-1).cursor
    : "No matching recorded events";
  for (const [id, path] of [
    ["csv", "/export.csv"],
    ["raw", "/export.jsonl"],
  ])
    $(id).href =
      path + (session ? "?session=" + encodeURIComponent(session) : "");
}
$("older").onclick = () => {
  frozen = true;
  showPage("older").catch((e) => message(e.message));
};
$("newer").onclick = () => {
  frozen = true;
  showPage("newer").catch((e) => message(e.message));
};
$("refreshSessions").onclick = () => {
  frozen = false;
  refreshSessions()
    .then(() => showPage())
    .catch((e) => message(e.message));
};
$("session").onchange = () => {
  frozen = !!$("session").value;
  $("detail").hidden = true;
  showPage().catch((e) => message(e.message));
};
let syncing = null;
function pauseReplay() {
  clearTimeout(playTimer);
  playTimer = null;
  if (playback) playback.playing = false;
  $("play").textContent = "Play 1×";
}
async function replayStep() {
  const p = playback;
  if (!p || p.loading) return;
  const version = replayVersion;
  p.loading = true;
  try {
    if (!p.buffer.length) {
      const q = new URLSearchParams({
        after: p.cursor,
        before: p.end + 1,
        session: p.session,
        limit: 200,
      });
      const more = await api("/api/events?" + q);
      if (version !== replayVersion) return;
      p.buffer = more;
    }
    const r = p.buffer.shift();
    if (!r) {
      pauseReplay();
      $("replaytime").textContent = "End of recording";
      return;
    }
    p.cursor = r.cursor;
    const e = r.event,
      d = e.data;
    if (e.name === "state") p.state = d;
    if (e.name === "gps" && (!d.sample_at || d.sample_at === "local_stream"))
      p.state = { ...p.state, gps: d };
    if (d.target_location && d.target_id)
      p.sites[d.target_id] = d.target_location;
    Object.assign(p.sites, e.host_context?.fixed_sites || d.sites || {});
    if (["result", "gps", "gap", "transport_lost"].includes(e.name))
      p.rows = p.rows.concat(r).slice(-600);
    fieldMap.update(p.rows, { state: p.state, sites: p.sites });
    targetSummary(
      p.state,
      p.sites[p.state.target_id],
      p.rows.findLast((row) => isTargetResult(row, p.state)),
      true,
    );
    $("replaytime").textContent =
      new Date(r.received_ms).toLocaleTimeString() +
      " · " +
      e.name +
      " · #" +
      r.cursor;
    if (p.playing) {
      const delay = p.buffer.length
        ? Math.max(0, p.buffer[0].received_ms - r.received_ms)
        : 0;
      playTimer = setTimeout(() => replayStep().catch(replayError), delay);
    }
  } finally {
    p.loading = false;
  }
}
function replayError(e) {
  pauseReplay();
  message(e.message);
}
$("replay").onclick = async () => {
  try {
    const id = $("session").value || host.state.session_id;
    const session = (await api("/api/sessions")).find((s) => s.id === id);
    if (!session) throw Error("Start a survey to create a recording");
    pauseReplay();
    replayVersion++;
    playback = {
      session: id,
      end: session.last,
      cursor: session.first - 1,
      buffer: [],
      rows: [],
      state: {},
      sites: {},
      playing: false,
    };
    $("replaybar").hidden = false;
    $("pick").hidden = true;
    selectView("field");
    await replayStep();
  } catch (e) {
    replayError(e);
  }
};
$("step").onclick = () => {
  pauseReplay();
  replayStep().catch(replayError);
};
$("play").onclick = () => {
  if (playback.playing) {
    pauseReplay();
    return;
  }
  playback.playing = true;
  $("play").textContent = "Pause playback";
  replayStep().catch(replayError);
};
$("exitReplay").onclick = () => {
  pauseReplay();
  replayVersion++;
  playback = null;
  $("replaybar").hidden = true;
  $("pick").hidden = true;
  render();
};
async function sync() {
  if (syncing) return syncing;
  syncing = (async () => {
    try {
      const next = await api("/api/state"),
        s = next.state;
      const reset =
        !host ||
        host.host_id !== next.host_id ||
        lastSession !== s.session_id ||
        next.cursor - cursor > 500;
      if (reset) {
        const q = new URLSearchParams({
          before: String(next.cursor + 1),
          names: "gps,result,gap,transport_lost",
          limit: "350",
        });
        if (s.session_id) q.set("session", s.session_id);
        rows = await api("/api/events?" + q);
        if (host && lastSession === s.session_id && next.cursor - cursor > 500)
          viewGap =
            "Display caught up to recent history. Full events are in the run log.";
        if (host && host.host_id !== next.host_id)
          viewGap =
            "Host restarted. Inspect the previous recording in Run log.";
        cursor = next.cursor;
        latestResult = null;
        const q2 = new URLSearchParams({
          before: String(next.cursor + 1),
          names: "result",
          limit: "1",
        });
        if (s.session_id) {
          q2.set("session", s.session_id);
          latestResult = (await api("/api/events?" + q2))[0] || null;
        }
      } else if (next.cursor > cursor) {
        const data = await api(
          "/api/events?after=" +
            cursor +
            "&before=" +
            (next.cursor + 1) +
            "&limit=500",
        );
        if (data.length && data[0].cursor > cursor + 1)
          viewGap = "Event cursor gap. Inspect raw evidence.";
        rows = rows
          .concat(
            data.filter(
              (r) =>
                ["result", "gps", "gap", "transport_lost"].includes(
                  r.event.name,
                ) &&
                (!s.session_id || r.event.data.session_id === s.session_id),
            ),
          )
          .slice(-600);
        cursor = next.cursor;
      }
      host = next;
      lastSession = s.session_id;
      connected = true;
      render();
      if (pendingAck) {
        const result = await api(
          "/api/ack?id=" + encodeURIComponent(pendingAck),
        );
        if (result.ack) {
          pendingAck = null;
          message(
            result.ack.ok
              ? "Applied · " + JSON.stringify(result.ack.applied)
              : result.ack.error,
          );
        }
      }
      if (view === "journal" && !frozen && Date.now() - sessionsAt > 4000) {
        await refreshSessions();
        await showPage();
      }
    } catch (e) {
      connected = false;
      alerts();
      renderRun();
      if (host) render();
      else $("connection").textContent = "Host unreachable";
    } finally {
      syncing = null;
    }
  })();
  return syncing;
}
async function loop() {
  await sync();
  setTimeout(loop, 950);
}
loop();
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) sync();
});
