import json
import math
import calendar
from datetime import datetime,timedelta,timezone
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as ET
import numpy as np
import networkx as nx
from scipy.spatial import cKDTree
from pyproj import Proj
from shapely.geometry import Point,LineString,shape
from shapely.ops import transform,nearest_points
from terrain import forward,inverse,elevation,ray,CRS
from geography import save_features,parts


def bearing(lon1,lat1,lon2,lat2):
    from pyproj import Geod
    az,_,d=Geod(ellps='WGS84').inv(lon1,lat1,lon2,lat2)
    return round(az%360),round(d,1)


def finish_sites(root,sites,active,gateways,parking,driving,routes,dem,meta,cfg):
    from field_names import field_code, field_name, navigation_name
    raw=json.loads((root/'source/local-osm.geojson').read_bytes())['features']
    graph=nx.Graph()
    for f in raw:
        p=f['properties']
        if not p.get('highway') or p.get('access') in ('no','private') or p.get('name','') in (
                'Cathedral Rock Trail','Upper Bristlecone Trail','Trail Canyon Trail','Mary Jane Falls Trail','Echo Road'):
            continue
        g=transform(forward.transform,shape(f['geometry']))
        for line in parts(g,'LineString'):
            xy=[(round(x,2),round(y,2)) for x,y in line.coords]
            for a,b in zip(xy,xy[1:]):
                if a!=b:graph.add_edge(a,b,weight=math.dist(a,b))
    nodes=list(graph); tree=cKDTree(nodes)
    def snap(xy):return nodes[tree.query(xy)[1]]
    official={
        'SK':'w1154358378','SI':'w593965244','CL':'w363844339','CH':'w363844339',
        'SA':'w593535195','CM':'w593535195',
        'MK':'w571835252','MU':'w571835252','LC':'w593535195'}
    named={'FL':'North Loop Trailhead','DV':'Desert View Overlook','SG':'North Loop Trailhead','AM':'North Loop Trailhead',
           'AV':'North Loop Trailhead','LS':'North Loop Trailhead','HT':'North Loop Trailhead','RR':"Robber\'s Roost Trailhead",
           'FV':'Fletcher Canyon','KJ':'Fletcher Canyon','DC':'Deer Creek Picnic Area','LF':'Lower Bristlecone Trailhead',
           'KR':'Stanley B Springs','AL':'North Loop Trailhead','EL':'','BC':'Desert View Overlook'}
    official['EL']='w593535195'
    nav=ET.Element('gpx',version='1.1',creator='SNORR winter siting',xmlns='http://www.topografix.com/GPX/1/1')
    gsites=[];stops=[];approaches=[]
    def waypoint(x,y,name,desc):
        lon,lat=inverse.transform(x,y)
        w=ET.SubElement(nav,'wpt',lat=f'{lat:.7f}',lon=f'{lon:.7f}')
        ET.SubElement(w,'name').text=name
        ET.SubElement(w,'desc').text=desc
    for i,s in enumerate(sites):
        code=s['id'];end=s['x'],s['y'];pt=Point(end)
        s['ll']=inverse.transform(*end);s['nom_ll']=inverse.transform(s['nx'],s['ny'])
        s['bearing'],s['shift']=bearing(*s['nom_ll'],*s['ll'])
        if i not in active:continue
        flag='estimated'
        if code=='SK':
            start=next(p.coords[0] for p,tags in parking if tags['osm_id']==official[code])
            stop='Upper Bristlecone trailhead lot'
            status='Owner confirms easy agency access. Staging uses a point inside the mapped lot.'
        elif code in cfg['drive_up_sites']:
            start=(s['nx'],s['ny'])
            stop='Owner drive-up at the supplied pin'
            status='Owner-confirmed access. Distance covers only the nominal pin to the modeled mount.'
        elif i in gateways:
            start=end
            stop='Station premises, host-guided stop; exact bay unknown'
            status='Owner station pin used as rendezvous; zero walking distance is a co-location assumption.'
        else:
            shortlist=[pair for pair in parking if pair[1]['osm_id']==official.get(code) or named.get(code,'--')==pair[1].get('name')]
            start_pt,tags=min(shortlist or parking,key=lambda gp:pt.distance(gp[0]))
            stop=tags.get('name') or {'SK':'Resort base lot','SA':'Sawmill lot','CM':'Sawmill lot','LC':'Sawmill lot',
                                       'MK':'Macks road mouth lot','MU':'Macks road mouth lot','EL':'Sawmill lot'}.get(code,'Mapped off-road lot')
            start=start_pt.coords[0]
            status=f"OSM {tags['osm_id']}; check signs, snow and gate on arrival."
            if code in ('AM','AV','MK','MU','LS','AL','EL','LC','CM','KJ','SG','BC'):
                near=nearest_points(pt,driving)[1]
                s['conditional_stop']=inverse.transform(near.x,near.y)
                s['conditional_walk_m']=round(pt.distance(near))
        xy=[start,end]
        if start!=end and code not in cfg['drive_up_sites']:
            a,b=snap(start),snap(end)
            try:
                path=nx.shortest_path(graph,a,b,weight='weight')
                if len(path)>1 and math.dist(start,a)<200 and math.dist(end,b)<550:
                    xy=[start]+path+[end]
                    flag='mapped centerlines + estimated connectors'
            except nx.NetworkXNoPath:
                pass
        line=LineString(xy)
        stations=np.linspace(0,line.length,max(2,math.ceil(line.length/10)))
        elevations=[elevation(dem,meta,p.x,p.y) for d in stations for p in [line.interpolate(d)]]
        ascent=sum(max(0,b-a) for a,b in zip(elevations,elevations[1:]))
        s.update(stop_ll=inverse.transform(*start),stop=stop,stop_evidence=status,walk_m=round(line.length),
                 ascent_m=round(ascent),approach=flag)
        waypoint(*end,navigation_name(code),'Search circle only; '+s['note'])
        waypoint(*start,navigation_name(code)+' - stage',stop+'; '+status)
        stops.append((Point(start),dict(id=code,name=stop,field_name=field_name(code),field_code=field_code(code),evidence=status)))
        if line.length:approaches.append((line,dict(id=code,field_name=field_name(code),field_code=field_code(code),method=flag)))
    selected_ids={sites[i]['id'] for i in active}
    for code in cfg['drive_up_sites']:
        if code not in selected_ids:
            s=next(s for s in sites if s['id']==code)
            waypoint(s['nx'],s['ny'],navigation_name(code)+' - drive-up test',
                     'Owner-supplied vehicle position for the Angel Peak radio comparison.')
    for s in sites:
        gsites.append((Point(s['x'],s['y']),{k:s[k] for k in ('id','name','z','h','shift','bearing','access')}|{'field_name':field_name(s['id']),'field_code':field_code(s['id']),'selected':sites.index(s) in active,'nom_lon':s['nom_ll'][0],'nom_lat':s['nom_ll'][1]}))
    save_features(root/'gis/sites.geojson',gsites);save_features(root/'gis/staging.geojson',stops)
    save_features(root/'gis/approaches.geojson',approaches)
    ET.ElementTree(nav).write(root/'navigation.gpx',encoding='utf-8',xml_declaration=True)


