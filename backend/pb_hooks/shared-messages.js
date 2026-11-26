const c = require(`${__hooks}/common.js`);
const limit = 233;
const evidence = {
  unknown: 'Publish outcome unknown · check the radios before composing another reply',
  not_sent: 'Publish did not start · draft can be sent manually',
  rejected: 'Broker rejected the publish · radio receipt unconfirmed',
  broker_accepted: 'Broker accepted · radio delivery and human receipt unconfirmed',
};

function heartbeat(e) {
  c.worker(e);
  const b = e.requestInfo().body;
  if (c.simulation() || typeof b.connected !== 'boolean' || typeof b.ready !== 'boolean')
    throw new BadRequestError('Invalid channel heartbeat.');
  // Process-local evidence expires on an API restart. Legacy GPS owns its separate feed row.
  e.app.store().set('channelHeartbeat', JSON.stringify({
    gatewayId: c.text(b.gatewayId, 'gateway', 80), connected: b.connected,
    ready: b.ready && b.connected, until: Date.now() + 20000,
  }));
  return e.json(200, {saved: true});
}

function availability(app) {
  const h = JSON.parse(app.store().get('channelHeartbeat') || '{}');
  const connected = h.connected === true && h.until > Date.now();
  let ready = false;
  if (connected && h.ready && $os.getenv('MESHLINK_DISPATCH_PYTHON')) {
    const designated = c.rows(app, 'devices', 'kind = "backhaul"')
      .filter(d => c.object(d, 'configuration').downlink === true);
    ready = designated.length === 1 && designated[0].getString('key') === h.gatewayId &&
      c.object(designated[0], 'configuration').radioNodeId === '!9ea13cc0';
  }
  return {connected, ready, until: ready ? h.until : 0, gatewayId: h.gatewayId || ''};
}

function prefix(app, auth) {
  const member = c.first(app, 'members', 'key = {:key}', {key: auth.getString('memberId')});
  return (member && member.getString('shortName')) || auth.getString('name');
}

function send(e) {
  const b = e.requestInfo().body;
  const text = c.text(b.text, 'message', 280);
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(b.requestId || ''))
    throw new BadRequestError('A manual send ID is required.');
  const requestKey = e.auth.id + '/' + b.requestId;
  let attempt, wire, packetId, expiresAt, created = false;
  // Commit the one-use reservation BEFORE any external I/O. Nothing scans or replays attempts.
  e.app.runInTransaction(app => {
    attempt = c.first(app, 'send_attempts', 'requestKey = {:key}', {key: requestKey});
    if (attempt) {
      if (attempt.getString('requestText') !== text)
        throw new ApiError(409, 'This send ID belongs to a different reply.');
      return;
    }
    const path = availability(app);
    if (!path.ready || !Number.isSafeInteger(b.until) || b.until <= Date.now() || b.until > path.until)
      throw new ApiError(409, 'Dispatch is unavailable. Keep the draft and send manually after recovery.');
    const author = prefix(app, e.auth);
    wire = author + ': ' + text;
    if (wire.includes('\0') || toBytes(wire).length > limit)
      throw new BadRequestError('The attributed radio text must fit in 233 UTF-8 bytes.');
    packetId = $security.randomStringWithAlphabet(8, '0123456789abcdef');
    if (packetId === '00000000') throw new ApiError(503, 'Try sending again.');
    const at = c.now();
    const message = c.create(app, 'messages', {
      packetKey: 'dispatch:' + packetId, authorId: e.auth.id, author, text: wire,
      at, direction: 'outbound', evidence: evidence.unknown,
    });
    attempt = c.create(app, 'send_attempts', {
      messageId: message.id, gatewayId: path.gatewayId, requestKey, requestText: text,
      at, status: 'unknown',
    });
    expiresAt = Math.min(b.until, Date.now() + 10000);
    created = true;
  });
  let status = attempt.getString('status');
  if (created) {
    try {
      const cmd = $os.cmd($os.getenv('MESHLINK_DISPATCH_PYTHON'), `${__hooks}/../mqtt_dispatch.py`);
      const input = cmd.stdinPipe();
      input.write(toBytes(JSON.stringify({packetId, text: wire, expiresAt})));
      input.close();
      const result = toString(cmd.output()).trim();
      if (Object.prototype.hasOwnProperty.call(evidence, result)) status = result;
    } catch {
      // Includes process termination or a lost result after a successful publish.
    }
    e.app.runInTransaction(app => {
      const message = app.findRecordById('messages', attempt.getString('messageId'));
      attempt.set('status', status);
      message.set('evidence', evidence[status]);
      app.save(attempt);
      app.save(message);
    });
  }
  return e.json(created ? 201 : 200, {id: attempt.getString('messageId'), status});
}

function radioAuthor(app, device, source, receivedAt) {
  if (!device) return 'Unknown radio ' + source;
  const label = device.getString('number') || device.getString('shortName') || source;
  if (device.getString('kind') !== 'member') return label + ' · ' + source;
  const id = c.memberAt(app, device.getString('key'), receivedAt);
  const member = id && c.first(app, 'members', 'key = {:id}', {id});
  return (member ? member.getString('name') : 'Unassigned') + ' · ' + label + ' · ' + source;
}

module.exports = {availability, heartbeat, prefix, radioAuthor, send};
