// Manual provisioning only; the private input supplies R001's planned location.
migrate((app) => {
  const d = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_R004_CONFIG') || '/etc/meshlink/r004.json')));
  const c = d.configuration;
  if (d.key !== 'r004' || d.kind !== 'repeater' || d.number !== 'R004' || d.shortName !== 'R004' ||
      !c || c.radioNodeId !== '!77fdb9f1' || c.hardwareId !== '75762d0c4f9b0c82f1b9fd774661875b' ||
      c.firmware !== '2.7.26.0b65f2e' || c.deploymentStatus !== 'planned' || c.downlink !== false ||
      typeof c.latitude !== 'number' || !Number.isFinite(c.latitude) || Math.abs(c.latitude) > 90 ||
      typeof c.longitude !== 'number' || !Number.isFinite(c.longitude) || Math.abs(c.longitude) > 180)
    throw new Error('Invalid verified R004 identity or planned configuration.');
  const source = app.findFirstRecordByFilter('devices', 'key = "r001"');
  const site = JSON.parse(source.getString('configuration') || '{}');
  if (c.latitude !== site.latitude || c.longitude !== site.longitude)
    throw new Error('R004 must share R001\'s recorded planned location.');
  const matches = app.findRecordsByFilter('devices', 'key = "r004"', '', 2);
  if (matches.length) {
    const previous = JSON.parse(matches[0].getString('configuration') || '{}');
    if (matches[0].getString('kind') !== 'repeater' || previous.hardwareId !== c.hardwareId || previous.radioNodeId !== c.radioNodeId)
      throw new Error('Existing R004 identity mismatch; no records changed.');
    return;
  }
  const record = new Record(app.findCollectionByNameOrId('devices'));
  ['key', 'kind', 'number', 'shortName', 'configuration'].forEach((key) => record.set(key, d[key]));
  app.save(record);
  const event = new Record(app.findCollectionByNameOrId('events'));
  event.set('deviceId', 'r004');
  event.set('at', new Date().toISOString());
  event.set('text', 'R004 provisioned at R001\'s owner-designated planned site with reported AHT-family and INA219 sensors; installation and calibration unverified.');
  app.save(event);
});
