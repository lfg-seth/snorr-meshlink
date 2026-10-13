# Check dispatch map sources and nonprofit access

Type: research
Label: wayfinder:research
Status: resolved
Assignee: codex-portal-map-research-2026-10-12
Parent: ../map.md
Blocked by: none

## Question

Which primary-source-backed map renderers, topographic and satellite/imagery sources, and nonprofit programs could support a small SAR dispatch portal around Mount Charleston, including online use, attribution, limits, and offline availability?

## Comments

### 2026-10-12

Separate open-source rendering software from map data, imagery, hosting rights, and nonprofit eligibility; no purchase, application, or provider selection authorized by this research.

## Answer

Completed primary-source [dispatch portal map research](../../../docs/research/dispatch-portal-maps.md) on 2026-10-12. Recommended evaluation shortlist: MapLibre GL JS for the open-source browser renderer, plus free USGS Topo, Imagery Only, and Imagery Topo services. Imagery is primarily aerial photography; source acquisition date and resolution must be verified locally, independently of cache refresh date and displayed zoom.

Mapbox has an application-based nonprofit donation/discount program; Esri has reviewed, discounted nonprofit access rather than guaranteed free access. MapTiler's specific nonprofit entitlement was not verified, its bulk/offline terms require care, and its operational safety restriction needs explicit suitability clarification for SAR.

OSM standard public tiles explicitly prohibit offline prefetch; OpenTopoMap's own current README deprecates old raster tiles and describes a vector transition. Offline rights, local portal/radio access, packaging, actual AO coverage/age, and browser/device compatibility remain implementation tests. No provider selected, donation approved, spending recorded, service deployed, or operational/offline behavior measured.
