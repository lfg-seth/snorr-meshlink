const el = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
function world(lon, lat) {
  const rad = (clamp(lat, -85, 85) * Math.PI) / 180;
  return [(lon + 180) / 360, (1 - Math.asinh(Math.tan(rad)) / Math.PI) / 2];
}
function good(g) {
  return g?.valid && hasPosition(g);
}
export function hasPosition(g) {
  return Number.isFinite(g?.lat_deg) && Number.isFinite(g?.lon_deg);
}
function color(value, metric) {
  if (!Number.isFinite(value)) return "#737975";
  const t =
    metric === "snr_db"
      ? clamp((value + 20) / 30, 0, 1)
      : clamp((value + 135) / 65, 0, 1);
  const ramp = [
      [169, 65, 91],
      [222, 163, 66],
      [22, 113, 81],
    ],
    u = t < 0.5 ? 0 : 1,
    f = (t - u * 0.5) * 2;
  return (
    "rgb(" +
    ramp[u].map((v, i) => Math.round(v + (ramp[u + 1][i] - v) * f)).join(",") +
    ")"
  );
}
export class SurveyMap {
  constructor(inspect) {
    this.canvas = el("map");
    this.ctx = this.canvas.getContext("2d");
    this.inspect = inspect;
    this.center = world(-115.642, 36.28);
    this.zoom = 14;
    this.follow = true;
    this.rows = [];
    this.hits = [];
    this.sites = {};
    this.targetNames = {};
    this.gps = null;
    this.queued = false;
    this.area = null;
    this.outage = false;
    new ResizeObserver(() => this.draw()).observe(this.canvas);
    el("locateTarget").onclick = () => this.frameTarget();
    el("follow").onclick = () => {
      this.setFollow(!this.follow);
      this.draw();
    };
    for (const [key, step] of [
      ["zoomIn", 1],
      ["zoomOut", -1],
    ])
      el(key).onclick = () => this.changeZoom(step);
    for (const id of ["direction", "metric", "filter"])
      el(id).onchange = () => this.draw();
    this.pointers = new Map();
    this.canvas.onpointerdown = (e) => {
      if (e.button !== 0 || this.pointers.size >= 2) return;
      this.canvas.setPointerCapture(e.pointerId);
      this.pointers.set(e.pointerId, this.localPoint(e));
      this.startGesture();
    };
    this.canvas.onpointermove = (e) => {
      if (!this.pointers.has(e.pointerId) || !this.gesture) return;
      this.pointers.set(e.pointerId, this.localPoint(e));
      const g = this.gesture,
        { mid, distance } = this.fingers();
      if (
        !g.moved &&
        Math.hypot(mid[0] - g.mid[0], mid[1] - g.mid[1]) < 3 &&
        this.pointers.size === 1
      )
        return;
      g.moved = true;
      this.setFollow(false);
      if (this.pointers.size === 2 && g.distance > 0 && distance > 0)
        this.zoom = clamp(g.zoom + Math.log2(distance / g.distance), 9, 16);
      this.placeAnchor(g.anchor, mid);
      this.draw();
    };
    const release = (e, tapped) => {
      if (!this.pointers.has(e.pointerId)) return;
      const isTap = tapped && !this.gesture?.moved && this.pointers.size === 1;
      this.pointers.delete(e.pointerId);
      if (isTap) this.tap(this.localPoint(e));
      if (this.pointers.size) this.startGesture(true);
      else this.gesture = null;
    };
    this.canvas.onpointerup = (e) => release(e, true);
    this.canvas.onlostpointercapture = (e) => release(e, false);
    this.canvas.onpointercancel = (e) => release(e, false);
    this.canvas.addEventListener(
      "wheel",
      (e) => {
        e.preventDefault();
        const delta =
          e.deltaY *
          (e.deltaMode === 1
            ? 16
            : e.deltaMode === 2
              ? this.canvas.clientHeight
              : 1);
        this.zoomAt(-clamp(delta, -300, 300) / 360, this.localPoint(e));
      },
      { passive: false },
    );
    this.canvas.onkeydown = (e) => {
      const d = {
        ArrowLeft: [-1, 0],
        ArrowRight: [1, 0],
        ArrowUp: [0, -1],
        ArrowDown: [0, 1],
      }[e.key];
      if (d) {
        e.preventDefault();
        this.setFollow(false);
        this.center = this.center.map((v, i) => v + (d[i] * 55) / this.size());
        this.draw();
      }
      if (e.key === "+" || e.key === "=") this.changeZoom(1);
      if (e.key === "-") this.changeZoom(-1);
    };
    this.load();
  }
  async load() {
    try {
      const r = await fetch("/map/area.json");
      if (!r.ok) throw Error("offline area unavailable");
      const a = await r.json(),
        img = new Image();
      img.src = a.terrain;
      await img.decode();
      const [w, s, e, n] = a.bounds;
      this.area = {
        nw: world(w, n),
        se: world(e, s),
        img,
        roads: a.roads.map(([name, kind, pts]) => {
          const points = pts.map((p) => world(...p));
          const xs = points.map((p) => p[0]),
            ys = points.map((p) => p[1]);
          return {
            name,
            kind,
            points,
            bounds: [
              Math.min(...xs),
              Math.min(...ys),
              Math.max(...xs),
              Math.max(...ys),
            ],
          };
        }),
      };
      el("mapinfo").textContent =
        "Offline Mount Charleston area installed · zoom " +
        a.zoom.join("–") +
        " · " +
        Math.round(Number(r.headers.get("Content-Length")) / 1024) +
        " KiB · W/S/E/N " +
        a.bounds.map((x) => x.toFixed(3)).join(", ");
    } catch {
      el("mapinfo").textContent =
        "Offline basemap unavailable. GPS and survey points are displayed on a coordinate grid.";
    }
    this.draw();
  }
  size() {
    return 256 * 2 ** this.zoom;
  }
  localPoint(e) {
    const b = this.canvas.getBoundingClientRect();
    return [e.clientX - b.left, e.clientY - b.top];
  }
  fingers() {
    const [a, b] = this.pointers.values();
    return b
      ? {
          mid: [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2],
          distance: Math.hypot(b[0] - a[0], b[1] - a[1]),
        }
      : { mid: a, distance: 0 };
  }
  anchorAt([x, y]) {
    return [
      this.center[0] + (x - this.canvas.clientWidth / 2) / this.size(),
      this.center[1] + (y - this.canvas.clientHeight / 2) / this.size(),
    ];
  }
  placeAnchor([wx, wy], [x, y]) {
    this.center = [
      wx - (x - this.canvas.clientWidth / 2) / this.size(),
      wy - (y - this.canvas.clientHeight / 2) / this.size(),
    ];
  }
  startGesture(moved = false) {
    const { mid, distance } = this.fingers();
    this.gesture = {
      mid,
      distance,
      anchor: this.anchorAt(mid),
      zoom: this.zoom,
      moved: moved || this.pointers.size === 2,
    };
  }
  zoomAt(step, point) {
    const anchor = this.anchorAt(point);
    this.setFollow(false);
    this.zoom = clamp(this.zoom + step, 9, 16);
    this.placeAnchor(anchor, point);
    this.draw();
  }
  tap(point) {
    const now = performance.now();
    if (
      this.previousTap &&
      now - this.previousTap.time < 325 &&
      Math.hypot(
        point[0] - this.previousTap.point[0],
        point[1] - this.previousTap.point[1],
      ) < 22
    ) {
      this.previousTap = null;
      this.zoomAt(1, point);
      return;
    }
    this.previousTap = { time: now, point };
    const hit = this.hits
      .map((h) => [Math.hypot(h[0] - point[0], h[1] - point[1]), h[2]])
      .sort((a, b) => a[0] - b[0])[0];
    if (hit && hit[0] < 20) this.inspect(hit[1]);
  }
  setFollow(v) {
    this.follow = v;
    el("follow").setAttribute("aria-pressed", String(v));
  }
  changeZoom(d) {
    this.zoom = clamp(this.zoom + d, 9, 16);
    this.draw();
  }
  frameTarget() {
    const site = this.sites[this.target];
    if (!hasPosition(site)) return;
    const dest = world(site.lon_deg, site.lat_deg);
    const start = good(this.gps)
      ? world(this.gps.lon_deg, this.gps.lat_deg)
      : dest;
    const w = this.canvas.clientWidth,
      h = this.canvas.clientHeight;
    const full = el("mapdialog").open;
    const top = full
      ? document.querySelector(".maphud").getBoundingClientRect().bottom + 20
      : 64;
    const bottom = full
      ? document.querySelector(".hudfoot").getBoundingClientRect().top - 16
      : h - 27;
    const usableHeight = Math.max(32, bottom - top);
    const usableWidth = Math.max(48, w - (full ? 146 : 88));
    const fit = Math.min(
      usableWidth / Math.abs(dest[0] - start[0]),
      usableHeight / Math.abs(dest[1] - start[1]),
    );
    this.setFollow(false);
    this.zoom = clamp(Math.min(this.zoom, Math.log2(fit / 256)), 9, 16);
    this.placeAnchor(
      [(start[0] + dest[0]) / 2, (start[1] + dest[1]) / 2],
      [full ? w / 2 - 25 : w / 2, clamp((top + bottom) / 2, h * 0.3, h * 0.8)],
    );
    this.draw();
  }
  update(rows, state) {
    this.rows = rows;
    this.sites = state.sites || {};
    this.targetNames = state.target_names || {};
    const radioGps = state.state.gps;
    this.laptopFallback = !good(radioGps) && good(state.laptop_gps);
    this.gps = this.laptopFallback ? state.laptop_gps : radioGps;
    this.target = state.state.target_id;
    this.outage = state.state.scenario === "Map outage";
    this.draw();
  }
  draw() {
    if (this.queued) return;
    this.queued = true;
    requestAnimationFrame(() => {
      this.queued = false;
      this.paint();
    });
  }
  paint() {
    const c = this.canvas,
      g = this.ctx,
      w = c.clientWidth,
      h = c.clientHeight;
    if (!w || !h) return;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    if (c.width !== Math.round(w * dpr) || c.height !== Math.round(h * dpr)) {
      c.width = Math.round(w * dpr);
      c.height = Math.round(h * dpr);
    }
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.fillStyle = "#e5e6d9";
    g.fillRect(0, 0, w, h);
    if (this.follow && good(this.gps))
      this.center = world(this.gps.lon_deg, this.gps.lat_deg);
    const sz = this.size(),
      proj = (p) => [
        (p[0] - this.center[0]) * sz + w / 2,
        (p[1] - this.center[1]) * sz + h / 2,
      ];
    const ll = (lon, lat) => proj(world(lon, lat));
    g.lineWidth = 1;
    g.strokeStyle = "#c6cbbd";
    g.beginPath();
    for (let x = (w / 2 - this.center[0] * sz) % 80; x < w; x += 80) {
      g.moveTo(x, 0);
      g.lineTo(x, h);
    }
    for (let y = (h / 2 - this.center[1] * sz) % 80; y < h; y += 80) {
      g.moveTo(0, y);
      g.lineTo(w, y);
    }
    g.stroke();
    let ready = "Grid only";
    if (this.area && !this.outage) {
      const a = this.area,
        tl = proj(a.nw),
        br = proj(a.se);
      g.drawImage(a.img, tl[0], tl[1], br[0] - tl[0], br[1] - tl[1]);
      ready =
        tl[0] <= w && br[0] >= 0 && tl[1] <= h && br[1] >= 0
          ? "Offline area"
          : "Outside area";
      const labels = [];
      for (const road of a.roads) {
        const b = road.bounds,
          lo = proj([b[0], b[1]]),
          hi = proj([b[2], b[3]]);
        if (hi[0] < 0 || hi[1] < 0 || lo[0] > w || lo[1] > h) continue;
        const major = /^(primary|secondary|tertiary|trunk)/.test(road.kind);
        if (!major && this.zoom < 12) continue;
        g.beginPath();
        for (const [i, p] of road.points.entries()) {
          const xy = proj(p);
          if (i) g.lineTo(...xy);
          else g.moveTo(...xy);
        }
        g.strokeStyle = major ? "#8d816d" : "#a5a68e";
        g.lineWidth = major ? 4 : 1;
        g.stroke();
        if (major) {
          g.strokeStyle = "#faf2c9";
          g.lineWidth = 2.3;
          g.stroke();
        }
        if (road.name && (major || this.zoom >= 15)) {
          const xy = proj(road.points[Math.floor(road.points.length / 2)]);
          if (
            xy[0] > 25 &&
            xy[0] < w - 50 &&
            xy[1] > 50 &&
            xy[1] < h - 35 &&
            labels.every((v) => Math.hypot(xy[0] - v[0], xy[1] - v[1]) > 100)
          )
            labels.push([...xy, road.name]);
        }
      }
      g.font = "11px system-ui";
      for (const [x, y, name] of labels) {
        g.strokeStyle = "#efeed9";
        g.lineWidth = 3;
        g.strokeText(name, x, y);
        g.fillStyle = "#58604f";
        g.fillText(name, x, y);
      }
    }
    el("mapready").textContent = this.outage ? "Outage · grid" : ready;
    const metric = el("metric").value,
      dir = el("direction").value,
      filter = el("filter").value;
    el("range").textContent =
      metric === "snr_db" ? "−20 to +10 dB" : "−135 to −70 dBm";
    this.hits = [];
    const targetSite = this.sites[this.target];
    if (good(this.gps) && hasPosition(targetSite)) {
      g.beginPath();
      g.moveTo(...ll(this.gps.lon_deg, this.gps.lat_deg));
      g.lineTo(...ll(targetSite.lon_deg, targetSite.lat_deg));
      g.strokeStyle = "#875009";
      g.lineWidth = 2;
      g.setLineDash([2, 5]);
      g.stroke();
      g.setLineDash([]);
    }
    g.beginPath();
    let last = null;
    for (const r of this.rows) {
      const e = r.event;
      if (e.name === "gap" || e.name === "transport_lost") last = null;
      if (
        e.name !== "gps" ||
        (e.data.sample_at && e.data.sample_at !== "local_stream")
      )
        continue;
      const p = e.data;
      if (!good(p)) {
        last = null;
        continue;
      }
      const xy = ll(p.lon_deg, p.lat_deg);
      if (
        last &&
        last.event.boot_id === e.boot_id &&
        last.event.data.session_id === p.session_id &&
        Math.abs(p.fix_utc_ms - last.event.data.fix_utc_ms) < 5000
      )
        g.lineTo(...xy);
      else g.moveTo(...xy);
      last = r;
    }
    g.strokeStyle = "#394e50";
    g.lineWidth = 1.6;
    g.setLineDash([4, 4]);
    g.stroke();
    g.setLineDash([]);
    for (const r of this.rows) {
      const e = r.event,
        p = e.data;
      if (
        e.name !== "result" ||
        !good(p.gps) ||
        (filter && p.target_id !== filter)
      )
        continue;
      const [x, y] = ll(p.gps.lon_deg, p.gps.lat_deg);
      this.hits.push([x, y, r]);
      g.lineWidth = 2;
      if (p.status === "success") {
        g.beginPath();
        g.arc(x, y, 5, 0, Math.PI * 2);
        g.fillStyle = color(p[dir]?.[metric], metric);
        g.fill();
        g.strokeStyle = "#faf9e9";
        g.stroke();
      } else if (p.status === "timeout") {
        g.strokeStyle = "#772b37";
        g.beginPath();
        g.moveTo(x - 4, y - 4);
        g.lineTo(x + 4, y + 4);
        g.moveTo(x + 4, y - 4);
        g.lineTo(x - 4, y + 4);
        g.stroke();
      } else {
        g.strokeStyle = "#585f60";
        g.strokeRect(x - 3, y - 3, 6, 6);
      }
    }
    for (const [id, p] of Object.entries(this.sites)) {
      if (!hasPosition(p) || id === this.target) continue;
      const name = p.site_name || this.targetNames[id]?.short_name || id;
      const [x, y] = ll(p.lon_deg, p.lat_deg);
      g.beginPath();
      g.moveTo(x, y - 7);
      g.lineTo(x - 6, y + 5);
      g.lineTo(x + 6, y + 5);
      g.closePath();
      g.fillStyle = "#253d32";
      g.fill();
      g.strokeStyle = "#f8f8ed";
      g.lineWidth = 2;
      g.stroke();
      g.font = "bold 12px system-ui";
      g.strokeText(name, x + 9, y + 4);
      g.fillText(name, x + 9, y + 4);
    }
    if (good(this.gps)) {
      const [x, y] = ll(this.gps.lon_deg, this.gps.lat_deg);
      g.beginPath();
      g.arc(x, y, 6, 0, Math.PI * 2);
      g.fillStyle = "#267389";
      g.fill();
      g.strokeStyle = "white";
      g.lineWidth = 2;
      g.stroke();
      if (this.laptopFallback) {
        g.font = "bold 12px system-ui";
        g.strokeText("Laptop GPS", x + 9, y + 4);
        g.fillStyle = "#1e4e64";
        g.fillText("Laptop GPS", x + 9, y + 4);
      }
    }
    if (hasPosition(targetSite)) {
      const [x, y] = ll(targetSite.lon_deg, targetSite.lat_deg);
      g.beginPath();
      g.arc(x, y, 11, 0, 2 * Math.PI);
      g.fillStyle = "#ffd77e";
      g.fill();
      g.strokeStyle = "#643710";
      g.lineWidth = 2.5;
      g.stroke();
      g.beginPath();
      g.moveTo(x, y - 7);
      g.lineTo(x + 6, y + 5);
      g.lineTo(x - 6, y + 5);
      g.closePath();
      g.fillStyle = "#492d0e";
      g.fill();
      const name =
        targetSite.site_name || this.targetNames[this.target]?.short_name || this.target;
      const label = name;
      g.font = "bold 12px system-ui";
      const width = g.measureText(label).width + 12;
      const left = clamp(
        x + 16 + width < w ? x + 16 : x - 16 - width,
        0,
        Math.max(0, w - width),
      );
      g.fillRect(left, y - 11, width, 22);
      g.fillStyle = "#fff4d6";
      g.fillText(label, left + 6, y + 4);
    }
    const lat = Math.atan(Math.sinh(Math.PI * (1 - 2 * this.center[1])));
    const meters = (100 * 40075017 * Math.cos(lat)) / sz;
    el("scale").textContent =
      "z" +
      Number(this.zoom.toFixed(1)) +
      " · 100 px ≈ " +
      Math.round(meters) +
      " m";
  }
}