def solar_position(utc,lon,lat):
    # NOAA fractional-year approximation; azimuth clockwise from true north.
    day=utc.timetuple().tm_yday
    hour=utc.hour+utc.minute/60
    gamma=2*math.pi/365*(day-1+(hour-12)/24)
    eq=229.18*(.000075+.001868*math.cos(gamma)-.032077*math.sin(gamma)-.014615*math.cos(2*gamma)-.040849*math.sin(2*gamma))
    dec=(.006918-.399912*math.cos(gamma)+.070257*math.sin(gamma)-.006758*math.cos(2*gamma)+
         .000907*math.sin(2*gamma)-.002697*math.cos(3*gamma)+.00148*math.sin(3*gamma))
    ha=math.radians((hour*60+eq+4*lon)/4-180)
    lat=math.radians(lat)
    alt=math.asin(math.sin(lat)*math.sin(dec)+math.cos(lat)*math.cos(dec)*math.cos(ha))
    az=math.atan2(math.sin(ha),math.cos(ha)*math.sin(lat)-math.tan(dec)*math.cos(lat))+math.pi
    return math.degrees(az)%360,math.degrees(alt)


def solar(root,sites,active,regional,rm,dem,meta,cfg):
    climatology=json.loads((root/'source/solar.json').read_bytes())['properties']['parameter']
    tz=ZoneInfo('America/Los_Angeles')
    proj=Proj(CRS)
    for i in active:
        s=sites[i];lon,lat=s['ll']
        convergence=proj.get_factors(lon,lat).meridian_convergence
        horizon=[]
        distances=np.r_[np.arange(5,600,5),np.arange(600,5000,15),np.arange(5000,cfg['solar_horizon_km']*1000+1,60)]
        for az in range(0,360,2):
            rad=math.radians(az-convergence);sky=0.
            for d in distances:
                x,y=s['x']+d*math.sin(rad),s['y']+d*math.cos(rad)
                z=elevation(dem,meta,x,y)
                if not np.isfinite(z):z=elevation(regional,rm,x,y)
                if np.isfinite(z):sky=max(sky,math.degrees(math.atan2(z-s['z']-2-d*d/(2*6371000),d)))
            horizon.append(sky)
        windows={};all_totals=[];dec=None
        orientations=[(a,t) for a in range(100,261,5) for t in range(10,86,5)]
        aa,tt=np.radians(np.array(orientations).T)
        normals=np.column_stack((np.sin(aa)*np.sin(tt),np.cos(aa)*np.sin(tt),np.cos(tt)))
        for m in cfg['winter_months']:
            year=2026 if m>=11 else 2027
            day=21 if m==12 else 15
            date=datetime(year,m,day,tzinfo=tz)
            vectors=[];altitudes=[];visible=[];periods=[];current=[]
            for t in range(0,24*60,5):
                local=date+timedelta(minutes=t)
                az,alt=solar_position(local.astimezone(timezone.utc),lon,lat)
                if alt<=0:continue
                hz=np.interp(az,list(range(0,361,2)),horizon+[horizon[0]])
                ok=alt>hz
                if ok:current.append(local.strftime('%H:%M'))
                elif current:periods.append(current);current=[]
                a,b=math.radians(az),math.radians(alt)
                vectors.append([math.cos(b)*math.sin(a),math.cos(b)*math.cos(a),math.sin(b)])
                altitudes.append(alt);visible.append(ok)
            if current:periods.append(current)
            key=date.strftime('%b %d')
            windows[key]=', '.join(f'{p[0]}-{p[-1]}' for p in periods) or 'none'
            mon=calendar.month_abbr[m].upper()
            # Distribute monthly mean daily DNI over the representative day's daylight.
            # Atmospheric weighting attenuates low sun. Isotropic diffuse includes sky-view reduction.
            scale=np.exp(-.14/np.maximum(.02,np.sin(np.radians(altitudes))))
            beam=np.maximum(0,np.array(vectors)@normals.T)
            direct=(scale*np.array(visible))@beam/scale.sum()*climatology['ALLSKY_SFC_SW_DNI'][mon]
            diffuse=(1+np.cos(tt))/2*np.mean(np.cos(np.radians(horizon))**2)*climatology['ALLSKY_SFC_SW_DIFF'][mon]
            total=direct+diffuse
            all_totals.append(total*calendar.monthrange(year,m)[1])
            if m==12:dec=total
        total=np.sum(all_totals,axis=0)
        best=int(np.argmax(total));db=int(np.argmax(dec))
        s['solar']=dict(az=orientations[best][0],tilt=orientations[best][1],dec_az=orientations[db][0],dec_tilt=orientations[db][1],
                        dec_gain=round((dec[db]/dec[best]-1)*100,1),windows=windows,horizon=horizon)


def valley(sites,ids,cfg,dem,meta,wav,radius):
    data=[]
    for name,lon,lat in cfg['valley_sectors']:
        x,y=forward.transform(lon,lat)
        for code in ('AV','AM'):
            s=sites[ids.index(code)]
            origin=np.array([s['x'],s['y'],s['z']+s['h']])
            hits=0;best=None
            for dx in (-500,0,500):
                for dy in (-500,0,500):
                    end=np.array([x+dx,y+dy,elevation(dem,meta,x+dx,y+dy)+4])
                    c,f,_=ray(dem,meta,origin,end,20,wav,radius)
                    hits+=int(c>=0)
                    if best is None or f>best:best=f
            data.append(dict(sector=name,angel=code,clear=hits,of=9,best_f1=round(best,2),km=round(math.hypot(x-s['x'],y-s['y'])/1000,1)))
    return data
