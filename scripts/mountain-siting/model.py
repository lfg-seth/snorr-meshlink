"""Fresh Lee-only site search. Run from repo root with the cached November GIS package."""
import csv
import json
import math
import os
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path.cwd()
DATA = ROOT / "private/winter-siting"
OUT = ROOT / "private/mountain-siting-final-20261117"
OUT.mkdir(exist_ok=True)
sys.path[:0] = [str(DATA / "envpkgs"), str(Path(__file__).resolve().parents[1] / "winter-siting")]
os.environ.setdefault("NUMBA_NUM_THREADS", "6")
os.environ.setdefault("MPLCONFIGDIR", str(OUT / "mpl-cache"))
import numpy as np
from numba import njit, prange
from shapely.geometry import Point, box, shape
from shapely.ops import transform, unary_union, linemerge
from shapely.strtree import STRtree
from scipy.spatial import cKDTree
from terrain import elevation, forward, inverse, load_dem, points, ray, sight
from native import Profiles

read = lambda p: json.loads(p.read_bytes().decode("utf-8-sig"))
grid, meta = load_dem(DATA / "cache/terrain-local.tif")
wave, radius = 299.792458 / 910.625, 6371000 * 4/3
profile = Profiles((DATA / "source").glob("USGS_1M*.tif"), grid, meta, wave, radius)
boundary = transform(forward.transform, box(-115.714,36.239,-115.521,36.377))
features = [(transform(forward.transform,shape(f["geometry"])),f["properties"])
            for f in read(DATA / "source/local-osm.geojson")["features"]]
pins = {"Lee Fire":(36.32123,-115.67211),"Upper Bristlecone":(36.30648,-115.67843),
        "Cathedral Rock":(36.25631,-115.64886),"Angel Vegas":(36.31763,-115.57288),
        "Angel Mountain":(36.31879,-115.58049),"Kyle Junction":(36.26489,-115.60370),
        "Lee Junction":(36.34236,-115.65398),"Shady Hollow":(36.27274,-115.58430),
        "Legacy Fletcher":(36.29665,-115.62654),"Kyle Fire":(36.25995,-115.64507)}
xy = {k:forward.transform(lon,lat) for k,(lat,lon) in pins.items()}
xy["Fletcher Peak"] = next(g.coords[0] for g,p in features if p.get("name")=="Fletcher Peak")
roadlines=defaultdict(list)
targets=[]
groups=[]
names=[]
weights=[]
part=[]
offset=[]
def sample(xy0, group, name, weight=1, line=-1, pos=0):
    targets.append(xy0)
    groups.append(group)
    names.append(name)
    weights.append(weight)
    part.append(line)
    offset.append(pos)

def parts(g):
    if g.geom_type=="LineString":
        yield g
    elif hasattr(g,"geoms"):
        for item in g.geoms:
            yield from parts(item)

resort=Point(forward.transform(-115.67969,36.30346))
excluded=[]
for g,p in features:
    if not g.intersects(boundary):
        continue
    name=p.get("name","")
    ref=p.get("ref")
    if ref in ("SR 156","SR 157","SR 158") and p.get("highway"):
        roadlines[ref].extend(parts(g.intersection(boundary)))
    if p.get("building") or p.get("amenity")=="parking" or p.get("aeroway")=="helipad":
        excluded.append(g.buffer(8))
    if p.get("highway"):
        excluded.append(g.buffer(6))
    lot=p.get("amenity")=="parking"
    trailhead="Trailhead" in name or p.get("highway")=="trailhead" or p.get("information")=="trailhead"
    if (lot or trailhead) and g.geom_type in ("Point","Polygon","MultiPolygon"):
        cls="Resort parking" if lot and g.distance(resort)<800 else "Trailheads" if trailhead else "Other parking"
        tag=name or p["osm_id"]
        probes=[g.representative_point()]
        if g.area>500:
            l,b,r,t=g.bounds
            probes=[Point(x,y) for x in np.arange(l+10,r,20) for y in np.arange(b+10,t,20) if g.contains(Point(x,y))] or probes
        for pt in probes:
            sample(pt.coords[0],cls,tag,1/len(probes))
road_inventory=[]
for ref,ls in sorted(roadlines.items()):
    merged=unary_union(ls)
    for line in parts(linemerge(merged) if merged.geom_type=="MultiLineString" else merged):
        idx=len(road_inventory)
        road_inventory.append((line,ref))
        n=math.ceil(line.length/40)
        for i in range(n):
            pos=(i+.5)*line.length/n
            sample(line.interpolate(pos).coords[0],"Highway",ref,line.length/n,idx,pos)
            if ref=="SR 156" and line.interpolate(pos).distance(resort)<1900:
                sample(targets[-1],"Resort approach","Upper SR 156",line.length/n)
