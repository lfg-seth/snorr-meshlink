migrate((app) => {
  const text = (name, required = false) => ({ name, type: 'text', required, max: 200 });
  const privateRules = { listRule: null, viewRule: null, createRule: null, updateRule: null, deleteRule: null };
  app.save(new Collection({
    name: 'neighbor_frontiers', type: 'base', ...privateRules,
    fields: [text('observerKey', true), { name: 'payload', type: 'json', maxSize: 2048 }],
    indexes: ['CREATE UNIQUE INDEX idx_neighbor_frontier_observer ON neighbor_frontiers (observerKey)'],
  }));
  app.save(new Collection({
    name: 'neighbor_current', type: 'base', ...privateRules,
    fields: [text('pairKey', true), text('observerKey', true), text('anchorReceivedAt', true),
      { name: 'payload', type: 'json', maxSize: 4096 },
      { name: 'watermark', type: 'json', maxSize: 1024 }],
    indexes: ['CREATE UNIQUE INDEX idx_neighbor_current_pair ON neighbor_current (pairKey)',
      'CREATE INDEX idx_neighbor_current_anchor ON neighbor_current (anchorReceivedAt)'],
  }));
  // The archive already owns boot history; do not copy it into growing boot lists.
  const reports = app.findCollectionByNameOrId('neighbor_reports');
  reports.indexes.push('CREATE INDEX idx_neighbor_report_source_boot ON neighbor_reports (deviceId, json_extract(payload, \'$.observerNodeId\'), json_extract(payload, \'$.bootId\'))');
  app.save(reports);
  const links = app.findCollectionByNameOrId('link_observations');
  links.indexes.push('CREATE INDEX idx_links_observed_at ON link_observations (observedAt)');
  app.save(links);
  // No historical signal is re-anchored or promoted into current state here.
}, (app) => {
  const reports = app.findCollectionByNameOrId('neighbor_reports');
  reports.indexes = reports.indexes.filter((sql) => !sql.includes('idx_neighbor_report_source_boot'));
  app.save(reports);
  const links = app.findCollectionByNameOrId('link_observations');
  links.indexes = links.indexes.filter((sql) => !sql.includes('idx_links_observed_at'));
  app.save(links);
  app.delete(app.findCollectionByNameOrId('neighbor_current'));
  app.delete(app.findCollectionByNameOrId('neighbor_frontiers'));
});
