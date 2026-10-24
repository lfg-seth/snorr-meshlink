const c = require(`${__hooks}/common.js`);
const EXPIRY_SECONDS = 7200;
// millis() is uint32, then divided by1000 on the wire, rather than a uint32 seconds clock.
const MILLIS_WRAP_SECONDS = 4294967.296;
// Both source clocks are floored independently. Across a millis rollover their
// fractional phases differ too; two seconds is a conservative hearing tolerance.
const HEARING_TOLERANCE_SECONDS = 2;

function observation(row) {
  return {
    id: row.id,
    observerDeviceId: row.getString('observerDeviceId'),
    heardDeviceId: row.getString('heardDeviceId') || null,
    originalSourceDeviceId: row.getString('originalSourceDeviceId') || null,
    source: row.getString('source'), path: row.getString('path'),
    ...c.object(row, 'signal'), ...c.object(row, 'details'),
    receivedAt: row.getString('receivedAt'), observedAt: row.getString('observedAt') || null,
  };
}

function previousArchive(app, report, deviceId, nodeId) {
  const filter = 'deviceId = {:device} && payload.observerNodeId = {:node} && payload.reportType = "snns-v1" && id != {:id}';
  const params = { device: deviceId, node: nodeId, id: report.id };
  const latest = c.rows(app, 'neighbor_reports', filter, '-receivedAt,-id', params, 1)[0];
  if (!latest) return null;
  const boot = c.object(latest, 'payload').bootId;
  // Late reports of this boot must not lower its already archived sequence frontier.
  const highest = c.rows(app, 'neighbor_reports', filter + ' && payload.bootId = {:boot}',
    '-payload.sequence,-receivedAt,-id', { ...params, boot }, 1)[0];
  const data = c.object(highest, 'payload');
  return { bootId: data.bootId, sequence: data.sequence, uptime: data.reportUptimeSeconds,
    unwrappedUptime: data.reportUptimeSeconds, receivedAt: latest.getString('receivedAt'),
    initialHearingFloor: data.reportUptimeSeconds };
}

