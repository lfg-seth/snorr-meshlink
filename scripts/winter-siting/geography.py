import json
from collections import defaultdict
from math import ceil
import numpy as np
from shapely.geometry import shape, mapping, box, Point, LineString
from shapely.ops import transform, substring, unary_union, linemerge
from shapely.strtree import STRtree
from terrain import forward, inverse


def parts(geometry, kind):
    if geometry.geom_type == kind:
        yield geometry
    elif hasattr(geometry, 'geoms'):
        for item in geometry.geoms:
            yield from parts(item,kind)


def save_features(path, pairs):
    features = [dict(type='Feature', geometry=mapping(transform(inverse.transform,g)), properties=p)
                for g,p in pairs]
    path.write_text(json.dumps(dict(type='FeatureCollection',features=features)),encoding='utf8')


def geography(root, cfg):
    bounds = transform(forward.transform,box(*cfg['boundary_wsen']))
    raw=json.loads((root/'source/local-osm.geojson').read_bytes())['features']
    rows=[(transform(forward.transform,shape(f['geometry'])),f['properties']) for f in raw]
    roads=defaultdict(list)
    trails=defaultdict(list)
    facilities=[]
    excluded=[]
    driving=[]
    parking=[]
    for g,p in rows:
        name=p.get('name','')
        hw=p.get('highway','')
        if name=='Upper Bristlecone Trail' and hw=='path':
            excluded.append(g.buffer(30.48))
        if p.get('building') or p.get('aeroway')=='helipad':
            excluded.append(g.buffer(8 if p.get('building') else 35))
        if p.get('amenity')=='parking':
            excluded.append(g.buffer(2))
            if g.geom_type=='Polygon' and (p.get('parking')!='shoulder' or name=='North Loop Trailhead') and p.get('access') not in ('private','no','customers'):
                parking.append((g.representative_point(),p))
        if hw and hw not in ('path','footway','steps','trailhead','cycleway','bridleway','crossing','bus_stop','pedestrian') and g.geom_type.endswith('LineString'):
            driving.append(g)
            excluded.append(g.buffer(5 if hw in ('secondary','tertiary') else 2.8))
        if not g.intersects(bounds):
            continue
        clipped=g.intersection(bounds)
        route=cfg['route_names'].get(p.get('ref','')) or cfg['route_names'].get(name)
        if route and hw:
            roads[route].extend(parts(clipped,'LineString'))
        elif hw in ('path','footway','bridleway','cycleway') and name:
            trails[name].extend(parts(clipped,'LineString'))
        if p.get('tourism')=='camp_site' and name and g.geom_type=='Polygon':
            facilities.append((g,name))
        if p.get('piste:type') in ('downhill','nordic') and g.geom_type=='LineString':
            facilities.append((clipped,'Lee ski terrain'))
    if not all(k in roads for k in cfg['route_names'].values()):
        raise ValueError('A requested road is missing')
    routes=[]
    for cls,groups in [('road',roads),('trail',trails)]:
        for name,lines in groups.items():
            union=unary_union(lines)
            merged=linemerge(union) if union.geom_type=='MultiLineString' else union
            for j,line in enumerate(parts(merged,'LineString')):
                if line.length>1:
                    routes.append((line,dict(kind=cls,name=name,part=j)))
    sample=[]
    def add(x,y,kind,name,weight,seg=None):
        sample.append(dict(x=x,y=y,kind=kind,name=name,w=float(weight),segment=seg))
    for line,p in routes:
        n=ceil(line.length/cfg['route_step_m'])
        for i in range(n):
            seg=substring(line,line.length*i/n,line.length*(i+1)/n)
            pt=seg.interpolate(.5,normalized=True)
            add(pt.x,pt.y,p['kind'],p['name'],seg.length,seg)
    for site,name in facilities:
        if site.geom_type=='Polygon':
            left,bottom,right,top=site.bounds
            raster=[Point(x,y) for x in np.arange(left+15,right,30) for y in np.arange(bottom+15,top,30) if site.contains(Point(x,y))]
            for pt in raster or [site.representative_point()]:
                add(pt.x,pt.y,'facility',name,1)
        else:
            n=max(1,ceil(site.length/40))
            for i in range(n):
                pt=site.interpolate((i+.5)/n,normalized=True)
                add(pt.x,pt.y,'facility',name,site.length/n)
    return bounds,routes,sample,STRtree(excluded),unary_union(driving),parking,facilities
