# Mount Charleston node and valley study, 18 November 2026

Angel road survey 5 has the greatest modeled highway reach of the four one-scout layouts. It covers 12.78 km of the 39.61 km of sampled highway, compared with 4.49 km for the documented deployment. Survey 3 has the largest regional fixed-radio footprint of the four scouts. Deployed Angel Vegas remains on air in all four cases. Test Mack’s at the intended 4 m mount against Upper Bristlecone, then match an ordinary member GPS packet at Lee Fire.

| Single scout in the proposed network | Mountain terrain with route to Lee | Highway km | Highway share | Same-pin Shady forwarding trial | Regional terrain visible from the scout to a 4 m receiver |
| --- | ---: | ---: | ---: | ---: | ---: |
| Angel road survey 1 | 19.50 km² | 8.63 | 21.8% | 21.8% | 1,286 km² |
| Angel road survey 3 | 47.76 km² | 10.51 | 26.5% | 26.5% | 1,485 km² |
| Angel road survey 5 | 66.39 km² | 12.78 | 32.3% | 32.3% | 758 km² |
| Angel road survey 6 | 48.51 km² | 10.95 | 27.6% | 27.6% | 844 km² |

The regional footprint for deployed Angel Vegas is 1,498 km². These areas span the entire map rectangle, including mountain terrain. The receiver is fixed outdoors at 4 m. The mountain member viewsheds use a 1.2 m receiver. Scout locations are map-derived shoulders and their access and mount positions need a field check.

## Radios and evidence

The common shortlist comprises Upper Bristlecone, Mack’s alternative, Showgirl, the supplied Escarpment trail pin, Cathedral Rock, deployed Angel Vegas and Kyle Junction. Each case adds one of the four Angel road scouts. G001 at Lee Fire is the uplink. The baseline uses the six documented deployed repeater positions, including Angel Mountain and Lee Junction. These two positions appear only in the historical baseline. Shady Hollow’s installed G002 records offline.

The four separate Shady trials add a forwarding radio at that site and admit directly recorded paths alongside modeled clear paths. Shady’s card recorded direct packets from Cathedral, Angel Vegas and Kyle Junction; those sites also reported hearing G002. Among the shortlisted sites these are the three recorded exceptions to predicted terrain blockage. All four trials return the same three-forwarder highway coverage as their respective recorder-only cases. The shortest Shady-to-Lee path in the survey 5 trial has five radio links: Shady, Escarpment, survey 5, Mack’s, Upper Bristlecone and Lee Fire. Shady’s forwarding and end-to-end delivery still require measurements. [Prior SD findings](mountain-siting-20261117.md#preferred-full-layout), [deployment field record](../../records/aar/2026-11-15-mount-charleston.md)

Of the 78 physical pairs among 13 sites, 15 clear 60% of the first Fresnel zone, two clear the terrain with less Fresnel clearance, and 61 intersect the terrain. Showing both directions gives 156 profiles. Every chapter takes its site as A and includes the field evidence, minimum terrain clearance and distance to that point from A. Each profile links to its reverse page. Close-in maps recalculate member visibility on 2.5 m or 5 m cells over the 5 m member terrain model. The broader mountain maps and shared area totals use the common 35 m grid. [Earlier study and terrain methods](mountain-siting-reachable-20261117.md#inputs-and-reproduction)

## Field report and offline packet

The private edition is in `private/mountain-node-study-20261118/`. The standalone PDF and ZIP contain the same 196-page report.

| Pages | Contents |
| --- | --- |
| 1–5 | Dated cover, full-page site map, full-page link map with close Angel positions enlarged, clickable contents, coordinates and purposes |
| 6–9 | Executive summary, deployed and shortlisted network viewsheds, Shady trial, four-scout comparison |
| 10–14 | Matched Mount Charleston–Las Vegas–Henderson viewsheds for deployed Angel Vegas and scouts 1, 3, 5 and 6 |
| 15–196 | Thirteen chapters, each with a site brief and neighbor index, one mountain viewshed and twelve direct profiles |

The ZIP includes the adjustable offline viewer for all 78 physical paths, the 13-node KML/GPX, 13 mountain viewshed GeoTIFFs and five regional GeoTIFFs. The dated report uses only the selected roster and omits the earlier Vegas alternative. The prior study retains its historical inputs and products.

## Reproduction

Run the study tools from the checkout that holds the November terrain package and the prior reachable-waypoint outputs. Set `MOUNTAIN_STUDY_OUTPUT=private/mountain-siting-reachable-20261117`. The generators use the study’s existing GIS Python packages plus ReportLab and PyMuPDF. The report embeds the Segoe UI and Georgia fonts available on the Windows study machine.

1. Run `node_valley.py --fetch` to acquire the three additional dated USGS 1/3 arc-second elevation tiles. The private cache records URLs, byte counts and SHA-256 digests. The scripts reuse the earlier pinned local fourth tile and Nevada OSM extract.
2. Run `node_valley.py` to build the full rectangular 20 m terrain mosaic and five regional viewsheds. The 120 m map cells represent independently surveyed model rays sampled at 20 m along each path. Each source and receiver is 4 m above its modeled local ground. The inputs span the whole valley through Henderson.
3. Run `node_report.py --packet` to build the front matter, node chapters, indexed report and scoped offline packet. Each mountain profile uses native 1 m terrain with mosaic fallback, 910.625 MHz and a 4/3 effective Earth radius.
4. Run `verify_node_report.py` to check directory and reverse links, each profile against its recorded terrain clearance, the printed mountain and regional masks against the GeoTIFFs, regional line-of-sight samples, routing cases, waypoint exports, viewer roster and the archived PDF.

[Study tools](../../scripts/mountain-siting/), [USGS 3DEP elevation](https://www.usgs.gov/3d-elevation-program), [OpenStreetMap attribution](https://www.openstreetmap.org/copyright)
