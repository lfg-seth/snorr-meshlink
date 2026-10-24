const c = require(`${__hooks}/common.js`);

// Receipt is a telemetry fallback, never a replacement GPS measurement clock.
function at(reading) {
  return reading ? reading.measuredAt || reading.receivedAt || null : null;
}

function newer(reading, latest) {
  return !latest || at(reading) > at(latest);
}

function powerReadings(readings) {
  return Object.keys(readings).filter((metric) =>
    /^(sensor(Voltage|CurrentMa)|power[1-8](Voltage|CurrentMa))$/.test(metric))
    .map((metric) => {
      const reading = { metric, ...readings[metric] };
      if (metric.endsWith('CurrentMa')) {
        // All fleet sensors share owner-confirmed wiring: invert only at the
        // API boundary so cached/history/queued evidence retains its wire sign.
        reading.rawValue = reading.value;
        reading.value = reading.value === 0 ? 0 : -reading.value;
        reading.currentConvention = 'positive-charging';
      }
      return reading;
    });
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

// Match the card's source selection; never combine unmapped power channels.
function currentMetric(readings) {
  const channels = Object.keys(readings).filter(metric => /^power[1-8]CurrentMa$/.test(metric));
  if (channels.length) return channels.length === 1 && channels[0] === 'power1CurrentMa' ? channels[0] : null;
  return readings.sensorCurrentMa ? 'sensorCurrentMa' : null;
}

function currentHistory(app, deviceId, metric, cutoff, end, limit) {
  if (['power1CurrentMa', 'sensorCurrentMa'].indexOf(metric) < 0)
    return { samples: [], truncated: false };
  const params = { id: deviceId, cutoff, end };
  const filter = `deviceId = {:id} && payload.${metric} != null && `;
  const measured = c.rows(app, 'observations', filter +
    'measuredAt != "" && measuredAt >= {:cutoff} && measuredAt <= {:end}',
    '-measuredAt,-receivedAt,-id', params, limit + 1);
  const received = c.rows(app, 'observations', filter +
    'measuredAt = "" && receivedAt >= {:cutoff} && receivedAt <= {:end}',
    '-receivedAt,-id', params, limit + 1);
  const samples = measured.concat(received).map(o => {
    const rawValue = c.object(o, 'payload')[metric];
    return { at: o.getString('measuredAt') || o.getString('receivedAt'),
      milliamps: rawValue === 0 ? 0 : -rawValue, rawValue, metric,
      currentConvention: 'positive-charging', measuredAt: o.getString('measuredAt') || null,
      receivedAt: o.getString('receivedAt'), timestampQuality: o.getString('timestampQuality') };
  }).filter(s => typeof s.rawValue === 'number' && Number.isFinite(s.rawValue))
    .sort((a, b) => b.at.localeCompare(a.at) || b.receivedAt.localeCompare(a.receivedAt));
  const unique = [];
  const seen = new Set();
  samples.forEach(s => { if (!seen.has(s.at)) { seen.add(s.at); unique.push(s); } });
  return { samples: unique.slice(0, limit).reverse(),
    truncated: unique.length > limit || measured.length > limit || received.length > limit };
}

module.exports = { at, newer, powerReadings, batteryHistory, currentMetric, currentHistory };
