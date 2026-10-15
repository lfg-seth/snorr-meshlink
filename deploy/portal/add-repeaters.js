// Manual transactional provisioning; input contains private planned-site coordinates.
migrate((app) => {
  const input = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_REPEATER_CONFIG') || '/etc/meshlink/repeaters.json')));
  const expected = { r001: '!a65601b3', r002: '!b456f760', r003: '!05237743' };
  if (!Array.isArray(input.devices) || JSON.stringify(input.devices.map((d) => d.key).sort()) !== JSON.stringify(Object.keys(expected)))
    throw new Error('Expected exactly the three verified pilot repeaters.');
  input.devices.forEach((d) => {
    const c = d.configuration;
    if (d.kind !== 'repeater' || d.shortName !== d.key.toUpperCase() ||
        !c || c.radioNodeId !== expected[d.key] || !/^[0-9a-f]+$/.test(c.hardwareId || '') ||
        typeof c.latitude !== 'number' || Math.abs(c.latitude) > 90 ||
        typeof c.longitude !== 'number' || Math.abs(c.longitude) > 180 ||
        c.deploymentStatus !== 'planned' || c.downlink !== false)
      throw new Error('Invalid repeater identity or planned configuration.');
    const matches = app.findRecordsByFilter('devices', 'key = {:key}', '', 2, 0, { key: d.key });
    if (matches.length) {
      const existing = matches[0];
      const previous = JSON.parse(existing.getString('configuration') || '{}');
      if (existing.getString('kind') !== 'repeater' || !previous ||
          previous.hardwareId !== c.hardwareId || previous.radioNodeId !== c.radioNodeId)
        throw new Error('Existing identity mismatch; no records changed.');
      return;
    }
    const record = new Record(app.findCollectionByNameOrId('devices'));
    ['key', 'kind', 'number', 'shortName', 'configuration'].forEach((key) => record.set(key, d[key]));
    app.save(record);
    const event = new Record(app.findCollectionByNameOrId('events'));
    event.set('deviceId', d.key);
    event.set('at', new Date().toISOString());
    event.set('text', 'Repeater provisioned with owner-provided planned site and equipment; installation unverified.');
    app.save(event);
  });
});
