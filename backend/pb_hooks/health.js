const c = require(`${__hooks}/common.js`);
// Run in an existing transaction. Feed loss never creates device-missing incidents.
function evaluate(app) {
  const feed = c.feed(app);
  if (!c.online(feed)) return;
  const now = Date.now();
  c.rows(app, 'devices', 'kind != "member"').forEach((device) => {
    const id = device.getString('key');
    const config = c.object(device, 'configuration');
    const readings = c.object(device, 'readings');
    const ruleRecord = c.first(app, 'rules', 'deviceId = {:id}', { id });
    const sharedRule = c.first(app, 'rules', 'deviceId = "*"', {});
    const rule = ruleRecord
      ? c.object(ruleRecord, 'payload')
      : sharedRule
        ? c.object(sharedRule, 'payload')
        : null;
    const batteryCadence =
      (config.reportCadenceMinutes || {}).battery || config.cadenceMinutes || 5;
    const batteryTimeout =
      ((config.missingTimeoutMinutes || {}).battery || batteryCadence * 3) *
      60000;
    const restored = Date.parse(feed.getString('restoredAt')) || 0;
    const enabledAt =
      Date.parse(device.getString('monitoringStartedAt')) || now;
    ['battery', 'solar', 'temperature', 'intrusion'].forEach((metric) => {
      const equipped =
        metric === 'battery' ||
        (config.equipped || {})[
          { temperature: 'weather', solar: 'solar', intrusion: 'intrusion' }[
            metric
          ]
        ];
      if (!equipped || (config.disabledMonitoring || []).indexOf(metric) >= 0)
        return;
      const metricEnabledAt =
        Date.parse((config.monitoringStartedAtByMetric || {})[metric]) ||
        enabledAt;
      const cadence =
        (config.reportCadenceMinutes || {})[metric] ||
        config.cadenceMinutes ||
        5;
      const timeout =
        ((config.missingTimeoutMinutes || {})[metric] || cadence * 3) * 60000;
      const reading = readings[metric];
      const measured =
        reading && reading.measuredAt ? Date.parse(reading.measuredAt) : 0;
      const fresh = measured > 0 && now - measured < timeout && measured <= now;
      const kind = `missing:${metric}`;
      const warning = c.first(
        app,
        'warnings',
        'deviceId = {:id} && kind = {:kind} && recoveredAt = ""',
        { id, kind },
      );
      if (
        !fresh &&
        now >= Math.max(metricEnabledAt, restored) + timeout &&
        !warning
      ) {
        c.create(app, 'warnings', { deviceId: id, kind, openedAt: c.now() });
        c.event(
          app,
          id,
          `Missing ${metric} reports: three configured reporting intervals elapsed.`,
        );
      }
      // Recovery needs a fresh sample, not merely a restored worker heartbeat.
      if (fresh && warning) {
        warning.set('recoveredAt', c.now());
        app.save(warning);
        c.event(
          app,
          id,
          `${metric} missing-report warning recovered on fresh evidence.`,
        );
      }
    });
    const battery = readings.battery;
    if (
      !rule ||
      rule.enabled === false ||
      !battery ||
      !battery.measuredAt ||
      now - Date.parse(battery.measuredAt) >= batteryTimeout
    )
      return;
    const warning = c.first(
      app,
      'warnings',
      'deviceId = {:id} && kind = "battery" && recoveredAt = ""',
      { id },
    );
    if (battery.value < rule.trigger && !warning) {
      c.create(app, 'warnings', {
        deviceId: id,
        kind: 'battery',
        openedAt: c.now(),
      });
      c.event(app, id, 'Low-battery warning opened on fresh voltage evidence.');
    } else if (warning && battery.value >= rule.recovery) {
      warning.set('recoveredAt', c.now());
      app.save(warning);
      c.event(
        app,
        id,
        'Battery warning recovered at the separate recovery threshold.',
      );
    }
  });
}
module.exports = { evaluate };
