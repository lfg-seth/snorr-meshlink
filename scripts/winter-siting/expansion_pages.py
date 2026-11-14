"""Lee-side gap comparison, navigable test stops and channel-load field card."""
import xml.etree.ElementTree as ET
import numpy as np
from shapely.geometry import Point
from shapely.ops import unary_union,linemerge
from matplotlib.collections import LineCollection
from cartography import plt,finish,frame,label,INK,TEAL,RED,features
from terrain import inverse
from field_names import field_name,field_code,navigation_name
from briefing import legend,coord

OLD='#748888'
FIRST='#126795'
SECOND='#bf6a08'
NAMES=('SR 156','Macks Canyon')


def stage(p):
    if p['status']=='reachable':return 0
    if p['with_eleven']:return 1
    if p['with_twelve']:return 2
    return 3


def field_stops(m,segments=None):
    """Use interior points of the longest contiguous run in each field-test class."""
    stops={}
    for name,idx,code in [('SR 156',0,'C'),('SR 156',1,'A'),('Macks Canyon',2,'B'),('Macks Canyon',3,'D')]:
        lines=[g for g,p in (segments if segments is not None else m.status) if p['name']==name and stage(p)==idx]
        if not lines:continue
        merged=unary_union(lines)
        if merged.geom_type=='MultiLineString':merged=linemerge(merged)
        longest=max(getattr(merged,'geoms',[merged]),key=lambda g:g.length)
        stops[code]=longest.interpolate(.5,normalized=True)
    return stops


def gain_map(m,sites,stops,segments=None):
    fig,ax=plt.subplots(figsize=(8.7,5.6))
    if segments is None:segments=[(g,p) for g,p in m.status if p['name'] in NAMES]
    b=unary_union([g for g,_ in segments]+[Point(m.sites[k]['x'],m.sites[k]['y']) for k in [*sites,'SI','GL']]).bounds
    extent=frame(b,.085)
    width=max(extent[1]-extent[0],1.35*(extent[3]-extent[2]))
    center=(extent[0]+extent[1])/2
    extent[:2]=[center-width/2,center+width/2]
    m.base(ax,extent)
    for idx,color,w in [(0,OLD,3.5),(3,RED,4.0),(1,FIRST,5.1),(2,SECOND,5.1)]:
        lines=[np.asarray(g.coords) for g,p in segments if stage(p)==idx]
        ax.add_collection(LineCollection(lines,colors=color,linewidths=w,zorder=5,capstyle='butt'))
    for k,name,off,color,marker in [('SI','10  Sisters',(-8,7),INK,'^'),('GL','Lee Fire Station',(-8,-1),INK,'D'),
                                    (sites[0],'11  '+field_name(sites[0]),(9,-8),FIRST,'^'),
                                    (sites[1],'12  '+field_name(sites[1]),(-9,9),SECOND,'^')]:
        s=m.sites[k];ax.scatter(s['x'],s['y'],s=70,marker=marker,fc=color,ec='white',lw=1.2,zorder=8)
        label(ax,s['x'],s['y'],name,off,10.1,color)
    m.labels_roads(ax,('SR 156','Macks Canyon','SR 158'))
    for code,pt in stops.items():
        ax.scatter(pt.x,pt.y,s=110,fc='white',ec=INK,lw=1.0,zorder=9)
        ax.text(pt.x,pt.y,code,ha='center',va='center',fontsize=8,weight='bold',color=INK,zorder=10)
    m.scale(ax);fig.subplots_adjust(left=.015,right=.985,top=.99,bottom=.01)
    return finish(fig)


