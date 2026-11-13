# Winter repeater siting

The field report, input coordinates, road geometry, rasters, route profiles and waypoints stay in the ignored study directory. The published code can be used with the matching private data package.

From the repository root, run the study using Python 3.14 and the existing private cache.

```powershell
python scripts/winter-siting/study.py private/winter-siting
```

The prepared Windows host has its GIS packages in the study’s `envpkgs` folder. On a new machine install `scripts/winter-siting/requirements.txt` in a virtual environment, then copy the private `inputs/` and `source/` folders. The program reads local data and verifies the raw source SHA-256 checksums. Regenerating from the pinned inputs requires no network. The local 5 m and regional 20 m terrain mosaics are reusable derived files. Delete those two mosaics and the terrain-inputs cache marker if changing the projection code or resampling algorithm. Keep the source tiles.

Edit `inputs/study.json` to change sites, heights, priorities, bounds and comparison assumptions. The explicit pins and search seeds use WGS84. Proposed stop-centered sites first get a nominal search point, then the same 20 m refinement as supplied points. The outputs report the two positions. Keep station anchors on their actual premises. The current study uses a metric NAD83 / UTM zone 11N model and a regional DEM extending toward the valley. A different study area requires matching terrain, geometry and projection.

The OSM line extract preserves object IDs from the pinned Geofabrik PBF. If changing the extraction bounds, regenerate `source/local-osm.geojson` from the PBF before running. Derived OpenStreetMap geometry is available under ODbL 1.0, © OpenStreetMap contributors. Source records preserve the original USGS catalog responses and NASA POWER climatology. To restore an absent downloadable source from the manifest, run `python scripts/winter-siting/sources.py private/winter-siting --restore`. A changed provider response fails the checksum and requires the preserved original or a newly reviewed source manifest.

The PDF and GPX appear at the root of the study directory. `gis/` contains the scored boundary, linework, candidate and selected locations, approaches, network edges, segments by status, gaps, individual footprints and single-node losses. GeoJSON is WGS84. GeoTIFF is EPSG:26911 with 255 outside the boundary. Reachability values are 0 for disconnected/blind, 1 for failure-vulnerable, and 2 for surviving every single removal. The visibility and loss files use 0/1. `tables/results.json` contains the full comparison results, including the height tests, optional home and alternate site allocations.

Run independent checks and render every page with:

```powershell
python scripts/winter-siting/verify.py private/winter-siting
```

This cross-check deletes each infrastructure node in a separate NetworkX graph, compares every classified raster cell and matches every selected PDF site/stage, GPX point and GeoJSON site. Page images for visual review appear in `cache/render/`. See the private field report for the survey sequence and the limits of the RF, winter access and solar estimates.
