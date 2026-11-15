# Winter repeater siting

The field report, input coordinates, road geometry, rasters, route profiles and waypoints stay in the ignored study directory. The published code can be used with the matching private data package.

From the repository root, run the study using Python 3.14 and the existing private cache.

```powershell
python scripts/winter-siting/study.py private/winter-siting
```

The prepared Windows host has its GIS packages in the study’s `envpkgs` folder. On a new machine install `scripts/winter-siting/requirements.txt` in a virtual environment, then copy the private `inputs/` and `source/` folders. The program reads local data and verifies the raw source SHA-256 checksums. Regenerating from the pinned inputs requires no network. The local 5 m and regional 20 m terrain mosaics are reusable derived files. Delete those two mosaics and the terrain-inputs cache marker if changing the projection code or resampling algorithm. Keep the source tiles.

Edit `inputs/study.json` to change sites, heights, priorities, bounds and comparison assumptions. The explicit pins and search seeds use WGS84. Proposed stop-centered sites first get a nominal search point, then the same 20 m refinement as supplied points. The outputs report the two positions. Keep station anchors on their actual premises. The current study uses a metric NAD83 / UTM zone 11N model and a regional DEM extending toward the valley. A different study area requires matching terrain, geometry and projection.

The OSM line extract preserves object IDs from the pinned Geofabrik PBF. If changing the extraction bounds, regenerate `source/local-osm.geojson` from the PBF before running. Derived OpenStreetMap geometry is available under ODbL 1.0, © OpenStreetMap contributors. Source records preserve the original USGS catalog responses and NASA POWER climatology. To restore an absent downloadable source from the manifest, run `python scripts/winter-siting/sources.py private/winter-siting --restore`. A changed provider response fails the checksum and requires the preserved original or a newly reviewed source manifest.

The current packet is `Mount-Charleston-winter-field-plan-Sisters.pdf`. The accompanying `navigation.gpx` contains the ten proposed repeaters, both station gateways, all twelve staging points and the alternate Angel Peak drive-up point. The separate `expansion-trials.gpx` marks the first winter trials, the longer ridge trials, an alternate for the marginal ridge link, staging and six marked road test references. Use one expansion pair at a time. `gis/` holds the scored boundary, routes, sites, approaches, network edges, road gaps and individual footprints. GeoJSON uses WGS84. GeoTIFF uses EPSG:26911 with 255 outside the boundary. Reachability is 1 where a station can receive a member packet and 0 elsewhere inside the boundary. Route status is `reachable` or `blind`.

The editable Angel Peak approach lists OSM way IDs and both drive-up destinations. The graph follows connected centerlines from their junction with SR 158 to the closest on-road point at each destination and counts shared pavement once. The outer road toward US 95 ends outside this objective. The helipad search permits agency access near the Upper Bristlecone trail while screening walking and landing surfaces, roads, roofs and steep ground. Each drive-up alternative gets a fresh search for the other eight sites. Results, heights and the optional home comparison are in `tables/results.json`.

Maps, bookmarks, GPX waypoint names and field sheets use the same human-readable names. For example, LB is Lower Bristlecone and SG is Showgirl. In the site, staging and approach GeoJSON layers, display `field_name` and `field_code`. Use the original `id` to join model tables, link endpoints, profile filenames and rasters. The dictionary in `field_names.py` records the crosswalk. These labels refer to proposed sites. Board assignments belong to the deployment roster.

The highway page uses one common north-up extent for the mountain roads. The station map traces paths to Lee and Kyle. The ten individual footprint panels share a common scale. The valley map draws local streets, arterials and highways from the same pinned Nevada PBF, cached for offline reruns.

The input fixes the previous nine and Sisters at their original micro-sites. Terrain profiles, road samples, forwarding cap and station positions stay consistent across counts. After the original shoulder and stop searches, 3,923 eligible grid points within 1.8 km of SR 156 or Macks Canyon were screened on a 100 m grid. Twelve dispersed candidates were carried through the 20 m mount refinement, native-resolution links and complete road sampling. To reproduce the supplementary screening with the cached ten-site model, run `python scripts/winter-siting/scout.py private/winter-siting`. The shortlist appears in `tables/lee-ridge-scout.json`; the reviewed locations and field names are in the study inputs. The standard study command already includes them.

The expansion comparison ranks net newly served length on the two target roads, then all scored roads, then the existing weighted score. The primary ranking considers every compatible, gateway-connected singleton and pair. The two-site field sequence requires one candidate to work independently at eleven. The separate conservative comparison requires at least 60% first-Fresnel clearance on newly introduced links. The practical winter pair also caps estimated ascent and distance at the Fletcher approach. `tables/results.json` preserves the all-candidate scores, winning paths, per-road gains and longest gaps. `gis/route-status.geojson` records prior-nine, ten and ridge-pair road/trail status as well as nine/ten Lee-only status. `gis/winter-trial-roads.geojson` stores ten, eleven and twelve statuses for the shorter winter approaches. Terrain search cannot determine radio congestion.

Run independent checks and render every page.

```powershell
python scripts/winter-siting/verify.py private/winter-siting
```

Verification compares station masks with the combined raster, traces expansion paths, remeasures staged route geometry, checks the winter access benchmark and matches the PDF site sheets and GPX coordinates. Use the mountain-side staging waypoint and the Vegas-side drive-up test waypoint for the owner's two exact vehicle positions. Page images for visual review appear in `cache/render/`.
