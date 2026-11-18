"""Rebuild the mountain study from the owner's accessible KML and bounded local searches."""
import re
import xml.etree.ElementTree as ET
from html import unescape
from itertools import product

from model import (DATA, OUT, boundary, csv, eligible, elevation, features, forward, grid, groups,
                   inverse, json, load_dem, math, meta, names, np, offset, part, points, profile,
                   radius, ray, read, road_samples, sight, target3, targets, wave, weights)
from shapely.geometry import Point

LEE = "Lee Alternative"
MACK = "Mack's alternative"
VEGAS = "Angel Vegas alternative"
ESC = "Escarpment trail"
SHOW = "Showgirl"
ANGEL = "Angel road"
ALIASES = {s.casefold():s for s in (LEE, MACK, VEGAS, ESC, SHOW)}
ORIGINAL = ["Lee Fire","Upper Bristlecone","Cathedral Rock","Angel Vegas","Angel Mountain",
            "Kyle Junction","Lee Junction","Shady Hollow","Legacy Fletcher","Fletcher intermediate",
            "Fletcher Peak","Kyle Fire"]


def load_waypoints(path):
    records = {}
    for node in ET.parse(path).findall(".//{*}Placemark"):
        source_name = node.findtext("{*}name").strip()
        clean = source_name.replace("’", "'")
        name = ALIASES.get(clean.casefold(), clean)
        coordinates = node.findtext("{*}Point/{*}coordinates")
        if coordinates is None or name in records:
            raise ValueError(f"Expected a unique Point for {source_name}")
        lon, lat = map(float, coordinates.strip().split(",")[:2])
        projected = forward.transform(lon, lat)
        if not boundary.covers(Point(projected)):
            raise ValueError(f"Outside the study area: {name}")
        description = unescape(re.sub(r"<[^>]*>", "", node.findtext("{*}description", "")))
        records[name] = (projected, description)
    missing = set(ORIGINAL + [LEE, MACK, VEGAS, ESC, SHOW]) - records.keys()
    if missing:
        raise ValueError(f"Missing study controls: {sorted(missing)}")
    return records


def disk(center, distance, step):
    return [(center[0]+x, center[1]+y) for x,y in product(range(-distance,distance+1,step),repeat=2)
            if 0 < math.hypot(x,y) <= distance and eligible(center[0]+x, center[1]+y)]


def shoulders(line, spacing, offsets):
    for station in np.arange(0,line.length,spacing):
        center = np.array(line.interpolate(station).coords[0])
        tangent = np.subtract(line.interpolate(min(line.length,station+1)).coords[0],
                              line.interpolate(max(0,station-1)).coords[0])
        normal = np.array([-tangent[1],tangent[0]]) / np.linalg.norm(tangent)
        for lateral in offsets:
            candidate = tuple(center + normal*lateral)
            if eligible(*candidate):
                yield candidate


def valley_probes():
    regional, transform = load_dem(DATA/"cache/terrain-regional.tif")
    names, receivers = [], []
    for sector,lon,lat in read(DATA/"inputs/study.json")["valley_sectors"]:
        x,y = forward.transform(lon,lat)
        names.append(sector)
        receivers.extend((x+dx,y+dy) for dx,dy in product((-500,0,500),repeat=2))
    return regional, transform, names, points(regional, transform, receivers, 4)


