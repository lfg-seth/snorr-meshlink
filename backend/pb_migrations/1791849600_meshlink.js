migrate(
  (app) => {
    const text = (name, required = false) => ({
      name,
      type: 'text',
      required,
      max: 500,
    });
    const json = (name) => ({ name, type: 'json', maxSize: 65536 });
    const create = (name, fields, indexes = []) => {
      const collection = new Collection({
        name,
        type: 'base',
        fields,
        listRule: null,
        viewRule: null,
        createRule: null,
        updateRule: null,
        deleteRule: null,
        indexes,
      });
      app.save(collection);
    };
    app.save(
      new Collection({
        name: 'accounts',
        type: 'auth',
        fields: [
          { name: 'email', type: 'email', required: false },
          text('username', true),
          text('name', true),
          text('memberId'),
          {
            name: 'role',
            type: 'select',
            required: true,
            maxSelect: 1,
            values: ['admin', 'member', 'worker'],
          },
        ],
        passwordAuth: { enabled: true, identityFields: ['username'] },
        authToken: { duration: 3600 },
        listRule: null,
        viewRule: 'id = @request.auth.id',
        createRule: null,
        updateRule: null,
        deleteRule: null,
        manageRule: null,
        indexes: [
          'CREATE UNIQUE INDEX idx_accounts_username ON accounts (username)',
          "CREATE UNIQUE INDEX idx_accounts_member ON accounts (memberId) WHERE memberId != ''",
        ],
      }),
    );
    create(
      'members',
      [text('key', true), text('name', true), text('initials')],
      ['CREATE UNIQUE INDEX idx_members_key ON members (key)'],
    );
    create(
      'devices',
      [
        text('key', true),
        text('kind', true),
        text('number'),
        text('shortName'),
        json('configuration'),
        json('latestPosition'),
        json('readings'),
        text('lastContactAt'),
        text('monitoringStartedAt'),
      ],
      ['CREATE UNIQUE INDEX idx_devices_key ON devices (key)'],
    );
    create(
      'assignments',
      [
        text('deviceId', true),
        text('memberId', true),
        text('startedAt', true),
        text('endedAt'),
        text('actorId'),
      ],
      [
        "CREATE UNIQUE INDEX idx_active_device ON assignments (deviceId) WHERE endedAt = ''",
        "CREATE UNIQUE INDEX idx_active_member ON assignments (memberId) WHERE endedAt = ''",
      ],
    );
    create(
      'positions',
      [
        text('packetKey', true),
        text('deviceId', true),
        text('memberId'),
        text('measuredAt'),
        text('timestampQuality', true),
        text('receivedAt', true),
        json('payload'),
      ],
      [
        'CREATE UNIQUE INDEX idx_positions_packet ON positions (packetKey)',
        'CREATE INDEX idx_positions_device_time ON positions (deviceId, measuredAt)',
      ],
    );
    create('packet_receipts', [
      text('packetKey'),
      text('deviceId'),
      text('gatewayId'),
      text('receivedAt', true),
      text('ingestedAt', true),
      text('outcome', true),
      text('reason'),
      json('payload'),
    ]);
    create(
      'observations',
      [
        text('packetKey', true),
        text('deviceId', true),
        text('measuredAt'),
        text('timestampQuality', true),
        text('receivedAt', true),
        json('payload'),
      ],
      [
        'CREATE UNIQUE INDEX idx_observations_packet ON observations (packetKey)',
      ],
    );
    create(
      'messages',
      [
        text('packetKey'),
        text('authorId'),
        text('author', true),
        text('text', true),
        text('at', true),
        text('direction', true),
        text('evidence', true),
      ],
      [
        "CREATE UNIQUE INDEX idx_messages_packet ON messages (packetKey) WHERE packetKey != ''",
      ],
    );
    create('send_attempts', [
      text('messageId', true),
      text('gatewayId', true),
      text('at', true),
      text('status', true),
    ]);
    create('name_jobs', [
      text('deviceId', true),
      text('assignmentId', true),
      text('longName', true),
      text('status', true),
      text('at', true),
    ]);
    create(
      'incidents',
      [
        text('deviceId', true),
        text('openedAt', true),
        text('acknowledgedAt'),
        text('acknowledgedBy'),
        text('resolvedAt'),
        text('resolvedBy'),
        text('note'),
      ],
      [
        "CREATE UNIQUE INDEX idx_open_intrusion ON incidents (deviceId) WHERE resolvedAt = ''",
      ],
    );
    create(
      'warnings',
      [
        text('deviceId', true),
        text('kind', true),
        text('openedAt', true),
        text('recoveredAt'),
        text('acknowledgedAt'),
        text('acknowledgedBy'),
      ],
      [
        "CREATE UNIQUE INDEX idx_open_warning ON warnings (deviceId, kind) WHERE recoveredAt = ''",
      ],
    );
    create(
      'rules',
      [text('deviceId', true), json('payload')],
      ['CREATE UNIQUE INDEX idx_rules_device ON rules (deviceId)'],
    );
    create('events', [
      text('deviceId'),
      text('at', true),
      text('actorId'),
      text('text', true),
    ]);
    create(
      'feed',
      [
        text('key', true),
        text('heartbeatAt'),
        text('restoredAt'),
        { name: 'connected', type: 'bool' },
        { name: 'forcedOffline', type: 'bool' },
      ],
      ['CREATE UNIQUE INDEX idx_feed_key ON feed (key)'],
    );
    const feed = new Record(app.findCollectionByNameOrId('feed'));
    feed.set('key', 'worker');
    feed.set('connected', false);
    app.save(feed);
    const settings = app.settings();
    settings.meta.appName = 'SNORR MeshLink';
    settings.logs.logIP = false;
    settings.rateLimits.enabled = true;
    app.save(settings);
  },
  (app) => {
    // Explicit migration rollback deletes pilot data; take a backup before using it.
    [
      'feed',
      'events',
      'rules',
      'warnings',
      'incidents',
      'name_jobs',
      'send_attempts',
      'messages',
      'observations',
      'packet_receipts',
      'positions',
      'assignments',
      'devices',
      'members',
      'accounts',
    ].forEach((name) => app.delete(app.findCollectionByNameOrId(name)));
  },
);
