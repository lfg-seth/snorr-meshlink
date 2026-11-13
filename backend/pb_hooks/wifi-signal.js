const c = require(`${__hooks}/common.js`);
const fields = ['bootId','sequence','uptimeSeconds','intervalSeconds','state','rssiDbm','channel','association'];
const uint = n => Number.isInteger(n) && n >= 0 && n <= 4294967295;

function validate(device, b, time) {
  const d = b.data;
  if (device.getString('kind') !== 'backhaul' || Object.keys(d).length !== fields.length ||
      fields.some(k => d[k] === undefined) || ![d.bootId,d.sequence,d.uptimeSeconds,d.intervalSeconds].every(uint) ||
      !d.bootId || !d.sequence || !d.intervalSeconds || d.intervalSeconds > 4294967 ||
      !['measured','disconnected','unavailable'].includes(d.state) ||
      !(b.measuredAt === null || ['valid','future'].includes(time.quality)) ||
      b.packetId !== [d.bootId,d.sequence].map(v => v.toString(16).padStart(8,'0')).join('-') ||
      (d.state === 'measured' ? !Number.isInteger(d.rssiDbm) || d.rssiDbm < -128 || d.rssiDbm > 127 ||
        !Number.isInteger(d.channel) || d.channel < 1 || d.channel > 14 || !uint(d.association) || !d.association :
        [d.rssiDbm,d.channel,d.association].some(v => v !== null)))
    throw new BadRequestError('Invalid Wi-Fi signal report.');
}

function matches(existing,b) {
  const d = c.object(existing,'payload');
  return d.sourceUtc === b.measuredAt && fields.every(k => d[k] === b.data[k]);
}

function save(app,device,packetKey,b,receivedAt,time) {
  const d = b.data, readings = c.object(device,'readings'), old = readings.wifiSignal;
  const valid = time.quality === 'valid';
  // Sequence restarts on reboot. Across boots use trusted source time, never replay time.
  const newer = !old || (old.bootId === d.bootId ? d.sequence > old.sequence :
    valid && (!old.measuredAt || time.measuredAt > old.measuredAt));
  const retired = old && d.bootId !== old.bootId && c.first(app,'observations',
    'deviceId = {:id} && payload.bootId = {:boot} && payload.wifiApplied = true',{id:b.deviceId,boot:d.bootId});
  const apply = newer && !retired && (valid ? !old?.measuredAt || time.measuredAt >= old.measuredAt :
    time.quality === 'unknown' && !old?.measuredAt);
  c.create(app,'observations',{packetKey,deviceId:b.deviceId,measuredAt:time.measuredAt || '',
    timestampQuality:time.quality,receivedAt,payload:{...d,sourceUtc:b.measuredAt,wifiApplied:!!apply}});
  if (apply) {
    readings.wifiSignal = {...d,measuredAt:time.measuredAt,receivedAt};
    device.set('readings',readings);
    app.save(device);
  }
}

module.exports = {validate,matches,save};
