// Explicit private manual migration. No source/application deployment.
migrate((app) => {
  const canonical = (value) => Array.isArray(value) ? value.map(canonical) :
    value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])])) : value;
  const equal = (left, right) => JSON.stringify(canonical(left)) === JSON.stringify(canonical(right));
  const change = JSON.parse(toString($os.readFile($os.getenv('MESHLINK_R006_METADATA_CHANGE'))));
  if (change.key !== 'r006' || !change.before || !change.after || !change.verifiedRadio ||
      change.verifiedRadio.profileVerified !== true || change.verifiedRadio.keysPreserved !== true ||
      change.verifiedRadio.nodeId !== '!da581e5f' ||
      change.verifiedRadio.deviceTelemetrySeconds !== 180 || change.verifiedRadio.powerTelemetrySeconds !== 180 ||
      change.verifiedRadio.environmentTelemetrySeconds !== 180 || change.verifiedRadio.effectiveSnnsCadenceSeconds !== 180 ||
      change.verifiedRadio.standardNeighborInfoIntervalSeconds !== 21600 ||
      change.verifiedRadio.environmentMeasurementEnabled !== false || change.verifiedRadio.powerMeasurementEnabled !== true ||
      change.after.radioNodeId !== '!da581e5f' || change.after.hardwareId !== 'b8bc8fa95c2cb1e95f1e58dafebb06cc' ||
      change.after.firmware !== change.verifiedRadio.version || change.after.cadenceMinutes !== 3 ||
      change.after.reportCadenceMinutes.battery !== 3 ||
      change.after.sensorCapabilities.temperature !== false || change.after.sensorCapabilities.humidity !== false ||
      change.after.equipped.weather !== false || change.after.downlink !== false ||
      !Number.isFinite(change.after.latitude) || !Number.isFinite(change.after.longitude) ||
      change.after.latitude < -90 || change.after.latitude > 90 || change.after.longitude < -180 || change.after.longitude > 180)
    throw new Error('Invalid verified R006 metadata update.');
  const records = app.findRecordsByFilter('devices', 'key = "r006"', '', 2);
  if (records.length !== 1 || records[0].getString('kind') !== 'repeater' ||
      records[0].getString('number') !== 'R006' || records[0].getString('shortName') !== 'R006')
    throw new Error('R006 identity not uniquely registered.');
  const existing = JSON.parse(records[0].getString('configuration') || '{}');
  if (equal(existing, change.after)) return;
  if (!equal(existing, change.before)) throw new Error('R006 metadata changed since staging; no records changed.');
  records[0].set('configuration', change.after);
  app.save(records[0]);
  const event = new Record(app.findCollectionByNameOrId('events'));
  event.set('deviceId', 'r006');
  event.set('at', new Date().toISOString());
  event.set('text', 'R006 owner-provided map point recorded; installation is unverified. Verified firmware and 180-second battery, power and passive-neighbor reporting configured; environmental reporting disabled with no temperature/humidity sensor fitted. Delivery cadence and current accuracy require separate measurements.');
  app.save(event);
});
