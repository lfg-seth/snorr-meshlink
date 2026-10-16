migrate((app) => {
  const collection = app.findCollectionByNameOrId('observations');
  collection.addIndex('idx_observations_device_time', false, 'deviceId, measuredAt', '');
  app.save(collection);
}, (app) => {
  const collection = app.findCollectionByNameOrId('observations');
  collection.removeIndex('idx_observations_device_time');
  app.save(collection);
});
