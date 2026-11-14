# Winter mesh siting study

The November 2026 planning run compared two station gateways, the owner's seven starting repeater placements and nine-radio alternatives for passive GPS tracking. Coordinate-bearing inputs, navigation, terrain, maps, site sheets and results are kept together under ignored `private/winter-siting/`. Use the [local workflow](../../scripts/winter-siting/README.md) with that private data package.

The current nine-radio layout reaches 41.26 of 52.43 km of scored road, 92.16 of 155.60 km of named trail and 110.59 of 265.40 km² of land in the terrain model. The Angel Peak road objective follows SR 158 to both owner-confirmed drive-up sites. It covers 98.38% of that approach. Upper Macks Canyon has a 3.39 km blind stretch. Earlier figures used a longer road corridor and a different siting objective.

The comparison uses a 5 m projected terrain grid for member visibility, native 1 m terrain sampling for backbone profiles and a three-forwarder limit. The owner confirms agency access and placement authority across the mountain. Physical mount selection, winter footing, body and vehicle attenuation, vegetation, packet delivery and power endurance require field observations.

The Upper Bristlecone helipad is the first recommended relay. Thirty-two cells in its 20 m circle pass the physical screen. The route connects Lee Junction to Lee Fire Station through the helipad. Angel Peak Mountain Side is selected for tracking. Angel Peak Vegas Side is the optional valley test location. Its clearest sampled sector is western North Las Vegas (9/9 terrain rays), followed by Centennial Hills (6/9). No home receiver has been selected or measured.

## Field atlas

The packet opens with the proposed deployment, then a single north-up road map with both stations, highway limits, the two Angel Peak destinations and the Upper Macks test stretch. The valley map uses actual OpenStreetMap streets and highways. Route and facility scores remain available in the private model output. Redundancy is deferred at the owner’s request.

The cartographic design uses consistent panel scales for comparisons and distinct palettes for site identity and route status. [UK Government Analysis Function chart guidance](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/), [ColorBrewer scheme guidance](https://colorbrewer2.org/learnmore/schemes.html).

## Sources

- High-resolution 3DEP terrain provides bare-earth orthometric elevations in metres. The dataset catalog and downloaded tile headers establish the source projection. [USGS 1 metre DEM](https://data.usgs.gov/datacatalog/data/USGS%3A77ae0551-c61e-4979-aedd-d797abdcde0e), [USGS DEM references](https://www.usgs.gov/faqs/what-projection-horizontal-datum-vertical-datum-and-resolution-a-usgs-digital-elevation-model).
- Scored geometry comes from the 12 November OSM snapshot, checked against state highway and recreation sources. [Geofabrik Nevada](https://download.geofabrik.de/north-america/us/nevada.html), [NDOT highway index](https://www.dot.nv.gov/home/showpublisheddocument/23124/638718361041470000), [Recreation.gov campground loops](https://www.recreation.gov/camping/campgrounds/232168).
- Winter restrictions, storm orders and operating hours govern access. The weekly recreation list and standing conditions page disagree on one upper-canyon trail. Consult the order exhibit and confirm the approach before a field visit. [NDOT winter restrictions](https://www.dot.nv.gov/safety/safe-winter-driving/mt-charleston-winter-safety), [USFS Order 04-17-25-04](https://www.fs.usda.gov/r04/humboldt-toiyabe/alerts/area-road-and-trail-closures-spring-mountains-national-recreation-area), [weekly update](https://www.gomtcharleston.com/spring-mountains-weekly-update/), [conditions](https://www.gomtcharleston.com/current-condition-closures/).
- Panel recommendations combine a local terrain horizon with regional monthly direct and diffuse solar climatology and a representative-day sun track. Case face angles, branch shade and power balance remain field measurements. [NASA POWER climatology](https://power.larc.nasa.gov/docs/services/api/temporal/climatology/), [NOAA solar equations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF).
- Hop accounting gives one repeat per forwarding radio. Each station acts as an RF sink and an uplink. [Meshtastic managed flooding](https://meshtastic.org/docs/overview/mesh-algo/), [project receive profile](../operations/airtime-sniffer.md).
