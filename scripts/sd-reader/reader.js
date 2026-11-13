'use strict';
const Sml = (() => {
  const names = ['Unknown','Boot','Raw RX','Decoded','Duplicate','Local outbound','Router admission','TX start',
    'TX complete','MQTT envelope','MQTT queued','MQTT queue discard','MQTT publish result','Connectivity',
    'Record loss','Clock anchor','Eviction','Radio queue discard','MQTT intent'];
  const crcTable = Array.from({length:256}, (_, i) => {
    for (let j = 0; j < 8; j++) i = (i >>> 1) ^ (i & 1 ? 0xedb88320 : 0);
    return i >>> 0;
  });
  function crc(bytes, start, stop) {
    let c = -1;
    for (let i = start; i < stop; i++) c = (c >>> 8) ^ crcTable[(c ^ bytes[i]) & 255];
    return (~c) >>> 0;
  }
  const hex = n => n.toString(16).padStart(8, '0');
  const magic = (b,i) => String.fromCharCode(...b.subarray(i,i+4));
  function header(b) {
    if (b.length < 24) return null;
    const v = new DataView(b.buffer,b.byteOffset,b.byteLength);
    const u = i => v.getUint32(i,true);
    return magic(b,0) === 'SML1' && u(16) === 1 && u(8) && u(12) && u(20) === crc(b,0,20)
      ? {node:hex(u(4)),segment:u(8),boot:hex(u(12))} : null;
  }
  function* parse(b) {
    const meta = header(b);
    if (!meta) { yield {event:'Corruption',detail:'Invalid segment header'}; return; }
    const v = new DataView(b.buffer,b.byteOffset,b.byteLength);
    const u = i => v.getUint32(i,true);
    let pos=24, count=0, closed=false;
    while (pos < b.length) {
      const start=pos;
      const tag=magic(b,pos);
      if (tag === 'END1' && pos+12===b.length && u(pos+8)===crc(b,pos,pos+8)) {
        closed=true;
        if (u(pos+4)!==count) yield {...meta,event:'Corruption',detail:'Footer count mismatch',offset:pos};
        break;
      }
      if (tag === 'EVT1' && pos+52<=b.length) {
        const len=v.getUint16(pos+4,true), end=pos+48+len;
        if (len<=640 && end+4<=b.length && u(end)===crc(b,pos,end) && hex(u(pos+44))===meta.boot) {
          const kind=b[pos+6], utc=u(pos+20), payload=b.subarray(pos+48,end);
          const detail=v.getInt32(pos+36,true);
          yield {...meta, event:names[kind] || 'Unknown', sequence:u(pos+8), uptimeMs:Number(v.getBigUint64(pos+12,true)),
            observed:utc ? new Date(utc*1000).toISOString() : null, clockSource:b[pos+7], source:hex(u(pos+24)),
            packetId:u(pos+28),related:u(pos+32),detail,rssi:v.getInt16(pos+40,true),snr:v.getInt16(pos+42,true)/4,
            text:kind===1 || ((kind===3 || kind===5) && detail===1) ? new TextDecoder().decode(payload) : '',
            raw:Array.from(payload,c=>c.toString(16).padStart(2,'0')).join('')};
          count++; pos=end+4; continue;
        }
      }
      do {pos++;} while(pos < b.length && !(b[pos]===69 && ['EVT1','END1'].includes(magic(b,pos))));
      yield {...meta,event:'Corruption',offset:start,detail:`${pos-start} damaged bytes`};
    }
    if (!closed) yield {...meta,event:'Open tail',offset:pos,detail:'Missing close marker'};
  }
  return {parse,header,crc,names};
})();
if (typeof module !== 'undefined') module.exports = Sml;
