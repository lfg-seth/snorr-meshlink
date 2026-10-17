// Manual provisioning only; the private input supplies R001's planned location.
migrate((app) => {
  const d = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_R005_CONFIG') || '/etc/meshlink/r005.json')));
  const c = d.configuration;
  if (d.key !== 'r005' || d.kind !== 'repeater' || d.number !== 'R005' || d.shortName !== 'R005' ||
      !c || c.radioNodeId !== '!f95b5501' || c.hardwareId !== '6bd77df9f05f3ce901555bf96d5ed7fc' ||
      c.firmware !== '2.7.26.8dd4dac' || c.deploymentStatus !== 'planned' || c.downlink !== false ||
      typeof c.latitude !== 'number' || !Number.isFinite(c.latitude) || Math.abs(c.latitude) > 90 ||
      typeof c.longitude !== 'number' || !Number.isFinite(c.longitude) || Math.abs(c.longitude) > 180)
    throw new Error('Invalid verified R005 identity or planned configuration.');
  const source = app.findFirstRecordByFilter('devices', 'key = "r001"');
  const site = JSON.parse(source.getString('configuration') || '{}');
  if (c.latitude !== site.latitude || c.longitude !== site.longitude)
    throw new Error('R005 must share R001\'s recorded planned location.');
  for (const other of app.findRecordsByFilter('devices', 'key != "r005"', '', 1000)) {
    const identity = JSON.parse(other.getString('configuration') || '{}');
    if (identity.hardwareId === c.hardwareId || identity.radioNodeId === c.radioNodeId)
      throw new Error('R005 identity is already assigned to another device.');
  }
  const matches = app.findRecordsByFilter('devices', 'key = "r005"', '', 2);
  if (matches.length) {
    const previous = JSON.parse(matches[0].getString('configuration') || '{}');
    if (matches[0].getString('kind') !== 'repeater' || previous.hardwareId !== c.hardwareId || previous.radioNodeId !== c.radioNodeId)
      throw new Error('Existing R005 identity mismatch; no records changed.');
    return;
  }
  const record = new Record(app.findCollectionByNameOrId('devices'));
  ['key', 'kind', 'number', 'shortName', 'configuration'].forEach((key) => record.set(key, d[key]));
  app.save(record);
  const event = new Record(app.findCollectionByNameOrId('events'));
  event.set('deviceId', 'r005');
  event.set('at', new Date().toISOString());
  event.set('text', 'R005 provisioned at R001\'s planned site with reported temperature and INA219 sensors, plus an AIN1/GPIO31 2N2222 dummy load through a 2 kohm base resistor; physical load current, installation and calibration unverified.');
  app.save(event);
});
