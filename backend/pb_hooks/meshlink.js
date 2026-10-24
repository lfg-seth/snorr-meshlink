const c = require(`${__hooks}/common.js`);
const health = require(`${__hooks}/health.js`);
const telemetry = require(`${__hooks}/telemetry.js`);
const neighborCurrent = require(`${__hooks}/neighbor_current.js`);
function assign(e) {
  c.human(e);
  const body = e.requestInfo().body;
  const deviceId = c.text(body.deviceId, 'device');
  const memberId = c.text(body.memberId, 'member');
  const isAdmin = e.auth.getString('role') === 'admin';
  if (!isAdmin && memberId !== e.auth.getString('memberId'))
    throw new ForbiddenError('Members may only claim for themselves.');
  e.app.runInTransaction((app) => {
    const device = c.device(app, deviceId);
    if (device.getString('kind') !== 'member')
      throw new BadRequestError('Only member trackers can be assigned.');
    const member = c.first(app, 'members', 'key = {:id}', { id: memberId });
    if (!member) throw new NotFoundError('Member not found.');
    const conflicts = c.rows(
      app,
      'assignments',
      'endedAt = "" && (deviceId = {:device} || memberId = {:member})',
      '',
      { device: deviceId, member: memberId },
    );
    if (
      conflicts.length === 1 &&
      conflicts[0].getString('deviceId') === deviceId &&
      conflicts[0].getString('memberId') === memberId
    )
      return;
    if (!isAdmin && conflicts.length)
      throw new ApiError(
        409,
        'Release your current tracker and choose an unassigned device.',
      );
    const at = c.now();
    conflicts.forEach((a) => {
      a.set('endedAt', at);
      app.save(a);
      if (a.getString('deviceId') !== deviceId) {
        const previous = c.device(app, a.getString('deviceId'));
        c.job(
          app,
          previous.getString('key'),
          `release-${a.id}`,
          `Device [${previous.getString('number')}]`,
        );
      }
    });
    const assignment = c.create(app, 'assignments', {
      deviceId,
      memberId,
      startedAt: at,
      actorId: e.auth.id,
    });
    c.job(
      app,
      deviceId,
      assignment.id,
      `${member.getString('name')} [${device.getString('number')}]`,
    );
    c.event(app, deviceId, 'Dated tracker assignment recorded.', e.auth.id);
  });
  return e.json(200, { saved: true });
}
function release(e) {
  c.human(e);
  const id = c.text(e.requestInfo().body.deviceId, 'device');
  e.app.runInTransaction((app) => {
    const assignment = c.currentAssignment(app, id);
    if (!assignment) return;
    if (
      e.auth.getString('role') !== 'admin' &&
      assignment.getString('memberId') !== e.auth.getString('memberId')
    )
      throw new ForbiddenError('You may release only your own tracker.');
    assignment.set('endedAt', c.now());
    app.save(assignment);
    const device = c.device(app, id);
    c.job(
      app,
      id,
      `release-${assignment.id}`,
      `Device [${device.getString('number')}]`,
    );
    c.event(
      app,
      id,
      'Tracker released; prior assignment history preserved.',
      e.auth.id,
    );
  });
  return e.json(200, { saved: true });
}
function send(e) {
  c.human(e);
  c.demo();
  const text = c.text(e.requestInfo().body.text, 'message', 280);
  let message;
  e.app.runInTransaction((app) => {
    if (!c.online(c.feed(app)))
      throw new ApiError(
        409,
        'The feed is unavailable. Keep the draft and send manually after recovery.',
      );
    const gateway = c.first(app, 'devices', 'kind = "backhaul"', {});
    const designated = c
      .rows(app, 'devices', 'kind = "backhaul"')
      .filter((d) => c.object(d, 'configuration').downlink === true);
    if (!gateway || designated.length !== 1)
      throw new ApiError(
        409,
        'Exactly one designated downlink gateway must be configured.',
      );
    const author = e.auth.getString('name');
    message = c.create(app, 'messages', {
      authorId: e.auth.id,
      author,
      text: `${author}: ${text}`,
      at: c.now(),
      direction: 'outbound',
      evidence:
        'Simulated gateway submission · radio and human receipt unconfirmed',
    });
    c.create(app, 'send_attempts', {
      messageId: message.id,
      gatewayId: designated[0].getString('key'),
      at: c.now(),
      status: 'simulated_submitted',
    });
  });
  return e.json(201, { id: message.id });
}
function rule(e) {
  c.admin(e);
  const b = e.requestInfo().body;
  const id = c.text(b.deviceId, 'device');
  if (
    typeof b.trigger !== 'number' ||
    typeof b.recovery !== 'number' ||
    !isFinite(b.trigger) ||
    !isFinite(b.recovery) ||
    b.trigger <= 0 ||
    b.recovery <= b.trigger
  )
    throw new BadRequestError(
      'Recovery must exceed a positive trigger voltage.',
    );
  e.app.runInTransaction((app) => {
    if (id !== '*' && c.device(app, id).getString('kind') === 'member')
      throw new BadRequestError('Infrastructure device required.');
    let record = c.first(app, 'rules', 'deviceId = {:id}', { id });
    const payload = {
      trigger: b.trigger,
      recovery: b.recovery,
      enabled: b.enabled !== false,
    };
    if (!record) c.create(app, 'rules', { deviceId: id, payload });
    else {
      record.set('payload', payload);
      app.save(record);
    }
    c.event(
      app,
      id,
      `Battery thresholds configured: ${b.trigger} V trigger / ${b.recovery} V recovery.`,
      e.auth.id,
    );
    health.evaluate(app);
  });
  return e.json(200, { saved: true });
}
function incident(e) {
  c.human(e);
  const b = e.requestInfo().body;
  const id = e.request.pathValue('id');
  if (b.action !== 'acknowledge' && b.action !== 'resolve')
    throw new BadRequestError('Unknown incident action.');
  if (b.action === 'resolve') c.admin(e);
  const note =
    b.action === 'resolve' ? c.text(b.note, 'resolution note', 400) : '';
  e.app.runInTransaction((app) => {
    const incident = app.findRecordById('incidents', id);
    if (incident.getString('resolvedAt'))
      throw new ApiError(409, 'Incident is already resolved.');
    if (note) {
      incident.set('resolvedAt', c.now());
      incident.set('resolvedBy', e.auth.id);
      incident.set('note', note);
    } else {
      incident.set('acknowledgedAt', c.now());
      incident.set('acknowledgedBy', e.auth.id);
    }
    app.save(incident);
    c.event(
      app,
      incident.getString('deviceId'),
      note
        ? `Intrusion resolved: ${note}`
        : 'Intrusion acknowledged; incident remains open.',
      e.auth.id,
    );
  });
  return e.json(200, { saved: true });
}
function ackWarning(e) {
  c.human(e);
  e.app.runInTransaction((app) => {
    const warning = app.findRecordById('warnings', e.request.pathValue('id'));
    warning.set('acknowledgedAt', c.now());
    warning.set('acknowledgedBy', e.auth.id);
    app.save(warning);
    c.event(
      app,
      warning.getString('deviceId'),
      `${warning.getString('kind')} warning acknowledged; recovery remains separate.`,
      e.auth.id,
    );
  });
  return e.json(200, { saved: true });
}
function configuration(e) {
  c.admin(e);
  const b = e.requestInfo().body;
  const id = c.text(b.deviceId, 'device');
  const metrics = ['battery', 'solar', 'temperature', 'humidity', 'intrusion'];
  const config = b.configuration;
  if (!config || typeof config !== 'object' || Array.isArray(config))
    throw new BadRequestError('Configuration must be an object.');
  if (
    config.cadenceMinutes !== undefined &&
    (typeof config.cadenceMinutes !== 'number' ||
      !isFinite(config.cadenceMinutes) ||
      config.cadenceMinutes <= 0)
  )
    throw new BadRequestError('Expected cadence must be positive minutes.');
  ['reportCadenceMinutes', 'missingTimeoutMinutes'].forEach((field) => {
    if (config[field] === undefined) return;
    if (
      !config[field] ||
      typeof config[field] !== 'object' ||
      Array.isArray(config[field])
    )
      throw new BadRequestError('Invalid reporting configuration.');
    Object.keys(config[field]).forEach((metric) => {
      if (
        metrics.indexOf(metric) < 0 ||
        typeof config[field][metric] !== 'number' ||
        !isFinite(config[field][metric]) ||
        config[field][metric] <= 0
      )
        throw new BadRequestError(
          'Report timeouts must be positive minutes for supported metrics.',
        );
    });
  });
  if (
    config.disabledMonitoring !== undefined &&
    (!Array.isArray(config.disabledMonitoring) ||
      config.disabledMonitoring.some((metric) => metrics.indexOf(metric) < 0))
  )
    throw new BadRequestError('Invalid disabled monitoring list.');
  if (config.batteryProfile !== undefined &&
      ['unknown', 'lipo-1s', 'eve-26v-1s'].indexOf(config.batteryProfile) < 0)
    throw new BadRequestError('Unknown battery profile.');
  if (config.batteryCapacityMah !== undefined && config.batteryCapacityMah !== null &&
      (!Number.isInteger(config.batteryCapacityMah) || config.batteryCapacityMah <= 0 ||
       config.batteryCapacityMah > 1000000))
    throw new BadRequestError('Battery capacity must be positive whole mAh or unknown.');
  const allowed = [
    'batteryProfile',
    'batteryCapacityMah',
    'cadenceMinutes',
    'reportCadenceMinutes',
    'missingTimeoutMinutes',
    'disabledMonitoring',
  ];
  if (Object.keys(config).some((key) => allowed.indexOf(key) < 0))
    throw new BadRequestError(
      'Only battery and reporting settings can be changed through this route.',
    );
  e.app.runInTransaction((app) => {
    const device = c.device(app, id);
    if (device.getString('kind') === 'member' &&
        Object.keys(config).some((key) => ['batteryProfile', 'batteryCapacityMah'].indexOf(key) < 0))
      throw new BadRequestError('Member configuration supports battery type and capacity only.');
    const previous = c.object(device, 'configuration');
    const enabledTimes = previous.monitoringStartedAtByMetric || {};
    if (config.disabledMonitoring)
      (previous.disabledMonitoring || []).forEach((metric) => {
        if (config.disabledMonitoring.indexOf(metric) < 0)
          enabledTimes[metric] = c.now();
      });
    device.set('configuration', {
      ...previous,
      ...config,
      monitoringStartedAtByMetric: enabledTimes,
    });
    app.save(device);
    c.event(
      app,
      id,
      'Device battery/reporting configuration changed; warning history retained.',
      e.auth.id,
    );
    health.evaluate(app);
  });
  return e.json(200, { saved: true });
}
function account(e) {
  c.admin(e);
  const b = e.requestInfo().body;
  const username = c.text(b.username, 'username', 80);
  const name = c.text(b.name, 'display name', 80);
  if (!/^[a-zA-Z0-9_.-]+$/.test(username))
    throw new BadRequestError(
      'Username may contain letters, digits, dots, underscores and dashes.',
    );
  const password = c.text(b.password, 'password', 200);
  if (password.length < 12)
    throw new BadRequestError(
      'Use at least 12 characters for the initial password.',
    );
  if (b.role !== 'admin' && b.role !== 'member')
    throw new BadRequestError(
      'Choose admin or member. Worker credentials are provisioned locally.',
    );
  const memberId = typeof b.memberId === 'string' ? b.memberId : '';
  if (memberId && !c.first(e.app, 'members', 'key = {:id}', { id: memberId }))
    throw new BadRequestError('Member does not exist.');
  if (b.role === 'member' && !memberId)
    throw new BadRequestError('Member account requires a member association.');
  const shortName = b.shortName === undefined ? null : c.shortName(b.shortName);
  if (shortName !== null && !memberId)
    throw new BadRequestError('A map shortname requires a member association.');
  let record;
  e.app.runInTransaction((app) => {
    record = c.create(app, 'accounts', {
      username, name, role: b.role, memberId, password, passwordConfirm: password,
    });
    if (shortName !== null) {
      const member = c.first(app, 'members', 'key = {:id}', { id: memberId });
      member.set('shortName', shortName);
      app.save(member);
    }
  });
  c.event(e.app, '', 'Account created by portal admin.', e.auth.id);
  return e.json(201, { id: record.id, username, role: b.role });
}
function profile(e) {
  c.human(e);
  const b = e.requestInfo().body;
  if (Object.keys(b).some((key) => key !== 'shortName'))
    throw new BadRequestError('Only your map shortname can be changed here.');
  const shortName = c.shortName(b.shortName);
  const memberId = e.auth.getString('memberId');
  if (!memberId) throw new BadRequestError('This account has no member association.');
  e.app.runInTransaction((app) => {
    const member = c.first(app, 'members', 'key = {:id}', { id: memberId });
    if (!member) throw new NotFoundError('Member not found.');
    member.set('shortName', shortName);
    app.save(member);
    c.event(app, '', 'Member map shortname updated.', e.auth.id);
  });
  return e.json(200, { saved: true });
}
function accountAction(e) {
  c.admin(e);
  const b = e.requestInfo().body;
  const id = e.request.pathValue('id');
  if (b.action !== 'disable' && b.action !== 'reset-password')
    throw new BadRequestError('Choose disable or reset-password.');
  const password =
    b.action === 'reset-password' ? c.text(b.password, 'password', 200) : '';
  if (password && password.length < 12)
    throw new BadRequestError('Use at least 12 characters.');
  e.app.runInTransaction((app) => {
    const account = app.findRecordById('accounts', id);
    if (account.getString('role') === 'worker')
      throw new ForbiddenError('Worker provisioning is local administration.');
    if (b.action === 'disable') {
      if (id === e.auth.id)
        throw new BadRequestError('You cannot disable your own account.');
      if (
        account.getString('role') === 'admin' &&
        c.rows(app, 'accounts', 'role = "admin"').length <= 1
      )
        throw new BadRequestError('Keep at least one enabled admin.');
      account.set('role', 'disabled');
    } else {
      account.set('password', password);
    }
    app.save(account);
    c.event(app, '', `Account action recorded: ${b.action}.`, e.auth.id);
  });
  return e.json(200, { saved: true });
}
function heartbeat(e) {
  c.worker(e);
  const b = e.requestInfo().body;
  if (typeof b.connected !== 'boolean')
    throw new BadRequestError('connected must be boolean.');
  e.app.runInTransaction((app) => {
    const feed = c.feed(app);
    const wasOnline = c.online(feed);
    feed.set('heartbeatAt', c.now());
    feed.set('connected', b.connected);
    if (!wasOnline && b.connected && !feed.getBool('forcedOffline'))
      feed.set('restoredAt', c.now());
    app.save(feed);
    health.evaluate(app);
  });
  return e.json(200, { saved: true, feedOnline: c.online(c.feed(e.app)) });
}
function demoFeed(e) {
  c.admin(e);
  c.demo();
  const b = e.requestInfo().body;
  if (typeof b.online !== 'boolean')
    throw new BadRequestError('online must be boolean.');
  e.app.runInTransaction((app) => {
    const f = c.feed(app);
    const wasOnline = c.online(f);
    f.set('forcedOffline', !b.online);
    if (!wasOnline && b.online) f.set('restoredAt', c.now());
    app.save(f);
    c.event(
      app,
      '',
      b.online
        ? 'Demo feed outage override removed.'
        : 'Demo feed outage enabled.',
      e.auth.id,
    );
  });
  return e.json(200, { saved: true });
}
function nameJob(e) {
  c.admin(e);
  c.demo();
  const b = e.requestInfo().body;
  if (b.status !== 'confirmed' && b.status !== 'failed')
    throw new BadRequestError('Invalid simulated job outcome.');
  e.app.runInTransaction((app) => {
    const job = c.rows(
      app,
      'name_jobs',
      'deviceId = {:id}',
      '-at,-id',
      { id: b.deviceId },
      1,
    )[0];
    if (!job || job.id !== b.jobId)
      throw new ApiError(409, 'Only the latest name job can be changed.');
    job.set('status', b.status);
    app.save(job);
    c.event(
      app,
      b.deviceId,
      `Radio-name outcome simulated: ${b.status}. No radio command sent.`,
      e.auth.id,
    );
  });
  return e.json(200, { saved: true });
}
function batteryHistory(e) {
  c.human(e);
  e.response.header().set('Cache-Control', 'no-store');
  const device = c.device(e.app, e.request.pathValue('id'));
  if (device.getString('kind') === 'member')
    throw new BadRequestError('Infrastructure device required.');
  const hours = Number(e.request.url.query().get('hours') || '24');
  if ([24, 168, 720].indexOf(hours) < 0)
    throw new BadRequestError('Choose 24, 168 or 720 hours.');
  const end = c.now();
  const cutoff = new Date(Date.parse(end) - hours * 3600000).toISOString();
  return e.json(200, telemetry.batteryHistory(e.app, device.getString('key'), cutoff, end, 50000));
}
function state(e) {
  c.human(e);
  e.response.header().set('Cache-Control', 'no-store');
  const app = e.app;
  const devices = c.rows(app, 'devices', '', 'key');
  const assignments = c.rows(app, 'assignments', '', 'startedAt').map((a) => ({
    id: a.id,
    deviceId: a.getString('deviceId'),
    memberId: a.getString('memberId'),
    startedAt: a.getString('startedAt'),
    endedAt: a.getString('endedAt') || null,
  }));
  const members = c.rows(app, 'members', '', 'key').map((m) => ({
    id: m.getString('key'),
    name: m.getString('name'),
    initials: m.getString('initials'),
    shortName: m.getString('shortName'),
  }));
  const cutoff = new Date(Date.now() - 12 * 3600000).toISOString();
  const trackers = devices
    .filter((d) => d.getString('kind') === 'member')
    .map((d) => {
      const position = c.object(d, 'latestPosition');
      const config = c.object(d, 'configuration');
      const battery = c.object(d, 'readings').battery;

      const history = c
        .rows(
          app,
          'positions',
          'deviceId = {:id} && measuredAt >= {:cutoff}',
          '-measuredAt',
          { id: d.getString('key'), cutoff },
          500,
        )
        .reverse()
        .map((p) => c.object(p, 'payload'));
      return {
        id: d.getString('key'),
        number: d.getString('number'),
        shortName: d.getString('shortName'),
        deviceType: config.deviceType || null,
        battery: position.battery === undefined ? null : position.battery,
        batteryVoltage: battery ? battery.value : null,
        batteryMeasuredAt: battery ? battery.measuredAt : null,
        batteryReceivedAt: battery ? battery.receivedAt : null,
        batteryTimestampQuality: battery ? battery.timestampQuality : 'unknown',
        batteryProfile: config.batteryProfile || 'unknown',
        batteryCapacityMah: config.batteryCapacityMah || null,
        position: position.longitude === undefined ? null : position,
        lastContactAt: d.getString('lastContactAt') || null,
        history,
      };
    });
  const infra = devices
    .filter((d) => d.getString('kind') !== 'member')
    .map((d) => {
      const config = c.object(d, 'configuration');
      const readings = c.object(d, 'readings');
      const value = (metric) =>
        readings[metric] ? readings[metric].value : null;
      const times = {};
      const receivedTimes = {};
      Object.keys(readings).forEach(
        (key) => {
          times[key] = readings[key].measuredAt;
          receivedTimes[key] = readings[key].receivedAt;
        },
      );
      const timesKnown = Object.keys(readings)
        .map((key) => telemetry.at(readings[key]))
        .filter(Boolean)
        .sort();
      return {
        ...config,
        id: d.getString('key'),
        role: d.getString('kind') === 'repeater' ? 'Repeater' : 'Backhaul',
        gatewayHealth: d.getString('kind') === 'backhaul' ? require(`${__hooks}/gateway-health.js`).status(d) : null,
        lastContactAt: d.getString('lastContactAt') || null,
        reportedAt: timesKnown[timesKnown.length - 1] || null,
        battery: value('battery'),
        temperature: value('temperature'),
        humidity: value('humidity'),
        solar: value('solar'),
        intrusion: value('intrusion'),
        readingTimes: times,
        readingReceivedTimes: receivedTimes,
        powerReadings: telemetry.powerReadings(readings),
        samples: telemetry.batteryHistory(app, d.getString('key'), '', c.now(), 40).samples,
      };
    });
  const incidentRows = c.rows(app, 'incidents', '', 'openedAt').map((i) => ({
    id: i.id,
    deviceId: i.getString('deviceId'),
    openedAt: i.getString('openedAt'),
    acknowledgedAt: i.getString('acknowledgedAt') || null,
    resolvedAt: i.getString('resolvedAt') || null,
    note: i.getString('note'),
  }));
  const warnings = c.rows(app, 'warnings', '', 'openedAt').map((w) => ({
    id: w.id,
    deviceId: w.getString('deviceId'),
    kind: w.getString('kind'),
    openedAt: w.getString('openedAt'),
    recoveredAt: w.getString('recoveredAt') || null,
    acknowledgedAt: w.getString('acknowledgedAt') || null,
  }));
  const rules = {};
  c.rows(app, 'rules').forEach(
    (r) => (rules[r.getString('deviceId')] = c.object(r, 'payload')),
  );
  const messages = c
    .rows(app, 'messages', '', '-at,-id', {}, 200)
    .reverse()
    .map((m) => ({
      id: m.id,
      author: m.getString('author'),
      authorId: m.getString('authorId'),
      text: m.getString('text'),
      at: m.getString('at'),
      evidence: m.getString('evidence'),
      direction: m.getString('direction'),
    }));
  const jobs = c.rows(app, 'name_jobs', '', 'at,id').map((j) => ({
    id: j.id,
    assignmentId: j.getString('assignmentId'),
    deviceId: j.getString('deviceId'),
    longName: j.getString('longName'),
    status: j.getString('status'),
  }));
  const events = c
    .rows(app, 'events', '', '-at,-id', {}, 200)
    .reverse()
    .map((a) => ({
      id: a.id,
      deviceId: a.getString('deviceId'),
      at: a.getString('at'),
      text: a.getString('text'),
      actorId: a.getString('actorId'),
    }));
  const f = c.feed(app);
  return e.json(200, {
    simulation: c.simulation(),
    trackers,
    members,
    assignments,
    infrastructure: infra,
    currentLinks: neighborCurrent.current(app),
    links: c.rows(app, 'link_observations', '', '-receivedAt,-id').map((row) => ({
      id: row.id,
      observerDeviceId: row.getString('observerDeviceId'),
      heardDeviceId: row.getString('heardDeviceId') || null,
      originalSourceDeviceId: row.getString('originalSourceDeviceId') || null,
      source: row.getString('source'),
      path: row.getString('path'),
      ...c.object(row, 'signal'),
      ...c.object(row, 'details'),
      receivedAt: row.getString('receivedAt'),
      observedAt: row.getString('observedAt') || null,
    })),
    incidents: incidentRows,
    warnings,
    rules,
    messages,
    nameJobs: jobs,
    events,
    feedOnline: c.online(f),
    heartbeatAt: f.getString('heartbeatAt') || null,
    historyLimitPerDevice: 500,
    account: {
      id: e.auth.id,
      name: e.auth.getString('name'),
      role: e.auth.getString('role'),
      memberId: e.auth.getString('memberId'),
    },
  });
}
module.exports = {
  assign,
  release,
  send,
  rule,
  incident,
  ackWarning,
  account,
  accountAction,
  profile,
  configuration,
  heartbeat,
  demoFeed,
  nameJob,
  state,
  batteryHistory,
};
