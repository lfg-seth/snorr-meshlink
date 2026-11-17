// Each PocketBase handler runs in its own scope; shared code is a local module.
onRecordAuthRequest((e) => {
  const role = e.record.getString('role');
  if (e.authMethod === 'password' && (role === 'admin' || role === 'member')
      && !require(`${__hooks}/common.js`).simulation() && e.requestInfo().body.rememberDevice === true) {
    // PocketBase accepts Go durations in nanoseconds.
    e.token = e.record.newStaticAuthToken(30 * 24 * 60 * 60 * 1e9);
  }
  e.next();
}, 'accounts');

routerAdd('GET', '/api/meshlink/activity', (e) => {
  const c = require(`${__hooks}/common.js`);
  c.human(e);
  if (c.simulation()) throw new NotFoundError('Field activity is available on the live portal.');
  e.response.header().set('Cache-Control', 'no-store');
  let snapshot;
  try {
    snapshot = JSON.parse(toString($os.readFile('/run/meshlink-activity/snapshot.json')));
  } catch {
    throw new ApiError(503, 'Waiting for the activity sampler.');
  }
  // A stopped sampler can leave a readable file behind. Age receipts from server time.
  const now = Date.now();
  snapshot.now = now / 1000;
  if (now - Date.parse(snapshot.at) > 15000) snapshot.status = 'No new snapshots';
  return e.json(200, snapshot);
}, $apis.requireAuth('accounts'));
routerAdd(
  'GET',
  '/api/meshlink/current-history/{id}',
  (e) => require(`${__hooks}/meshlink.js`).currentHistory(e),
  $apis.requireAuth('accounts'),
);
routerAdd(
  'GET',
  '/api/meshlink/battery-history/{id}',
  (e) => require(`${__hooks}/meshlink.js`).batteryHistory(e),
  $apis.requireAuth('accounts'),
);
routerAdd(
  'GET',
  '/api/meshlink/state',
  (e) => require(`${__hooks}/meshlink.js`).state(e),
  $apis.requireAuth('accounts'),
);
routerAdd(
  'POST',
  '/api/meshlink/assign',
  (e) => require(`${__hooks}/meshlink.js`).assign(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/release',
  (e) => require(`${__hooks}/meshlink.js`).release(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/messages',
  (e) => require(`${__hooks}/meshlink.js`).send(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/rules',
  (e) => require(`${__hooks}/meshlink.js`).rule(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/incidents/{id}',
  (e) => require(`${__hooks}/meshlink.js`).incident(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/warnings/{id}/ack',
  (e) => require(`${__hooks}/meshlink.js`).ackWarning(e),
  $apis.requireAuth('accounts'),
);
routerAdd(
  'POST',
  '/api/meshlink/accounts',
  (e) => require(`${__hooks}/meshlink.js`).account(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/profile',
  (e) => require(`${__hooks}/meshlink.js`).profile(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/worker/ingest',
  (e) => require(`${__hooks}/ingest.js`).ingest(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(65536),
);
routerAdd(
  'POST',
  '/api/meshlink/worker/heartbeat',
  (e) => require(`${__hooks}/meshlink.js`).heartbeat(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/demo/feed',
  (e) => require(`${__hooks}/meshlink.js`).demoFeed(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/demo/name-job',
  (e) => require(`${__hooks}/meshlink.js`).nameJob(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);

routerAdd(
  'POST',
  '/api/meshlink/configuration',
  (e) => require(`${__hooks}/meshlink.js`).configuration(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);
routerAdd(
  'POST',
  '/api/meshlink/accounts/{id}',
  (e) => require(`${__hooks}/meshlink.js`).accountAction(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(16384),
);

routerAdd(
  'POST',
  '/api/meshlink/worker/archive',
  (e) => require(`${__hooks}/archive.js`).archive(e),
  $apis.requireAuth('accounts'),
  $apis.bodyLimit(400000000),
);
