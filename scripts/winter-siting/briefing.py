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
    b.text(40,53,'Ten planned repeaters   /   Two expansion trials   /   Two stations',13,b.font,'#e4eee5')
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
ROADS=[('Reaches a station',TEAL,'line'),('Predicted blind stretch',RED,'line')]

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
    keys=['LC','SK','GL'];edges=[('LC','SK',False),('SK','GL',False),('LC','GL',True)]
    b.image(m.location_image(keys,edges),195)
    legend(b,[('Modeled clear link',TEAL,'line'),('Terrain blocks the direct path',RED,'dash')])
    b.h('1   Upper Bristlecone Helipad (UB)  →  Lee Fire Station (LFS)')
    b.p('Put the transmitter at the selected mount beside the Upper Bristlecone trailhead, 4 m above ground. Measure the station antenna and test the 1 m planning height. Send ten paced, numbered payloads. Expect matching IDs at Lee and corresponding gateway uploads. If RF arrives without an upload, check station Wi-Fi and MQTT first.')
    b.h('2   Lee Junction (LJ)  →  Upper Bristlecone Helipad  →  Lee Fire Station')
    b.p('At Lee Junction, send from the planned 4 m antenna. Compare a run with Upper Bristlecone Helipad relaying against a run with that relay silent. Keep other relays out of the controlled test. Expect Lee receipts with the relay active and fewer or none when silent. If the chain fails, repeat at 7 m or try an adjacent mount before relying on it.')
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
    colors=[('#81978e','Stations only','Direct'),('#648499','Starting seven','Starting / lower'),(TEAL,'Ten with Sisters','Recommended')]
    b.begin('Mountain coverage','What the repeaters add','The map traces the named trail network. Teal sections have a terrain path to dispatch through Lee or Kyle. The bars compare station-only service, the original seven placements and the ten-site plan.')
    b.image(m.operating_roads(trails=True),243)
    legend(b,ROADS)
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
    b.end()

def road_page(b,m,r):
    b.begin('Highways and access roads','Where the roads reach dispatch','Follow SR 156, SR 157 and SR 158 on one north-up map. The open circles mark the scored highway limits. The Angel Peak approach runs from SR 158 to the two drive-up pins.')
    b.image(m.operating_roads(),398)
    legend(b,ROADS+[('Highway limit',INK,'point'),('Drive-up site',INK,'triangle'),STATIONS[1]])
    names=['SR 156','SR 157','SR 158','Angel Peak']
    for i,n in enumerate(names):
        x=36+i*136;v=r['scenarios']['Recommended'][n];g=r['roads'][n]
        b.text(x,b.y-10,n,10,b.bold);b.text(x,b.y-29,f'{v:.0f}% reachable',12,b.bold,TEAL)
        b.text(x,b.y-43,f"Longest gap {g[0]['km']:.2f} km" if g else 'No sampled gap',8.8)
    b.y-=57
    gap=r['roads']['Macks Canyon'][0]
    b.h(f"First gap drive   /   Upper Macks Canyon   /   {gap['km']:.2f} km")
    b.p('Enter from SR 156. Send a numbered GPS packet from a reachable stop near the road mouth, again on either side of A, and near B if the snow permits. Log the receiving station and upload ID. Teal-to-red marks the predicted transition.')
    b.p('A  '+coord(gap['a'])+'     •     B  '+coord(gap['b']),9.2,4)
    b.end()

def coord(ll):return f'{ll[1]:.5f}, {ll[0]:.5f}'

