migrate((app) => {
  const members = app.findCollectionByNameOrId('members');
  members.fields.add(new TextField({ name: 'shortName', max: 5 }));
  app.save(members);
  // These two registered member devices were verified as original Heltec V4s.
  for (const key of ['b001', 'b002']) {
    const devices = app.findRecordsByFilter('devices', 'key = {:key} && kind = "member"', '', 1, 0, { key });
    if (!devices.length) continue;
    const device = devices[0];
    const config = JSON.parse(device.getString('configuration') || '{}');
    if (!config.deviceType) {
      device.set('configuration', { ...config, deviceType: 'Heltec V4' });
      app.save(device);
    }
  }
}, (app) => {
  const members = app.findCollectionByNameOrId('members');
  members.fields.removeByName('shortName');
  app.save(members);
});
