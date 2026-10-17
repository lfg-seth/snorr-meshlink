migrate((app) => {
  const text = (name, required = false) => ({ name, type: 'text', required, max: 200 });
  app.save(new Collection({
    name: 'neighbor_reports', type: 'base',
    listRule: null, viewRule: null, createRule: null, updateRule: null, deleteRule: null,
    fields: [text('packetKey', true), text('deviceId', true), text('receivedAt', true),
      { name: 'payload', type: 'json', maxSize: 20000 }],
    indexes: ['CREATE UNIQUE INDEX idx_neighbor_report_packet ON neighbor_reports (packetKey)'],
  }));
  const links = app.findCollectionByNameOrId('link_observations');
  links.fields.add(new TextField({ name: 'reportId', max: 200 }));
  links.fields.add(new JSONField({ name: 'details', maxSize: 2048 }));
  app.save(links);
}, (app) => {
  const links = app.findCollectionByNameOrId('link_observations');
  links.fields.removeByName('reportId');
  links.fields.removeByName('details');
  app.save(links);
  app.delete(app.findCollectionByNameOrId('neighbor_reports'));
});