def build():
    records = load_waypoints(OUT/"owner-waypoints.kml")
    xy = {k:v[0] for k,v in records.items()}
    descriptions = {k:v[1] for k,v in records.items()}
    trail = min((g for g,p in features if p.get("highway") in ("path","footway") and g.geom_type=="LineString"),
                key=Point(xy[ESC]).distance)
    if trail.distance(Point(xy[ESC])) > 20:
        raise ValueError("Escarpment pin is not on a mapped trail")
    angel_pins = [xy[k] for k in ("Angel Vegas","Angel Mountain",VEGAS)]
    lines = [g for g,p in features if g.geom_type=="LineString" and p.get("highway")
             and any(g.distance(Point(pin))<=500 for pin in angel_pins)]
    search = {LEE:disk(xy[LEE],20,5), SHOW:disk(xy[SHOW],100,10),
              ESC:list(shoulders(trail,25,(-10,10))),
              ANGEL:[pos for line in lines for pos in shoulders(line,20,(-20,-10,10,20))
                     if min(math.dist(pos,pin) for pin in angel_pins)<=500]}
    fixed = list(xy)
    regional, trans, sectors, receivers = valley_probes()
    road_probes = points(grid,meta,road_samples[::8],1.2)

    def city(pos):
        # Match the winter-sector geometry, with mountain terrain at the transmitter.
        origin = points(grid,meta,[pos],4)[0]
        return [int(ray(regional,trans,origin,end,20,wave,radius)[0]>=0) for end in receivers]

    valley = {}
    families = {}
    counts = {}
    rows = []
    for group,locations in search.items():
        locations = list(dict.fromkeys(locations))
        counts[group] = len(locations)
        leaders = []
        for pos in locations:
            origin = points(grid,meta,[pos],4)[0]
            def margin(k):
                end = points(grid,meta,[xy[k]],1 if k.endswith("Fire") else 4)[0]
                return ray(grid,meta,origin,end,5,wave,radius)[1]
            fs = {k:margin(k) for k in fixed if math.dist(pos,xy[k])>1}
            lee = max(fs["Lee Fire"],fs["Upper Bristlecone"])
            bridge = min(lee, max(fs["Angel Mountain"],fs[MACK],fs[VEGAS]))
            direct = sum(v>=0 for v in fs.values())
            visible = int(sight(grid,meta,origin,road_probes,10,wave,radius).sum())
            city_hits = sum(city(pos)) if group==ANGEL else 0
            if group==ANGEL:
                weak = min(fs["Shady Hollow"],fs[MACK])
                ranks = [(weak>=0,city_hits,weak), (fs["Shady Hollow"]>=0,city_hits,fs[MACK]),
                         (fs[MACK]>=0,city_hits,fs["Shady Hollow"]), (city_hits,weak),
                         (fs["Shady Hollow"],city_hits),
                         (min(fs[MACK],fs[ESC])>=.6,city_hits,min(fs[MACK],fs[ESC])),
                         (min(fs[MACK],fs["Legacy Fletcher"])>=.6,city_hits,min(fs[MACK],fs["Legacy Fletcher"]))]
            else:
                ranks = [(bridge,visible), (lee,visible), (direct,visible), (visible,direct),
                         (max(fs["Legacy Fletcher"],fs["Fletcher Peak"]),visible)]
            for i,rank in enumerate(ranks):
                if len(leaders)==i:
                    leaders.append((rank,pos))
                elif rank>leaders[i][0]:
                    leaders[i]=(rank,pos)
            lon,lat = inverse.transform(*pos)
            rows.append([group,lat,lon,visible,city_hits if group==ANGEL else "",*map(fs.get,fixed)])
        families[group]=[]
        for _,pos in leaders:
            if any(math.dist(pos,other)<1 for other in xy.values()):
                continue
            name=f"{group} survey {len(families[group])+1}"
            families[group].append(name)
            xy[name]=pos
            descriptions[name] = {LEE:"5 m search grid inside the owner's 20 m circle.",
                                  SHOW:"10 m search grid inside the owner's 100 m circle.",
                                  ESC:"10 m beside the mapped footway passing the owner's Escarpment pin.",
                                  ANGEL:"Map-derived road shoulder near Angel pins. Confirm access before visiting."}[group]
        print(group,counts[group],families[group],flush=True)
    for k in ["Angel Vegas","Angel Mountain",VEGAS,*families[ANGEL]]:
        valley[k]=np.array(city(xy[k])).reshape(-1,9).sum(axis=1).tolist()
    with (OUT/"search-screen.csv").open("w",newline="",encoding="utf-8-sig") as f:
        writer=csv.writer(f)
        writer.writerow(["region","latitude","longitude","sampled road hits","valley hits",*fixed])
        writer.writerows(rows)
    ids=list(xy)
    masks=[sight(grid,meta,points(grid,meta,[xy[k]],1 if k.endswith("Fire") else 4)[0],target3,5,wave,radius) for k in ids]
    links={}
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            clear,f1,_=profile.stats((*xy[a],1 if a.endswith("Fire") else 4),
                                     (*xy[b],1 if b.endswith("Fire") else 4))
            if not np.isfinite(clear+f1):
                raise ValueError((a,b))
            links[a+"|"+b]=[clear,f1]
    payload=dict(xy=xy,links=links,display=ids,descriptions=descriptions,source_pins=fixed,
                 families=families,counts=counts,sectors=sectors,valley=valley,
                 trail_length=trail.length,trail_id=next(p["osm_id"] for g,p in features if g is trail),
                 start=[MACK,"Upper Bristlecone"],primary="Reachable plan")
    (OUT/"search.json").write_text(json.dumps(payload,indent=2))
    np.savez_compressed(OUT/"targets.npz",masks=masks,ids=ids,targets=targets,groups=groups,
                        names=names,weights=weights,part=part,offset=offset)


if __name__=="__main__":
    if not (OUT/"owner-waypoints.kml").is_file():
        raise SystemExit("Set MOUNTAIN_STUDY_OUTPUT to the revision folder containing owner-waypoints.kml")
    build()
