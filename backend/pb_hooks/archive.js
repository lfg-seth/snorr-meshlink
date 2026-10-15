const c = require(`${__hooks}/common.js`);
function archive(e) {
  c.worker(e);
  const b = e.requestInfo().body;
  if (typeof b.receiptId !== 'string' ||
      !/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(b.receiptId))
    throw new BadRequestError('Invalid archive receipt ID.');
  c.text(b.topic, 'MQTT topic', 65535);
  if (typeof b.receivedAt !== 'string' ||
      !/(Z|[+-]\d\d:\d\d)$/.test(b.receivedAt) || !isFinite(Date.parse(b.receivedAt)))
    throw new BadRequestError('Invalid archive receipt time.');
  if (typeof b.payloadBase64 !== 'string' ||
      !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(b.payloadBase64) ||
      !Number.isInteger(b.payloadBytes) || b.payloadBytes < 0 ||
      b.payloadBytes !== b.payloadBase64.length / 4 * 3 -
        (b.payloadBase64.endsWith('==') ? 2 : b.payloadBase64.endsWith('=') ? 1 : 0))
    throw new BadRequestError('Invalid archive payload.');
  if ([0, 1, 2].indexOf(b.qos) < 0 || typeof b.retained !== 'boolean' ||
      typeof b.duplicate !== 'boolean' ||
      ['normalized', 'unsupported', 'rejected', 'error'].indexOf(b.decodeOutcome) < 0)
    throw new BadRequestError('Invalid archive metadata.');
  const fields = ['receiptId', 'topic', 'receivedAt', 'qos', 'retained', 'duplicate',
    'payloadBase64', 'payloadBytes', 'decodeOutcome', 'decodeReason'];
  if (Object.keys(b).some((key) => fields.indexOf(key) < 0) ||
      (b.decodeReason !== undefined && (typeof b.decodeReason !== 'string' || b.decodeReason.length > 200)))
    throw new BadRequestError('Invalid archive fields.');
  let outcome = 'saved';
  e.app.runInTransaction((app) => {
    const existing = c.first(app, 'mqtt_archive', 'receiptId = {:id}', { id: b.receiptId });
    if (existing) {
      // Retries must match the original receipt, never replace its evidence.
      const original = c.object(existing, 'envelope');
      if (fields.some((key) => original[key] !== b[key]))
        throw new BadRequestError('Archive receipt ID already has different contents.');
      outcome = 'duplicate';
      return;
    }
    c.create(app, 'mqtt_archive', {
      receiptId: b.receiptId, topic: b.topic, receivedAt: b.receivedAt,
      ingestedAt: c.now(), envelope: b,
    });
  });
  return e.json(200, { outcome });
}
module.exports = { archive };
