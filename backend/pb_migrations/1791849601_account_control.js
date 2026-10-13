migrate((app) => {
  const accounts = app.findCollectionByNameOrId('accounts');
  accounts.fields.getByName('role').values = [
    'admin',
    'member',
    'worker',
    'disabled',
  ];
  accounts.authRule = 'role != "disabled"';
  app.save(accounts);
});
