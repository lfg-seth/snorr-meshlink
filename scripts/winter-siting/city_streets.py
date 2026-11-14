"""Read the street network around the valley trial directly from the pinned Nevada PBF."""
import json
from shapely.geometry import LineString, box, mapping
from geography import parts


def streets(root, bounds):
    import osmium
    cache = root / 'cache/valley-streets.json'
    pbf = root / 'source/nevada.osm.pbf'
    manifest = json.loads((root / 'inputs/sources.json').read_bytes())
    digest = next(f['sha256'] for f in manifest['files'] if f['file'] == pbf.name)
    signature = [digest, list(bounds), 1]
    if cache.is_file():
        saved = json.loads(cache.read_bytes())
        if saved['signature'] == signature:
            return saved['roads']
    bounds_polygon = box(*bounds)
    roads = []
    classes = {'motorway','trunk','primary','secondary','tertiary','residential','unclassified'}
    class Reader(osmium.SimpleHandler):
        def way(self,w):
            kind = w.tags.get('highway')
            if kind not in classes or len(w.nodes)<2:
                return
            geom = LineString([(n.lon,n.lat) for n in w.nodes])
            if not geom.intersects(bounds_polygon):
                return
            for piece in parts(geom.intersection(bounds_polygon),'LineString'):
                roads.append([kind,w.tags.get('ref',''),w.tags.get('name',''),mapping(piece)['coordinates']])
    Reader().apply_file(str(pbf),locations=True)
    if not any(kind=='motorway' for kind,_,_,_ in roads):
        raise ValueError('The valley street extract contains no freeway')
    cache.write_text(json.dumps({'signature':signature,'roads':roads},separators=(',',':')),encoding='utf-8')
    return roads
