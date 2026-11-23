import { receiptRoute } from "./route.js";

// The publisher supplies original transmissions in first-receipt order, newest first.
export function mountPacketRow(section, streamName) {
  const row = section.querySelector("ol");
  const empty = section.querySelector("p");
  const win = row.ownerDocument.defaultView;
  const tiles = new Map();
  const gap = 6;
  let packets = [], nodes = new Map(), timer, clockOffset = 0;

  function createTile(packet, age) {
    const box = row.ownerDocument.createElement("li");
    const name = row.ownerDocument.createElement("strong");
    const type = row.ownerDocument.createElement("span");
    type.className = "packet-type";
    const time = row.ownerDocument.createElement("time");
    const route = row.ownerDocument.createElement("div");
    route.className = "packet-route";
    const hops = row.ownerDocument.createElement("span");
    const relay = row.ownerDocument.createElement("span");
    const gateway = row.ownerDocument.createElement("span");
    route.append(hops, relay, gateway);
    type.textContent = streamName(packet);
    time.dateTime = new Date(packet.received * 1000).toISOString();
    box.style.animationDelay = -age + "s";
    box.append(name, type, time, route);
    return {box, name, time, hops, relay, gateway};
  }

  function paint() {
    if (section.hidden) return;
    const now = win.Date.now() / 1000 + clockOffset;
    const width = row.getBoundingClientRect().width;
    // Route names need room on phones and on the unfolded portrait display.
    const phoneLandscape = win.matchMedia("(orientation: landscape) and (max-width:850px)").matches;
    const slots = width >= 840 ? 8 : width >= 560 && !phoneLandscape ? 6 : width >= 240 ? 4 : 2;
    const stride = (width + gap) / slots;
    row.style.setProperty("--packet-width", stride - gap + "px");
    const visible = packets.filter(p => now - p.received <= 3600).slice(0, slots);
    const keep = new Set(visible.map(p => p.id));
    for (const [id, tile] of tiles) {
      if (keep.has(id)) {
        // A wider viewport can bring a departing packet back before its fade ends.
        if (tile.exit) {
          win.clearTimeout(tile.exit);
          tile.exit = null;
          tile.box.removeAttribute("aria-hidden");
          tile.box.classList.remove("leaving");
        }
        continue;
      }
      if (tile.exit) continue;
      tile.box.setAttribute("aria-hidden", "true");
      tile.box.classList.add("leaving");
      const remove = () => { tile.box.remove(); tiles.delete(id); };
      if (win.matchMedia("(prefers-reduced-motion: reduce)").matches) remove();
      else tile.exit = win.setTimeout(remove, 430);
    }
    visible.forEach((packet, index) => {
      const age = Math.max(0, now - packet.received);
      let tile = tiles.get(packet.id);
      if (!tile) {
        tile = createTile(packet, age);
        tiles.set(packet.id, tile);
        // Insert in reading order while keeping moving cards attached.
        const next = row.querySelectorAll("li:not(.leaving)")[index];
        row.insertBefore(tile.box, next ?? null);
      }
      tile.box.style.setProperty("--left", index * stride + "px");
      const node = nodes.get(packet.radio);
      const label = node?.kind === "member"
        ? [node.label || packet.radio, packet.memberName].filter(Boolean).join(" · ")
        : node?.name || packet.radio;
      if (tile.name.textContent !== label) tile.name.textContent = label;
      tile.box.title = label + " · " + streamName(packet);
      const details = receiptRoute(packet);
      const relay = details.relay ? details.relay + (details.gateway ? " >" : "") : "";
      for (const [element, text] of [[tile.hops,details.label.replace("hop","Hop")],[tile.relay,relay],[tile.gateway,details.gateway]]) {
        if (element.textContent !== text) element.textContent = text;
        element.hidden = !text;
      }
      const elapsed = age < 60 ? Math.floor(age) + "s" : Math.floor(age / 60) + "m";
      const text = elapsed + " ago";
      if (tile.time.textContent !== text) tile.time.textContent = text;
    });
    empty.hidden = visible.length > 0;
    if (!visible.length) win.clearInterval(timer);
  }

  const resize = win.ResizeObserver && new win.ResizeObserver(paint);
  resize?.observe(row);
  return {
    render(snapshot) {
      section.hidden = !Array.isArray(snapshot.packets);
      clockOffset = snapshot.now - win.Date.now() / 1000;
      packets = snapshot.packets ?? [];
      nodes = new Map(snapshot.nodes.map(node => [node.radio, node]));
      win.clearInterval(timer);
      if (packets.length) timer = win.setInterval(paint, 1000);
      paint();
    },
    destroy() {
      resize?.disconnect();
      win.clearInterval(timer);
      for (const tile of tiles.values()) win.clearTimeout(tile.exit);
    },
  };
}
