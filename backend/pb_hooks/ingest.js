const c = require(`${__hooks}/common.js`);
const health = require(`${__hooks}/health.js`);
function timestamp(value, now) {
  if (value === null || value === undefined || value === '')
    return { measuredAt: null, quality: 'unknown' };
  if (
    typeof value !== 'string' ||
    !/(Z|[+-]\d\d:\d\d)$/.test(value) ||
    !isFinite(Date.parse(value))
  )
    return { measuredAt: null, quality: 'invalid' };
  if (Date.parse(value) > now) return { measuredAt: null, quality: 'future' };
  return { measuredAt: new Date(value).toISOString(), quality: 'valid' };
}
function number(value, name, min, max) {
  if (
    typeof value !== 'number' ||
    !isFinite(value) ||
    value < min ||
    value > max
  )
    throw new BadRequestError(`Invalid ${name}.`);
  return value;
}
function ingest(e) {
  c.worker(e);
  const b = e.requestInfo().body;
  let outcome = 'accepted';
  let reason = '';
  let packetKey = '';
  // Validation failures still retain a bounded receipt; auth failures do not.
  e.app.runInTransaction((app) => {
    let device, data, time, receivedAt;
    try {
      c.text(b.packetId, 'packet ID', 80);
      c.text(b.deviceId, 'device ID', 80);
      c.text(b.gatewayId, 'gateway ID', 80);
      if (['position', 'telemetry', 'message'].indexOf(b.kind) < 0)
        throw new BadRequestError('Unknown normalized packet kind.');
      packetKey = `${b.kind}:${b.deviceId}:${b.packetId}`;
      device = c.device(app, b.deviceId);
      const gateway = c.device(app, b.gatewayId);
      if (gateway.getString('kind') !== 'backhaul')
        throw new BadRequestError(
          'Receipt gateway must be a provisioned backhaul.',
        );
      if (
        typeof b.receivedAt !== 'string' ||
        !/(Z|[+-]\d\d:\d\d)$/.test(b.receivedAt) ||
        !isFinite(Date.parse(b.receivedAt)) ||
        Date.parse(b.receivedAt) > Date.now()
      )
        throw new BadRequestError('Invalid receipt time.');
      receivedAt = new Date(b.receivedAt).toISOString();
      time = timestamp(b.measuredAt, Date.now());
      data = b.data;
      if (!data || typeof data !== 'object' || Array.isArray(data))
        throw new BadRequestError('Packet data must be an object.');
      if (b.kind === 'position') {
        if (device.getString('kind') !== 'member')
          throw new BadRequestError(
            'Only member trackers report member positions.',
          );
        number(data.longitude, 'longitude', -180, 180);
        number(data.latitude, 'latitude', -90, 90);
        if (data.battery !== null && data.battery !== undefined)
          number(data.battery, 'battery percent', 0, 100);
      }
      if (b.kind === 'telemetry') {
        if (device.getString('kind') === 'member')
          throw new BadRequestError(
            'Infrastructure telemetry requires an infrastructure device.',
          );
        const keys = Object.keys(data);
        if (
          !keys.length ||
          keys.some(
            (key) =>
              ['battery', 'temperature', 'humidity', 'solar', 'intrusion'].indexOf(key) < 0,
          )
        )
          throw new BadRequestError('Unknown or empty telemetry metrics.');
        keys.forEach((key) => {
          if (key === 'intrusion') {
            if (typeof data[key] !== 'boolean')
              throw new BadRequestError('Intrusion must be boolean.');
          } else
            number(
              data[key],
              key,
              key === 'temperature' ? -100 : 0,
              key === 'temperature' ? 150 : key === 'humidity' ? 100 : 10000,
            );
        });
      }
      if (b.kind === 'message') {
        c.text(data.text, 'inbound text', 400);
        c.text(data.author, 'reported author', 80);
      }
    } catch (error) {
      outcome = 'rejected';
      reason = error.message || 'Packet rejected.';
    }
    const collection =
      b.kind === 'position'
        ? 'positions'
        : b.kind === 'telemetry'
          ? 'observations'
          : 'messages';
    const existing =
      outcome === 'accepted'
        ? c.first(app, collection, 'packetKey = {:key}', { key: packetKey })
        : null;
    if (existing) outcome = 'duplicate';
    c.create(app, 'packet_receipts', {
      packetKey,
      deviceId: typeof b.deviceId === 'string' ? b.deviceId.slice(0, 80) : '',
      gatewayId:
        typeof b.gatewayId === 'string' ? b.gatewayId.slice(0, 80) : '',
      receivedAt: receivedAt || c.now(),
      ingestedAt: c.now(),
      outcome,
      reason,
      payload: b,
    });
    if (outcome === 'rejected') return;
    // Contact is not GPS freshness; duplicate receipts may update contact only.
    if (
      !device.getString('lastContactAt') ||
      receivedAt > device.getString('lastContactAt')
    ) {
      device.set('lastContactAt', receivedAt);
      app.save(device);
    }
    if (outcome === 'duplicate') return;
    if (b.kind === 'position') {
      const position = {
        longitude: data.longitude,
        latitude: data.latitude,
        battery: data.battery === undefined ? null : data.battery,
        measuredAt: time.measuredAt,
        receivedAt,
        timestampQuality: time.quality,
      };
      c.create(app, 'positions', {
        packetKey,
        deviceId: b.deviceId,
        memberId: c.memberAt(app, b.deviceId, time.measuredAt),
        measuredAt: time.measuredAt || '',
        timestampQuality: time.quality,
        receivedAt,
        payload: position,
      });
      const latest = c.object(device, 'latestPosition');
      const newer =
        time.measuredAt &&
        (!latest.measuredAt || time.measuredAt > latest.measuredAt);
      if (newer || latest.longitude === undefined) {
        device.set('latestPosition', position);
        app.save(device);
      }
    } else if (b.kind === 'telemetry') {
      c.create(app, 'observations', {
        packetKey,
        deviceId: b.deviceId,
        measuredAt: time.measuredAt || '',
        timestampQuality: time.quality,
        receivedAt,
        payload: data,
      });
      const readings = c.object(device, 'readings');
      const config = c.object(device, 'configuration');
      Object.keys(data).forEach((metric) => {
        const supported =
          metric === 'battery' ||
          (config.equipped || {})[
            { solar: 'solar', temperature: 'weather', humidity: 'weather', intrusion: 'intrusion' }[
              metric
            ]
          ];
        if (!supported) return;
        const latest = readings[metric];
        if (
          !latest ||
          (!latest.measuredAt && !time.measuredAt && time.quality === 'unknown' &&
            receivedAt > latest.receivedAt) ||
          (time.measuredAt &&
            (!latest.measuredAt || time.measuredAt > latest.measuredAt))
        )
          readings[metric] = {
            value: data[metric],
            measuredAt: time.measuredAt,
            receivedAt,
            timestampQuality: time.quality,
          };
      });
      device.set('readings', readings);
      app.save(device);
      if (
        config.equipped &&
        config.equipped.intrusion &&
        data.intrusion === true
      ) {
        let incident = c.first(
          app,
          'incidents',
          'deviceId = {:id} && resolvedAt = ""',
          { id: b.deviceId },
        );
        if (!incident)
          incident = c.create(app, 'incidents', {
            deviceId: b.deviceId,
            openedAt: c.now(),
          });
        c.event(
          app,
          b.deviceId,
          'Reported intrusion recorded on the open incident.',
        );
      }
      health.evaluate(app);
    } else {
      c.create(app, 'messages', {
        packetKey,
        author: data.author,
        text: data.text,
        at: time.measuredAt || receivedAt,
        direction: 'inbound',
        evidence: c.simulation()
          ? 'Simulated inbound · reported author'
          : 'Received packet · reported author, human receipt unconfirmed',
      });
    }
  });
  return e.json(outcome === 'rejected' ? 400 : 200, { outcome, reason });
}
module.exports = { ingest };