def add_base_targets():
    # Outdoor probes by the mapped base buildings and plazas, approximate study boundaries.
    for geom,p in features:
        if p.get("building") and geom.distance(resort)<430 and geom.area>100:
            sample(geom.representative_point().coords[0],"Lodge / base",p.get("name") or p["osm_id"])
    sample(resort.coords[0],"Lodge / base","Mapped resort entrance")
    for label,lat,lon in [("Bristlecone lodge exterior",36.303424,-115.680152),
                          ("Ponderosa base west",36.304747,-115.677468),
                          ("Ponderosa base east",36.304949,-115.675117)]:
        sample(forward.transform(lon,lat),"Lodge / base",label)
add_base_targets()
groups=np.array(groups)
names=np.array(names)
weights=np.array(weights)
part=np.array(part)
offset=np.array(offset)
targets=np.array(targets)
target3=points(grid,meta,targets,1.2)
assert np.isfinite(target3).all()
roads=unary_union([line for line,_ in road_inventory])
blocked=STRtree(excluded)
road_samples=targets[groups=="Highway"]
disttree=cKDTree(road_samples)
divide=Point(forward.transform(-115.666261,36.288922))
def eligible(x,y):
    p=Point(x,y)
    if not boundary.contains(p) or p.distance(divide)<1400 or len(blocked.query(p,predicate="intersects")):
        return False
    zx=elevation(grid,meta,x+10,y)-elevation(grid,meta,x-10,y)
    zy=elevation(grid,meta,x,y+10)-elevation(grid,meta,x,y-10)
    return math.hypot(zx,zy)<12

@njit(parallel=True)
def screen(origins,ends,grid,meta,wave,radius):
    mask=np.empty((len(origins),len(ends)),np.uint8)
    for i in prange(len(origins)):
        for j in range(len(ends)):
            mask[i,j]=ray(grid,meta,origins[i],ends[j],20.,wave,radius,True)[0]>0
    return mask

