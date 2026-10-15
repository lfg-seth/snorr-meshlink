migrate((app) => {
  app.save(new Collection({
    name: 'mqtt_archive',
    type: 'base',
    // Raw traffic is available only to trusted PocketBase administration.
    listRule: null, viewRule: null, createRule: null,
    updateRule: null, deleteRule: null,
    fields: [
      { name: 'receiptId', type: 'text', required: true, max: 36 },
      { name: 'topic', type: 'text', required: true, max: 65535 },
      { name: 'receivedAt', type: 'text', required: true, max: 40 },
      { name: 'ingestedAt', type: 'text', required: true, max: 40 },
      // Accommodates base64 expansion of the MQTT maximum packet size.
      { name: 'envelope', type: 'json', required: true, maxSize: 400000000 },
    ],
    indexes: [
      'CREATE UNIQUE INDEX idx_mqtt_archive_receipt ON mqtt_archive (receiptId)',
      'CREATE INDEX idx_mqtt_archive_received ON mqtt_archive (receivedAt)',
    ],
  }));
}, (app) => {
  app.delete(app.findCollectionByNameOrId('mqtt_archive'));
});
