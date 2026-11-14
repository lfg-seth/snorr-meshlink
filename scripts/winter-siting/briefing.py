"""The map-led presentation and field-test section of the winter packet."""
from pathlib import Path
import math
import numpy as np
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from cartography import INK,TEAL,GOLD,RED,BLANK,MUTE,SITE_COLORS,SHARED,finish,plt
from field_names import field_name,field_code
from terrain import load_dem
from native import Profiles


def cover(b,m):
    c=b.c;b.n+=1;c.bookmarkPage('cover');c.addOutlineEntry('Mount Charleston winter field packet','cover')
    c.setFillColor(HexColor('#f7f6ef'));c.rect(0,0,612,792,fill=1,stroke=0)
    logo=Path(__file__).resolve().parents[2]/'portal/src/assets/snorr-logo.png'
    if logo.is_file():c.drawImage(str(logo),39,712,117,44,preserveAspectRatio=True,mask='auto')
    b.text(398,737,'M E S H L I N K    /    F I E L D  O P S',9,b.bold,INK)
    c.setStrokeColor(HexColor('#a7b4a9'));c.line(40,690,572,690)
    b.text(40,653,'SPRING MOUNTAINS, NEVADA',12,b.bold,TEAL)
    b.text(38,590,'Mount Charleston',48,b.serif,INK)
    b.text(40,547,'Winter mesh field plan',28,b.font,INK)
    b.text(40,502,'Passive GPS tracking • Repeater siting and field validation',13,b.font,MUTE)
    img=ImageReader(m.cover_art());w,h=img.getSize()
    # Fill the band with the actual terrain without stretching either map axis.
    c.saveState();clip=c.beginPath();clip.rect(0,119,612,348);c.clipPath(clip,stroke=0)
    scale=max(612/w,348/h);c.drawImage(img,(612-w*scale)/2,119+(348-h*scale)/2,w*scale,h*scale)
    c.restoreState()
    c.setFillColor(HexColor(INK));c.rect(0,0,612,119,fill=1,stroke=0)
    b.text(40,79,'WINTER 2026–27',12,b.bold,'#fcf8e9')
    b.text(40,53,'Nine repeaters   /   Two fire-station gateways',13,b.font,'#e4eee5')
    b.text(40,29,'Private planning copy     •     Terrain model dated 13 November 2026',9,b.font,'#c1d4ca')
    c.showPage()


def legend(b,items):
    """Shape and fill are repeated using exactly the map's symbols."""
    x=36;y=b.y-8
    for text,color,kind in items:
        width=b.c.stringWidth(text,b.font,9.1)+32
        if x+width>580:x=36;y-=20
        c=b.c;c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(color))
        if kind in ('line','dash'):
            c.saveState();c.setLineWidth(2.5)
            if kind=='dash':c.setDash(4,2)
            c.line(x,y+2,x+13,y+2);c.restoreState()
        elif kind=='point':c.circle(x+6,y+2,3.7,stroke=1,fill=0)
        elif kind in ('triangle','diamond'):
            path=c.beginPath();xy=([(x,y-2),(x+6,y+7),(x+12,y-2)] if kind=='triangle' else [(x+1,y+2),(x+6,y+7),(x+11,y+2),(x+6,y-3)])
            path.moveTo(*xy[0])
            for pt in xy[1:]:path.lineTo(*pt)
            path.close();c.drawPath(path,stroke=0,fill=1)
        else:
            c.setStrokeColor(HexColor('#9ca9a3'));c.rect(x,y-3,13,10,stroke=1,fill=1)
        b.text(x+18,y-2,text,9.1,b.font,INK);x+=width
    b.y=y-17


STATIONS=[('Repeater',INK,'triangle'),('Fire-station gateway',INK,'diamond')]
REACH=[('Blind or disconnected',BLANK,'fill'),('Lost in at least one outage',GOLD,'fill'),('Survives every single outage',TEAL,'fill')]
ROADS=[('Blind stretch',RED,'line'),('Reachable, vulnerable',GOLD,'line'),('Survives all single outages',TEAL,'line')]

def flag(b,title,detail):
    b.c.setStrokeColor(HexColor('#bacac3'));b.c.line(36,b.y,576,b.y)
    b.y-=8;b.h(title);b.p(detail,10.3,10)

def field_log(b,columns):
    b.h('Field notes')
    y=b.y
    for index,heading in enumerate(columns):
        x=36+index*180
        b.text(x,y-9,heading,9,b.bold,MUTE)
        b.c.setStrokeColor(HexColor('#94a6a1'));b.c.line(x,y-26,x+166,y-26)
    b.y-=40

