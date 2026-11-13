'use strict';
const Sml = (() => {
  const names = ['Unknown','Boot','Raw RX','Decoded','Duplicate','Local outbound','Router admission','TX start',
    'TX complete','MQTT envelope','MQTT queued','MQTT queue discard','MQTT publish result','Connectivity',
    'Record loss','Clock anchor','Eviction','Radio queue discard','MQTT intent','TX queue eviction','USB Wi-Fi survey'];
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
  // Read the subset of protobuf wire types used by Meshtastic Data payloads.
  function fields(b) {
    const result=new Map(), v=new DataView(b.buffer,b.byteOffset,b.byteLength);
    let p=0;
    function varint() {
      let n=0n;
      for(let shift=0n;shift<70n && p<b.length;shift+=7n) {
        const x=b[p++]; n|=BigInt(x&127)<<shift;
        if(x<128)return Number(BigInt.asUintN(32,n));
      }
      throw Error('Invalid varint');
    }
    while(p<b.length) {
      const tag=varint(), field=tag>>>3, type=tag&7;
      if(!field)throw Error('Missing protobuf field');
      if(type===0)result.set(field,{integer:varint()});
      else if(type===5) {
        result.set(field,{integer:v.getUint32(p,true),float:v.getFloat32(p,true)});p+=4;
      } else if(type===2) {
        const size=varint();if(size>b.length-p)throw Error('Invalid field length');
        result.set(field,{bytes:b.subarray(p,p+size)});p+=size;
      } else if(type===1 && p+8<=b.length)p+=8;
      else throw Error('Unsupported wire type');
    }
    return result;
  }
  function decodeApplication(port,b) {
    try {
      if(port===256 && magic(b,0)==='SNWF' && b.length===36 && b[4]===1) {
        const v=new DataView(b.buffer,b.byteOffset,b.byteLength);
        return {type:'SNWF v1',state:['disconnected','unavailable','measured'][b[5]],rssiDbm:b[5]===2?v.getInt8(6):null,
          channel:b[7]||null,association:v.getUint32(32,true)||null,node:hex(v.getUint32(8,true)),boot:hex(v.getUint32(12,true)),
          sequence:v.getUint32(16,true),uptime:v.getUint32(20,true),sourceUtc:v.getUint32(24,true)||null,interval:v.getUint32(28,true)};
      }
      if(port===256 && magic(b,0)==='SNSD' && b.length===52 && b[4]===1) {
        const v=new DataView(b.buffer,b.byteOffset,b.byteLength);
        return {type:'SNSD v1',flags:b[5],clock:b[6],node:hex(v.getUint32(8,true)),boot:hex(v.getUint32(12,true)),
          sequence:v.getUint32(16,true),uptime:v.getUint32(20,true),sourceUtc:v.getUint32(24,true)||null,
          interval:v.getUint32(28,true),usedBytes:b[5]&8?v.getBigUint64(32,true).toString():null,
          totalBytes:b[5]&8?v.getBigUint64(40,true).toString():null,dropped:v.getUint32(48,true)};
      }
      if (port!==3 && port!==67) return null;
      const f=fields(b);
      if(port===3) {
        const coordinate=n=>f.has(n)?(f.get(n).integer|0)/1e7:null;
        const gps=f.get(7)?.integer,adjust=(f.get(8)?.integer||0)|0;
        return {type:'Position',latitude:coordinate(1),longitude:coordinate(2),packetUtc:f.get(4)?.integer||null,
          gpsMeasuredAt:gps && Math.abs(adjust)<=999?new Date(gps*1000+adjust).toISOString():null};
      }
      const result={type:'Telemetry',sourceTime:f.get(1)?.integer||null};
      for(const [group,labels] of [[2,['batteryPercent','voltage']], [3,['temperature','humidity',null,null,'voltage','currentMa']],
        [5,Array.from({length:16},(_,i)=>'ch'+(Math.floor(i/2)+1)+(i%2?'CurrentMa':'Voltage'))]]) {
        if(!f.get(group)?.bytes)continue;
        const nested=fields(f.get(group).bytes);
        labels.forEach((key,i)=>{const x=nested.get(i+1);if(key && x)result[key]=x.float??x.integer;});
      }
      return result;
    } catch {return {decodeError:'Malformed application payload'};}
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
            application:kind===20 && len===8 && payload[0]===1 ? {type:'USB Wi-Fi survey',state:['disconnected','unavailable','measured'][payload[1]],
              rssiDbm:payload[1]===2?v.getInt8(pos+50):null,channel:payload[3]||null,association:u(pos+52)||null} :
              kind===3 || kind===5 ? decodeApplication(detail,payload) : null,
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
