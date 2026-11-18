# Mount Charleston repeater study using the reachable November 17 waypoints

**First outing. Take a portable to Mack’s alternative and keep the deployed radios operating as controls.** Try ordinary member GPS traffic over **Angel Mountain → Mack’s → Upper Bristlecone → Lee Fire**. Adding Mack’s alone raises modeled reach from 11.3% to 31.0% of the same 39.61 km of sampled highway. The previous 94.6% option depended on ridge sites omitted from the owner’s revised KML. Its results describe a different set of placements. [Earlier study](mountain-siting-20261117.md)

## What to test at Mack’s

| Direct path at nominal mounts | Distance | Minimum terrain clearance | Minimum first Fresnel clearance |
| --- | ---: | ---: | ---: |
| Mack’s to Upper Bristlecone | 5.58 km | +2.05 m | 68% |
| Upper Bristlecone to Lee Fire | 1.73 km | +1.31 m | 124% |
| Mack’s to Angel Mountain | 6.96 km | +3.72 m | 40% |
| Mack’s to Angel Vegas alternative | 7.38 km | +4.04 m | 213% |
| Mack’s directly to Lee Fire | 3.89 km | −43.26 m | Blocked |

Raise the test antenna at Mack’s to the intended **4 m above ground** if the site supports it. With Upper Bristlecone at 4 m and Mack’s at 2 m, the modeled minimum is **+0.06 m**, with just 2% first Fresnel clearance. A low handheld test could miss the best link. At the proposed height the weaker leg is Angel Mountain. Record actual heights, reciprocal packet IDs and the member GPS fix and receipt times at Lee. Confirm G001 power and uplink before interpreting a missing dispatch receipt. Compare a known working route before and after each trial, including with the tracker worn on foot. The field criterion remains a GPS fix less than 15 minutes old. [Field AAR](../../records/aar/2026-11-15-mount-charleston.md)

## Should R005 move on Angel Peak?

**Use a portable at the supplied Angel Vegas alternative before moving R005.** The alternative clears Mack’s by 4.04 m. Deployed R005’s modeled path to Mack’s is blocked by 43.63 m. The alternative also reaches 20 of 36 modeled valley receivers, compared with 19 for R005. These are four sets of nine outdoor 4 m probes. They do not measure the fraction of Las Vegas covered.

| Angel position | Centennial Hills | Lone Mountain foothills | Providence / northwest | Western North Las Vegas | Direct to Shady Hollow |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deployed Angel Vegas / R005 | 6/9 | 0/9 | 4/9 | 9/9 | −116.6 m |
| Owner’s Angel Vegas alternative | 7/9 | 0/9 | 4/9 | 9/9 | −124.2 m |
| Deployed Angel Mountain / R011 | 0/9 | 0/9 | 0/9 | 0/9 | −120.6 m |
| Angel road survey 5 | 0/9 | 0/9 | 0/9 | 0/9 | −117.1 m |

