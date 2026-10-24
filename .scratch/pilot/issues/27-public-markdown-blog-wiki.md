# LOCAL-5 - Public Markdown blog and hardware documentation/wiki

Created 2026-10-23. Status: Deferred; owner-requested side-tangent ticket.
Capture only; site implementation and publication are not started.

## Requested outcome

The existing site has a public blog and documentation/wiki section driven by
repository Markdown. Updating approved public Markdown and deploying the site
updates the corresponding page. Each node type has a page explaining hardware,
assembly, configuration and operation with actual photographs.

## Acceptance sections

- [ ] Implement the owner's broad-public-content direction in
  [content policy](../../../records/content.md#public-documentation-direction---2026-10-23).
  Include human-readable hardware/setup, designs, tests/results, project decisions,
  release notes and suitable inventory/cost summaries. Use an explicit published
  content directory/allowlist, asset directory, metadata, slugs and draft status
  to select reader-ready material rather than categorically hiding operations.
- [ ] Exclude internal agent instructions/prompts, raw session/task bookkeeping
  from site rendering. Provisionally exclude issue/task pages; confirm that final
  boundary when implementing. Preserve existing secrets/member/raw-track privacy.
- [ ] Provide draft and owner copyedit/review stages before public rendering.
  Owner expects to edit most/all prose for a natural human voice: concrete facts,
  useful steps/photos, measured outcomes and limitations, without generic AI filler.
- [ ] Implement blog index/date ordering and permanent article pages; implement
  documentation index/navigation and per-node pages with headings, internal links,
  images/captions/alt text, code blocks and mobile-readable layout. Clarify any
  search requirement when implementation is selected.
- [ ] Integrate content validation/rendering into the existing site's build and
  release process. Use manual deployment without a staging site for now. Verify an approved
  Markdown/image change updates the deployed
  page and index; drafts stay hidden, removed/renamed pages have defined behavior,
  links work and old assets/content do not linger. Record update/rollback steps.
- [ ] Keep public content separate from authenticated live tracking and member
  information. Treat embedded HTML safely and review photo metadata/backgrounds
  for sensitive information before public release.
- [ ] Seed pages for Heltec V3 gateways, RAK4631 repeaters and Heltec V4 member
  trackers, distinguishing hardware variants and board-specific firmware.
  Each includes parts, wiring/power path, enclosure/print files where applicable,
  setup/profile steps without secrets, photos, verification and known limits.
- [ ] Reuse the new `docs/hardware/` source notes after public-content review;
  relocate/rewrite internal links for public navigation. Preserve one maintained
  source per page rather than divergent wiki and repository copies.
- [ ] Confirm intended public site and authorize publication when ready. Current
  authorization covers ticket/docs capture and GitHub records, not a site launch.

Content owner: LOCAL-4 for gateway hardware and measurements, LOCAL-3 for RAK
firmware readiness. No stock photo or generated illustration counts as an actual
assembly photograph; absent photos remain explicitly pending.

Next when activated: select public source layout and site build integration,
then deliver a reviewable draft using the hardware pages. No new hosting or CMS
purchase is selected.