def tests(b,m):
    b.begin('Field sequence  /  Lee Canyon','Start at Lee Fire Station',
            'Bring the station receiver, a known-good member radio, two temporary relays and a way to read per-gateway packet IDs. Establish the direct link before testing the chain.')
    keys=['LC','LF','GL'];edges=[('LC','LF',False),('LF','GL',False),('LC','GL',True)]
    b.image(m.location_image(keys,edges),195)
    legend(b,[('Modeled clear link',TEAL,'line'),('Terrain blocks the direct path',RED,'dash')])
    b.h('1   Lower Bristlecone (LB)  →  Lee Fire Station (LFS)')
    b.p('Put the transmitter at the proposed Lower Bristlecone tree, 4 m above ground. Measure the station antenna and test the 1 m planning height. Send ten paced, numbered payloads. Expect matching IDs at Lee and corresponding gateway uploads. If RF arrives without an upload, check station Wi-Fi and MQTT first.')
    b.h('2   Lee Junction (LJ)  →  Lower Bristlecone  →  Lee Fire Station')
    b.p('At Lee Junction, send from the planned 4 m antenna. Compare a run with Lower Bristlecone relaying against a run with that relay silent. Keep other relays out of the controlled test. Expect Lee receipts with the relay active and fewer or none when silent. If the chain fails, repeat at 7 m or try an adjacent mount before relying on it.')
    b.p('At a safe off-road stop, repeat a member GPS packet on person, in the cabin and with the roof antenna. Record fix time, send time, ID, RF receipt and dispatch arrival separately. The project marks a GPS position stale at 15 minutes.',9.4)
    field_log(b,['Station antenna AGL','Test 1  /  station RF and uploads','Test 2  /  relay on and off'])
    b.end()
    b.begin('Field sequence  /  Kyle Canyon','Prove the Cathedral relay',
            'This test decides whether the high-value Kyle branch is maintainable. Confirm the upper approach and actual mounting surface before sending a crew up Fletcher.')
    b.image(m.location_image(['FL','CH','CL','GK'],[('FL','CH',False),('FL','CL',True),('CH','GK',False)]),194)
    legend(b,[('Modeled clear link',TEAL,'line'),('Terrain-blocked comparison',RED,'dash')])
    b.h('3   Fletcher (FL)  →  Upper Cathedral (UC)  →  Kyle Fire Station (KFS)')
    b.p('First establish Upper Cathedral to Kyle at 4 m and 1 m. Then transmit ten numbered packets from Fletcher at 4 m with Upper Cathedral as the sole forwarding relay. Record Fletcher IDs heard at Cathedral and uploaded at Kyle. Repeat with the relay silent to check the dependency.')
    b.h('Repeat from Lower Cathedral (LC)')
    b.p('Keep the Fletcher transmitter, Kyle receiver, payload cadence and antenna heights fixed. Move only the intermediate radio. The model predicts a blocked Fletcher-to-Lower Cathedral path. Repeatable lower-site receipts justify testing its easier access; loss of the upper approach triggers the upper-site-unavailable layout.')
    b.p('For both canyon tests, log attempted and received IDs, RSSI/SNR, antenna heights, snow and obstructions. Ten attempts diagnose a link; revisit the same configuration on another day before treating it as reliable.',9.4)
    field_log(b,['Upper site access / AGL','Upper relay  /  Kyle uploads','Lower relay  /  Kyle uploads'])
    b.end()

def cover_chart(b,m,r):
    colors=[('#8b9e9a','Stations only','Direct'),('#648499','Starting seven','Starting / lower'),
            (TEAL,'Recommended nine','Recommended'),('#ae7721','Survives any one loss','Survives every single loss')]
    b.begin('Coverage comparison','What the repeaters add','Each bar shows the share of the same measured road network, trail network or land area that can send a GPS packet to a station. Each group has its own denominator.')
    b.image(m.comparison_maps(),142)
    legend(b,[('Member can reach a gateway',TEAL,'fill'),('Outside that reach',BLANK,'fill'),STATIONS[1]])
    for title,key,unit in [('Roads','road_km','km'),('Named trails','trail_km','km'),('Mountain land','land_km2','km²')]:
        total=r['total'][key];b.h(f'{title}   /   {total:.1f} {unit} scored')
        for color,name,scenario in colors:
            val=r['scenarios'][scenario][key];pct=val/total
            y=b.y-11;b.text(37,y,name,10,b.font)
            b.c.setFillColor(HexColor(BLANK));b.c.rect(190,y,254,8,stroke=0,fill=1)
            b.c.setFillColor(HexColor(color));b.c.rect(190,y,254*pct,8,stroke=0,fill=1)
            b.text(454,y,f'{val:.1f} {unit}  ·  {pct:.0%}',10,b.bold)
            b.y-=18
        b.y-=4
    b.p('The nine-radio layout gives roughly three quarters of scored road length a path in the intact network. Most of those roads still depend on a particular relay or station. The outage maps show which terrain loses that path.',10.2)
    b.end()