**Shady is the deciding field test.** Its offline G002 recorder previously captured direct packets from the deployed R005 and R011 despite both modeled obstructions. Compare numbered packets from R005 and the proposed pin at the same antenna height with G002 recording and one stationary valley receiver listening. Read the SD card to check the direct sender and count, then separately verify a normal GPS packet at Lee. G002 currently records offline with forwarding disabled. [Earlier study and SD evidence](mountain-siting-20261117.md#preferred-full-layout)

**Angel road survey 5 is the mountain-facing alternative.** It lies about 154 m southwest of the owner’s Vegas alternative. It clears Mack’s by 4.26 m, Angel Mountain by 4.12 m and the supplied Escarpment trail point by 4.00 m. Its valley score is 0/36. With the Lee offset and Mack’s in place, adding a scout radio here while retaining both deployed Angels brings modeled highway reach to **36.5%**. Repositioning R011 here while holding R005 gives **36.2%**. This is a separate trial subject to access confirmation. None of the 908 road-shoulder probes produced a clear Shady ray in the local screen. The USGS quad identifies Angel Peak Road, and Clark County operates a facility there. The sources establish geographic context and do not establish public access to an individual shoulder. [USGS Angel Peak quadrangle](https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/USTopo/PDF/NV/NV_Angel_Peak_20210917_TM_geo.pdf), [Clark County facility](https://www.clarkcountynv.gov/government/departments/juvenile_justice_services/services/spring-mountain-youth-camp)

## Other points from the KML

| Area | Field choice | Contribution |
| --- | --- | --- |
| Lee Alternative, 20 m circle | Start at the owner’s center. Compare survey 2, 5 m east and 5 m south. | The center clears Upper Bristlecone by 4.14 m. The offset clears it by 4.03 m and slightly improves member road reach. Both are blocked directly to Lee Fire, Mack’s and Angel Mountain. |
| Escarpment trail | Survey 3 is about 21 m from the supplied waypoint, beside the mapped footway. | Clears Shady by 3.99 m, Kyle Junction by 3.88 m and both deployed Angels. At the exact owner pin the Angel Mountain path is blocked by 8.5 m. Good local reception comparison. |
| Showgirl, 100 m circle | Test the legacy pin first. | It clears Angel Mountain by 3.90 m. Its deployed Angel Vegas leg has +1.06 m terrain clearance with only 13% Fresnel clearance. No position in the screened circle cleared the direct Shady ray. |
| Fletcher | Keep legacy, intermediate and summit as comparison points for one assembly. | Each adds zero modeled Lee-reachable highway on the revised backbone. The summit clears the Cathedral Rock ray by just 0.4 m. |
| Kyle Junction, Cathedral Rock and Shady | Retain the deployed Kyle and Cathedral positions as controls. Use G002 to compare Shady receptions. | None adds a member first hop to Lee within three repeats on the reachable plan. A tracker first heard at Escarpment, then forwarded via Angel Mountain, Mack’s and Upper, would need four forwarders. |

The Escarpment placemark is about 1 m from a 4.67 km mapped footway. We used that line to interpret the point-only instruction and included it in the revised KML so the owner can check the intended trail. The Forest Service also identifies Escarpment among its designated trails at the Spring Mountains Visitor Gateway. [Forest Service project listing](https://www.fs.usda.gov/sopa/components/reports/sopa-110417-2025-04.pdf), [mapped footway](https://www.openstreetmap.org/way/572462412)

## Member GPS reach to the Lee Fire uplink

| Layout | Highway reach | SR 156 | SR 157 | SR 158 | Highway with 60% backbone clearance |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deployed | 11.3% | 32.5% | 0.0% | 8.4% | 11.3% |
| Add Mack’s, keep every deployed radio | 31.0% | 76.1% | 2.4% | 29.4% | 23.7% |
| Mack’s + Lee offset, keep R005 | 33.0% | 83.9% | 2.4% | 29.4% | 25.7% |
| Mack’s + exact Lee center + owner’s Vegas alternative | 33.0% | 83.2% | 2.4% | 30.0% | 29.4% |
| Mack’s + Lee offset + owner’s Vegas alternative | **33.2%** | **83.9%** | **2.4%** | **30.0%** | **29.6%** |

In the 33.2% layout use one additional assembly at Mack’s, move R006 to the Lee offset and trial R005 at the supplied Vegas alternative. Keep R010, R001, R011 and R008 at their supplied locations. Five of seven relay positions can serve as a member’s first hop to Lee. This layout reaches **13.14 km** of highway versus 4.49 km deployed. The longest contiguous gap on a mapped part is 6.94 km on SR 157, followed by 6.51 km on SR 158. The resort approach reaches 88.7%, the mapped resort parking lot 31.8% and the outdoor lodge/base probes 28.6%. Trailhead and other parking scores are 26.7% and 29.4%. The hypothetical addition of Kyle Fire Wi-Fi raises the highway result to 50.4%. Kyle Fire has no confirmed uplink in this study.

## Inputs and reproduction

The 19-page atlas draws contours, roads, trails and waypoint labels as PDF vectors. The Angel Peak and Escarpment pages each have a 4,212 × 2,988 PNG in the packet. Angel Peak uses 1 m USGS elevation samples with a 10 m contour interval. Escarpment includes the complete mapped footway and a 2 m contour inset around the two survey pins. The offline viewer carries a 6 m regional relief layer and 47 local 1 m tiles with vector contours and mapped ways. The colored member viewsheds retain their modeled 35 m cells. [USGS northern tile](https://www.sciencebase.gov/catalog/item/69685cb7d4be021259f1fbe8), [USGS southern tile](https://www.sciencebase.gov/catalog/item/69685cb7d4be021259f1fbea), [OpenStreetMap attribution](https://www.openstreetmap.org/copyright)

All 17 owner placemarks supplied the exact horizontal position. Antenna height comes from the study assumptions and ground elevation from USGS terrain. The KML’s altitude field is unused. The additional candidate searches screened 31 eligible offsets at Lee on a 5 m lattice, 272 at Showgirl on a 10 m lattice, 349 beside the mapped Escarpment footway and 908 at Angel. Escarpment offsets are 10 m either side of the trail at 25 m stations. Angel offsets are 10 or 20 m from mapped ways at 20 m stations within 500 m of one of the three owner Angel points. The physical screen removes steep ground and mapped road, building, parking and landing surfaces. Placement on a suitable tree, conditions and access remain on-site observations.

The search retained 15 derived locations and computed all 496 mountain profiles among the resulting 32 points. It compared 36,480 physical layouts of up to ten repeaters, preserving the earlier ceiling of six deployed and four additional assemblies. Ranking uses 70% strict and 30% terrain-clear service, with highway length and the earlier five facility objectives and weights. Ties prefer retaining deployed positions and fewer total radios. The main plan excludes the map-only Angel scouts. The 36.5% scout trial is reported separately. Results are finite-search comparisons.

The same member targets, 910.625 MHz radio model, 4/3 effective Earth radius, 1.2 m member, 4 m repeaters and 1 m stations support comparison with the unrestricted study. Member visibility uses the 5 m mosaic. Direct mountain profiles use native 1 m sampling with mosaic fallback. The viewer plots 35 m nominal member viewsheds and can vary both direct-link antenna heights. Valley rays use the earlier 20 m regional terrain and four nine-probe sectors. Trees, buildings, snow, polarization, interference and transmitter/receiver budgets remain uncalibrated. [USGS 3DEP](https://www.usgs.gov/3d-elevation-program-standards-and-specifications), [USGS Topo](https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer), [OpenStreetMap attribution](https://www.openstreetmap.org/copyright)

From the checkout containing the GIS cache, set `MOUNTAIN_STUDY_OUTPUT` to `private/mountain-siting-reachable-20261117` and save the supplied KML there as `owner-waypoints.kml`. Run `reachable_search.py`, `reachable_layouts.py`, `reachable_atlas.py`, `profiles.py`, `reachable_packet.py` and `verify.py` in order. Run `reachable_packet.py --zip` to include the portable brief and check the archive against the local originals. The offline packet includes the atlas, HTML viewer, KML, GPX, layout results, gap/height/overlap/valley tables, screened locations and GIS viewsheds. The original labeled-topo packet stays in its dated folder. [Study tools](../../scripts/mountain-siting/), [GIS dependencies and data](../../scripts/winter-siting/README.md)