def trial_nav(m,sites,stops,winter_stops):
    ns='http://www.topografix.com/GPX/1/1'
    tree=ET.Element('gpx',version='1.1',creator='SNORR MeshLink',xmlns=ns)
    def waypoint(ll,name,text):
        lon,lat=ll;w=ET.SubElement(tree,'wpt',lat=f'{lat:.7f}',lon=f'{lon:.7f}')
        ET.SubElement(w,'name').text=name;ET.SubElement(w,'desc').text=text
    for i,k in enumerate(sites,11):
        s=m.sites[k];waypoint(s['ll'],f'Trial {i} - '+navigation_name(k),'Temporary 4 m mount. Verify terrain path and paired channel-load measurements.')
        waypoint(s['stop_ll'],f'Trial {i} - stage',s['stop']+'. '+s['stop_evidence'])
    e=m.r['expansion']
    winter=e['access_pair']['sites']
    for i,k in enumerate(winter,11):
        s=m.sites[k]
        waypoint(s['ll'],f'Winter {i} - '+navigation_name(k),'First winter trial. Temporary 4 m mount.')
        waypoint(s['stop_ll'],f'Winter {i} - stage',s['stop']+'. '+s['stop_evidence'])
    alternatives=e['strict_pair']['sites']
    for k in alternatives:
        if k in sites or k in winter:continue
        s=m.sites[k]
        waypoint(s['ll'],'Alternate - '+navigation_name(k),'Alternative mount; do not add to the 12-site layout.')
        waypoint(s['stop_ll'],'Alternate stage - '+field_code(k),s['stop']+'. '+s['stop_evidence'])
    meanings={'A':'SR 156 gain at 11','B':'Macks Canyon gain at 12','C':'SR 156 served control','D':'Macks Canyon remaining gap'}
    for code,p in stops.items():
        waypoint(inverse.transform(p.x,p.y),code+' - '+meanings[code],'Road reference. Find a safe nearby stop and record actual position.')
    for code,source in [('E','A'),('F','B')]:
        p=winter_stops[source]
        waypoint(inverse.transform(p.x,p.y),code+' - winter '+meanings[source],'Road reference for the shorter-carry pair. Record actual parked position.')
    ET.ElementTree(tree).write(m.root/'expansion-trials.gpx',encoding='utf-8',xml_declaration=True)


def channel_page(b):
    b.begin('Expansion decision  /  radio load','Will fresh GPS still reach dispatch?',
            'Compare the same member traffic with ten, eleven and twelve repeaters. A station can have a clear terrain path while forwarded copies or other traffic delay the next GPS update.')
    fig,ax=plt.subplots(figsize=(8.7,2.8))
    for j,n in enumerate((10,11,12)):
        rates=(20/2+n*4/3)/60
        low,high=100*rates*.559,100*rates*.764
        ax.barh(j,low,color='#cbdcd7',height=.46)
        ax.barh(j,high-low,left=low,color='#33867b',height=.46)
        ax.text(high+.4,j,f'{low:.1f}–{high:.1f}%',va='center',weight='bold',fontsize=11,color=INK)
    ax.axvline(25,ls='--',lw=1.1,c='#8e672d')
    ax.set_xlim(0,40);ax.set_yticks([0,1,2],['10 repeaters','11 repeaters','12 repeaters'])
    ax.invert_yaxis();ax.set_xticks([0,10,20,25,30,40],['0%','10%','20%','25%','30%','40%'])
    ax.set_xlabel('Illustrative airtime for original packets in one shared radio area',fontsize=9)
    for sp in ax.spines.values():sp.set_visible(False)
    ax.tick_params(length=0,colors=INK);fig.tight_layout(pad=.4)
    b.image(finish(fig),146)
    b.p('Assumptions: 20 moving trackers send once per 120 s. Each fitted repeater originates up to four reports per 180 s. Using 40–70 total on-air bytes gives 0.559–0.764 s per frame at LongFast. Each extra radio adds 1.2–1.7 percentage points for its own reports. One extra forwarded copy of every GPS report adds another 9.3–12.7 points wherever all copies can be heard.',9.6,5)
    b.p('The dashed line marks the firmware’s 25% polite-utilization check. Actual message sizes, admission, jitter, forwarding, other users and spatial separation change local load. The existing three-minute bench capture saw 10 receptions from 3 distinct packets. Its final 60-second window was 10.27% received airtime. Mountain capacity is unmeasured.',9.4,7)
    b.h('Run matched laps with one change at a time')
    b.p('At Lee Fire Station log RF receipts and uploads. Monitor the busiest relay and the Kyle control station. Use the same radios, antenna positions, moving-member count, packet interval, route and hop settings. Run 10 → 11 → 10, then 11 → 12 → 11. Allow at least 30 minutes per state and repeat a matched cycle during representative busy traffic.',10,5)
    b.p('Use E and F for the shorter winter approaches, or A and B for the ridge pair. Count distinct GPS IDs that reach dispatch out of the IDs actually emitted. At C and a served Kyle control stop, compare that fraction, 95th-percentile GPS age, updates older than 15 minutes, queue drops, copies per unique packet and time above the polite-utilization check. Separate station RF receipt from MQTT arrival.',10,5)
    b.h('Keep an addition only after the paired runs agree')
    b.p('Require repeatable new dispatch receipts in the intended gap. The existing routes must retain delivery and GPS freshness within the variation of the two surrounding control runs, without a repeatable rise in drops or stale tracks. If the load was too light, counts too small, or repeats disagree, keep the lower count and rerun.',10,5)
    b.p('Sources: R001 commissioning profile, member GPS cadence study, direct-hop airtime calculation, dedicated airtime-sniffer capture and firmware airtime.h. Meshtastic managed flooding is listed on the sources page.',8.5,4)
    b.end()


