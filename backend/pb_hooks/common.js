function now() {
  return new Date().toISOString();
}
function rows(
  app,
  collection,
  filter = '',
  sort = '',
  params = {},
  limit = 2000,
) {
  const found = app.findRecordsByFilter(
    collection,
    filter,
    sort,
    limit,
    0,
    params,
  );
  // Go slices are not ordinary arrays: copy before JS reverse/sort mutations.
  const result = [];
  for (let i = 0; i < found.length; i++) result.push(found[i]);
  return result;
}
function first(app, collection, filter, params) {
  return rows(app, collection, filter, '', params, 1)[0] || null;
}
function create(app, collection, data) {
  const record = new Record(app.findCollectionByNameOrId(collection));
  Object.keys(data).forEach((key) => record.set(key, data[key]));
  app.save(record);
  return record;
}
function object(record, key) {
  return JSON.parse(record.getString(key) || '{}') || {};
}
function role(e, allowed) {
  if (!e.auth || allowed.indexOf(e.auth.getString('role')) < 0)
    throw new ForbiddenError('This account cannot perform that operation.');
}
function human(e) {
  role(e, ['admin', 'member']);
}
function admin(e) {
  role(e, ['admin']);
}
function worker(e) {
  role(e, ['worker']);
}
function simulation() {
  return $os.getenv('MESHLINK_SIMULATION') === '1';
}
function demo() {
  if (!simulation())
    throw new ForbiddenError('Simulation controls are disabled.');
}
function text(value, name, max = 200) {
  if (typeof value !== 'string' || !value.trim() || value.length > max)
    throw new BadRequestError(`Invalid ${name}.`);
  return value.trim();
}
function device(app, key) {
  const d = first(app, 'devices', 'key = {:key}', { key });
  if (!d) throw new NotFoundError('Device not found.');
  return d;
}
function event(app, deviceId, message, actorId = '') {
  return create(app, 'events', { deviceId, text: message, actorId, at: now() });
}
function feed(app) {
  return first(app, 'feed', "key = 'worker'", {});
}
function online(feed, at = Date.now()) {
  return (
    feed.getBool('connected') &&
    !feed.getBool('forcedOffline') &&
    at - Date.parse(feed.getString('heartbeatAt')) < 20000
  );
}
function job(app, deviceId, assignmentId, longName) {
  return create(app, 'name_jobs', {
    deviceId,
    assignmentId,
    longName,
    status: 'pending',
    at: now(),
  });
}
function currentAssignment(app, deviceId) {
  return first(app, 'assignments', 'deviceId = {:id} && endedAt = ""', {
    id: deviceId,
  });
}
function memberAt(app, deviceId, at) {
  if (!at) return '';
  const a = first(
    app,
    'assignments',
    'deviceId = {:id} && startedAt <= {:at} && (endedAt = "" || endedAt > {:at})',
    { id: deviceId, at },
  );
  return a ? a.getString('memberId') : '';
}
module.exports = {
  now,
  rows,
  first,
  create,
  object,
  role,
  human,
  admin,
  worker,
  simulation,
  demo,
  text,
  device,
  event,
  feed,
  online,
  job,
  currentAssignment,
  memberAt,
};
