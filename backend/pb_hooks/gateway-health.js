const c = require(`${__hooks}/common.js`);

function validate(device, data) {
  if (device.getString('kind') !== 'backhaul') throw new BadRequestError('Gateway health requires a provisioned backhaul.');
  const keys = ['bootId', 'sequence', 'uptimeSeconds', 'intervalSeconds', 'wifiConnected', 'mqttConnected'];
  if (Object.keys(data).length !== keys.length || keys.some(k => data[k] === undefined))
    throw new BadRequestError('Invalid gateway health fields.');
  for (const k of keys.slice(0, 4)) {
    if (!Number.isInteger(data[k]) || data[k] < (k === 'uptimeSeconds' ? 0 : k === 'intervalSeconds' ? 180 : 1) || data[k] > (k === 'intervalSeconds' ? 2147468 : 4294967295))
      throw new BadRequestError('Invalid gateway health counter.');
  }
  if (typeof data.wifiConnected !== 'boolean' || typeof data.mqttConnected !== 'boolean' || (!data.wifiConnected && data.mqttConnected))
    throw new BadRequestError('Invalid gateway connectivity flags.');
}

function save(app, device, packetKey, b, receivedAt, time) {
  const readings = c.object(device, 'readings');
  const latest = readings.gatewayHealth;
  const data = b.data;
  // Archive every generation, but only a newer, clocked report changes health.
  const seenBoot = latest && latest.bootId !== data.bootId && c.first(app, 'observations',
    'deviceId = {:id} && payload.bootId = {:boot} && payload.gatewayHealthApplied = true', { id: b.deviceId, boot: data.bootId });
  const current = time.quality === 'valid' && Date.parse(receivedAt) - Date.parse(time.measuredAt) < data.intervalSeconds * 3000;
  const newer = !latest || (time.measuredAt > latest.measuredAt &&
    (latest.bootId !== data.bootId || data.sequence > latest.sequence));
  c.create(app, 'observations', { packetKey, deviceId: b.deviceId, measuredAt: time.measuredAt || '',
    timestampQuality: time.quality, receivedAt, payload: { ...data, gatewayHealthApplied: !!(current && newer && !seenBoot) } });
  if (!current || !newer || seenBoot) return;
  readings.gatewayHealth = { ...data, measuredAt: time.measuredAt, receivedAt, transportGatewayId: b.gatewayId,
    radioReceivedAt: b.gatewayId !== b.deviceId ? time.measuredAt : null };
  device.set('readings', readings);
  app.save(device);
}

function duplicate(app, device, b, receivedAt, time) {
  const readings = c.object(device, 'readings');
  const latest = readings.gatewayHealth;
  if (!latest || latest.bootId !== b.data.bootId || latest.sequence !== b.data.sequence ||
      time.measuredAt !== latest.measuredAt || b.gatewayId === b.deviceId) return;
  latest.radioReceivedAt = latest.measuredAt;
  latest.transportGatewayId = b.gatewayId;
  device.set('readings', readings);
  app.save(device);
}

function status(device, now = Date.now()) {
  const report = c.object(device, 'readings').gatewayHealth;
  if (!report) return { state: 'unknown', label: 'Awaiting gateway health report' };
  const fresh = now - Date.parse(report.measuredAt) < report.intervalSeconds * 3000;
  const radioAlive = !!report.radioReceivedAt && now - Date.parse(report.radioReceivedAt) < report.intervalSeconds * 3000;
  const state = !fresh ? 'stale' : !report.wifiConnected ? 'wifi-lost' : !report.mqttConnected ? 'mqtt-lost' : 'online';
  const label = state === 'stale' ? 'Gateway health stale' : state === 'wifi-lost' ? 'Wi-Fi disconnected' :
    state === 'mqtt-lost' ? 'MQTT disconnected' : 'Wi-Fi and MQTT connected';
  return { ...report, state, label, radioAlive };
}

function evaluate(app, device) {
  const current = status(device);
  const id = device.getString('key');
  const warning = c.first(app, 'warnings', 'deviceId = {:id} && kind = "backhaul" && recoveredAt = ""', { id });
  if ((current.state === 'wifi-lost' || current.state === 'mqtt-lost') && !warning) {
    c.create(app, 'warnings', { deviceId: id, kind: 'backhaul', openedAt: c.now() });
    c.event(app, id, `Backhaul unavailable: ${current.label}.`);
  } else if (current.state === 'online' && warning) {
    warning.set('recoveredAt', c.now());
    app.save(warning);
    c.event(app, id, 'Backhaul recovered on a fresh gateway health report.');
  }
}

module.exports = { validate, save, duplicate, status, evaluate };