def expansion_pages(b,m,r,cfg):
    e=r['expansion'];one=e['step_one'];two=e['pair'];sites=two['sites']
    stops=field_stops(m);winter_lines=features(m.root,'winter-trial-roads')
    winter_stops=field_stops(m,winter_lines);trial_nav(m,sites,stops,winter_stops)
    b.begin('Lee Canyon  /  greatest terrain gain','Which gaps do two more radios fill?',
            'Sisters occupies slot 10. Adding it to the previous nine recovers zero road metres on SR 156 or Macks Canyon. These ridge sites offer the largest modeled gain. Page 6 maps the first winter trial, with shorter carries.')
    b.image(gain_map(m,sites,stops),335)
    legend(b,[('Reachable with ten',OLD,'line'),('Gained with 11',FIRST,'line'),('Gained with 12',SECOND,'line'),('Blind with 12',RED,'line')])
    rows=[]
    for name in NAMES:
        d=r['addition']['roads'][name];g=d['new_gap']
        cells=[f"{r['scenarios']['Recommended'][name]:.1f}%  /  {g['km']:.2f} km"]
        for step in (one,two):
            v=step['corridors'][name];cells.append(f"{v['reachable_pct']:.1f}%  /  {v['gap_km']:.2f} km")
        rows.append([name]+cells)
    b.table(['Reach / longest blind run','9 or 10 repeaters','11 repeaters','12 repeaters'],rows,[152,130,130,128],9.1)
    b.p('A and B mark predicted gains. C is an already-served control and D is a remaining blind stretch. Each marker is a road reference for the field test. Reach means a 1.2 m member antenna has a modeled path to either station within the three-forwarder limit.',9.6,5)
    b.p(f"Across the two routes, the trial pair gains {two['lee_road_gain_km']:.2f} km. The full former {r['addition']['roads']['SR 156']['old_gap']['km']:.2f} km SR 156 gap is recovered. Macks Canyon gains {two['corridors']['Macks Canyon']['former_gap_recovered_km']:.2f} km within its former longest gap.",9.7,5)
    if 'sisters_marginal' in two:
        marginal=two['sisters_marginal']
        b.h('What Sisters contributes once it has a path')
        b.p(f"Once site 11 is on, Sisters can forward through it to Lee. In the twelve-site layout, Sisters itself adds {marginal['land_km2']:.1f} km² of reachable land and {marginal['trail_km']:.2f} km of named trail. The two expansion mounts supply the road gains.",9.8,5)
    b.end()
    b.begin('Temporary relays  /  radio paths','Test the paths into Lee Fire Station',
            'Use the supplied Sisters replacement pin. At 4 m its direct ray to the 1 m station passes 5.2 m below terrain. Via Champion or Angel Peak Mountain Side it needs a fourth forwarder. Raising Sisters alone to 7 m leaves both road scores unchanged.')
    a,z=sites
    chains=[('SI',a,False),(z,a,False),(a,'GL',False),('SI','GL',True)]
    b.image(m.location_image(['SI',a,z,'GL'],chains),163)
    legend(b,[('Terrain-clear radio path',TEAL,'line'),('Blocked direct ray',RED,'dash')])
    for idx,k in enumerate(sites,11):
        s=m.sites[k];sol=s['solar'];sequence=two['paths'][k]
        b.h(f'{idx}   {navigation_name(k)}   →   '+field_name(sequence[1]))
        b.p('Mount '+coord(s['ll'])+' at 4 m AGL. Stage '+coord(s['stop_ll'])+
            f". One-way estimate {s['walk_m']/1000:.2f} km, +{s['ascent_m']} m ({s['approach']}). Winter solar {sol['az']}° true, tilt {sol['tilt']}°. Scout the actual winter approach before carrying a relay.",9.4,4)
        if idx==11:
            b.p('Establish ten paced, numbered reports from the trial mount to Lee. Then send from Sisters with this relay active and silent. From stop A, send fresh GPS fixes and match IDs at Lee and dispatch.',9.6,5)
        else:
            p=next(v for v in r['pairs'] if {v['a'],v['b']}=={z,a})
            b.p(f"The {p['length_m']/1000:.2f} km link back to {field_code(a)} clears bare earth by only {p['clear_m']:.1f} m. Its tightest first-Fresnel clearance is {100*p['f1']:.0f}%. Compare IDs at {field_code(a)}, Lee and dispatch, then repeat from B with site 12 silent. Expect D to remain difficult.",9.6,5)
    best=e['best_single'];alternative=field_name(best['sites'][0]);strict=e.get('strict_pair')
    b.p(f"With only one extra slot, {alternative} gives {best['corridors']['SR 156']['reachable_pct']:.1f}% on SR 156 and {best['corridors']['Macks Canyon']['reachable_pct']:.1f}% on Macks. The two-site sequence uses {field_name(a)} to connect both proposed paths.",9.3,4)
    if strict:
        b.p('Requiring 60% first-Fresnel clearance on every new link changes the best pair to '+
            ' and '.join(map(field_name,strict['sites']))+f", adding {strict['lee_road_gain_km']:.2f} km across both roads. Winter access, trees and packet delivery determine which is practical.",9.2,4)
    if 'access_pair' in e:
        b.p('The modeled Lee Meadows East climb exceeds Fletcher’s ascent and the Macks North Ridge carry exceeds Fletcher’s distance. Use the shorter winter approaches on the next page first unless a better agency route is confirmed.',9.1,4)
    b.p('First measure the Lee antenna. The model’s first direct Sisters link appears at a 9 m station height. With that height and ten repeaters, SR 156 reaches 85.1% and Macks stays at 28.6%. If the installed antenna is near 9 m, test Sisters directly before hauling a ridge relay.',9.2,4)
    b.end()
    practical_page(b,m,e,winter_stops,winter_lines)
    channel_page(b)