def briefing_pages(b,m,r,cfg):
    order=r['selected'];rec=r['scenarios']['Recommended']
    b.begin('Deployment plan','Start at the Upper Bristlecone helipad','Place the first temporary relay at the authorized trailhead mount and receive at Lee Fire Station. Then add Lee Junction. The model links both sites to Lee before the Kyle branch is built.')
    b.image(m.overview('deployment'),358);legend(b,STATIONS+[('Modeled relay chain',TEAL,'line'),('Upper Macks gap',RED,'line')])
    b.h('Deployment order')
    for i in range(0,len(order),3):
        for j,k in enumerate(order[i:i+3]):
            x=36+180*j;b.text(x,b.y-10,str(i+j+1).zfill(2),9.4,b.bold,TEAL)
            b.text(x+18,b.y-10,f'{field_name(k)} ({field_code(k)})',9.4,b.bold)
        b.y-=21
    b.p(f"UB and LJ together bring modeled SR 156 reach from {r['scenarios']['Direct']['SR 156']:.0f}% to {r['scenarios']['Order 2']['SR 156']:.0f}%. Sisters is slot 10. Measure Lee’s antenna first. For winter expansion, test Lee Junction South (11), then Macks Mouth North (12). Pages 4–7 map the choices and the GPS acceptance test.")
    b.end()
    road_page(b,m,r)
    from expansion_pages import expansion_pages
    expansion_pages(b,m,r,cfg)
    tests(b,m)
    b.begin('Terrain visibility','Where a member can see a radio','Green land has a modeled clear terrain ray between a 1.2 m member antenna and at least one of the twelve infrastructure antennas. The next map identifies the receiving station.')
    b.image(m.overview('union'),419);legend(b,[('Antenna visible','#72bca9','fill'),('Terrain blocks all twelve',BLANK,'fill')]+STATIONS)
    code_key(b,order,r['gateways']);b.end()
    b.begin('Station destinations','Which fire station gets the packet?','Each color names the station that a member can reach with the ten planned repeater sites. Dark teal means the member has a modeled path to both stations.')
    station_image,mask=m.station_image(cfg['hop_limit']);b.image(station_image,410)
    legend(b,[('Neither',BLANK,'fill'),('Kyle only','#9e83b6','fill'),('Lee only','#77b6c9','fill'),('Either station',TEAL,'fill'),STATIONS[1]])
    area_per_cell=cfg['area_pixel_m']**2/1e6
    kms=[np.count_nonzero(mask==i)*area_per_cell for i in (1,2,3)]
    b.p(f'Within the scored area, {kms[0]:.1f} km² reach Kyle alone, {kms[1]:.1f} km² reach Lee alone and {kms[2]:.1f} km² have a modeled path to both.',10.3,6)
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
    b.begin('Repeater footprints','Which repeater covers which slope?','All ten panels use the same north-up frame and scale. Green shows one repeater’s complete footprint. The triangle marks its mount. Road length below each panel counts individual visibility.')
    b.image(m.mini_grid(order),503)
    legend(b,[('Visible to this repeater','#4a9f8f','fill'),('Outside its footprint',BLANK,'fill'),('Selected mount',INK,'triangle')])
    b.p('The helipad covers a small area around the resort. Its value is the clear relay path from Lee Junction down to Lee Fire Station. The individual footprints show only the first radio contact.',10)
    b.end();cover_chart(b,m,r)

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

def profile_pages(b,m,root,cfg,r):
    dem,meta=load_dem(root/'cache/terrain-local.tif')
    native=Profiles((root/'source').glob('USGS_1M*.tif'),dem,meta,299.792458/cfg['frequency_mhz'],6371000*cfg['effective_earth_k'])
    dst=root/'tables/profiles';dst.mkdir(exist_ok=True)
    sets=[('Kyle','FL','CH','CL','GK'),('Lee','LC','SK','GL',None)]
    current_files=set()
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
            filename=u+'-'+v+'.csv'
            current_files.add(filename)
            np.savetxt(dst/filename,np.column_stack([dist,ground,line,f1]),delimiter=',',fmt='%.3f',header='distance_m,terrain_plus_bulge_m,radio_ray_m,first_fresnel_radius_m',comments='')
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
    for file in dst.glob('*.csv'):
        if file.name not in current_files:
            archive=root/'cache/archived-profiles'
            archive.mkdir(exist_ok=True)
            file.replace(archive/file.name)
