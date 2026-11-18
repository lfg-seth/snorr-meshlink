# Mount Charleston repeater study · Favorite-router edition

The nine proposed sites together have direct terrain visibility to **95.77 km²** inside the mountain boundary and **24.88 of 39.61 km** of sampled highway (62.8%). Every site has a route to G001 at Lee Fire using the assumed favorite-router settings. The eight terrain-clear pairs alone connect all nine sites. Two historical receptions at Shady are additional paths to retest with the replacement hardware. These are planning estimates for member GPS. End-to-end receipt remains a field check.

## Sites and forwarding

The modeled routers are Upper Bristlecone, Mack’s alternative, a RAK at Shady Hollow, Escarpment trail, Cathedral Rock, Angel road survey 5 and deployed Angel Vegas. G002 moves to Kyle Fire as a forwarding CLIENT with local SD recording. Kyle Fire and Lee Fire use the earlier station antenna assumption of 1 m. Router antennas are 4 m and a member antenna is 1.2 m. Kyle Junction and Showgirl are outside this edition. Angel road survey 5 operates alongside Angel Vegas. [Site record](../../records/sites.md)

A member starts with a three-hop budget. The first relay charges one hop. A subsequent router receiving from a favorite router preserves the remaining budget when it forwards. A forwarding CLIENT consumes a hop and the router forwarding immediately after that CLIENT consumes another. Relays need a positive remaining budget to transmit. A gateway receiving a packet is its destination. This scenario assumes reciprocal favorite entries for eligible router neighbors and an enabled rebroadcast setting at G002. The field trial should verify the settings and a fresh member receipt. [Firmware hop rule](https://github.com/lfg-seth/firmware/blob/5bd492399f5f3d4a65c01256f907f7b907b80921/src/mesh/Router.cpp#L85)

For a tracker first heard by G002, the modeled route runs from Kyle Fire through Cathedral Rock, Escarpment, survey 5, Mack’s and Upper Bristlecone to Lee Fire. It consumes two budgeted hops across six radio legs after first reception. A tracker first heard by the Shady RAK can use five radio legs via Escarpment, survey 5, Mack’s and Upper for one budgeted hop. Shady’s recorded links to Cathedral and Angel Vegas were measured with G002 at its former location. [Historical SD and reciprocal neighbor evidence](mountain-siting-20261117.md#preferred-full-layout)

## Package and page guide

The new private files are under `private/mountain-node-study-20261118-favorites/`. The previous 79-page PDF and field ZIP retain their original SHA-256 digests and paths. [Previous edition](mountain-node-study-20261118.md)

| Pages | Contents |
| --- | --- |
| 1 | Whole-area aerial cover with all nine active study pins |
| 2–4 | Labeled network, combined mountain viewshed in the same frame, potential direct links |
| 5–6 | Clickable contents, site directory and favorite-router assumptions |
| 7–8 | Matched fixed outdoor 4 m viewsheds for Angel Vegas and road survey 5 through Las Vegas and Henderson |
| 9–46 | Nine site briefs, annotated single-site viewsheds, and both directions of the ten retained paths |

The ZIP contains the PDF, offline path viewer, GPX/KML, nine site viewshed GeoTIFFs, the combined mountain viewshed GeoTIFF and two valley viewshed GeoTIFFs. The combined raster uses 35 m cells. Values are 1 for visible, 0 for terrain shadow and 255 outside the study boundary. Its Angel inset independently samples all nine sites on a 2.5 m grid over the 5 m terrain model. Mountain area totals use the common 35 m grid. Highway totals use the distance-weighted road samples. [Terrain methods and source inputs](mountain-siting-reachable-20261117.md#inputs-and-reproduction)

## Reproduction and verification

Run the edition’s `scripts/mountain-siting/node_report.py --packet` and then `scripts/mountain-siting/verify_node_report.py` from the repository holding the private November data. Set `MOUNTAIN_STUDY_OUTPUT=private/mountain-siting-reachable-20261117` and include the study GIS packages and PyMuPDF on the Python path. The report reuses the previous valley DEM, imagery and rasters as read-only inputs. On first build it caches a public USGS NAIP aerial of the full area for the cover, then projects the photo, road lines and site pins through the same elevation transform. The cached JPEG SHA-256 is `784adefe28b5ec2378f380a706fbf44f950ad3a729e0731b3000319c53fe0c07`. [USGS NAIP imagery service](https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer)

Verification compares the combined mask with the source rasters, checks traversable routes by remaining hop budget, and checks the profile evidence, site markers, reciprocal navigation, valley rays and archived deliverables. Field acceptance includes confirming the antenna mounts and favorites, testing both recorded Shady paths with the new RAK, and matching an ordinary member GPS fix at Lee Fire.