function advance(app, report, b, receivedAt, links) {
  const data = b.data;
  if (data.reportType !== 'snns-v1') return;
  const observerKey = `${b.deviceId}:${data.observerNodeId}`;
  let record = c.first(app, 'neighbor_frontiers', 'observerKey = {:key}', { key: observerKey });
  let previous = record ? c.object(record, 'payload') : previousArchive(app, report, b.deviceId, data.observerNodeId);
  // Persist a bootstrap baseline even when this incoming report is rejected
  // below; rejected archive rows must not become the next bootstrap baseline.
  if (!record && previous) record = c.create(app, 'neighbor_frontiers', { observerKey, payload: previous });
  let uptime = data.reportUptimeSeconds;
  let floor = null;
  if (previous) {
    if (previous.bootId === data.bootId) {
      // A different mesh packet ID/gateway does not make a repeated generation new.
      if (data.sequence <= previous.sequence) return;
      let elapsed = uptime - previous.uptime;
      if (elapsed < 0) {
        if (previous.uptime < MILLIS_WRAP_SECONDS / 2 || uptime >= MILLIS_WRAP_SECONDS / 2) return;
        elapsed += MILLIS_WRAP_SECONDS;
      }
      uptime = previous.unwrappedUptime + elapsed;
      floor = previous.initialHearingFloor === undefined ? null : previous.initialHearingFloor;
    } else {
      // Never reactivate a retired, previously archived boot, even under a novel packet ID.
      const known = c.first(app, 'neighbor_reports',
        'deviceId = {:device} && payload.observerNodeId = {:node} && payload.reportType = "snns-v1" && payload.bootId = {:boot} && id != {:id}',
        { device: b.deviceId, node: data.observerNodeId, boot: data.bootId, id: report.id });
      if (known || receivedAt < previous.receivedAt) return;
    }
  }
  const next = { bootId: data.bootId, sequence: data.sequence, uptime: data.reportUptimeSeconds,
    unwrappedUptime: uptime, receivedAt: previous && previous.receivedAt > receivedAt ? previous.receivedAt : receivedAt };
  if (floor !== null) next.initialHearingFloor = floor;
  if (!record) record = c.create(app, 'neighbor_frontiers', { observerKey, payload: next });
  else { record.set('payload', next); app.save(record); }

  data.rows.forEach((row, index) => {
    const pairKey = `${observerKey}:${row.heardNodeId}`;
    let current = c.first(app, 'neighbor_current', 'pairKey = {:key}', { key: pairKey });
    const old = current ? c.object(current, 'watermark') : null;
    const hearing = uptime - row.hearingAgeSeconds;
    // Bootstrap ordering only. Previously archived hearings wait for new source
    // evidence; an application upgrade must never reset their relative age.
    if (floor !== null && hearing <= floor + HEARING_TOLERANCE_SECONDS) return;
    const sameBoot = old && old.bootId === data.bootId;
    const newerHearing = !sameBoot || hearing > old.hearingCoordinate + HEARING_TOLERANCE_SECONDS;
    const increasedCount = sameBoot && row.observationCount > old.observationCount &&
      hearing >= old.hearingCoordinate - HEARING_TOLERANCE_SECONDS;
    if (!newerHearing && !increasedCount) {
      // Keep a monotone coordinate watermark, but keep the selected signal and
      // original receipt anchor. Repeated publication is not a new reception.
      if (sameBoot && hearing > old.hearingCoordinate) {
        current.set('watermark', { ...old, hearingCoordinate: hearing });
        app.save(current);
      }
      return;
    }
    const values = { pairKey, observerKey, anchorReceivedAt: receivedAt,
      payload: { ...observation(links[index]), freshness: {
        basis: 'relative', anchorReceivedAt: receivedAt, ageAtAnchorSeconds: row.hearingAgeSeconds } },
      watermark: { bootId: data.bootId, hearingCoordinate: hearing, observationCount: row.observationCount } };
    if (!current) c.create(app, 'neighbor_current', values);
    else { Object.keys(values).forEach((key) => current.set(key, values[key])); app.save(current); }
  });
}

function current(app, at = Date.now()) {
  const cutoff = new Date(at - EXPIRY_SECONDS * 1000).toISOString();
  const relative = c.rows(app, 'neighbor_current', 'anchorReceivedAt > {:cutoff}',
    '-anchorReceivedAt,-id', { cutoff }).map((row) => {
    const link = c.object(row, 'payload');
    // The indexed field is the durable anchor; expose the same value to clients.
    link.freshness.anchorReceivedAt = row.getString('anchorReceivedAt');
    return link;
  }).filter((link) => {
    const age = link.freshness.ageAtAnchorSeconds + (at - Date.parse(link.freshness.anchorReceivedAt)) / 1000;
    return isFinite(age) && age >= 0 && age < EXPIRY_SECONDS;
  });
  const zonedTime = (value) => typeof value === 'string' && /(Z|[+-]\d\d:\d\d)$/.test(value) && isFinite(Date.parse(value));
  const absolute = c.rows(app, 'link_observations', 'observedAt > {:cutoff} && observedAt <= {:now}',
    '-observedAt,-id', { cutoff, now: new Date(at).toISOString() }).map(observation)
    .filter((link) => link.reportType !== 'neighbor-info' && zonedTime(link.observedAt) && zonedTime(link.receivedAt) &&
      Date.parse(link.receivedAt) <= at && Date.parse(link.observedAt) <= Date.parse(link.receivedAt) &&
      at - Date.parse(link.observedAt) < EXPIRY_SECONDS * 1000);
  const estimate = (link) => link.freshness ? Date.parse(link.freshness.anchorReceivedAt) -
    link.freshness.ageAtAnchorSeconds * 1000 : Date.parse(link.observedAt);
  return relative.concat(absolute).sort((a, b) => estimate(b) - estimate(a)).slice(0, 2000);
}

module.exports = { advance, current, observation };