def road_pages(b,m,r):
    b.begin('Field sequence  /  gap checks','Two road gaps to drive first','Both road traces are north-up. Red sections are predicted blind. A and B bracket the longest continuous blind stretch on each road. A mapped endpoint is a test reference; choose a safe stop nearby.')
    b.image(m.corridors(['Macks Canyon','Lucky Strike']),234);legend(b,ROADS)
    for title,name,instruction in [
        ('4   Upper Macks Canyon','Macks Canyon','Enter from SR 156. Start on a reachable segment near the road mouth, check both sides of A and continue toward the upper terminus B only if passable.'),
        ('5   Lucky Strike east branch','Lucky Strike','Work from authorized vehicle stops on the east branch. Check both ends and a mid-gap location. Record which gateway hears each packet before comparing the Lucky Strike and Angel placements.')]:
        g=r['roads'][name][0];b.h(f"{title}   /   {g['km']:.2f} km")
        b.p(instruction+' Send from the 1.2 m member baseline. Expect receipts to drop across the red stretch; repeated delivery inside it would change the placement score.',9.8,5)
        b.p('A  '+coord(g['a'])+'     •     B  '+coord(g['b']),9,9)
    b.end()
    b.begin('Highway coverage','Where each highway loses the mesh','Follow each highway from A to B. The endpoints are the study limits. Each close-up uses its own scale and keeps north at the top.')
    for name in ('SR 156','SR 157','SR 158'):
        fig,(ax,info)=plt.subplots(1,2,figsize=(8.4,2),gridspec_kw={'width_ratios':[1.45,1]})
        m.corridor(ax,name,ends=True)
        info.axis('off')
        desc={'SR 156':'Lee Canyon Road','SR 157':'Kyle Canyon Road','SR 158':'Deer Creek Road'}[name]
        info.text(.02,.84,f'{name}   /   {desc}',fontsize=12,weight='bold',color=INK)
        value=r['scenarios']['Recommended'][name];gap=r['roads'][name][0]
        info.text(.02,.59,f'{value:.0f}% reachable',fontsize=14,weight='bold',color=TEAL)
        info.text(.02,.40,f"Longest blind stretch   {gap['km']:.2f} km",fontsize=10,color=INK)
        for i,p in enumerate(r['highways'][name]):
            info.text(.02,.22-i*.15,f"{'AB'[i]}    {coord(p)}",fontsize=9.7,color=MUTE)
        fig.tight_layout(pad=.2);b.image(finish(fig),133)
    legend(b,ROADS);b.p('Gaps are measured along road centerlines using samples no farther than 40 m apart. Champion Road has no blind midpoint in the intact model; it can still lose its uplink during an outage.',9.4);b.end()

def coord(ll):return f'{ll[1]:.5f}, {ll[0]:.5f}'

