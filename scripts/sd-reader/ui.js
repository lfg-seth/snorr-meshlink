'use strict';
const $ = id => document.getElementById(id);
const limit = 75;
let segments=[], anchors=new Map(), page=0, revision=0;
const eventNames=[...Sml.names.slice(1),'Corruption','Open tail','Segment gap'];
for (const name of eventNames) $('kind').add(new Option(name));
const key = m => m.node+'/'+m.boot;
async function* records(file) {
  // Firmware segments are at most one MiB. Reject oversize/foreign input without reading it into memory.
  if (file.size > 1048576) {yield {event:'Corruption',detail:'Oversize segment',file:file.name};return;}
  for (const r of Sml.parse(new Uint8Array(await file.arrayBuffer()))) yield {...r,file:file.name};
}
async function load() {
  const token=++revision, selected=Array.from($('files').files);
  const list=[], first=new Map();
  $('status').textContent='Indexing copied segments…';
  for (const file of selected) {
    const meta=Sml.header(new Uint8Array(await file.slice(0,24).arrayBuffer())) || {};
    list.push({file,...meta});
    if (meta.boot && !first.has(key(meta))) {
      for await (const r of records(file)) {
        if (r.observed) {first.set(key(meta),r);break;}
      }
    } else if (meta.boot && meta.segment < first.get(key(meta)).segment) {
      for await (const r of records(file)) {
        if (r.observed) {first.set(key(meta),r);break;}
      }
    }
    if (token!==revision) return;
  }
  segments=list.sort((a,b)=>(a.node||'').localeCompare(b.node||'') || a.segment-b.segment);
  anchors=first; page=0; await render();
}
async function* filtered(token) {
  const from=$('from').value ? new Date($('from').value).getTime() : -Infinity;
  const to=$('to').value ? new Date($('to').value).getTime() : Infinity;
  const node=$('node').value.trim().toLowerCase().replace(/^!|^0x/,'');
  const kind=$('kind').value;
  let previous;
  for (const segment of segments) {
    if (token!==revision) return;
    const gap=previous && previous.node===segment.node && segment.segment>previous.segment+1
      ? {event:'Segment gap',node:segment.node,detail:`Segments ${previous.segment+1}–${segment.segment-1} absent`} : null;
    previous=segment;
    async function* items() { if (gap) yield gap; yield* records(segment.file); }
    for await (const r of items()) {
      if (token!==revision) return;
      // Only infer before the earliest observed anchor in the same device/boot.
      const anchor=anchors.get(key(r));
      r.reconstructed=!r.observed && anchor && r.uptimeMs<=anchor.uptimeMs
        ? new Date(Date.parse(anchor.observed)+r.uptimeMs-anchor.uptimeMs).toISOString() : null;
      const time=Date.parse(r.observed || r.reconstructed);
      if (from!==-Infinity || to!==Infinity) {
        if (!Number.isFinite(time) || time<from || time>to) continue;
      }
      if ((!node || r.source===node || r.node===node) && (!kind || kind===r.event)) yield r;
    }
  }
}
function cell(row,text) {row.insertCell().textContent=text;}
async function render() {
  const token=++revision;
  const body=document.createDocumentFragment();
  let index=0, more=false;
  for await (const r of filtered(token)) {
    if (index++<page*limit) continue;
    if (index>(page+1)*limit) {more=true;break;}
    const row=document.createElement('tr'); body.append(row);
    cell(row,[r.node,r.boot].filter(Boolean).join(' / '));
    cell(row,(r.observed || (r.reconstructed && r.reconstructed+' (reconstructed)') || 'UTC unknown')+
      (r.sequence ? ` · +${r.uptimeMs} ms · #${r.sequence}` : ''));
    cell(row,r.event);
    const details=document.createElement('details'), summary=document.createElement('summary'), code=document.createElement('code');
    summary.textContent=[r.source,r.packetId && 'id '+r.packetId,r.text||r.detail].filter(x=>x!==undefined).join(' · ');
    code.textContent=JSON.stringify(r);
    details.append(summary,code); row.insertCell().append(details);
  }
  if (token!==revision) return;
  $('rows').replaceChildren(body); $('prev').disabled=page===0; $('next').disabled=!more;
  $('status').textContent=`${segments.length} files · Page ${page+1} · ${$('rows').childElementCount} events`;
}
const columns=['file','node','boot','segment','event','sequence','uptimeMs','observed','reconstructed','clockSource','source',
  'packetId','related','detail','rssi','snr','text','raw','offset'];
async function exportFile(format) {
  const token=revision;
  if (!window.showSaveFilePicker) { $('status').textContent='Open this reader in a browser with streaming file saving, such as desktop Chrome or Edge.';return; }
  let out;
  try {
    const handle=await showSaveFilePicker({suggestedName:'meshlink-log.'+format});
    out=await handle.createWritable();
    await out.write(format==='csv' ? columns.join(',')+'\r\n' : '[\n');
    let count=0, buffer='';
    for await (const r of filtered(token)) {
      if (format==='json') buffer+=(count?',\n':'')+JSON.stringify(r);
      else buffer+=columns.map(k=>{
        let s=String(r[k]??''); if (/^[\s]*[=+@-]/.test(s) && typeof r[k]==='string') s="'"+s;
        return '"'+s.replaceAll('"','""')+'"';
      }).join(',')+'\r\n';
      if (buffer.length>=65536) {await out.write(buffer);buffer='';}
      count++;
    }
    if (revision!==token) throw Error('Selection changed during export');
    await out.write(buffer+(format==='json'?'\n]\n':''));await out.close();
    $('status').textContent=`Exported ${count} events.`;
  } catch(error) {if(out) await out.abort(); $('status').textContent=error.message;}
}
$('files').onchange=load; $('filters').onsubmit=e=>{e.preventDefault();page=0;render();};
$('prev').onclick=()=>{page--;render();}; $('next').onclick=()=>{page++;render();};
$('csv').onclick=()=>exportFile('csv'); $('json').onclick=()=>exportFile('json');
