const c = require(`${__hooks}/common.js`);
const fields = ['bootId', 'sequence', 'uptimeSeconds', 'intervalSeconds', 'clockSource', 'flags', 'usedBytes', 'totalBytes', 'dropped'];
const uint32 = n => Number.isInteger(n) && n >= 0 && n <= 4294967295;
// The hooks runtime and JSON transport must retain all 64 bits.
const lessOrEqual = (a, b) => a.length === b.length ? a <= b : a.length < b.length;
const bytes = s => typeof s === 'string' && /^(0|[1-9][0-9]{0,19})$/.test(s) && lessOrEqual(s, '18446744073709551615');

function validate(device, b, time) {
  const d = b.data;
  if (device.getString('kind') !== 'backhaul' || Object.keys(d).length !== fields.length ||
      fields.some(k => d[k] === undefined) || ![d.bootId, d.sequence, d.uptimeSeconds, d.dropped].every(uint32) ||
      !d.bootId || !d.sequence || !uint32(d.intervalSeconds) || d.intervalSeconds < 180 || d.intervalSeconds > 2147468 ||
      ![0, 2, 3, 4].includes(d.clockSource) ||
      ![0, 1, 3, 7, 11, 15].includes(d.flags) ||
      (d.clockSource ? !['valid', 'future'].includes(time.quality) : b.measuredAt !== null) ||
      b.packetId !== [d.bootId, d.sequence].map(v => v.toString(16).padStart(8, '0')).join('-'))
    throw new BadRequestError('Invalid SD report or generation identity.');
  if (d.flags & 8 ? !bytes(d.usedBytes) || !bytes(d.totalBytes) || d.totalBytes === '0' ||
      !lessOrEqual(d.usedBytes, d.totalBytes) : d.usedBytes !== null || d.totalBytes !== null)
    throw new BadRequestError('Invalid mounted filesystem capacity.');
}

function matches(existing, b, time) {
  const prior = c.object(existing, 'payload');
  return prior.sourceUtc === b.measuredAt && fields.every(k => prior[k] === b.data[k]);
}

function save(app, device, packetKey, b, receivedAt, time) {
  const d = b.data;
  const readings = c.object(device, 'readings');
  const latest = readings.sdHealth;
  const valid = time.quality === 'valid';
  // Sequence is reserved in NVS across boots. An unknown clock cannot refresh
  // a clocked reading. A new identity after NVS reset needs a later source time.
  const newer = !latest || (d.bootId === latest.bootId ? d.sequence > latest.sequence :
    d.sequence > latest.sequence || (valid && latest.measuredAt && time.measuredAt > latest.measuredAt));
  const oldBoot = latest && latest.bootId !== d.bootId && c.first(app, 'observations',
    'deviceId = {:id} && payload.bootId = {:boot} && payload.sdApplied = true', {id: b.deviceId, boot: d.bootId});
  const apply = newer && !oldBoot && (valid ? !latest || !latest.measuredAt || time.measuredAt >= latest.measuredAt :
    time.quality === 'unknown' && (!latest || !latest.measuredAt && d.sequence > latest.sequence));
  c.create(app, 'observations', { packetKey, deviceId: b.deviceId, measuredAt: time.measuredAt || '',
    timestampQuality: time.quality, receivedAt, payload: {...d, sourceUtc: b.measuredAt, sdApplied: !!apply} });
  if (apply) {
    readings.sdHealth = {...d, measuredAt: time.measuredAt, receivedAt};
    device.set('readings', readings);
    app.save(device);
  }
}

module.exports = {validate, matches, save};
