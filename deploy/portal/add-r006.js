// Manual provisioning only. Input is private, and R006 has no recorded site.
migrate((app) => {
  const canonical = (value) => Array.isArray(value) ? value.map(canonical) :
    value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])])) : value;
  const d = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_R006_CONFIG'))));
  const c = d.configuration;
  if (d.key !== 'r006' || d.kind !== 'repeater' || d.number !== 'R006' || d.shortName !== 'R006' ||
      !c || c.radioNodeId !== '!da581e5f' || c.hardwareId !== 'b8bc8fa95c2cb1e95f1e58dafebb06cc' ||
      c.firmware !== '2.7.26.09d8a9d' || c.downlink !== false ||
      c.deploymentStatus !== 'bench' || c.latitude !== undefined || c.longitude !== undefined ||
      c.equipped.weather !== false || c.sensorCapabilities.temperature !== false ||
      c.sensorCapabilities.humidity !== false || c.sensorConfiguration.environmentMeasurementEnabled !== false ||
      c.sensorConfiguration.powerTelemetrySeconds !== 900 || c.sensorConfiguration.powerMeasurementEnabled !== true ||
      c.cadenceMinutes !== 15 || c.reportCadenceMinutes.battery !== 15 ||
      c.equipped.solar !== false || c.equipped.intrusion !== false ||
      c.batteryConfiguration.cellType !== '18650' || c.batteryConfiguration.cellCount !== null ||
      c.batteryConfiguration.chemistry !== null || c.batteryConfiguration.arrangement !== null ||
      c.batteryConfiguration.capacityMahPerCell !== null || c.batteryConfiguration.packCapacityMah !== null)
    throw new Error('Invalid verified R006 identity or INA219-only bench configuration.');
  for (const other of app.findRecordsByFilter('devices', 'key != "r006"', '', 1000)) {
    const identity = JSON.parse(other.getString('configuration') || '{}');
    if (identity.hardwareId === c.hardwareId || identity.radioNodeId === c.radioNodeId)
      throw new Error('R006 identity is already assigned to another device.');
  }
  const matches = app.findRecordsByFilter('devices', 'key = "r006"', '', 2);
  if (matches.length) {
    if (matches[0].getString('kind') !== 'repeater' ||
        JSON.stringify(canonical(JSON.parse(matches[0].getString('configuration') || '{}'))) !== JSON.stringify(canonical(c)) ||
        matches[0].getString('number') !== 'R006' || matches[0].getString('shortName') !== 'R006')
      throw new Error('Existing R006 differs; no records changed.');
    return;
  }
  const record = new Record(app.findCollectionByNameOrId('devices'));
  ['key', 'kind', 'number', 'shortName', 'configuration'].forEach((key) => record.set(key, d[key]));
  app.save(record);
  const event = new Record(app.findCollectionByNameOrId('events'));
  event.set('deviceId', 'r006');
  event.set('at', new Date().toISOString());
  event.set('text', 'R006 registered for bench use with INA219 power telemetry only; no temperature sensor or recorded site. Battery arrangement, independent current accuracy and field acceptance remain unverified.');
  app.save(event);
});
