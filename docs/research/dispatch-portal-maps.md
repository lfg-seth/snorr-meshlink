# Dispatch portal map sources

Primary-source desk research, checked 2026-10-12. Scope: a small authenticated SNORR dispatch portal around Mount Charleston, Nevada. No provider selected, account created, donation application submitted, map downloaded, browser integration tested, or operational availability established.

## Recommended shortlist

Start the map evaluation with **MapLibre GL JS plus USGS Topo and USGS aerial imagery**. This separates the free/open-source browser renderer from free federal map services. It does not require nonprofit approval. Keep commercial providers as alternatives if the federal layers do not give sufficient detail or performance; approval, quota, acquisition dates, and offline rights must be checked for the exact service.

MapLibre is a browser mapping library with WebGL rendering; it supports third-party raster sources as well as vector maps. Its BSD license permits use and modification with the applicable notices. It supplies the renderer, not a free imagery database or hosted tile entitlement. Mobile/tablet/computer suitability still needs a prototype on the actual browsers and rugged Linux Dell. [MapLibre introduction](https://maplibre.org/maplibre-gl-js/docs/), [raster-source example](https://maplibre.org/maplibre-gl-js/docs/examples/map-tiles/), [license](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt).

USGS states that National Map services and downloaded data are free and public domain and requests source acknowledgment. Keep attribution visible and inspect source-specific metadata: historical US Topo maps can include licensed road data, and some non-CONUS imagery has restrictions. Nevada is within CONUS; this is not a blanket license for every layer from every map vendor. [National Map terms FAQ](https://www.usgs.gov/faqs/what-are-terms-uselicensing-map-services-and-data-national-map), [US Topo copyright exceptions](https://www.usgs.gov/faqs/are-usgs-topographic-maps-copyrighted).

| Candidate | What the official service currently documents | Evaluation limitation |
| --- | --- | --- |
| [USGS Topo](https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer) | Multi-scale contours, shaded relief, names, transportation and other reference data; 256-pixel Web Mercator tiles. Metadata reports refresh on September 4, 2026. | Refresh is not proof every road/trail is current. Check Mount Charleston contour legibility, trail coverage, and useful zoom range. |
| [USGS Imagery Only](https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer) | Mostly NAIP aerial imagery at detailed CONUS scales; Landsat/Blue Marble at smaller scales. Metadata gives 2017–2021 CONUS source years and June 2024 cache refresh. | Acquisition dates are older than cache refresh. Published maximum scale is approximately 1:9,028, corresponding to level 16; although cache metadata lists levels through 23, this does not establish useful imagery at those levels. |
| [USGS Imagery Topo](https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer) | Aerial imagery combined with topo reference information; April 2026 metadata refresh; same published approximately 1:9,028 maximum scale. | Source description broadly gives imagery resolution from six inches to one meter, with mostly one-meter NAIP. It does not establish Mount Charleston acquisition year or resolution. |

The imagery above is primarily **aerial photography**, which gives the desired photographic basemap experience; label it “Aerial imagery” rather than implying live satellite observation. Imagery resolution, map display scale, acquisition date, and GPS uncertainty are separate facts. Zooming further cannot create new ground detail.

For a later implementation, the cached service tile path uses ArcGIS order `tile/{z}/{y}/{x}` rather than XYZ order `/{z}/{x}/{y}`. The following templates are candidates derived from the published REST service directories, not a tested application configuration:

```text
https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}
https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}
https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}
```

## Higher-detail NAIP follow-up

The federal [GeoPlatform NAIP Plus ImageServer](https://imagery.geoplatform.gov/iipp/rest/services/NAIP/NAIP_plus/ImageServer) serves USDA imagery through USFS GTAC. It documents 0.3–0.6-meter sources and includes Nevada, but its service-description and description fields disagree on source years: one says 2021–2022 and the other 2022–2023 with exceptions. It exposes `year` and `state` catalog fields. Exact Mount Charleston coverage, acquisition date, source ground resolution, and licensing metadata should be inspected before choosing it. This is an uncached ImageServer, not a drop-in cached XYZ tile URL; adapter/rendering work would need evaluation. The current directory confirms a dataset/service exists, not its performance in the portal.

[USGS NAIP Plus](https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPPlus/ImageServer) and the historical USDA-hosted NAIP endpoint were also checked, but direct fetches failed during research. Do not build the shortlist around assumed availability. The [National Map service directory](https://apps.nationalmap.gov/services/) is the official discovery point for changed endpoints. A source acquisition year must come from local imagery metadata, not the date a search engine crawled a service.

## OpenStreetMap and OpenTopoMap

OpenStreetMap data and OSM's donated public tile infrastructure have different rules. The standard `tile.openstreetmap.org` policy allows normal interactive viewing with visible attribution, identifying requests and compliant caching. It explicitly forbids bulk prefetch and offline-download features, and service can be blocked without notice. Use a self-hosted dataset or a provider with explicit offline rights for downloaded regional maps. It is a reference-map option, not satellite imagery. [OSMF tile policy](https://operations.osmfoundation.org/policies/tiles/).

OpenTopoMap's own repository describes an OSM/SRTM topographic map with a CC-BY-SA online map and files for running one's own server. Crucially, its current README marks old raster tiles deprecated and describes a move to vector tiles. The official usage page could not be fetched during this check. Therefore, do not assume the familiar public raster endpoint is a stable operational dependency, that bulk regional downloading is permitted, or that its Garmin downloads can be embedded in this browser portal. The Garmin maps have a separate CC-BY-NC-SA license. Keep OpenTopoMap as a secondary cartography candidate after verifying the current service/policy. [OpenTopoMap repository README](https://github.com/der-stefan/OpenTopoMap/blob/master/README.md), [official usage page](https://opentopomap.org/about#verwendung).

## Nonprofit and commercial alternatives

| Provider | Verified opportunity | Limits relevant to this portal |
| --- | --- | --- |
| [Mapbox nonprofit support](https://www.mapbox.com/nonprofit) | Offers donated or discounted services, guidance and promotion. If usage exceeds free tiers, applications are reviewed in May/November; approved support starts July/January and requires annual renewal. | SAR nonprofit status does not establish acceptance or a particular free allowance. Evaluate normal quota first; obtain actual award and use rights before budgeting on a donation. Raster imagery API is usable by compatible XYZ renderers, with tokens and API billing. [Raster Tiles API](https://docs.mapbox.com/api/maps/raster-tiles/). |
| [Esri Nonprofit Program](https://www.esri.com/en-us/industries/nonprofit/nonprofit-program) | US eligibility requires 501(c)(3) public-charity status plus review of activities; TechSoup verification precedes the application. Includes discounted software, maps and developer tools. | It is discounted access, not automatically free imagery. Esri's published 2025 flier lists ArcGIS Online at $100/year and ArcGIS Pro at $100/year; confirm current exact package, seats, credits, custom portal usage and imagery/offline rights. [Pricing flier](https://www.esri.com/content/dam/esrisites/en-us/media/fliers/nonprofit-program-pricing.pdf). |
| [MapTiler Cloud](https://www.maptiler.com/cloud/pricing/) | Free plan for testing/personal/noncommercial use; current directly opened page lists Flex at $30/month plus extra traffic. Quota exhaustion pauses the free service. | No specific nonprofit donation entitlement was verified. Terms permit temporary individual-device caching, while proxying, export and bulk downloads generally need written agreement. More seriously, §7.6.4 restricts services whose failure/use could cause death, injury or environmental/property damage; clarify suitability/appropriate agreement before treating it as an operational SAR option. [Cloud terms](https://www.maptiler.com/terms/cloud/). |

Published prices are research references only, not booked expenses, quotes, subscriptions, or approved spending. Hosted tile usage and offline rights are separate from the renderer's license. A nonprofit award does not by itself settle every API, redistribution, or safety-related use restriction.

## Offline and prototype prerequisites

Offline maps remain a separate requirement and **have not been verified**. A portal hosted only in the home Proxmox VM is not reachable from an isolated command post merely because its map tiles were downloaded. Local portal access, local radio ingestion, map assets and authentication each need a deliberate outage path.

For the map portion, a defensible direction is to download authorized federal source products for a bounded AO, record acquisition date/resolution/credits, then generate and serve local tiles. PMTiles is a possible packaging format: its official tooling documents GeoTIFF conversion and local tile serving. This establishes available tools, not a proven browser offline workflow or permission to scrape any public tile service. [PMTiles creation](https://docs.protomaps.com/pmtiles/create), [local serving](https://docs.protomaps.com/pmtiles/cli).

Before choosing layers, test:

1. Mount Charleston visual coverage, trails, contours, useful close zoom, and per-area imagery dates.
2. Tile fetches, browser cross-origin behavior, attribution, panning/zooming performance and mobile/tablet layout with member pins and history overlays.
3. Provider failures and internet loss: make map unavailability visible while position-age and connectivity indicators remain distinguishable.
4. The bounded offline AO/zoom levels, storage size, authorized source download route and refresh procedure; verify a cold start without internet on the actual field equipment.

The strongest current first step is an online map prototype using the three USGS layers above. Do not make SAR access to an unapproved donation, an old raster endpoint, or a silently cached browser viewport a prerequisite for the tracking pilot.
