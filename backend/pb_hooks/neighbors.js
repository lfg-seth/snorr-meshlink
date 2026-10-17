const c = require(`${__hooks}/common.js`);
function validate(app, data, deviceId) {
  const node = (id) => typeof id === 'string' && /^![0-9a-f]{8}$/.test(id) && id !== '!00000000';
  const integer = (value, low, high) => Number.isInteger(value) && value >= low && value <= high;
  const snns = data.reportType === 'snns-v1';
  if ((!snns && data.reportType !== 'neighbor-info') || !node(data.observerNodeId) ||
      !Array.isArray(data.rows) || data.rows.length > (snns ? 8 : 32))
    throw new BadRequestError('Invalid neighbor report.');
  if (snns && (!data.rows.length || !integer(data.bootId, 1, 4294967295) ||
      !integer(data.sequence, 1, 4294967295) || !integer(data.reportUptimeSeconds, 0, 4294967) ||
      !integer(data.totalNeighbors, data.rows.length, 255) ||
      typeof data.capacityEvicted !== 'boolean' ||
      data.subset !== (data.totalNeighbors > data.rows.length)))
    throw new BadRequestError('Invalid SNNS report metadata.');
  const seen = {};
  data.rows.forEach((row) => {
    if (!row || !node(row.heardNodeId) || row.heardNodeId === data.observerNodeId || seen[row.heardNodeId])
      throw new BadRequestError('Invalid neighbor identity.');
    seen[row.heardNodeId] = true;
    if (row.heardDeviceId !== null) {
      c.device(app, c.text(row.heardDeviceId, 'heard device', 80));
      if (row.heardDeviceId === deviceId) throw new BadRequestError('Self neighbor.');
    }
    const signal = (value, low, high) => typeof value === 'number' && isFinite(value) && value >= low && value <= high;
    if ((row.snrDb !== null && !signal(row.snrDb, -100, 100)) ||
        (row.rssiDbm !== null && !signal(row.rssiDbm, -200, -1)) ||
        (snns && (row.snrDb === null || row.rssiDbm === null ||
          !integer(row.hearingAgeSeconds, 0, 1799) || !integer(row.observationCount, 1, 4294967295))))
      throw new BadRequestError('Invalid neighbor reading.');
  });
}
function save(app, packetKey, b, receivedAt) {
  const data = b.data;
  const report = c.create(app, 'neighbor_reports', { packetKey, deviceId: b.deviceId, receivedAt, payload: data });
  data.rows.forEach((row) => {
    const details = { reportType: data.reportType, observerNodeId: data.observerNodeId,
      heardNodeId: row.heardNodeId, transportGatewayId: b.gatewayId };
    if (data.reportType === 'snns-v1') {
      ['bootId', 'sequence', 'reportUptimeSeconds', 'subset', 'capacityEvicted', 'totalNeighbors']
        .forEach((key) => { details[key] = data[key]; });
      details.hearingAgeSeconds = row.hearingAgeSeconds;
      details.observationCount = row.observationCount;
    }
    c.create(app, 'link_observations', {
      reportId: report.id, observerDeviceId: b.deviceId, heardDeviceId: row.heardDeviceId || '',
      originalSourceDeviceId: '', source: 'neighbor', path: 'direct',
      signal: { snrDb: row.snrDb, rssiDbm: row.rssiDbm }, details,
      receivedAt, observedAt: '',
    });
  });
}
module.exports = { validate, save };