def shortlist():
    fixed=list(xy)
    anchors=points(grid,meta,[xy[k] for k in fixed],4)
    anchors[0,2]-=3
    roads_every=road_samples[::7]
    test_targets=np.vstack((anchors,points(grid,meta,roads_every,1.2)))
    candidates=[]
    left,bottom,right,top=boundary.bounds
    for x in np.arange(left,right,160):
        for y in np.arange(bottom,top,160):
            if disttree.query((x,y))[0]>3000:
                continue
            options=[(elevation(grid,meta,x+dx,y+dy),x+dx,y+dy) for dx in (-55,0,55) for dy in (-55,0,55) if eligible(x+dx,y+dy)]
            if options:
                candidates.append(max(options)[1:])
    orig=points(grid,meta,candidates,4)
    view=screen(orig,test_targets,grid,meta,wave,radius)
    road=view[:,len(fixed):].sum(axis=1)
    connected=view[:,0].astype(bool)
    angel=view[:,[2,3,4,5,7]].sum(axis=1)
    ridges=np.array(candidates)
    offroad=disttree.query(ridges)[0]
    gradebonus=road-offroad/350
    picked=[]
    def select(score,mask,n,spacing):
        local=[]
        for i in np.argsort(-score,kind="stable"):
            if mask[i] and all(math.dist(ridges[i],ridges[j])>spacing for j in local):
                local.append(i)
                if i not in picked:
                    picked.append(i)
                if len(local)>=n:
                    break
    for connected_mask in (connected,view[:,1]>0,angel>0,np.ones(len(road),bool)):
        select(gradebonus,connected_mask,16,950)
    select(gradebonus,connected & (angel>0),9,400)
    select(gradebonus,connected & (offroad<300),10,450)
    for k in ("Lee Junction","Kyle Junction","Angel Mountain","Shady Hollow"):
        select(gradebonus,np.linalg.norm(ridges-xy[k],axis=1)<1600,4,450)
    # Look specifically for Lee-facing bridges into receivers that can serve Cathedral.
    # Road-footprint leaders alone can miss low-area, high-value backbone positions.
    terminals=[fixed.index(k) for k in ("Cathedral Rock","Shady Hollow","Kyle Junction","Legacy Fletcher","Fletcher Peak")]
    for j in terminals:
        select(gradebonus,view[:,j].astype(bool),8,700)
    south=[i for i in picked if view[i,terminals].any()]
    southview=screen(orig,orig[south],grid,meta,wave,radius)
    for j,i in enumerate(south):
        select(gradebonus,connected & (southview[:,j]>0),2,350)
    for a in terminals:
        select(gradebonus,connected & (view[:,a]>0),4,350)
    # Access-based intermediate positions on the mapped approach above legacy latitude band.
    trails=unary_union([g for g,p in features if p.get("highway") in ("path","footway") and g.intersects(Point(xy["Fletcher Peak"]).buffer(2500))])
    f=[]
    for x in np.arange(xy["Fletcher Peak"][0]-1100,xy["Fletcher Peak"][0]+1100,35):
        for y in np.arange(xy["Fletcher Peak"][1]+170,xy["Legacy Fletcher"][1]-80,35):
            z=elevation(grid,meta,x,y)
            if (elevation(grid,meta,*xy["Legacy Fletcher"])<z<elevation(grid,meta,*xy["Fletcher Peak"])
                    and trails.distance(Point(x,y))<90 and eligible(x,y)):
                f.append((x,y))
    fv=screen(points(grid,meta,f,4),test_targets,grid,meta,wave,radius)
    fs=fv[:,len(fixed):].sum(axis=1)+5*fv[:,:len(fixed)].sum(axis=1)
    xy["Fletcher intermediate"]=f[int(fs.argmax())]
    for j,i in enumerate(picked):
        xy[f"C{j+1:02}"]=tuple(ridges[i])
    junction=xy["Lee Junction"]
    local=[]
    for east in range(-2100,2101,35):
        for north in range(-2200,2201,35):
            x,y=junction[0]+east,junction[1]+north
            if math.hypot(east,north)<2400 and eligible(x,y):
                local.append((x,y))
    lv=screen(points(grid,meta,local,4),anchors,grid,meta,wave,radius)
    trial=[]
    for i,(x,y) in enumerate(local):
        if not lv[i,fixed.index("Angel Mountain")] or not (lv[i,0] or lv[i,1]):
            continue
        trial.append((math.dist(local[i],junction),i))
    # Native terrain confirmation near the current pin plus dispersed fallbacks.
    qualified=[]
    for side in (1,-1):
        count=0
        for _,i in sorted(trial):
            if (local[i][1]-junction[1])*side<0 or any(math.dist(local[i],prev)<95 for prev in qualified):
                continue
            here=(*local[i],4)
            def f1(k):
                return profile.stats(here,(*xy[k],1 if k=="Lee Fire" else 4))[1]
            if f1("Angel Mountain")>=.6 and max(f1("Upper Bristlecone"),f1("Lee Fire"))>=.6:
                qualified.append(local[i])
                count+=1
                if count==5:
                    break
    for i,coords in enumerate(qualified):
        xy[f"J{i+1}"]=coords
    for road in ("SR 156","SR 158"):
        point=Point(junction)
        line=min(roadlines[road],key=lambda geom:geom.distance(point))
        foot=np.array(line.interpolate(line.project(point)).coords[0])
        across=foot-np.array(junction)
        across/=np.linalg.norm(across)
        sites=[]
        for dx in range(-90,91,10):
            for dy in range(-90,91,10):
                pos=foot+np.array([dx,dy])
                if np.dot(pos-foot,across)>=15 and 8<line.distance(Point(pos))<100 and eligible(*pos):
                    sites.append(tuple(pos))
        ranked=[]
        for pos in sites:
            a=(*pos,4)
            endpoints=["Lee Fire","Upper Bristlecone","Angel Mountain"]
            margins=[profile.stats(a,(*xy[k],1 if k=="Lee Fire" else 4))[1] for k in endpoints]
            ranked.append(((min(max(margins[:2]),margins[2])>=.6,max(margins[:2])>=.6,
                            margins[2],-math.dist(pos,junction)),pos))
        if ranked:
            xy["Across "+road]=max(ranked)[1]
    if not qualified:
        # Keep a trial for explicitly comparing a blocked direct path to a two-relay alternative.
        xy["J1"]=max(local,key=lambda p:elevation(grid,meta,*p))
    return dict(screened=len(candidates),intermediate=len(f),shortlist=len(picked),junction_screened=len(local),junction_confirmed=len(qualified))

if __name__=="__main__":
    info=shortlist()
    ids=list(xy)
    masks=[]
    for k in ids:
        h=1 if k.endswith("Fire") else 4
        masks.append(sight(grid,meta,points(grid,meta,[xy[k]],h)[0],target3,5.,wave,radius))
    origins=points(grid,meta,list(xy.values()),4)
    for i,k in enumerate(ids):
        if k.endswith("Fire"):
            origins[i,2]-=3
    links={}
    for a,b in combinations(range(len(ids)),2):
        k,l=ids[a],ids[b]
        coarse=ray(grid,meta,origins[a],origins[b],10,wave,radius)
        if coarse[0]<-12 and k.startswith("C") and l.startswith("C"):
            continue
        A=(*xy[k],1 if k.endswith("Fire") else 4)
        B=(*xy[l],1 if l.endswith("Fire") else 4)
        c,f,_=profile.stats(A,B)
        if np.isfinite(c):
            links[k+"|"+l]=[c,f]
    (OUT/"search.json").write_text(json.dumps(dict(xy=xy,info=info,links=links)))
    np.savez_compressed(OUT/"targets.npz",masks=masks,ids=ids,targets=targets,groups=groups,names=names,weights=weights,part=part,offset=offset)
    print(info,len(links),flush=True)
