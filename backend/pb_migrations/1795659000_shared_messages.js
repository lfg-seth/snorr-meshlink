migrate((app) => {
  const attempts = app.findCollectionByNameOrId('send_attempts');
  attempts.fields.add(new TextField({name: 'requestKey', max: 100}));
  attempts.fields.add(new TextField({name: 'requestText', max: 280}));
  attempts.addIndex('idx_send_request', true, 'requestKey', "requestKey != ''");
  app.save(attempts);
}, (app) => {
  const attempts = app.findCollectionByNameOrId('send_attempts');
  attempts.removeIndex('idx_send_request');
  attempts.fields.removeByName('requestKey');
  attempts.fields.removeByName('requestText');
  app.save(attempts);
});
