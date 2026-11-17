migrate((app) => {
  const collection = new Collection({
    name: 'field_roster', type: 'base',
    listRule: null, viewRule: null, createRule: null, updateRule: null, deleteRule: null,
    fields: [
      { name: 'radio', type: 'text', required: true, pattern: '^![0-9a-f]{8}$' },
      { name: 'shortName', type: 'text', required: true, max: 32 },
      { name: 'name', type: 'text', required: true, max: 120 },
      { name: 'kind', type: 'select', required: true, maxSelect: 1,
        values: ['repeater', 'offlineRecorder', 'stationBackhaul', 'mobileGateway'] },
      { name: 'pin', type: 'json', maxSize: 512 },
      { name: 'batterySetup', type: 'text', max: 200 },
      { name: 'antenna', type: 'text', max: 200 },
      { name: 'solarSetup', type: 'text', max: 200 },
      { name: 'sortOrder', type: 'number', onlyInt: true },
    ],
    indexes: ['CREATE UNIQUE INDEX idx_field_roster_radio ON field_roster (radio)'],
  });
  app.save(collection);
  const previousRoster = [
    ["!f95b5501", "R001", "Cathedral Rock", "repeater", {"latitude": 36.25631, "longitude": -115.64886}, ""],
    ["!a65601b3", "R005", "Angel Peak Vegas Side", "repeater", {"latitude": 36.31763, "longitude": -115.57288}, ""],
    ["!638b9515", "R006", "Lee Junction", "repeater", {"latitude": 36.34236, "longitude": -115.65398}, ""],
    ["!120b04fd", "R008", "Kyle Junction", "repeater", {"latitude": 36.26259, "longitude": -115.60118}, ""],
    ["!da581e5f", "R009", "Sahara", "repeater", {"latitude": 36.14484090826288, "longitude": -115.11061987480886}, ""],
    ["!77fdb9f1", "R010", "Upper Bristle", "repeater", {"latitude": 36.30648, "longitude": -115.67843}, ""],
    ["!8737c2c9", "R011", "Angel Peak Mountain Side", "repeater", {"latitude": 36.31879, "longitude": -115.58049}, ""],
    ["!1bbf0638", "G001", "Lee Fire Station", "stationBackhaul", {}, "Owner-reported 5 W panels via USB-C"],
    ["!1bbf0ab8", "G002", "Shady Hollow", "offlineRecorder", {"latitude": 36.27274, "longitude": -115.5843}, ""],
    ["!b03d6790", "G006", "Terry Home", "stationBackhaul", {"latitude": 36.26153180096932, "longitude": -115.18904437592454}, ""],
    ["!849ad7a0", "G003", "Seth Mobile", "mobileGateway", {}, ""]
  ];
  previousRoster.forEach(([radio, shortName, name, kind, pin, solarSetup], sortOrder) => {
    const row = new Record(collection);
    for (const [key, value] of Object.entries({radio, shortName, name, kind, pin, solarSetup, sortOrder}))
      row.set(key, value);
    if (kind === 'repeater' || kind === 'offlineRecorder') {
      row.set('batterySetup', 'Eight cells');
      row.set('antenna', 'Muzi');
    }
    app.save(row);
  });
}, (app) => app.delete(app.findCollectionByNameOrId('field_roster')));