def practical_page(b,m,e,stops,lines):
    opt=e['access_pair'];first,second=opt['sites'];one=e['access_step'];ref=e['access_reference']
    b.begin('Winter access  /  first field choice','Try the shorter winter approaches first',
            f"These mounts fit within Fletcher’s modeled one-way {ref['walk_m']/1000:.1f} km and +{ref['ascent_m']} m carry. Every new relay link passes the 60% first-Fresnel clearance test. The original ten sites stay fixed.")
    b.image(gain_map(m,opt['sites'],{'E':stops['A'],'F':stops['B'],'C':stops['C']},lines),340)
    legend(b,[('Reachable with ten',OLD,'line'),('Gained with 11',FIRST,'line'),('Gained with 12',SECOND,'line'),('Blind with 12',RED,'line')])
    for i,k,trial,stop in [(11,first,one,'E'),(12,second,opt,'F')]:
        site=m.sites[k];chain=' → '.join(field_code(x) for x in trial['paths'][k])
        b.h(f'{i}   {navigation_name(k)}     /     {chain}')
        b.p(f"Mount {coord(site['ll'])} at 4 m. Stage {coord(site['stop_ll'])}. Estimated one-way approach {site['walk_m']/1000:.2f} km and +{site['ascent_m']} m. Verify the route on foot. From {stop}, send ten paced GPS packets and match IDs at Lee and dispatch with the trial radio active, then silent.",9.7,5)
    sr,mc=[opt['corridors'][k] for k in NAMES]
    b.p(f"With both sites, SR 156 reaches {sr['reachable_pct']:.1f}% (longest gap {sr['gap_km']:.2f} km). Macks reaches {mc['reachable_pct']:.1f}% (longest gap {mc['gap_km']:.2f} km). Site 11 also connects Sisters to Lee. If site 12 cannot reproduce the F gain under load, stop at eleven.",10,4)
    b.p('Use the “Winter 11” and “Winter 12” mounts and staging points in the trial GPX. E and F are the drive references for this layout. At C, check that deliveries on an already-served road hold up during both stages.',9.3,4)
    b.end()
