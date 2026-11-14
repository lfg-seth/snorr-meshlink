"""Find ridge and shoulder alternatives near the two Lee-side gaps before the full study."""
import argparse
import json
import math
from pathlib import Path
from study import configure


def shortlist(root):
    import numpy as np
    from numba import njit, prange
    from shapely.geometry import Point
    from shapely.ops import unary_union
    from geography import geography
    from terrain import load_dem, elevation, points, inverse, ray
    from routing import routes_to_gateways
    cfg=json.loads((root/'inputs/study.json').read_bytes())
    previous=json.loads((root/'tables/results.json').read_bytes())
    bounds,routes,samples,exclude,_,_,_=geography(root,cfg)
    dem,meta=load_dem(root/'cache/terrain-local.tif')
    names=('SR 156','Macks Canyon')
    route=unary_union([g for g,p in routes if p['name'] in names and p['kind']=='road'])
    core=cfg['gateways']+cfg['baseline_nine']+[cfg['additional_repeater']]
    sites={s['id']:s for s in previous['sites']}
    keys=[(sites[k]['x'],sites[k]['y']) for k in core]
    anchors=points(dem,meta,keys,0)
    anchors[:,2]+=[sites[k]['h'] for k in core]
    backbone=np.zeros((len(core),len(core)),bool)
    for p in previous['pairs']:
        if p['los'] and p['a'] in core and p['b'] in core:
            i,j=core.index(p['a']),core.index(p['b'])
            backbone[i,j]=backbone[j,i]=True
    hops=cfg['hop_limit']
    gateways=list(range(len(cfg['gateways'])))
    parent=routes_to_gateways(list(range(len(core))),gateways,backbone,hops-1)
    selected=[s for s in samples if s['kind']=='road' and s['name'] in names]
    targets=points(dem,meta,[(s['x'],s['y']) for s in selected],cfg['member_m'])
    w=np.array([s['w'] for s in selected])
    is_macks=np.array([s['name']=='Macks Canyon' for s in selected])
    @njit(parallel=True)
    def cast(grid,metadata,starts,ends,step,wav,radius):
        out=np.zeros((len(starts),len(ends)),np.bool_)
        for i in prange(len(starts)):
            for j in range(len(ends)):
                out[i,j]=ray(grid,metadata,starts[i],ends[j],step,wav,radius,True)[0]>=0
        return out
    wav=299.792458/cfg['frequency_mhz'];radius=6371000*cfg['effective_earth_k']
    def visibility(starts,ends,step):
        return cast(dem,meta,starts,ends,step,wav,radius)
    linked=routes_to_gateways(list(range(len(core))),gateways,backbone,hops)
    blind=~visibility(anchors[list(linked)],targets,5.).any(0)
    zone=route.buffer(1800).intersection(bounds)
    w0,s0,e0,n0=zone.bounds
    options=[]
    for x in range(100*math.floor(w0/100),math.ceil(e0),100):
        for y in range(100*math.floor(s0/100),math.ceil(n0),100):
            p=Point(x,y)
            if not zone.contains(p) or len(exclude.query(p,predicate='intersects')):continue
            slope=math.hypot(elevation(dem,meta,x+5,y)-elevation(dem,meta,x-5,y),
                             elevation(dem,meta,x,y+5)-elevation(dem,meta,x,y-5))/10
            if slope<=.57:options.append((x,y))
    origins=points(dem,meta,options,cfg['repeater_m'])
    sees=visibility(origins,targets[blind],10.)
    uplinks=visibility(origins,anchors,7.)
    active=uplinks[:,list(parent)].any(1)
    # Screen both a stand-alone serving site and a Macks-serving site that needs a bridge.
    # Keep candidates separated so distinct slopes survive the shortlist.
    gains=sees@w[blind]
    macks=sees@(w*is_macks)[blind]
    si=core.index(cfg['additional_repeater'])
    gain_sisters=(visibility(anchors[[si]],targets[blind],5.)[0]*w[blind]).sum()
    bridge_parent=routes_to_gateways(list(range(len(core))),gateways,backbone,hops-2)
    makes_sisters=uplinks[:,si] & uplinks[:,list(bridge_parent)].any(1)
    chosen=[]
    for scores,valid,count in [(gains,active,4),(macks,active,2),(macks,~active,4),(gains+makes_sisters*gain_sisters,makes_sisters,1)]:
        added=0
        for i in np.argsort(-scores,kind='stable'):
            if scores[i]<=0:break
            if not valid[i] or any(math.dist(options[i],options[j])<450 for j in chosen):continue
            chosen.append(i);added+=1
            if added==count:break
    # Seek bridges able to forward one more repeater within the hop limit.
    relayable=uplinks[:,list(bridge_parent)].any(1)
    donors=np.array([i for i in chosen if macks[i]>0 and not active[i]],dtype=int)
    if len(donors):
        edges=visibility(origins,origins[donors],7.)
        pair_scores=np.zeros(len(origins))
        for col,j in enumerate(donors):
            combined=(sees|sees[j])@w[blind]
            pair_scores=np.maximum(pair_scores,np.where(edges[:,col]&relayable,combined,0))
        added=0
        for i in np.argsort(-pair_scores,kind='stable'):
            if pair_scores[i]<=0:break
            if any(math.dist(options[i],options[j])<250 for j in chosen):continue
            chosen.append(i);added+=1
            if added==3:break
    result=[]
    for i in chosen:
        lon,lat=inverse.transform(*origins[i,:2])
        result.append(dict(lon=lon,lat=lat,screen_gain_m=round(gains[i]),macks_m=round(macks[i]),
                           road_offset_m=round(route.distance(Point(options[i]))),linked=bool(active[i]),
                           may_link_sisters=bool(makes_sisters[i])))
    output=dict(grid_m=100,radius_m=1800,screened=len(origins),shortlist=result)
    (root/'tables/lee-ridge-scout.json').write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    root=parser.parse_args().directory.resolve();configure(root);shortlist(root)
