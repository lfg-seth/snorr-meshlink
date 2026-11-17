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
  function readingTile(m,changed) {
    const age = m.reading.age == null ? "Age unknown" : duration(m.reading.age)+" ago";
    return {key:"reading:"+m.key, kind:"metric", tone:m.tone, label:m.label, value:m.value,
      unit:m.value === "Unknown" ? "" : m.unit, age, fraction:m.fraction, signed:m.key==="batteryCurrent", changed,
      title:(m.value === "USB*" ? "Charging or no battery detected · " : "") + age+" · "+stateNames[m.reading.state]};
  }
  function timerTile(t,changed) {
    return {key:"timer:"+t.stream, kind:"timer", tone:t.state, label:streamName(t),
      value:t.age == null && !t.missed ? "Waiting" : timerValue(t,true),
      age:t.period ? "every "+duration(t.period,t.period % 60 !== 0) : "Event", title:timerHint(t), changed,
      fraction:t.period ? (t.missed ? 1 : t.age == null ? 0 : Math.max(0,Math.min(1,t.due/t.period))) : null};
  }
  function setText(node,value) {
    const text = String(value);
    if (node.textContent === text) return;
    // Replacing even the text inside a visible age can lose WebKit's scroll anchor.
    if (node.firstChild) node.firstChild.data = text;
    else node.textContent = text;
  }
  function pulse(element) {
    if (element.ownerDocument.defaultView.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    for (const animation of element.getAnimations()) animation.cancel();
    element.animate([{boxShadow:"inset 0 0 0 2px var(--ice)"},{boxShadow:"inset 0 0 0 2px transparent"}],1400);
  }
  // Keep the elements Safari uses as scroll anchors attached while readings change.
  function tileList(className) {
    const element = el("div",null,className), tiles = new Map(), empty = el("p",null,"empty");
    function update(items,emptyMessage) {
      const present = new Set(items.map(item=>item.key));
      for (const [key,tile] of tiles) if (!present.has(key)) { tile.box.remove(); tiles.delete(key); }
      if (!items.length) {
        setText(empty,emptyMessage);
        if (!empty.parentNode) element.append(empty);
        return;
      }
      empty.remove();
      items.forEach((item,index)=>{
        let tile = tiles.get(item.key);
        if (!tile) {
          const box = el("div"), label = el("span"), number = el("b"), value = document.createTextNode("");
          const unit = el("small"), age = el("small",null,"age"), track = el("div",null,"track"), level = el("i");
          track.setAttribute("aria-hidden","true");
          track.append(level);
          number.append(value,unit);
          box.append(label,number,age,track);
          tile = {box,label,value,unit,age,track,level};
          tiles.set(item.key,tile);
        }
        const {box,label,value,unit,age,track,level} = tile;
        box.className = item.kind+" "+item.tone;
        box.title = item.title;
        setText(label,item.label);
        setText(value,item.value);
        setText(unit,item.unit || "");
        unit.hidden = !item.unit;
        setText(age,item.age);
        track.hidden = item.fraction == null;
        track.classList.toggle("signed",!!item.signed);
        if (item.fraction != null) {
          level.style.marginLeft = 100*(item.signed ? Math.min(.5,item.fraction) : 0)+"%";
          level.style.width = 100*(item.signed ? Math.abs(item.fraction-.5) : item.fraction)+"%";
        }
        const current = element.children[index];
        if (box !== current) element.insertBefore(box,current ?? null);
        if (item.changed) pulse(box);
      });
    }
    return {element,update};
  }
  function createView() {
    const article = el("article"), heading = el("div",null,"topline"), controls = el("div",null,"controls");
    const name = el("h2"), badge = el("span",null,"badge dot"), heard = el("div",null,"heard");
    const identity = el("span",null,"radio-label"), label = el("strong");
    const contact = el("span"), receipt = el("span","↳ Received","rx");
    heading.append(name,badge);
    identity.append(label,receipt);
    heard.append(identity,contact);
    const highlights = tileList("metrics"), body = tileList("tiles");
    const reason = el("span",null,"reason");
    const view = {article,name,badge,heard,label,contact,receipt,highlights,body,reason,mode:"Readings",previous:null};
    for (const mode of ["Readings","Timers"]) {
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
    article.append(heading,heard,highlights.element,controls,body.element);
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
    const {article,highlights,body} = view;
    article.className = node.health;
    article.dataset.radio = node.radio;
    setText(view.name,node.name);
    setText(view.badge,groups[node.health]);
    const role = {recorder: " · Offline SD recorder", gateway: " · Backhaul"}[node.kind] ?? "";
    setText(view.label,node.label + role);
    const age = node.seen ? duration(data.now-Date.parse(node.seen)/1000) : null;
    const route = node.heardThrough ? " through " + node.heardThrough : "";
    setText(view.contact,age ? "Last heard " + age + " ago" + route : "Never heard");
    view.receipt.style.visibility = received ? "visible" : "hidden";
    view.heard.title = node.radio;
    const measures = values(node);
    const displayed = ["voltage","busy",measures.has("mqttConnected") ? "mqttConnected" : "temperature",
      "neighbors","charge"].filter(key=>measures.has(key)).slice(0,3);
    if (measures.has("batteryCurrent")) displayed.push("batteryCurrent");
    highlights.element.style.setProperty("--columns",Math.max(1,displayed.length));
    highlights.update(displayed.map(key=>{
      const m = measures.get(key);
      return readingTile(m,readChanged(m.source));
    }),"No telemetry yet");
    const timers = node.timers.filter(t=>!["position","neighbor_info","nodeinfo"].includes(t.stream));
    const late = timers.filter(t=>t.period && t.missed).length;
    const reasons = [node.linkDown && "Link down",late && late+" overdue"].filter(Boolean);
    if (!reasons.length && node.contact==="aging") reasons.push("Late contact");
    setText(view.reason,reasons.join(" · "));
    view.reason.className = "reason "+(node.linkDown ? "down" : "aging");
    if (view.mode==="Readings") {
      const others = [...measures.values()].filter(m=>!displayed.includes(m.key));
      body.update(others.map(m=>readingTile(m,readChanged(m.source))),displayed.length ? "All readings shown above" : "No readings yet");
    } else {
      timers.sort((a,b)=>Number(!!b.missed)-Number(!!a.missed));
      body.update(timers.map(t=>timerTile(t,timerChanged(t))),"No timers yet");
    }
    if (received) pulse(article);
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
      setText(button.lastChild,latest?.at ? counts[key] : "—");
    }
    setText(empty,latest?.at && !counts[filter] ? "No nodes in this view" : "");
  }
  function render(data) {
      setText(statusLine,data.status === "Live" ? "Live feed" : data.status);
      statusLine.className = "dot " + (data.status === "Live" ? "fresh" : "aging");
      setText(root.querySelector("#stamp"),data.at ? "Snapshot " + new Date(data.at).toLocaleTimeString() : "");
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
