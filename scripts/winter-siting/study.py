"""Build outputs from editable inputs and locally cached public data."""
from pathlib import Path
import argparse
import sys
import os
import json
import math


def configure(root):
    libs=root/'envpkgs'
    if libs.is_dir():
        sys.path.insert(0,str(libs))
    os.environ.setdefault('NUMBA_NUM_THREADS','8')
    os.environ.setdefault('MPLCONFIGDIR',str(root/'cache/matplotlib'))
    for sub in ('gis','cache','tables','inputs'):
        (root/sub).mkdir(exist_ok=True,parents=True)


def run(root):
    import numpy as np
    import rasterio as rio
    from sources import verify_sources
    verify_sources(root)
    from shapely.geometry import Point,LineString
    from terrain import forward,inverse,load_dem,mosaic,elevation,points,sight,write_raster
    from geography import geography,save_features
    from routing import choose,routes_to_gateways,union_mask
    cfg=json.loads((root/'inputs/study.json').read_text())
    source=root/'source'
    if not (source/'local-osm.geojson').exists():
        from extract_map import extract
        extract(source/'nevada.osm.pbf',source/'local-osm.geojson',cfg['map_extract_wsen'])
    bounds,routes,samples,excluded,driving,parking,facilities=geography(root,cfg)
    gis=root/'gis'
    save_features(gis/'boundary.geojson',[(bounds,{'use':'scoring boundary'})])
    save_features(gis/'routes.geojson',routes)
    save_features(gis/'facilities.geojson',[(g,dict(name=n)) for g,n in facilities])
    left,bottom,right,top=bounds.bounds
    res=cfg['area_pixel_m']
    west=math.floor(left/res)*res
    north=math.ceil(top/res)*res
    width,height=math.ceil((right-west)/res),math.ceil((north-bottom)/res)
    affine=rio.transform.from_origin(west,north,res,res)
    xs=west+(np.arange(width)+.5)*res
    ys=north-(np.arange(height)+.5)*res
    from shapely import contains_xy
    xx,yy=np.meshgrid(xs,ys)
    inside=contains_xy(bounds,xx,yy)
    area_xy=np.column_stack((xx[inside],yy[inside]))
    base=root/'cache/terrain-local.tif'
    regional=root/'cache/terrain-regional.tif'
    local_bounds=[west-500,north-height*res-500,west+width*res+500,north+500]
    # Derived DEMs are keyed to editable bounds, spacing and source file identity.
    signature=json.dumps([local_bounds,cfg['regional_bounds'],cfg['terrain_m'],[(p.name,p.stat().st_size) for p in sorted(source.glob('*.tif'))]])
    marker=root/'cache/terrain-inputs.json'
    if not marker.exists() or marker.read_text()!=signature or not base.exists() or not regional.exists():
        mosaic(source,base,local_bounds,cfg['terrain_m'],True)
        mosaic(source,regional,cfg['regional_bounds'],20,False)
        marker.write_text(signature)
    dem,meta=load_dem(base)
    rg,rm=load_dem(regional)
    wav=299.792458/cfg['frequency_mhz']
    radius=6371000*cfg['effective_earth_k']
    rawxy=np.array([(s['x'],s['y']) for s in samples])
    sample_targets=points(dem,meta,rawxy,cfg['member_m'])
    land_targets=points(dem,meta,area_xy,cfg['member_m'])
    if not np.isfinite(sample_targets).all() or not np.isfinite(land_targets).all():
        raise ValueError('Missing target ground')
    def weight_of(s):
        _,lat=inverse.transform(s['x'],s['y'])
        return cfg['lee_weight'] if lat>=cfg['lee_north_of_lat'] or 'Lee' in s['name'] or s['name'] in ['SR 156','McWilliams Campground'] else 1.
    weights=np.array([s['w']*weight_of(s) for s in samples])
    for kind in ('road','trail','facility'):
        flags=np.array([s['kind']==kind for s in samples])
        if kind=='facility':
            for name in sorted({s['name'] for s in samples if s['kind']==kind}):
                ii=flags & np.array([s['name']==name for s in samples])
                weights[ii]/=sum(samples[i]['w'] for i in np.flatnonzero(ii))
        weights[flags]*=cfg['class_weights'][kind]/weights[flags].sum()
    # Explore road-accessible bridges throughout the corridor before refining a 20 m circle.
    # Sort geographically along the main corridor, then sample both sides of each centreline.
    anchors=points(dem,meta,[forward.transform(v[3],v[2]) for v in cfg['sites']],cfg['repeater_m'])
    seed_ids=[s[0] for s in cfg['sites']]
    anchor_gate=[seed_ids.index(g) for g in cfg['gateways']]
    anchors[anchor_gate,2]-=cfg['repeater_m']-cfg['gateway_m']
    probes=sample_targets[::18]; pw=weights[::18]*18
    for code,name,route,low,high in cfg.get('corridor_searches',[]):
        pool=[s for s in samples if s['kind']=='road' and s['name']==route]
        pool.sort(key=lambda s:s['y'] if route in ('SR 156','SR 158') else -s['x'] if route=='Macks Canyon' else s['x'])
        best=None
        for entry in pool[int(low*len(pool)):int(high*len(pool)):5]:
            line=entry['segment']; a,b=line.coords[0],line.coords[-1]
            angle=math.atan2(b[1]-a[1],b[0]-a[0])+math.pi/2
            for setback in (-140,-65,-20,20,65,140):
                x=entry['x']+setback*math.cos(angle);y=entry['y']+setback*math.sin(angle)
                if not bounds.contains(Point(x,y)) or len(excluded.query(Point(x,y),predicate='intersects')):continue
                z=float(elevation(dem,meta,x,y))
                slope=math.hypot(elevation(dem,meta,x+5,y)-elevation(dem,meta,x-5,y),elevation(dem,meta,x,y+5)-elevation(dem,meta,x,y-5))/10
                if slope>.58:continue
                o=np.array([x,y,z+cfg['repeater_m']])
                v=sight(dem,meta,o,anchors,8,wav,radius)
                reach=sight(dem,meta,o,probes,15,wav,radius)@pw
                # Reward connections into both canyon systems as well as actual member visibility.
                cross=float(any(v[seed_ids.index(k)] for k in ('GK','CL','CH','FL') if k in seed_ids) and
                            any(v[seed_ids.index(k)] for k in ('GL','SK','SI','SA','LC') if k in seed_ids))
                score=reach+.09*sum(map(float,v[anchor_gate]))+.065*cross+.003*sum(map(float,v))-.00008*abs(setback)
                if best is None or score>best[0]:best=(score,x,y)
        if best:
            lon,lat=inverse.transform(best[1],best[2])
            cfg['sites'].append([code,name,lat,lon,'corridor','Inspect the road-to-tree approach from a legal off-road stop; use the mapped staging alternative if the shoulder is restricted.'])
    ids=[s[0] for s in cfg['sites']]
    gateway=[ids.index(i) for i in cfg['gateways']]
    def ground(x,y):return float(elevation(dem,meta,x,y))
    def site_origin(s):
        return np.array([s['x'],s['y'],s['z']+s['h']])
    sites=[]
    for code,name,lat,lon,access,instruction in cfg['sites']:
        x,y=forward.transform(lon,lat)
        if access=='search':
            # Find a practical new nominal pin within 250 m of an inventoried road or trail stop.
            # Exclude the carriageway and implausibly steep/constructed ground.
            options=[]
            for dx in range(-240,241,20):
                for dy in range(-240,241,20):
                    dist=math.hypot(dx,dy)
                    if dist>250:continue
                    p=Point(x+dx,y+dy)
                    if len(excluded.query(p,predicate='intersects')):continue
                    z=ground(p.x,p.y)
                    slope=math.hypot(ground(p.x+5,p.y)-ground(p.x-5,p.y),ground(p.x,p.y+5)-ground(p.x,p.y-5))/10
                    if slope<.57:options.append((z-.11*dist-.06*p.distance(driving),p.x,p.y))
            if options:_,x,y=max(options)
        sites.append(dict(id=code,name=name,access=access,note=instruction,nx=x,ny=y,x=x,y=y,z=ground(x,y),
                          h=cfg['gateway_m'] if access=='station' else cfg['repeater_m'],
                          difficulty={'station':0,'search':1,'corridor':1,'owner':1,'conditional':4,'hike':3,'hard':7}[access]))
    nominal=np.array([site_origin(s) for s in sites])
    survey=np.vstack((sample_targets[::8],land_targets[::120]))
    survey_w=np.r_[weights[::8]*8,np.full(len(land_targets[::120]),.08/len(land_targets[::120]))]
    for i,s in enumerate(sites):
        if i in gateway:continue
        options=[]
        for dx in range(-20,21,5):
            for dy in range(-20,21,5):
                if math.hypot(dx,dy)>20:continue
                x,y=s['nx']+dx,s['ny']+dy
                p=Point(x,y)
                if len(excluded.query(p,predicate='intersects')):continue
                slope=math.hypot(ground(x+5,y)-ground(x-5,y),ground(x,y+5)-ground(x,y-5))/10
                if slope>.75:continue
                o=np.array([x,y,ground(x,y)+s['h']])
                vis=sight(dem,meta,o,survey,12,wav,radius)
                infra=sight(dem,meta,o,nominal,6,wav,radius)
                score=vis@survey_w+.048*sum(float(infra[g]) for g in gateway)+.002*sum(infra)-.001*slope
                options.append((score,-math.hypot(dx,dy),x,y))
        if options:
            _,_,s['x'],s['y']=max(options)
        else:s['mount_warning']='No screened cell in circle; conditional scouting only'
        s['z']=ground(s['x'],s['y'])
        s['tested_cells']=len(options)
    print('Scored local search circles',flush=True)
    origins=np.array([site_origin(s) for s in sites])
    from native import Profiles
    native=Profiles(source.glob('USGS_1M*.tif'),dem,meta,wav,radius)
    def links_for(orig,heights=None):
        heights=heights if heights is not None else [s['h'] for s in sites]
        matrix=np.zeros((len(orig),len(orig)),bool)
        values={}
        for i in range(len(orig)):
            for j in range(i):
                v=native.stats((*orig[i,:2],heights[i]),(*orig[j,:2],heights[j]))
                values[i,j]=v
                matrix[i,j]=matrix[j,i]=v[0]>=0
        return matrix,values
    links,profiles=links_for(origins)
    member=np.array([sight(dem,meta,o,sample_targets,cfg['terrain_m'],wav,radius) for o in origins],bool)
    area=np.array([sight(dem,meta,o,land_targets,cfg['terrain_m'],wav,radius) for o in origins],bool)
    print('Full member footprints ready',flush=True)
    def integer(a):return int.from_bytes(np.packbits(a,bitorder='little').tobytes(),'little')
    # Integer bitsets give exact unions; equal-width weight buckets approximate the score only.
    allweights=np.r_[weights,np.full(len(area_xy),cfg['class_weights']['land']/len(area_xy))]
    unique=np.unique(np.round(np.log(np.maximum(allweights,1e-16))/.08).astype(int))
    bucket=np.round(np.log(np.maximum(allweights,1e-16))/.08).astype(int)
    grouped=[(integer(bucket==b),allweights[bucket==b].mean()) for b in unique]
    masks=[integer(np.r_[m,a]) for m,a in zip(member,area)]
    hops=cfg['hop_limit']
    allowed=[i for i,s in enumerate(sites) if s.get('mount_warning')]
    rec,merit=choose(sites,gateway,links,hops,masks,grouped,9,excluded=allowed)
    first=[ids.index(k) for k in cfg['preferred_first_tests'] if ids.index(k) in rec]
    rec=first+[i for i in rec if i not in first]
    print('Selected', [ids[i] for i in rec],flush=True)
    recset=gateway+rec
    def score(indices,failed=None, matrix=links, members=member, lands=area):
        paths=routes_to_gateways(indices,gateway,matrix,hops,failed)
        if paths:
            ix=list(paths)
            return members[ix].any(0),lands[ix].any(0),paths
        return np.zeros(member.shape[1],bool),np.zeros(area.shape[1],bool),{}
    start=gateway+[ids.index(k) for k in cfg['start']]
    sw=np.array([s['w'] for s in samples])
    def metrics(m,a):
        out={'land_km2':round(float(sum(a)*res**2/1e6),3)}
        for kind in ('road','trail'):
            mask=np.array([s['kind']==kind for s in samples])
            out[kind+'_km']=round(float(sw[m & mask].sum()/1000),3)
        for name in sorted({s['name'] for s in samples if s['kind'] in ('road','facility')}):
            mask=np.array([s['name']==name for s in samples])
            out[name]=round(float(sw[m & mask].sum()/sw[mask].sum()*100),2)
        return out
    baseline_m,baseline_a,paths=score(recset)
    summary={'selected':[ids[i] for i in rec],'gateways':cfg['gateways'],'sites':sites,
             'paths':{ids[i]:[ids[j] for j in p] for i,p in paths.items()},'scenarios':{},'alternatives':{},
             'heights':[],'roads':{},'pairs':[],'valley':[],'sample_count':len(samples)}
    def scenario(label,idx,**kwargs):
        m,a,p=score(idx,**kwargs)
        summary['scenarios'][label]=metrics(m,a)
    summary['total']=metrics(np.ones(len(samples),bool),np.ones(len(area_xy),bool))
    scenario('Direct',gateway)
    scenario('Starting / lower',start)
    scenario('Starting / higher',[ids.index('CH') if ids[i]=='CL' else i for i in start])
    scenario('Starting / no Angel Vegas',[i for i in start if ids[i]!='AV'])
    scenario('Starting / no Angel mountain',[i for i in start if ids[i]!='AM'])
    scenario('Starting / neither Angel',[i for i in start if ids[i] not in ('AV','AM')])
    upper=[ids.index('CH') if ids[i]=='CL' else i for i in start]
    for name,omit in [('no Vegas',['AV']),('no mountain',['AM']),('neither',['AM','AV'])]:
        scenario('Higher / '+name,[i for i in upper if ids[i] not in omit])
    scenario('Recommended',recset)
    # Re-optimize the other eight positions for each owner drive-up candidate.
    summary['drive_up_trials']={}
    for key in cfg['owner_site_trials']:
        index=ids.index(key)
        if index in allowed:
            raise ValueError(f'Owner site {key} has no physically screened mount; inspect the search mask.')
        chosen,_=choose(sites,gateway,links,hops,masks,grouped,9,excluded=allowed,forced=[index])
        gains=metrics(*score(gateway+chosen)[:2])
        summary['drive_up_trials'][key]={'layout':[ids[i] for i in chosen],'metrics':gains,
                                        'direct_gateways':[ids[j] for j in gateway if links[index,j]]}
    if ids.index('FL') in rec:
        nofl,_=choose(sites,gateway,links,hops,masks,grouped,9,excluded=allowed+[ids.index('FL')])
    else:nofl=rec
    summary['no_fletcher']=[ids[i] for i in nofl]
    scenario('Fletcher unavailable',gateway+nofl)
    noch,_=choose(sites,gateway,links,hops,masks,grouped,9,excluded=allowed+[ids.index('CH')])
    summary['no_high_cathedral']=[ids[i] for i in noch]
    scenario('Higher Cathedral unavailable',gateway+noch)
    nominal_links=links_for(nominal)[0]
    nominal_members=np.array([sight(dem,meta,o,sample_targets,cfg['terrain_m'],wav,radius) for o in nominal],bool)
    nominal_lands=np.array([sight(dem,meta,o,land_targets,cfg['terrain_m'],wav,radius) for o in nominal],bool)
    scenario('Nominal starting pins',start,matrix=nominal_links,members=nominal_members,lands=nominal_lands)
    scenario('Recommended at nominal pins',recset,matrix=nominal_links,members=nominal_members,lands=nominal_lands)
    for i,s in enumerate(sites):
        s['nominal_footprint']=metrics(nominal_members[i],nominal_lands[i])
        s['selected_footprint']=metrics(member[i],area[i])
    def raster(label,arr):
        data=np.full(inside.shape,255,'uint8')
        data[inside]=arr
        write_raster(gis/(label+'.tif'),data,affine,255)
    for i in recset:
        raster('viewshed-'+ids[i],area[i])
        if i in rec:
            leftset=[k for k in rec if k!=i]
            options=[k for k in range(len(sites)) if k not in recset+allowed and
                     not {'CL','CH'}<={ids[j] for j in leftset+[k]}]
            alt=max(options,key=lambda k:merit(leftset+[k]))
            easy=[k for k in options if sites[k]['difficulty']<=sites[i]['difficulty']]
            easy=max(easy,key=lambda k:merit(leftset+[k])) if easy else alt
            summary['alternatives'][ids[i]]={'best':ids[alt],'easy':ids[easy],'metrics':metrics(*score(gateway+leftset+[easy])[:2])}
    for k in range(1,len(rec)+1):scenario('Order '+str(k),gateway+rec[:k])
    for code in ('AV','AM'):
        i=ids.index(code)
        scenario('Recommended +/- '+code,([k for k in recset if k!=i] if i in recset else recset+[i]))
    candidates=[i for i in range(len(sites)) if i not in recset+allowed and not ({'CL','CH'}<={ids[j] for j in rec+[i]})]
    extra=max(candidates,key=lambda i:merit(rec+[i]));summary['extra']=ids[extra]
    scenario('Tenth candidate',recset+[extra])
    raster('terrain-union',area[recset].any(0))
    raster('relay-overlap',area[rec].sum(0))
    raster('reachability',baseline_a.astype('uint8'))
    scenario('60 percent F1 backbone',recset,matrix=np.array([[profiles[max(i,j),min(i,j)][1]>=.6 if i!=j else False for j in range(len(sites))] for i in range(len(sites))]))
    for kind,h in [('Inside vehicle',cfg['in_vehicle_m']),('Roof antenna',cfg['roof_m'])]:
        if h==cfg['member_m']:scenario(kind,recset)
        else:
            mm=member.copy();aa=area.copy()
            for i in recset:
                mm[i]=sight(dem,meta,origins[i],sample_targets+[0,0,h-cfg['member_m']],5,wav,radius)
                aa[i]=sight(dem,meta,origins[i],land_targets+[0,0,h-cfg['member_m']],5,wav,radius)
            scenario(kind,recset,members=mm,lands=aa)
    for i in recset:
        for h in (cfg['gateway_heights'][1:] if i in gateway else [sites[i]['h']+cfg['lift_m']]):
            orig=origins.copy();orig[i,2]+=h-sites[i]['h']
            mat=links.copy()
            for j in recset:
                if j!=i:mat[i,j]=mat[j,i]=native.stats((*orig[i,:2],h),(*orig[j,:2],sites[j]['h']))[0]>=0
            mm=member.copy();aa=area.copy()
            mm[i]=sight(dem,meta,orig[i],sample_targets,5,wav,radius)
            aa[i]=sight(dem,meta,orig[i],land_targets,5,wav,radius)
            m,a,_=score(recset,matrix=mat,members=mm,lands=aa)
            summary['heights'].append(dict(id=ids[i],height=h,new=[ids[j] for j in recset if mat[i,j] and not links[i,j]],**metrics(m,a)))
    save_features(gis/'route-status.geojson',[(s['segment'],dict(name=s['name'],status=('reachable' if b else 'blind'))) for s,b in zip(samples,baseline_m) if s['segment'] is not None])
    gaps=[]
    for name in sorted({s['name'] for s in samples if s['kind']=='road'}):
        # Join contiguous pieces in their original measured order; avoid fragile geometric exact-equality at splits.
        runs=[];run=[]
        for s,v in zip(samples,baseline_m):
            if s['name']!=name or v or s['segment'] is None:
                if run:runs.append(run);run=[]
                continue
            coords=list(s['segment'].coords)
            if run and math.dist(run[-1],coords[0])>.01:runs.append(run);run=[]
            run+=coords if not run else coords[1:]
        if run:runs.append(run)
        geom=[LineString(k) for k in runs if len(k)>1]
        for g in geom:gaps.append((g,dict(name=name,length_m=round(g.length,1))))
        ranking=sorted(geom,key=lambda g:-g.length)
        summary['roads'][name]=[dict(km=g.length/1000,a=inverse.transform(*g.coords[0]),b=inverse.transform(*g.coords[-1])) for g in ranking[:3]]
    save_features(gis/'road-gaps.geojson',gaps)
    pairs=[]
    for (i,j),(clear,f1,at) in profiles.items():
        a,b=sites[i],sites[j]
        length=math.dist(origins[i,:2],origins[j,:2])
        data=dict(a=ids[i],b=ids[j],length_m=length,clear_m=clear,f1=f1,at_m=at,active=i in recset and j in recset,los=bool(links[i,j]))
        pairs.append((LineString([origins[i,:2],origins[j,:2]]),data));summary['pairs'].append(data)
    save_features(gis/'links.geojson',pairs)
    from supplemental import finish_sites,solar,valley
    finish_sites(root,sites,recset,gateway,parking,driving,routes,dem,meta,cfg)
    solar(root,sites,recset,rg,rm,dem,meta,cfg)
    summary['valley']=valley(sites,ids,cfg,rg,rm,wav,radius)
    # Portable drive-up tests use the supplied vehicle position, before tree refinement.
    drive_sites=[dict(s,x=s['nx'],y=s['ny'],z=ground(s['nx'],s['ny'])) if s['id'] in ('AM','AV') else s for s in sites]
    summary['valley_drive_up']=valley(drive_sites,ids,cfg,rg,rm,wav,radius)
    # Model a hypothetical receiving home reachable from the Vegas-side Angel only.
    # No direct home/member rays are credited and the home never forwards on RF.
    av=ids.index('AV')
    move=max((i for i in rec if i!=av),key=lambda i:merit([j for j in rec if j!=i]+[av]))
    home_ix=len(sites);ext=np.pad(links,((0,1),(0,1)))
    ext[av,home_ix]=ext[home_ix,av]=True
    def homecase(layout):
        p=routes_to_gateways(gateway+layout+[home_ix],gateway+[home_ix],ext,hops)
        ix=[i for i in p if i!=home_ix]
        return metrics(member[ix].any(0),area[ix].any(0))
    h9=rec if av in rec else [i for i in rec if i!=move]+[av]
    summary['home']={'swapped':ids[move] if av not in rec else None,'nine':homecase(h9),'add_vegas_site':homecase(list(dict.fromkeys(rec+[av])))}
    for file in gis.glob('viewshed-*.tif'):
        if file.stem.removeprefix('viewshed-') not in {ids[i] for i in recset}:file.unlink()
    # Older packets exported loss rasters. Keep them out of the current GIS set.
    for file in gis.glob('loss-*.tif'):
        archive=root/'cache/archived-loss-rasters'
        archive.mkdir(exist_ok=True)
        file.replace(archive/file.name)
    tips=[]
    for name in ('SR 156','SR 157','SR 158'):
        group=[g for g,p in routes if p['name']==name]
        endpoints=[(x,y) for g in group for x,y in [g.coords[0],g.coords[-1]]]
        p,q=max(((a,b) for a in endpoints for b in endpoints),key=lambda ab:math.dist(*ab))
        summary.setdefault('highways',{})[name]=[inverse.transform(*p),inverse.transform(*q)]
        tips.extend([(Point(pt),dict(name=name,end=end)) for pt,end in [(p,'A'),(q,'B')]])
    save_features(gis/'highway-limits.geojson',tips)
    (root/'tables/results.json').write_text(json.dumps(summary,indent=2,allow_nan=False),encoding='utf8')
    from report import make_report
    make_report(root,cfg,summary)
    print('Completed field report',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    args=parser.parse_args()
    root=args.directory.resolve()
    configure(root)
    run(root)
