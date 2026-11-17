# G006 at Terry Home

On 2026-11-16 the owner selected existing Heltec V3 **!b03d6790** for fixed
Wi-Fi backhaul. It has a Muzi antenna and a 1,000 mAh battery according to the
owner and will use AC power at the site. The owner approved the fixed display
pin **36.26153180096932, -115.18904437592454** for GitHub and the portal.

## Board configuration

COM41 returned hardware ID `82575ef52d9bdfa05f26cb3d83e71348` and the same
radio ID as the [original G006](g005-g006-provisioning.md). Its complete
owner, channel, local and module configuration matched that board's prior
verified profile. A fresh private backup was taken before writing.

The installed target **heltec-v3-gateway / 2.7.26.6fea6aa** matched the
[verified V3 gateway build](g003-mobile-gateway.md). The reference application
SHA256 was rechecked as
`c26a61e96b4553958c4632bb4074e89bbea0a214dbed15289cc2bbf54f5263f7`.
The newer survey and SD images in the firmware fork target other functions
or hardware. The existing application was retained.

Set the long name to **Terry Home**, retained short name **G006**, installed
the supplied Wi-Fi settings and disabled GPS acquisition for the fixed site.
Radio coordinates read back as **36.2615318, -115.1890444**, to the board's
seven decimal places. No altitude was supplied.

The complete intended profile and coordinates passed independent USB readback
before and after an explicit reboot. Verification included the exact Wi-Fi
credentials, the board's own keys and admin settings, private channel, CLIENT
role, slot 35, MQTT permission, encrypted TLS uplink, disabled channel
downlink and 180-second device telemetry interval.

At **2026-11-17 02:48:19 UTC** (November 16 at **18:48 Pacific**) the
post-reboot USB session read the saved profile. The board's connection-status
response reported **Wi-Fi disconnected and direct MQTT disconnected**.
A second USB check at **02:50:19 UTC** returned the same states and passed
the full profile comparison again. Both serial sessions closed.
Private backups, intended profile, logs and readbacks are under the ignored
`private/bench/g006-terry-20261116/` directory.

## Production portal and radio receipts

[MeshLink 0.4.3](https://github.com/lfg-seth/snorr-meshlink/pull/75) deployed
from `31a905b`. The production registry retains the existing physical device
row for **!b03d6790**, its history and its gateway/source mappings. The field
roster uses the approved display pin, which matches the saved radio position
to seven decimal places. In a signed-in Edge session, the
[map](https://meshlink.spp.lol/#map) rendered all nine markers including G006,
the [Infrastructure card](https://meshlink.spp.lol/#infrastructure) showed
Terry Home, Heltec V3, Muzi antenna, 1,000 mAh battery and planned AC power,
and Activity listed G006 with attention status. At **02:57:09 UTC**, the
authenticated check passed for all nine cards, ten public asset hashes and
seven production services.

From **02:48:19 to 02:57:09 UTC** on November 17, production accepted a
gateway-health report at **02:51:24.599** and a neighbor report at
**02:51:25.767**, both originating on G006 and arriving through **!9ea13cc0**.
Those are server receipt times. The health report advertised a 180-second
interval and reported Wi-Fi and direct MQTT disconnected. Its source clock
was unknown, so the server archived the report without applying it to current
gateway health. There were zero accepted or duplicate receipts with G006 as
the receiving gateway during that interval.

## On-site check

With the gateway on AC at Terry Home, confirm Wi-Fi and direct MQTT connect
and verify a fresh, non-retained receipt with G006 as the receiving gateway.
Packets from G006 seen through a peer can establish RF contact only.
