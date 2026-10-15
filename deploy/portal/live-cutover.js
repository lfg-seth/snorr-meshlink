// One-time offline migration. Copy as a timestamped migration into a PRIVATE
// staging directory only after a verified backup and stopping both services.
// Not part of automatic application/schema migrations.
migrate((app) => {
  const config = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_MQTT_CONFIG') || '/etc/meshlink/mqtt.json')));
  const mappings = { ...config.members, ...config.gateways };
  const expected = ['b001', 'b002', 'g001', 'g002'];
  if (JSON.stringify(Object.values(mappings).sort()) !== JSON.stringify(expected))
    throw new Error('Expected exactly two verified trackers and two gateways.');
  const rows = (name) => {
    const result = app.findRecordsByFilter(name, '', '', 100001, 0);
    if (result.length > 100000) throw new Error('Cutover record bound exceeded.');
    const copy = [];
    for (let i = 0; i < result.length; i++) copy.push(result[i]);
    return copy;
  };
  const devices = rows('devices');
  const keys = devices.map((d) => d.getString('key')).sort();
  if (JSON.stringify(keys) !== JSON.stringify(['b1', 'b2', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'r1', 'r2']))
    throw new Error('Database is not the expected simulation; no changes applied.');
  const members = rows('members');
  if (members.length !== 5 || members.some((m) => !m.getString('name').startsWith('Demo ')))
    throw new Error('Non-demo members present; no changes applied.');
  const demoKeys = new Set(keys);
  const collections = ['assignments', 'positions', 'packet_receipts', 'observations',
    'messages', 'send_attempts', 'name_jobs', 'warnings', 'incidents', 'events', 'rules'];
  const records = {};
  collections.forEach((name) => {
    records[name] = rows(name);
    records[name].forEach((r) => {
      const device = r.getString('deviceId');
      if (device && device !== '*' && !demoKeys.has(device))
        throw new Error('Non-demo device evidence present; no changes applied.');
    });
  });
  // PocketBase applies migration operations transactionally. Archive contains
  // complete fictional history; no real observations are permitted in this input.
  collections.forEach((name) => records[name].forEach((r) => app.delete(r)));
  devices.forEach((r) => app.delete(r));
  members.forEach((r) => app.delete(r));
  rows('accounts').forEach((a) => {
    if (a.getString('role') === 'member') {
      a.set('role', 'disabled');
      a.set('memberId', '');
      a.set('name', 'Disabled demo member');
    }
    if (a.getString('role') === 'admin') a.set('name', 'Dispatch');
    if (a.getString('role') === 'worker') a.set('name', 'MQTT GPS worker');
    app.save(a);
  });
  const now = new Date().toISOString();
  Object.entries(mappings).forEach(([nodeId, key]) => {
    const tracker = key.startsWith('b');
    const identity = config.identities[key];
    if (!identity || !identity.hardwareId || identity.nodeId !== nodeId)
      throw new Error('Verified physical identity missing.');
    const record = new Record(app.findCollectionByNameOrId('devices'));
    record.set('key', key);
    record.set('kind', tracker ? 'member' : 'backhaul');
    record.set('number', key.toUpperCase());
    record.set('shortName', identity.shortName);
    record.set('monitoringStartedAt', now);
    record.set('configuration', {
      name: tracker ? `Bench tracker ${key.toUpperCase()}` : `Bench gateway ${key.toUpperCase()}`,
      hardwareId: identity.hardwareId, radioNodeId: nodeId,
      firmware: '2.7.26.54e0d8d', source: 'live', downlink: false,
      // GPS-only integration: no fitted sensor, battery or cadence claims.
      equipped: { solar: false, weather: false, intrusion: false },
      cadenceMinutes: 0,
      disabledMonitoring: ['battery', 'solar', 'temperature', 'intrusion'],
      antenna: 'Unknown', batterySetup: 'Unverified', solarSetup: 'Unconfigured',
    });
    app.save(record);
  });
  const feed = app.findFirstRecordByFilter('feed', "key = 'worker'");
  feed.set('connected', false);
  feed.set('forcedOffline', false);
  feed.set('heartbeatAt', '');
  feed.set('restoredAt', '');
  app.save(feed);
});