def briefing_pages(b,m,r,cfg):
    order=r['selected'];safe=r['scenarios']['Survives every single loss'];rec=r['scenarios']['Recommended']
    b.begin('Deployment plan','Start on the Lee side','Survey both station antenna bases. Build Lower Bristlecone and Lee Junction first, then prove the Fletcher–Cathedral path before committing the other Kyle-side radios.')
    b.image(m.overview('deployment'),361);legend(b,STATIONS+[('Modeled relay chain',TEAL,'line'),('Priority blind stretch',RED,'line')])
    b.h('Deployment order')
    for i in range(0,len(order),3):
        for j,k in enumerate(order[i:i+3]):
            x=36+180*j
            b.text(x,b.y-10,str(i+j+1).zfill(2),10,b.bold,TEAL)
            b.text(x+22,b.y-10,f'{field_name(k)} ({field_code(k)})',10.6,b.bold)
        b.y-=20
    b.p('The first two repeaters bring modeled SR 156 reach from 10% to 76%. Upper Macks Canyon remains a priority blind stretch. Read the three field-test pages next before carrying equipment to a permanent mount.',9.8)
    b.end()
    tests(b,m)
    road_pages(b,m,r)
    b.begin('Terrain visibility','Where a member can see a radio','Green land has a modeled clear terrain ray between a 1.2 m member antenna and at least one of the eleven infrastructure antennas. The next map checks whether that radio can forward the packet.')
    b.image(m.overview('union'),419);legend(b,[('Antenna visible','#72bca9','fill'),('Terrain blocks all eleven',BLANK,'fill')]+STATIONS)
    code_key(b,order,r['gateways']);b.end()
    b.begin('Station reachability','Can the packet reach dispatch?','Read the land color at the member’s position. A route must reach an operating fire-station gateway within three forwarding repeaters. Station internet service is assumed available.')
    b.image(m.overview('reach'),420);legend(b,REACH);legend(b,STATIONS)
    b.p(f"With all radios working, {rec['road_km']:.1f} km of scored road can reach a station. Only {safe['road_km']:.1f} km keep a route through every single outage tested. Amber includes locations with two visible radios that share the same downstream relay.",10.1)
    b.end()
    b.begin('Station destinations','Which fire station gets the packet?','Each color names the station that a member can reach with all nine repeaters operating. A member can reach either station from the dark teal land. Routes to the two stations can share a repeater.')
    station_image,mask=m.station_image(cfg['hop_limit']);b.image(station_image,410)
    legend(b,[('Neither',BLANK,'fill'),('Kyle only','#9e83b6','fill'),('Lee only','#77b6c9','fill'),('Either station',TEAL,'fill'),STATIONS[1]])
    area_per_cell=cfg['area_pixel_m']**2/1e6
    kms=[np.count_nonzero(mask==i)*area_per_cell for i in (1,2,3)]
    b.p(f'Within the scored area, {kms[0]:.1f} km² reach Kyle alone, {kms[1]:.1f} km² reach Lee alone and {kms[2]:.1f} km² have a modeled path to both. The previous map tests whether a route remains after each individual failure.',10.3,6)
    b.end()
    b.begin('Repeater footprints','Where each repeater stands alone','Each site color identifies land visible to that repeater alone. Slate shows land visible to two or more repeaters. Use the individual footprints on the next page to see which radios overlap there.')
    b.image(m.overview('overlap'),403)
    legend(b,[('No repeater visible',BLANK,'fill'),('Two or more repeaters visible',SHARED,'fill'),STATIONS[0]])
    for i in range(0,len(order),3):
        row=order[i:i+3]
        for j,k in enumerate(row):
            x=36+j*180;b.c.setFillColor(HexColor(SITE_COLORS[i+j]));b.c.rect(x,b.y-9,11,9,fill=1,stroke=0)
            b.text(x+17,b.y-9,field_name(k)+' ('+field_code(k)+')',9.4)
        b.y-=17
    b.end()
    b.begin('Repeater footprints','Which repeater covers which slope?','All nine panels use the same north-up frame and scale. Green shows one repeater’s complete footprint. The triangle marks its mount. Road length below each panel counts individual visibility.')
    b.image(m.mini_grid('foot',order),503)
    legend(b,[('Visible to this repeater','#4a9f8f','fill'),('Outside its footprint',BLANK,'fill'),('Selected mount',INK,'triangle')])
    b.p('Compare Lower Bristlecone with Lee Junction, then compare Fletcher with Upper Cathedral. The different canyon-facing footprints explain why these radios work in pairs.',10)
    b.end();cover_chart(b,m,r)
    b.begin('Route coverage','Which routes keep a gateway path?','The road and trail panels share the same extent. Follow the line color along a route. A member can have service at a trailhead and lose the gateway path after crossing the next ridge.')
    b.image(m.road_trail_image(),278);legend(b,ROADS)
    b.h('Follow a route from a known starting point')
    b.p('Upper Macks Canyon and the east end of Lucky Strike are the two red road stretches to check first. On the trail map, short red breaks separate otherwise reachable sections. The stations are marked with diamonds in both panels.')
    flag(b,'Read a gap at the scale of the measurement','Each short road or trail segment was scored at its midpoint, up to 40 m apart. The land maps score an 80 m grid. A segment can therefore differ from the land color behind it. Use the individual route results when planning a stop.')
    b.end()
    b.begin('Area guide','Where the named places sit','The numbered locations lead to the six detailed maps on the next page. The two red road stretches locate the priority drive tests in relation to the stations, highways and recreation areas.')
    b.image(m.area_guide(),391)
    legend(b,[('Campground boundary or ski run',TEAL,'line'),('Priority road gap',RED,'line'),STATIONS[1]])
    for i,n in enumerate(m.facility_names()):
        x=36+270*(i%2);y=b.y-12-22*(i//2)
        b.text(x,y,str(i+1),10.5,b.bold,TEAL);b.text(x+20,y,n.replace('Lee ski terrain','Lee Canyon ski terrain'),10.5)
    b.y-=74
    b.p('KFS marks Kyle Fire Station. LFS marks Lee Fire Station. The faint perimeter is the area used for land scoring.',9.4)
    b.end()
    b.begin('Facility coverage','Campgrounds and ski terrain','Black outlines trace the mapped campground boundaries. Black lines at the resort trace the scored ski runs. Each place has its own north-up map and scale.')
    b.image(m.facility_grid(),365);legend(b,REACH)
    b.h('Reading the percentages')
    b.p('Campground percentages count member-height samples inside the mapped footprint. Resort percentages use length along ski runs. The colors show the 80 m land grid, so a narrow campground can sample differently from its background cell.')
    b.p('McWilliams includes the former Dolomite loops. The Kyle Canyon campground outline also covers a location listed for day use. Access and seasonal closures are on the site sheets.')
    b.end();outages(b,m,r)

def code_key(b,order,gw):
    for i,k in enumerate(order+gw):
        x=36+180*(i%3);y=b.y-9-17*(i//3)
        b.text(x,y,field_code(k),9.5,b.bold,TEAL);b.text(x+27,y,field_name(k),9.3)
    b.y-=17*math.ceil((len(order)+len(gw))/3)+7

def solar_windows(b,sites,active):
    x0,x1=221,452
    def x_at(hour):
        return x0+(hour-6)*(x1-x0)/12
    def clock_time(value):
        h,m=map(int,value.split(':'))
        return h+m/60
    b.text(36,b.y-10,'Mount',9,b.bold)
    b.text(x0,b.y-10,'Direct sun on 21 December  /  PST',9,b.bold)
    b.text(466,b.y-10,'Face and tilt¹',9,b.bold)
    b.y-=26
    for tick in (6,9,12,15,18):
        b.text(x_at(tick)-6,b.y,f'{tick:02}',8,b.font,MUTE)
    b.y-=9
    for index,k in enumerate(active):
        y=b.y-10;solar=sites[k]['solar']
        b.text(36,y,field_name(k),9.4,b.font)
        b.c.setFillColor(HexColor(BLANK));b.c.rect(x0,y+1,x1-x0,6,fill=1,stroke=0)
        for interval in solar['windows']['Dec 21'].split(', '):
            if interval=='none':continue
            start,end=map(clock_time,interval.split('-'))
            b.c.setFillColor(HexColor('#b57d20'));b.c.rect(x_at(start),y+1,x_at(end)-x_at(start),6,fill=1,stroke=0)
        b.text(466,y,f"{solar['az']}°  /  {solar['tilt']}°",9.3)
        b.y-=15.5
    b.y-=7
    b.p('¹ Face is the November–April azimuth measured clockwise from true north. Tilt is measured up from horizontal. The individual sheets give the exact clock times for all six dates.',9.2,7)

def outages(b,m,r):
    active=sorted(m.active,key=lambda k:-r['failures'][k]['road_km']);worst=active[0]
    b.begin('Single-node failures','Where a single failure cuts service','Each panel removes one radio and searches again for a route. Red shows land that loses its last gateway path. Pale green land still reaches a station. Gray land was already outside the intact network.')
    b.image(m.mini_grid('loss',active[:4]),370)
    legend(b,[('Gateway path lost',RED,'fill'),('Still reachable','#a7cfc2','fill'),('Already unreachable',BLANK,'fill')])
    flag(b,field_name(worst)+' is the largest dependency',f"Removing it costs {r['failures'][worst]['road_km']:.1f} road km and {r['failures'][worst]['trail_km']:.1f} trail km. Compare its red area with Upper Cathedral’s. The two failure footprints overlap because the Fletcher route uses both.")
    b.p('Under the recorded receive-only gateway profile, a station backhaul outage has the same effect on remote dispatch as removing its radio. A powered station may still receive RF locally.',9.8)
    b.end()
    b.begin('Single-node failures','The other seven outage footprints','Read these panels at the same mountain extent. A small loss in the intact network can still matter because a repeater supplies an alternate route when another site fails.')
    b.image(m.mini_grid('loss',active[4:]),485)
    legend(b,[('Gateway path lost',RED,'fill'),('Still reachable','#a7cfc2','fill'),('Already unreachable',BLANK,'fill')])
    v=r['scenarios']['Resilience alternative'];alt=r['scenarios']['Alternative survives all'];rec=r['scenarios']['Recommended'];surv=r['scenarios']['Survives every single loss']
    b.p(f"The Lee Highway placement gives up {v['road_km']-rec['road_km']:.2f} km of intact road coverage to keep {surv['road_km']-alt['road_km']:.2f} km more road reachable through every single-node outage.",10.2);b.end()

def profile_pages(b,m,root,cfg,r):
    dem,meta=load_dem(root/'cache/terrain-local.tif')
    native=Profiles((root/'source').glob('USGS_1M*.tif'),dem,meta,299.792458/cfg['frequency_mhz'],6371000*cfg['effective_earth_k'])
    dst=root/'tables/profiles';dst.mkdir(exist_ok=True)
    sets=[('Kyle','FL','CH','CL','GK'),('Lee','LC','LF','GL',None)]
    for canyon,a,h,lo,g in sets:
        pairs=[(a,h),(a,lo),(h,g)] if g else [(a,h),(h,lo),(a,lo)]
        b.begin('Critical radio paths',canyon+' Canyon terrain profiles','Match the endpoint names to the locator. Each section runs from the first named site on the left to the second on the right. The horizontal axis measures distance along that link.')
        paths=[]
        for u,v in pairs:
            p=next(p for p in r['pairs'] if {p['a'],p['b']}=={u,v})
            paths.append((u,v,not p['los']))
        b.image(m.location_image(list(dict.fromkeys(i for p in pairs for i in p)),paths),158)
        legend(b,[('Clear terrain ray',TEAL,'line'),('Blocked direct ray',RED,'dash')])
        for u,v,blocked in paths:
            su,sv=m.sites[u],m.sites[v]
            dist,ground,line,f1=native.trace((su['x'],su['y'],su['h']),(sv['x'],sv['y'],sv['h']))
            np.savetxt(dst/(u+'-'+v+'.csv'),np.column_stack([dist,ground,line,f1]),delimiter=',',fmt='%.3f',header='distance_m,terrain_plus_bulge_m,radio_ray_m,first_fresnel_radius_m',comments='')
            clearance=line-ground;ix=np.argmin(clearance[1:-1])+1
            p=next(p for p in r['pairs'] if {p['a'],p['b']}=={u,v})
            b.p(f"{field_name(u)} ({field_code(u)}, {su['h']:g} m)  →  {field_name(v)} ({field_code(v)}, {sv['h']:g} m)   •   {dist[-1]/1000:.2f} km",9.4,1)
            fig,ax=plt.subplots(figsize=(8.2,1.43))
            ax.fill_between(dist/1000,ground,min(ground)-18,color='#ded1b9');ax.plot(dist/1000,ground,color='#756047',lw=1)
            ax.plot(dist/1000,line,color=TEAL,lw=1.6);ax.plot(dist/1000,line-.6*f1,color='#bd772c',lw=1.1,ls='--')
            ax.fill_between(dist/1000,line,ground,where=ground>line,color=RED,alpha=.68,interpolate=True)
            ax.scatter(dist[ix]/1000,line[ix],s=15,facecolor='white',edgecolor=INK,zorder=5)
            ax.set_xlim(0,dist[-1]/1000);ax.set_ylabel('m NAVD88',fontsize=8);ax.tick_params(labelsize=8,pad=1)
            ax.xaxis.set_major_formatter(lambda value,pos:f'{value:g} km')
            ax.grid(alpha=.15);fig.tight_layout(pad=.25);b.image(finish(fig),81)
            b.p(f"Minimum terrain clearance {p['clear_m']:+.1f} m at {dist[ix]/1000:.2f} km from {field_name(u)}. Minimum clearance / first Fresnel radius {p['f1']:.2f}.",8.6,5)
        legend(b,[('Terrain','#bba582','fill'),('Terrain above ray',RED,'fill'),('Radio ray',TEAL,'line'),
                  ('Lower 60% Fresnel envelope','#bd772c','dash'),('Least clearance',INK,'point')])
        b.end()
