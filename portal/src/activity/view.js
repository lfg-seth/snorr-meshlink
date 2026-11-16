import template from "./view.html?raw";

// Shared layout and interactions from the field dashboard at 8cfd518.
export function mountActivity(root) {
  root.innerHTML = template;
  const cards = root.querySelector("#cards");
  const statusLine = root.querySelector("#status");
  const groups = {all:"All nodes", reporting:"Reporting", attention:"Attention", silent:"Silent", unknown:"Unknown"};
  const stateNames = {fresh:"On time", aging:"One cycle missed", stale:"Two or more cycles missed", event:"Event", unknown:"Unknown"};
  const metrics = {voltage:["Device voltage","V"], charge:["Battery",""], inaVoltage:["INA219 voltage","V"],
    inaCurrent:["INA219 current","mA"], envVoltage:["Sensor voltage","V"], envCurrent:["Sensor current","mA"],
    temperature:["Temperature","°C"], humidity:["Humidity","%"], busy:["Channel use","%"], tx:["TX airtime","%"],
    uptime:["Uptime",""], neighbors:["SNNS neighbors",""], standardNeighbors:["Standard neighbors",""]};
  const streams = {device:"Device",environment:"Environment",power:"Power",snns:"SNNS",position:"GPS packet",
    gateway:"Backhaul",wifi:"Wi-Fi",sd:"SD",neighbor_info:"NeighborInfo",nodeinfo:"NodeInfo"};
  const views = new Map(), buttons = new Map();
  let filter = "all", latest;
  function el(tag, text, cls) {
    const node = document.createElement(tag);
    if (text != null) node.textContent = text;
    if (cls) node.className = cls;
    return node;
  }
  function duration(seconds, precise=false) {
    if (seconds == null || !Number.isFinite(seconds) || seconds < 0) return "Unknown";
    const s = Math.floor(seconds);
    for (const [scale, unit, next, suffix] of [[86400,"d",3600,"h"],[3600,"h",60,"m"],[60,"m",1,"s"]]) {
      if (s >= scale) return Math.floor(s / scale) + unit + (precise ? " " + Math.floor(s % scale / next) + suffix : "");
    }
    return s + "s";
  }
  function streamName(t) { return streams[t.stream] ?? t.stream.replace(/^(packet|telemetry):/, "").replace(/_/g," "); }
  function timerValue(t, precise=false) {
    if (!t.period) return t.age == null ? "Waiting" : duration(t.age,precise) + " ago";
    if (t.due == null) return "Unknown";
    if (t.age == null && !t.missed && !precise) return "Waiting";
    return duration(Math.abs(t.due),precise) + (t.missed ? " late" : " left");
  }
  function timerHint(t) {
    return (t.age == null ? "Awaiting first report · " : "") + stateNames[t.state] + " · " + timerValue(t,true)
      + (t.period ? " · every " + duration(t.period,true) : "");
  }
  function row(list, label, value, state, hint, changed) {
    const pair = el("div",null,"row" + (changed ? " incoming" : ""));
    pair.append(el("dt",label),el("dd",value,state));
    pair.title = hint;
    list.append(pair);
  }
  function values(node) {
    const result = new Map();
    for (const [key, reading] of Object.entries(node.readings)) {
      const v = reading.value;
      const add = (id,label,value,unit="") => result.set(id,{key,label,value,unit,reading});
      if (metrics[key]) {
        const [label,unit] = metrics[key];
        add(key,label,v === "USB*" ? "USB*" : v,unit);
      } else if (key === "gps") {
        add("gps","GPS fix age",duration(reading.age));
        if (v.satellites != null) add("sats","Satellites",v.satellites);
        if (v.pdop != null) add("pdop","GPS PDOP",v.pdop);
        if (v.altitude != null) add("altitude","Altitude",v.altitude,"m");
      } else if (key === "gateway") {
        for (const [field,label] of [["wifiConnected","Wi-Fi"],["mqttConnected","MQTT"]])
          add(field,label,v[field] == null ? "Unknown" : v[field] ? "Up" : "Down");
      } else if (key === "wifi" && v.rssiDbm != null) add("wifi","Wi-Fi signal",v.rssiDbm,"dBm");
      else if (key === "sd") {
        add("sd","SD used",v.usedBytes != null && Number(v.totalBytes)>0 ? (100*Number(v.usedBytes)/Number(v.totalBytes)).toFixed(1)+"%" : "Unknown");
        if (v.dropped != null) add("dropped","SD drops",v.dropped);
      }
    }
    return result;
  }
  function metricHint(m) {
    return (m.value === "USB*" ? "Charging or no battery detected · " : "") +
      "Reading age " + duration(m.reading.age,true) + " · " + stateNames[m.reading.state];
  }
  function createView() {
    const article = el("article"), face = el("div"), details = el("details"), body = el("div");
    const summary = el("summary","Telemetry & timer details");
    details.append(summary,body);
    article.append(face,details);
    cards.append(article);
    return {article,face,body,details,previous:null};
  }
  function paint(view,node,data) {
    const old = view.previous;
    const readChanged = key => !!old && node.readings[key].revision !== old.readings[key]?.revision;
    const priorTimers = new Map(old?.timers.map(t=>[t.stream,t.received]) ?? []);
    const timerChanged = t => !!old && !!t.received && t.received !== priorTimers.get(t.stream);
    const received = old && ((node.seen && node.seen !== old.seen) ||
      Object.keys(node.readings).some(readChanged) || node.timers.some(timerChanged));
    const {article,face,body} = view;
    article.className = node.health;
    article.dataset.radio = node.radio;
    const heading = el("div",null,"topline");
    heading.append(el("h2",node.name),el("span",groups[node.health],"badge dot"));
    const heard = el("div",null,"heard");
    heard.append(el("strong",node.label + (node.kind === "recorder" ? " · Offline SD recorder" : "")));
    heard.append(el("span",node.seen ? "Last heard " + duration(data.now-Date.parse(node.seen)/1000,true) + " ago" : "Never heard"));
    if (received) heard.append(el("span","↳ Received","rx"));
    const measures = values(node), highlights = el("div",null,"metrics");
    const preferred = ["voltage",node.kind === "member" ? "gps" : "busy",
      measures.has("mqttConnected") ? "mqttConnected" : "temperature","inaCurrent","busy","neighbors","charge"];
    const displayed = [...new Set(preferred)].filter(key=>measures.has(key)).slice(0,3);
    for (const key of displayed) {
      const m = measures.get(key);
      const tile = el("div",null,"metric " + m.reading.state + (readChanged(m.key) ? " incoming" : ""));
      tile.title = metricHint(m);
      const number = el("b",m.value);
      number.append(el("small",m.unit));
      tile.append(el("span",m.label),number);
      highlights.append(tile);
    }
    const strip = el("div",null,"timers");
    const periodic = node.timers.filter(t=>t.period);
    const late = periodic.filter(t=>t.missed).length;
    const label = el("div",null,"section-label");
    label.append(el("span","Watchdogs"));
    let reason = late ? late + " overdue" : "";
    if (node.linkDown) reason = "Link down" + (reason ? " · "+reason : "");
    else if (node.contact === "aging" && !reason) reason = "Late contact";
    if (reason) label.append(el("span",reason,"reason"));
    for (const t of periodic) {
      const tile = el("div",null,"timer " + t.state + (timerChanged(t) ? " incoming" : ""));
      tile.title = timerHint(t);
      const track = el("div",null,"track"), level = el("i");
      const fraction = t.missed ? 1 : t.age == null ? 0 : Math.max(.04,Math.min(1,t.due/t.period));
      level.style.width = 100*fraction + "%";
      track.append(level);
      const countdown = t.age == null && !t.missed ? "Waiting" : timerValue(t,true);
      tile.append(el("span",streamName(t)),el("b",countdown),track);
      strip.append(tile);
    }
    face.replaceChildren(heading,heard,displayed.length ? highlights : el("p","No telemetry yet","empty"),
      label,periodic.length ? strip : el("p","No scheduled streams","empty"));
    if (received) {
      // Restart the accent even when two consecutive polls each contain a new packet.
      for (const animation of article.getAnimations()) animation.cancel();
      if (!matchMedia("(prefers-reduced-motion: reduce)").matches) article.animate(
        [{boxShadow:"inset 0 0 0 2px #a8ecff"},{boxShadow:"inset 0 0 0 2px transparent"}],1400);
    }
    if (view.details.open || !old) fillDetails(body,node,measures,readChanged,timerChanged);
    view.previous = node;
  }
  function fillDetails(body,node,measures,readChanged,timerChanged) {
    const readings = el("dl"), timers = el("dl");
    for (const m of measures.values()) row(readings,m.label,m.value + (m.unit ? " "+m.unit : ""),m.reading.state,metricHint(m),readChanged(m.key));
    for (const t of node.timers) row(timers,streamName(t),timerHint(t),t.state,timerHint(t),timerChanged(t));
    body.replaceChildren(el("p",node.radio,"empty"),el("h3","Telemetry"),
      readings.childElementCount ? readings : el("p","No readings yet","empty"),el("h3","Timers"),
      timers.childElementCount ? timers : el("p","No timers yet","empty"));
  }
  for (const [key,label] of Object.entries(groups)) {
    const button = el("button",null,"stat "+key);
    button.type = "button";
    button.append(el("span",label,"dot"),el("strong","—"));
    button.addEventListener("click",()=>{ filter = filter === key ? "all" : key; applyFilter(); });
    root.querySelector("#summary").append(button);
    buttons.set(key,button);
  }
  const empty = el("p","","empty");
  cards.after(empty);
  function applyFilter() {
    const counts = {all:views.size,reporting:0,attention:0,silent:0,unknown:0};
    for (const view of views.values()) {
      const state = view.previous.health;
      counts[state]++;
      view.article.hidden = filter !== "all" && filter !== state;
    }
    for (const [key,button] of buttons) {
      button.setAttribute("aria-pressed",String(key===filter));
      button.lastChild.textContent = latest?.at ? counts[key] : "—";
    }
    empty.textContent = latest?.at && !counts[filter] ? "No nodes in this view" : "";
  }
  function render(data) {
      statusLine.textContent = data.status === "Live" ? "Live feed" : data.status;
      statusLine.className = "dot " + (data.status === "Live" ? "fresh" : "aging");
      root.querySelector("#stamp").textContent = data.at ? "Snapshot " + new Date(data.at).toLocaleTimeString() : "";
      const present = new Set();
      for (const node of data.nodes) {
        present.add(node.radio);
        if (!views.has(node.radio)) {
          const view = createView();
          views.set(node.radio,view);
          view.details.addEventListener("toggle",()=>{
            if (view.details.open && view.previous) fillDetails(view.body,view.previous,values(view.previous),()=>false,()=>false);
          });
        }
        paint(views.get(node.radio),node,data);
      }
      for (const [id,view] of views) if (!present.has(id)) { view.article.remove(); views.delete(id); }
      // The sampler supplies the same roster order used by the CLI.
      data.nodes.forEach((node,index)=>{
        const article = views.get(node.radio).article;
        const current = cards.children[index];
        if (article !== current) {
          if (cards.moveBefore) cards.moveBefore(article,current);
          else cards.insertBefore(article,current);
        }
      });
      latest = data;
      applyFilter();
  }
  function disconnected() {
      statusLine.textContent = "Disconnected · retrying";
      statusLine.className = "dot stale";
  }
  applyFilter();
  return {render, disconnected};
}
