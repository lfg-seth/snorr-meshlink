import template from "./view.html?raw";

// Shared layout and interactions from the field dashboard at 8cfd518.
export function mountActivity(root) {
  root.innerHTML = template;
  const cards = root.querySelector("#cards");
  const statusLine = root.querySelector("#status");
  const groups = {all:"All nodes", reporting:"Reporting", attention:"Attention", silent:"Silent", unknown:"Unknown"};
  const stateNames = {fresh:"On time", aging:"One cycle missed", stale:"Two or more cycles missed", event:"Event", unknown:"Unknown"};
  const metrics = {
    voltage:["Device voltage","V",3.2,4.2], charge:["Battery","",0,100],
    batteryVoltage:["Battery voltage","V",3.2,4.2], batteryCurrent:["Battery current","mA",-100,100],
    temperature:["Temperature","°C",-20,50], humidity:["Humidity","%",0,100],
    busy:["Channel use","%",0,100], tx:["TX airtime","%",0,100], uptime:["Uptime","",0,3600],
    neighbors:["SNNS neighbors","",0,12], wifiConnected:["Wi-Fi","",0,1],
    mqttConnected:["MQTT","",0,1], wifi:["Wi-Fi signal","dBm",-100,-40], sd:["SD used","%",0,100],
  };
  const streams = {device:"Device",environment:"Environment",power:"Power",snns:"SNNS",
    gateway:"Backhaul",wifi:"Wi-Fi",sd:"SD"};
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
  function toneFor(key,n) {
    if (!Number.isFinite(n)) return "unknown";
    switch (key) {
      case "voltage": case "batteryVoltage": return n < 3.5 ? "down" : n < 3.75 ? "aging" : "fresh";
      case "charge": return n < 30 ? "down" : n <= 60 ? "aging" : "fresh";
      case "uptime": return n <= 120 ? "down" : n < 3600 ? "aging" : "fresh";
      case "wifi": return n < -80 ? "down" : n < -67 ? "aging" : "fresh";
      case "busy": return n > 25 ? "aging" : "fresh";
      case "sd": return n >= 95 ? "down" : n >= 80 ? "aging" : "fresh";
      default: return "fresh";
    }
  }
  function values(node) {
    const result = new Map();
    const readings = node.readings;
    function add(key,source,value,numeric,tone=toneFor(key,numeric)) {
      const [label,unit,min,max] = metrics[key];
      const fraction = Number.isFinite(numeric) ? Math.max(0,Math.min(1,(numeric-min)/(max-min))) : 0;
      result.set(key,{key,source,label,unit,value,tone,fraction,reading:readings[source]});
    }
    for (const key of Object.keys(metrics)) {
      let source = key;
      if (key === "batteryVoltage" || key === "batteryCurrent") {
        const sources = key === "batteryVoltage" ? ["inaVoltage","envVoltage"] : ["inaCurrent","envCurrent"];
        source = sources.filter(id=>readings[id] && Number.isFinite(parseFloat(readings[id].value)))
          .sort((a,b)=>(readings[a].age ?? Infinity)-(readings[b].age ?? Infinity))[0];
      }
      if (key === "wifiConnected" || key === "mqttConnected") source = "gateway";
      const reading = readings[source];
      if (!reading) continue;
      const v = reading.value;
      if (source === "gateway") {
        const status = v[key];
        add(key,source,status == null ? "Unknown" : status ? "Up" : "Down",
          status == null ? NaN : 1,status == null ? "unknown" : status ? "fresh" : "down");
      } else if (key === "wifi") {
        if (v.rssiDbm != null) add(key,source,v.rssiDbm,v.rssiDbm);
      } else if (key === "sd") {
        const used = v.usedBytes != null && v.totalBytes > 0 ? 100*v.usedBytes/v.totalBytes : NaN;
        add(key,source,Number.isFinite(used) ? used.toFixed(1) : "Unknown",used);
      } else if (key === "uptime") {
        add(key,source,Number.isFinite(reading.seconds) ? duration(reading.seconds,true) : v,reading.seconds);
      } else {
        add(key,source,v,parseFloat(v));
      }
    }
    return result;
  }
  function bar(fraction,signed=false) {
    const track = el("div",null,signed ? "track signed" : "track"), level = el("i");
    const start = signed ? Math.min(.5,fraction) : 0;
    level.style.marginLeft = 100*start+"%";
    level.style.width = 100*(signed ? Math.abs(fraction-.5) : fraction)+"%";
    track.setAttribute("aria-hidden","true");
    track.append(level);
    return track;
  }
  function readingTile(m,changed) {
    const tile = el("div",null,"metric "+m.tone+(changed ? " incoming" : ""));
    const number = el("b",m.value);
    if (m.unit && m.value !== "Unknown") number.append(el("small",m.unit));
    const age = m.reading.age == null ? "Age unknown" : duration(m.reading.age)+" ago";
    tile.title = (m.value === "USB*" ? "Charging or no battery detected · " : "")+
      age+" · "+stateNames[m.reading.state];
    tile.append(el("span",m.label),number,el("small",age,"age"),bar(m.fraction,m.key==="batteryCurrent"));
    return tile;
  }
  function createView() {
    const article = el("article"), face = el("div"), controls = el("div",null,"controls"), body = el("div",null,"tiles");
    const reason = el("span",null,"reason");
    const view = {article,face,body,reason,mode:"Timers",previous:null};
    for (const mode of ["Timers","Readings"]) {
      const button = el("button",mode);
      button.type = "button";
      button.setAttribute("aria-pressed",String(mode===view.mode));
      button.addEventListener("click",()=>{
        view.mode = mode;
        for (const other of controls.querySelectorAll("button"))
          other.setAttribute("aria-pressed",String(other===button));
        paint(view,view.previous,latest);
      });
      controls.append(button);
    }
    controls.append(reason);
    article.append(face,controls,body);
    cards.append(article);
    return view;
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
    const role = {recorder: " · Offline SD recorder", gateway: " · Backhaul"}[node.kind] ?? "";
    heard.append(el("strong",node.label + role));
    heard.append(el("span",node.seen ? "Last heard " + duration(data.now-Date.parse(node.seen)/1000,true) + " ago" : "Never heard"));
    if (received) heard.append(el("span","↳ Received","rx"));
    const measures = values(node), highlights = el("div",null,"metrics");
    const displayed = ["voltage","busy",measures.has("mqttConnected") ? "mqttConnected" : "temperature",
      "neighbors","charge"].filter(key=>measures.has(key)).slice(0,3);
    if (measures.has("batteryCurrent")) displayed.push("batteryCurrent");
    highlights.style.setProperty("--columns",Math.max(1,displayed.length));
    for (const key of displayed) {
      const m = measures.get(key);
      highlights.append(readingTile(m,readChanged(m.source)));
    }
    const timers = node.timers.filter(t=>!["position","neighbor_info","nodeinfo"].includes(t.stream));
    const late = timers.filter(t=>t.period && t.missed).length;
    const reasons = [node.linkDown && "Link down",late && late+" overdue"].filter(Boolean);
    if (!reasons.length && node.contact==="aging") reasons.push("Late contact");
    view.reason.textContent = reasons.join(" · ");
    view.reason.className = "reason "+(node.linkDown ? "down" : "aging");
    heard.title = node.radio;
    face.replaceChildren(heading,heard,displayed.length ? highlights : el("p","No telemetry yet","empty"));
    body.replaceChildren();
    if (view.mode==="Readings") {
      for (const [key,m] of measures) {
        if (!displayed.includes(key)) body.append(readingTile(m,readChanged(m.source)));
      }
      if (!body.childElementCount) body.append(el("p",displayed.length ? "All readings shown above" : "No readings yet","empty"));
    } else {
      for (const t of timers.sort((a,b)=>Number(!!b.missed)-Number(!!a.missed))) {
        const tile = el("div",null,"timer "+t.state+(timerChanged(t) ? " incoming" : ""));
        tile.title = timerHint(t);
        tile.append(el("span",streamName(t)),el("b",t.age == null && !t.missed ? "Waiting" : timerValue(t,true)),
          el("small",t.period ? "every "+duration(t.period,t.period % 60 !== 0) : "Event","age"));
        if (t.period) tile.append(bar(t.missed ? 1 : t.age == null ? 0 : Math.max(0,Math.min(1,t.due/t.period))));
        body.append(tile);
      }
      if (!body.childElementCount) body.append(el("p","No timers yet","empty"));
    }
    if (received) {
      // Restart the accent even when two consecutive polls each contain a new packet.
      for (const animation of article.getAnimations()) animation.cancel();
      if (!matchMedia("(prefers-reduced-motion: reduce)").matches) article.animate(
        [{boxShadow:"inset 0 0 0 2px #a8ecff"},{boxShadow:"inset 0 0 0 2px transparent"}],1400);
    }
    view.previous = node;
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
