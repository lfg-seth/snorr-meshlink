const {test}=require('node:test');
const assert=require('node:assert/strict');
const Sml=require('./reader.js');
function block(tag,len,fill) {
  const b=Buffer.alloc(len);b.write(tag);fill(b);
  b.writeUInt32LE(Sml.crc(b,0,len-4),len-4);return b;
}
const header=block('SML1',24,b=>{[123,1,42,1].forEach((n,i)=>b.writeUInt32LE(n,4+i*4));});
function entry(kind,seq,payload,related=0) {
  return block('EVT1',52+payload.length,b=>{
    b.writeUInt16LE(payload.length,4);b[6]=kind;b.writeUInt32LE(seq,8);
    b.writeBigUInt64LE(BigInt(seq)*100n,12);b.writeUInt32LE(123,24);b.writeUInt32LE(7,28);
    b.writeUInt32LE(related,32);b.writeUInt32LE(1,36);b.writeUInt32LE(42,44);payload.copy(b,48);
  });
}
test('equal packet IDs keep independent raw receptions and linked outcomes; corruption resynchronizes',()=>{
  const raw=Buffer.from([255,16,19]);
  const unsafe=Buffer.from('<img src=x onerror=alert(1)>');
  const b=Buffer.concat([header,entry(2,1,raw),entry(3,2,unsafe,1),Buffer.from('damaged!'),
    entry(2,3,raw),entry(4,4,Buffer.alloc(0),3),entry(5,5,unsafe),entry(12,6,Buffer.alloc(0))]);
  const rows=Array.from(Sml.parse(b));
  assert.deepEqual(rows.filter(x=>x.event==='Raw RX').map(x=>x.sequence),[1,3]);
  assert.equal(rows[1].text,unsafe.toString());assert.equal(rows[1].related,1);
  assert.equal(rows[2].event,'Corruption');assert.equal(rows[4].related,3);
  assert.equal(rows.at(-1).event,'Open tail');assert.equal(rows[0].observed,null);
});
test('scan multi-month segments without accumulating records',()=>{
  const event=entry(2,1,Buffer.alloc(600));
  const events=Array(1000).fill(event);
  const footer=block('END1',12,b=>b.writeUInt32LE(events.length,4));
  const segment=Buffer.concat([header,...events,footer]);
  let count=0;
  for(let day=0;day<182;day++) for (const row of Sml.parse(segment)) if(row.event==='Raw RX')count++;
  assert.equal(count,182000);
});
