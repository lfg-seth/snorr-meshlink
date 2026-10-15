// Each PocketBase handler runs in its own scope; shared code is a local module.
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
