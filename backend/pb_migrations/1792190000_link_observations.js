migrate((app) => {
  const text = (name, required = false) => ({ name, type: 'text', required, max: 200 });
  app.save(new Collection({
    name: 'link_observations', type: 'base',
    listRule: null, viewRule: null, createRule: null, updateRule: null, deleteRule: null,
    fields: [
      text('observerDeviceId', true), text('heardDeviceId'), text('originalSourceDeviceId'),
      { name: 'source', type: 'select', required: true, maxSelect: 1, values: ['gateway', 'neighbor'] },
      { name: 'path', type: 'select', required: true, maxSelect: 1, values: ['direct', 'relayed', 'unknown'] },
      { name: 'signal', type: 'json', maxSize: 256 },
      text('receivedAt', true), text('observedAt'),
    ],
    indexes: ['CREATE INDEX idx_links_observer_time ON link_observations (observerDeviceId, receivedAt)'],
  }));
}, (app) => app.delete(app.findCollectionByNameOrId('link_observations')));
