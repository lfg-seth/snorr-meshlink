const c = require(`${__hooks}/common.js`);

// Receipt is a telemetry fallback, never a replacement GPS measurement clock.
function at(reading) {
  return reading ? reading.measuredAt || reading.receivedAt || null : null;
}

function newer(reading, latest) {
  return !latest || at(reading) > at(latest);
}

function batteryHistory(app, deviceId, cutoff, end, limit) {
  const params = { id: deviceId, cutoff, end };
  const filter = 'deviceId = {:id} && payload.battery > 0 && ';
  const measured = c.rows(app, 'observations', filter +
    'measuredAt != "" && measuredAt >= {:cutoff} && measuredAt <= {:end}',
    '-measuredAt,-receivedAt,-id', params, limit + 1);
  const received = c.rows(app, 'observations', filter +
    'measuredAt = "" && receivedAt >= {:cutoff} && receivedAt <= {:end}',
    '-receivedAt,-id', params, limit + 1);
  const samples = measured.concat(received).map(o => ({
    at: o.getString('measuredAt') || o.getString('receivedAt'),
    volts: c.object(o, 'payload').battery,
    measuredAt: o.getString('measuredAt') || null,
    receivedAt: o.getString('receivedAt'),
    timestampQuality: o.getString('timestampQuality'),
  })).sort((a, b) => b.at.localeCompare(a.at) || b.receivedAt.localeCompare(a.receivedAt));
  return { samples: samples.slice(0, limit).reverse(), truncated: samples.length > limit };
}

module.exports = { at, newer, batteryHistory };
