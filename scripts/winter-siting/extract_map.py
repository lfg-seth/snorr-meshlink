"""Extract editable WGS84 geometry from a regional OSM PBF."""
import osmium
import json
from shapely.geometry import LineString, box, mapping, Polygon


def extract(pbf, output, bounds):
    boundary = box(*bounds)
    features = []

    def add(geom, oid, tags):
        if geom.is_empty:
            return
        features.append(dict(type='Feature', geometry=mapping(geom),
                             properties=dict(osm_id=oid, **tags)))

    keys = 'name alt_name official_name ref highway amenity tourism leisure aerialway landuse piste:type aeroway service access surface building operator parking barrier'.split()

    class Reader(osmium.SimpleHandler):
        def way(self, w):
            tags = {k: w.tags[k] for k in keys if k in w.tags}
            if not tags or not any(k in tags for k in keys[4:]):
                return
            if not w.nodes or not w.nodes[0].location.valid():
                return
            start = w.nodes[0].location
            if not (bounds[0] - .12 < start.lon < bounds[2] + .12 and bounds[1] - .12 < start.lat < bounds[3] + .12):
                return
            coords = [(n.lon, n.lat) for n in w.nodes]
            if len(coords) < 2:
                return
            shape = LineString(coords)
            if not shape.intersects(boundary):
                return
            if w.is_closed() and len(coords) >= 4 and ('building' in tags or tags.get('amenity') == 'parking' or
                    tags.get('tourism') == 'camp_site' or tags.get('aeroway') == 'helipad'):
                shape = Polygon(coords)
                if not shape.is_valid:
                    shape = shape.buffer(0)
            add(shape.intersection(boundary), 'w'+str(w.id), tags)

        def node(self, n):
            if not (bounds[0] <= n.location.lon <= bounds[2] and bounds[1] <= n.location.lat <= bounds[3]):
                return
            tags = {k: n.tags[k] for k in keys if k in n.tags}
            if tags and ('name' in tags or 'amenity' in tags or 'aeroway' in tags):
                from shapely.geometry import Point
                add(Point(n.location.lon,n.location.lat), 'n'+str(n.id), tags)

    Reader().apply_file(str(pbf), locations=True)
    output.write_text(json.dumps(dict(type='FeatureCollection', features=features)), encoding='utf-8')
