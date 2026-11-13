"""Offline letter-size field atlas. Values and plotted pins use the model output."""
import json
import math
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape
import numpy as np
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from cartography import Maps,PALETTE,plt
from terrain import load_dem
from native import Profiles

INK='#182e39';TEAL='#16675d';MUTED='#4c656a';LINE='#ccdad6';LIGHT='#edf4f0'

def ll(pos):return f'{pos[1]:.5f}, {pos[0]:.5f}'
def num(v):return f'{v:.1f}'

class Book:
    def __init__(self,path):
        self.c=Canvas(str(path),pagesize=(612,792),pageCompression=1,invariant=True)
        self.c.setTitle('Mount Charleston | Winter mesh field study')
        self.c.setAuthor('SNORR MeshLink')
        self.n=0
        self.font='Helvetica';self.bold='Helvetica-Bold';self.serif='Times-Bold'
        fonts=Path('C:/Windows/Fonts')
        if (fonts/'segoeui.ttf').exists():
            for key,file in [('Body','segoeui.ttf'),('Strong','segoeuib.ttf'),('Title','georgia.ttf')]:
                pdfmetrics.registerFont(TTFont(key,str(fonts/file)))
            self.font,self.bold,self.serif='Body','Strong','Title'

    def text(self,x,y,txt,size,font=None,color=INK):
        c=self.c;c.setFillColor(HexColor(color));c.setFont(font or self.font,size);c.drawString(x,y,str(txt))

    def begin(self,section,title,sub):
        self.n+=1;c=self.c
        c.setFillColor(HexColor(TEAL));c.rect(0,781,612,11,fill=1,stroke=0)
        self.text(36,750,'SNORR   /   MOUNT CHARLESTON',9,self.bold,TEAL)
        c.setFillColor(HexColor(MUTED));c.setFont(self.font,9);c.drawRightString(576,750,section.upper())
        self.text(36,708,title,25,self.serif)
        self.y=684;self.p(sub,10.1)
        self.y-=3;c.bookmarkPage('p'+str(self.n));c.addOutlineEntry(title,'p'+str(self.n),0)

    def end(self):
        if self.y<45:raise ValueError(f'Page {self.n} overflows (y={self.y:.1f})')
        c=self.c;c.setStrokeColor(HexColor(LINE));c.line(36,37,576,37)
        self.text(36,21,'PRIVATE FIELD COPY     /     13 NOV 2026     /     WGS84',8,self.bold,MUTED)
        c.setFont(self.font,9);c.drawRightString(576,21,str(self.n));c.showPage()

    def p(self,text,size=10,space=8):
        style=ParagraphStyle('p',fontName=self.font,fontSize=size,leading=size*1.34,textColor=HexColor(INK),splitLongWords=True)
        para=Paragraph(escape(str(text)),style)
        _,h=para.wrap(540,1000);para.drawOn(self.c,36,self.y-h);self.y-=h+space

    def h(self,text):
        self.y-=4;self.text(36,self.y-12,text,12,self.bold,TEAL);self.y-=22

    def table(self,head,rows,widths=None,size=8.6):
        if widths is None:widths=[540/len(head)]*len(head)
        for ir,row in enumerate([head]+list(rows)):
            header=ir==0
            style=ParagraphStyle('cell',fontName=self.bold if header else self.font,fontSize=size,leading=size*1.22,
                                 textColor=white if header else HexColor(INK))
            cells=[Paragraph(escape(str(v)),style) for v in row]
            heights=[p.wrap(w-10,1000)[1] for p,w in zip(cells,widths)]
            h=max(heights)+7
            self.c.setFillColor(HexColor(TEAL if header else (LIGHT if ir%2 else '#ffffff')))
            self.c.rect(36,self.y-h,540,h,stroke=0,fill=1)
            x=36
            for p,w,hp in zip(cells,widths,heights):
                p.drawOn(self.c,x+5,self.y-3.5-hp);x+=w
            self.y-=h
        self.y-=9

    def image(self,buf,maxheight):
        img=ImageReader(buf);w,h=img.getSize();k=min(540/w,maxheight/h)
        self.c.drawImage(img,36+(540-w*k)/2,self.y-h*k,w*k,h*k,mask='auto')
        self.y-=h*k+8


def make_report(root,cfg,r):
    b=Book(root/'Mount-Charleston-winter-mesh.pdf')
    maps=Maps(root,r);sites=maps.sites;order=r['selected'];active=r['gateways']+order
    scen=r['scenarios'];rec=scen['Recommended'];total=r['total'];safe=scen['Survives every single loss']
    fails=r['failures'];worst=max(fails,key=lambda i:fails[i]['road_km'])
    def route(code):return ' > '.join(r['paths'].get(code,['isolated']))
    def hardest(name):return (r['roads'].get(name) or [{}])[0]
    roadnames=['SR 156','SR 157','SR 158','Lucky Strike','Macks Canyon','Champion']
    def impacted(code):
        return ', '.join(f'{name} {fails[code][name]:.0f}%' for name in sorted(roadnames,key=lambda n:-fails[code][n])[:2])
    def coverage_rows(labels):
        return [[k,num(scen[k]['road_km']),num(scen[k]['trail_km']),num(scen[k]['land_km2'])] for k in labels]
    b.begin('Deployment decision','Mount Charleston winter mesh','Winter 2026-27   /   Nine omnidirectional repeaters, two station gateways. Site codes identify field locations independently of physical radio labels.')
    b.p(f"Survey both stations first. Start the repeater sequence at {sites[order[0]]['name']}, then {sites[order[1]]['name']}. Verify their gateway receipts before carrying radios up the next approach.")
    rows=[]
    prior=scen['Direct']
    for i,k in enumerate(order,1):
        v=scen['Order '+str(i)]
        rows.append([str(i),k,sites[k]['name'],route(k),f"+{v['road_km']-prior['road_km']:.1f} km"])
        prior=v
    b.table(['Order','Site','Placement','One modeled route','Roads added'],rows,[43,42,183,173,99])
    b.h('Most consequential gaps')
    for name in ['Macks Canyon','Lucky Strike']:
        g=hardest(name)
        if g:b.p(f"{name} has a continuous {g['km']:.2f} km blind stretch, from {ll(g['a'])} to {ll(g['b'])}.",9.8,5)
    b.h('Single-failure objective')
    b.p(f"{num(safe['road_km'])} km of {num(rec['road_km'])} reachable road survives every single-node loss. Removing {sites[worst]['name']} ({worst}) costs {num(fails[worst]['road_km'])} km of road. Verify that a packet from Fletcher reaches Kyle through the higher Cathedral tree at the planned heights.")
    b.p('This is a terrain-based deployment trial. The model provides neither dispatch assurance nor authority to mount equipment. Carry the GIS and GPX with this copy.',9)
    b.end()
    for mode,title,sub in [
        ('union','Combined terrain visibility','All selected antenna footprints at a 1.2 m member endpoint. Teal cells have a clear bare-earth ray to at least one antenna. Uncolored cells have none.'),
        ('overlay','Nine repeater footprints','Each dot color identifies a repeater. Interleaved colors show overlap. The nine individual GeoTIFFs preserve full footprints at every 80 m cell.'),
        ('reach','Reach to a fire station','Teal survives the loss of any one radio or station. Amber reaches a station in the intact layout and loses that path under at least one failure. Uncolored land is blind or disconnected.')]:
        b.begin('Overview maps',title,sub);b.image(maps.image(mode),454)
        if mode=='overlay':
            for i,k in enumerate(order):
                x=36+(i%3)*180;y=b.y-(i//3)*18
                b.text(x,y-8,k,9,b.bold,PALETTE[i]);b.text(x+19,y-8,sites[k]['name'][:24],8.2)
            b.y-=58
        elif mode=='reach':
            b.p('Red road sections are blind at 40 m midpoint spacing. Hollow circles mark the scored highway ends. A diamond marks a station and a triangle a repeater. Gray fine lines show adjoining named trails. One colored cell describes the sample at its center.')
        else:
            b.p('The outline defines the scored mountain area. Dark lines show the six priority road corridors. Light lines show named adjoining paths. Gray relief includes the canyon walls and ridges that intercept the radio rays.')
        b.p('NAD83 / UTM zone 11N. Terrain USGS 3DEP. Roads and trails © OpenStreetMap contributors, ODbL. Grid north is within about 1° of true north here.',8.6)
        b.end()
    b.begin('Coverage evidence','How much of the mountain is reachable?','Distances sum modeled centerlines inside the scoring boundary. Land uses grid-cell centers. Each scenario has identical denominators.')
    b.table(['Configuration','Road km','Trail km','Land km²'],[['All scored geometry',num(total['road_km']),num(total['trail_km']),num(total['land_km2'])]]+
            coverage_rows(['Direct','Nominal starting pins','Starting / lower','Starting / higher','Recommended','Survives every single loss','Fletcher unavailable','Roof antenna','60 percent F1 backbone']),[267,91,91,91])
    facility=sorted(set(rec)-set(roadnames)-{'road_km','trail_km','land_km2'})
    b.table(['Facility or corridor','Direct','Start / low','Nine','Survives all'],
            [[n]+[f'{scen[k][n]:.0f}%' for k in ['Direct','Starting / lower','Recommended','Survives every single loss']] for n in roadnames+facility],[184,78,96,77,105],8.3)
    b.p('Facility percentages use 30 m samples inside mapped campground boundaries. The resort score follows mapped ski runs by length. McWilliams includes former Dolomite loops. Kyle Canyon Campground is scored as its mapped footprint; the November update lists day use. Roads include both mapped branches at divided segments.',8.7)
    b.end()
    b.begin('Survey limits','Road endpoints and blind stretches','WGS84 latitude, longitude. Highway endpoints mark the mountain scoring limits. Keep US 95 and valley contacts outside the placement score.')
    b.table(['Highway','One scored end','Other scored end'],[[k,ll(a),ll(z)] for k,(a,z) in r['highways'].items()],[100,220,220])
    b.h('Longest contiguous modeled road gap in each corridor')
    b.table(['Corridor','Length','From','To'],[[k,f"{hardest(k)['km']:.2f} km",ll(hardest(k)['a']),ll(hardest(k)['b'])] if hardest(k) else [k,'0 km','All sampled centers reachable',''] for k in roadnames],[88,63,194,195])
    b.p("SR 156 follows Lee Canyon Road, SR 157 follows Kyle Canyon Road and SR 158 follows Deer Creek Road between the canyons. The USFS and Nevada highway sources identify these corridors. The OSM line named Lucky Strike Trail includes an asphalt private-access portion and the eastbound gravel track. Champion is FR 45203. Mack's Canyon Road follows the westward unpaved spur from SR 156.")
    b.p('The eastern Lucky Strike and Kyle boundaries clip the mountain approaches. Northbound Lee coverage stops at the study boundary. Approximate the ends of shorter gaps from road-gaps.geojson, then walk or drive both shoulders of the predicted transition. Features intersecting the boundary are clipped.')
    b.h('Away from roads')
    b.p(f"The intact layout reaches {num(rec['trail_km'])} of {num(total['trail_km'])} km of mapped named trails and {num(rec['land_km2'])} of {num(total['land_km2'])} km² of land. Short dead pockets can fall between samples. Trail geometry describes potential member locations even when a route is closed to visitors.")
    b.end()
    b.begin('Failure analysis','What breaks when one node fails?','Each row removes the radio, all its edges and its member footprint. The graph searches again from the surviving station sinks, allowing up to three forwarding repeaters.')
    b.table(['Removed','Lost roads km','Lost trails km','Lost land km²','Largest road losses¹'],[[k,num(fails[k]['road_km']),num(fails[k]['trail_km']),num(fails[k]['land_km2']),impacted(k)] for k in sorted(active,key=lambda k:-fails[k]['road_km'])],[72,76,77,90,225],8.5)
    b.p('¹ Percentage points of each entire named corridor. A point can depend on several nodes in series, so the rows overlap. The survives-all layer intersects all eleven independent outage scenarios.')
    b.h('Station RF and internet outages')
    b.p('Both station radios are modeled as receive-and-uplink sinks with rebroadcast disabled. Losing station Wi-Fi or MQTT therefore removes the same paths to remote dispatch as losing that radio. A powered station can still hear RF locally. Field evidence must establish buffering or later replay.')
    b.h('Coverage-first comparison')
    v=scen['Resilience alternative'];w=scen['Alternative survives all']
    b.p(f"Giving intact coverage more weight chooses {', '.join(r['resilience_layout'])}. It reaches {num(v['road_km'])} km of road with {num(w['road_km'])} km surviving all single removals. The recommended arrangement gives up {v['road_km']-rec['road_km']:.2f} km of intact road to protect {safe['road_km']-w['road_km']:.2f} km more during single failures.")
    b.end()
    b.begin('Alternatives','Where a change of site pays off','Each alternate row moves one of the nine and keeps the other eight. The reported alternative is the highest-scoring equal-or-easier access class tested for that slot.')
    b.table(['Remove','Replacement','Alternative roads','Alternative trails','Road loss if simply removed'],
            [[k,r['alternatives'][k]['easy'],num(r['alternatives'][k]['metrics']['road_km'])+' km',num(r['alternatives'][k]['metrics']['trail_km'])+' km',num(fails[k]['road_km'])+' km'] for k in order],[64,98,113,110,155])
    b.table(['Starting-layout or sensitivity test','Road km','Trail km','Land km²'],coverage_rows(['Starting / lower','Starting / higher','Starting / no Angel Vegas','Starting / no Angel mountain','Starting / neither Angel','Higher / no Vegas','Higher / no mountain','Higher / neither','Fletcher unavailable','Tenth candidate']),[267,91,91,91],8.1)
    b.p(f"Without Fletcher, use {', '.join(r['no_fletcher'])}. The strongest tenth candidate was {r['extra']}, adding {scen['Tenth candidate']['road_km']-rec['road_km']:.2f} road km. Keep the nine; the gap trials and 3 m mast test come first. The candidate register at the back decodes every alternate site.",9.2)
    b.end()
    more_pages(b,maps,root,cfg,r,active,facility)
    b.c.save()


def more_pages(b,maps,root,cfg,r,active,facility):
    sites=maps.sites;rec=r['scenarios']['Recommended'];order=r['selected'];scen=r['scenarios']
    dem,meta=load_dem(root/'cache/terrain-local.tif')
    wavelength=299.792458/cfg['frequency_mhz']
    native=Profiles((root/'source').glob('USGS_1M*.tif'),dem,meta,wavelength,6371000*cfg['effective_earth_k'])
    profile_dir=root/'tables/profiles';profile_dir.mkdir(exist_ok=True)
    selected_pairs=[('FL','CH'),('FL','CL'),('CH','GK'),('LC','LF'),('LF','GL'),('LC','GL')]
    for page in range(2):
        b.begin('Radio engineering','Critical terrain profiles' if page==0 else 'Lee-side relay clearances',
                'Height in metres above NAVD88. Brown is curved-Earth terrain, teal is the direct ray and amber is its lower 60% first-Fresnel envelope. The inset reports the limiting sample anywhere along the path.')
        for a,z in selected_pairs[3*page:3*page+3]:
            s,t=sites[a],sites[z];path=next(p for p in r['pairs'] if {p['a'],p['b']}=={a,z})
            dist,ground,line,f1=native.trace((s['x'],s['y'],s['h']),(t['x'],t['y'],t['h']))
            np.savetxt(profile_dir/(a+'-'+z+'.csv'),np.column_stack([dist,ground,line,f1]),delimiter=',',fmt='%.3f',
                       header='distance_m,terrain_plus_bulge_m,radio_ray_m,first_fresnel_radius_m',comments='')
            fig,ax=plt.subplots(figsize=(8.4,1.75))
            ax.fill_between(dist/1000,ground,np.min(ground)-15,color='#dfd4bf');ax.plot(dist/1000,ground,color='#745d3e',lw=.9)
            ax.plot(dist/1000,line,color=TEAL,lw=1.1);ax.plot(dist/1000,line-.6*f1,color='#bc742a',lw=.9,ls='--')
            ax.set_ylabel('m NAVD88',fontsize=8);ax.set_xlabel('km from '+a,fontsize=8);ax.tick_params(labelsize=8);ax.grid(alpha=.15)
            fig.tight_layout(pad=.4);buf=BytesIO();fig.savefig(buf,format='png',dpi=145);plt.close(fig);buf.seek(0)
            b.p(f"{a} ({s['h']:g} m AGL) to {z} ({t['h']:g} m)   |   {dist[-1]/1000:.2f} km   |   min clearance {path['clear_m']:+.1f} m   |   min F1 {path['f1']:.2f}",9.5,2)
            b.image(buf,106)
        b.p('Minimum F1 is the smallest clearance divided by the local first-Fresnel radius along the ray. Its location can differ from the minimum clearance in metres. Sample spacing ≤1 m. Local foliage, poles, snow and buildings are absent from the DEM.',9)
        b.end()
    b.begin('Antenna height','Test a mast before moving a radio','Both station pins stay fixed on the supplied premises. The baseline antenna is 1 m above local ground. Each height trial changes a single endpoint and repeats member and infrastructure visibility.')
    b.table(['Location','AGL tested (m)','Reachable road km at each height','New backbone links'],[
        [k,'1, '+', '.join(str(v['height']) for v in r['heights'] if v['id']==k),
         f"{rec['road_km']:.2f}, "+', '.join(f"{v['road_km']:.2f}" for v in r['heights'] if v['id']==k),
         ', '.join(sorted({j for v in r['heights'] if v['id']==k for j in v['new']})) or 'None'] for k in r['gateways']],[68,100,275,97])
    b.table(['Repeater','4 to 7 m: roads gained','Trails gained','New backbone links'],[
        [v['id'],f"{v['road_km']-rec['road_km']:+.2f} km",f"{v['trail_km']-rec['trail_km']:+.2f} km",', '.join(v['new']) or 'None']
        for v in r['heights'] if v['id'] in order],[102,153,135,150])
    b.p('Neither station gained a backbone link or 250 m of scored road at any tested height through 12 m. The terrain alone gives no reason to specify a taller mast there. At a station, record actual antenna AGL, roof lip, nearby wall and departure bearing. Compare 1, 2 and 4 m first, using the same antenna, cable, remote radio and packet cadence.')
    b.h('Member carried, in a vehicle and on the roof')
    b.p(f"The 1.2 m on-person and in-cabin screens both reach {rec['road_km']:.2f} km before body and vehicle loss. An assumed 2.2 m external roof antenna reaches {scen['Roof antenna']['road_km']:.2f} km. Metal, cabin orientation, whip gain, jacket position and foliage have no measured local loss distribution. Paired packets at the same stop can separate height from shielding.")
    b.end()
    b.begin('Access and staging','Winter access determines the installation','The owner reports vehicle access beyond ordinary visitor routes, easy historical Angel access, acceptable Sisters and Showgirl outings, and Fletcher as the upper walking limit.')
    b.h('Department and land-manager checks')
    b.p('NDOT restricts winter right-of-way parking on SR 157 between SR 158 and the lodge, along SR 156 from the Meadows to the resort, and near the Lee station. Use an authorized off-highway stop. December to March rules, plow operations and traction restrictions can change the available route. Check Nevada 511 and posted signs that morning. [4]')
    b.p('USFS Order 04-17-25-04, updated 16 June 2026, identifies the Upper Bristlecone Trail and 100 ft on each side, an Upper Kyle area, and named roads/trails through 12 May 2027 unless rescinded. The November recreation update and standing conditions page disagree on Cathedral Rock Trail. Confirm the proposed approach against Exhibit A and district guidance. A visitor trailhead listing alone cannot settle equipment access. [5–7]')
    b.p('The resort pin falls beside the mapped Upper Bristlecone trailhead. The 20 m search yielded no acceptable screened point when the trail buffer, roads, structures and slope were excluded. The starting scenario retains it only as an RF comparison. Lower Bristlecone offers the Lee-side alternative. Coordinate any helipad clearance with resort operations. [5,8]')
    b.p('Macks Canyon Road reopened in July 2026. The recreation partner also retains an older two-mile camping note. Neither source establishes plowing. Confirm the gate and turning room below the snow line. Champion is undeveloped and unpaved. On 1 November, the weekly update listed Fletcher View open, Hilltop closing 4 November, and McWilliams and Mahogany Grove closed for the season. [6,7]')
    b.h('Conditional Kyle branch')
    fallback=scen['Higher Cathedral unavailable']
    b.p(f"If the higher Cathedral pin or access route fails, reallocate the nine to {', '.join(r['no_high_cathedral'])}. That layout reaches {fallback['road_km']:.1f} road km and {fallback['trail_km']:.1f} trail km. If Fletcher alone is inaccessible, use the separate Fletcher fallback on the alternatives page. Do not transfer a result from the upper pin to the lower one.")
    b.p('Orange dashed approaches combine any mapped centerline with an estimated final connector. Where only a direct estimate exists it is a terrain transect. Positive ascent sums the climbs along that estimate. Snow, cliffs, driveway restrictions and unrepresented switchbacks can make a short estimate unusable.')
    b.end()
    b.begin('Optional third gateway','Angel to the Las Vegas valley','Historical member contacts justify an attended trial. The two-station recommendation gives no credit to Las Vegas or to an unselected home.')
    rows=[]
    for name in dict.fromkeys(v['sector'] for v in r['valley']):
        v=[i for i in r['valley'] if i['sector']==name]
        rows.append([name,f"{v[0]['clear']}/9",f"{v[1]['clear']}/9",f"{v[0]['km']:.1f}",f"{v[0]['best_f1']:.2f}"])
    b.table(['Broad test sector','Vegas side','Mountain side','Range km¹','Best F1¹'],rows,[210,78,98,77,77])
    b.p('¹ From Vegas-side Angel. Nine test points spaced 500 m in a 1 km square represent each broad sector. Each hypothetical home antenna is 4 m AGL. Regional 20 m terrain sampling includes the intervening foothills, effective Earth curvature and both endpoints. Buildings and home Wi-Fi reach remain unknown.')
    h=r['home']
    b.table(['Hypothetical network','Road km','Trail km','Land km²'],[
        [label,num(v['road_km']),num(v['trail_km']),num(v['land_km2'])] for label,v in [
            ('Two stations, main nine',rec),(f"Third sink; move {h['swapped']} to AV",h['nine']),('Same nine, Kyle station failed',h['no_kyle']),
            ('Same nine, Lee station failed',h['no_lee']),('Same nine, home unavailable',h['no_home']),('Third sink; keep nine and add AV',h['ten'])]],[258,94,94,94])
    b.p('Third-sink rows assume a verified Angel Vegas-to-home radio link, internet, AC and permission. Only packets reaching AV within the hop budget can use this uplink; the model gives no direct member-to-house credit. Every antenna is omni. Ridge terrain, rather than an antenna pointing direction, distinguishes the two Angel pins.')
    b.p('First test western North Las Vegas, then Centennial Hills. Use a consenting home or authorized surrogate at the intended antenna height. Alternate the two Angel pins, record per-packet RSSI/SNR and gateway upload IDs, then disable the other gateways during a controlled test. A successful voice or historical radio contact alone cannot qualify a tracking uplink.')
    b.end()
    b.begin('Winter energy','Panel orientation at the tree','Azimuth is clockwise from true north. Tilt is degrees above horizontal. Terrain windows use Pacific local time, PST in November through February and PDT for the March and April dates.')
    b.table(['Site','Nov–Apr az / tilt','December az / tilt','December-only gain','Dec 21 direct window'],[
        [k,f"{sites[k]['solar']['az']}° / {sites[k]['solar']['tilt']}°",f"{sites[k]['solar']['dec_az']}° / {sites[k]['solar']['dec_tilt']}°",
         f"{sites[k]['solar']['dec_gain']:.1f}%",sites[k]['solar']['windows']['Dec 21']] for k in active],[55,103,112,110,160])
    b.p('For each site, trace a terrain horizon every 2° in azimuth out to 30 km at an assumed panel height of 2 m. The model combines NOAA sun angles at five-minute intervals with NASA POWER monthly DNI and diffuse climatology for 2001–2025. A representative day is weighted by days in its month. The orientation grid is 5°. Terrain-only windows assume clear sky. Solar resource is regional and does not resolve a specific tree. [9,10]')
    b.p('For a single fitted face, point its normal at the listed bearing. For the two angled v4 faces, center their outward normals around that bearing if the case geometry allows. Check both faces with an inclinometer and compass set to true. V3 has one fitted panel; v1 has three with unverified angles. Cases 10 and 11 have external 5 W pass-throughs. Panel nameplate current alone cannot establish winter charging.')
    b.p('At each tree, sight the solstice arc from panel height. Mark branch or trunk shade at the beginning, middle and end of the listed window. Check snow shedding and log panel input, battery temperature, voltage and overnight draw across an actual storm cycle before relying on autonomy.')
    b.p('Far-horizon rays stop at the regional DEM edge where it falls within 30 km. Near-field terrain gets finer sampling. A single regional climatology and approximate sky-view factor limit orientation precision to a practical range around the listed bearing.',8.5)
    b.end()
    for index,k in enumerate(active):
        s=sites[k];station=k in r['gateways'];solar=s['solar'];alt=r['alternatives'].get(k)
        b.begin('Station gateway' if station else f'Repeater field sheet  /  {order.index(k)+1} of 9',k+'  /  '+s['name'],
                ('Station survey rendezvous. ' if station else 'Search circle 20 m. ')+s['note'])
        b.image(maps.image('site',k),170)
        offset=('Fixed station point; identify the actual mount on the premises.' if station else
                f"From nominal move {s['shift']:.0f} m at {s['bearing']}° true. {s['tested_cells']} possible cells screened in.")
        b.table(['Navigation and mounting','Field value'],[
            ['Nominal WGS84',ll(s['nom_ll'])],['Selected WGS84',ll(s['ll'])+'   |   '+offset],
            ['Ground / antenna AGL',f"{s['z']:.0f} m / {s['z']*3.28084:.0f} ft NAVD88   |   {s['h']:g} m AGL"],
            ['Staging or vehicle stop',s['stop']+'   |   '+ll(s['stop_ll'])],
            ['One-way approach',f"{s['walk_m']/1000:.2f} km, +{s['ascent_m']} m. {s['approach']}. "+s['stop_evidence']],
            ],[144,396],8.1)
        if 'conditional_stop' in s:
            b.p(f"Owner vehicle option: nearest mapped drive line {ll(s['conditional_stop'])}, final straight-line offset {s['conditional_walk_m']} m. Reconnoiter a lawful off-road stop; this coordinate is a road reference.",8.5,5)
        b.p('Modeled chain: '+' > '.join(r['paths'].get(k,['isolated']))+
            f". Removing {k} loses {r['failures'][k]['road_km']:.2f} road km and {r['failures'][k]['trail_km']:.2f} trail km."+
            (f" Closest equal-or-easier alternative: {alt['easy']} / {sites[alt['easy']]['name']}." if alt else ''),9.2,5)
        if 'nominal_footprint' in s:
            b.p(f"Local pin comparison: individual road footprint {s['nominal_footprint']['road_km']:.2f} km nominal and {s['selected_footprint']['road_km']:.2f} km selected. Routing and weighted member coverage also influence the choice.",8.3,4)
        b.p(f"Winter solar: face {solar['az']}° true at {solar['tilt']}° above horizontal. December-only optimum {solar['dec_az']}° / {solar['dec_tilt']}°. Check branches at the actual fitted panel.",9.1,5)
        b.table(list(solar['windows']),[list(solar['windows'].values())],[90]*6,7.8)
        b.p('Field selection: use a stable tree or approved mount with the radio path clear at antenna height. Map precision is a navigation aid; allow the full search radius and re-test a moved mount. Record actual AGL, coordinate and dated two-way observations.',8.3)
        b.end()
    field_and_sources(b,root,cfg,r)


def field_and_sources(b,root,cfg,r):
    s={v['id']:v for v in r['sites']}
    b.begin('Field validation','The shortest tests that change the layout','Run attended trials at agreed stops. Use a known-good GPS member, two available station receivers and temporary masts. Site codes and GPS logs stay private.')
    steps=[
        ('1   Lee station / Lower Bristlecone',f"GL {ll(s['GL']['ll'])}; LF {ll(s['LF']['ll'])}. Verify the 1 m station endpoint and a 4 m omni at the proposed tree. At a marked stop, alternate on-person, cabin and external roof positions. Record packet sequence, GPS fix time and which station uploads it."),
        ('2   Lee and Deer Creek junction',f"LC {ll(s['LC']['ll'])}. Force the LC > LF > GL path by isolating other relays during a controlled test. The LC–LF ray has only 0.31 F1 minimum. If messages fail, compare 4 and 7 m, then move within the circle. Confirm a separate receiving route before relying on redundant map cells."),
        ('3   Upper Macks Canyon',f"Start at {ll(r['roads']['Macks Canyon'][0]['a'])}; the persistent blind stretch ends at {ll(r['roads']['Macks Canyon'][0]['b'])}. Sample at the mouth, the transition and near the mapped upper terminus only if passable. Try both canyon walls at a safe stop. If repeatable receipts extend deep into the canyon, re-score the field evidence before moving a unit from elsewhere."),
        ('4   Kyle station / Cathedral / Fletcher','First work from the station and a permitted Cathedral approach. Compare lower and higher pins at matched height. Send identifiable Fletcher packets via one relay to Kyle, then remove that relay. A lower-pin success or an inaccessible upper pin changes the deployment branch. The modeled upper approach gains nearly 300 m; confirm a workable ascent before carrying equipment.'),
        ('5   Lucky Strike and optional valley','Use an authorized stop on either side of the mapped east-branch gap. Compare the Lucky Strike shoulder with mountain-side Angel. For a home test, isolate Vegas-side Angel and verify raw gateway receipts and GPS measurement age from a consenting northwest-valley station.'),
    ]
    for title,detail in steps:b.h(title);b.p(detail,9.4,5)
    b.p('Use ten paced unique payloads per configuration as a diagnostic sample. Log attempted/received IDs, antenna AGL and orientation, hop settings, RSSI/SNR, UTC, weather and gateway/backhaul status. Revisit on another day. Record reception separately from dispatch GPS age; the project stale threshold is 15 minutes.',8.8)
    b.end()
    b.begin('Model notes','Terrain, routing and uncertainty','The rankings compare feasible paths through sampled bare earth. No deployment reception, clearance of vegetation, winter parking inspection or battery-runtime test occurred in this study.')
    b.h('Terrain and footprints')
    b.p('Six USGS NV_Southern_D23 1 m bare-earth lidar tiles cover the mountain. Source NAD83 / UTM zone 11N, NAVD88 orthometric metres. A 1/3 arc-second NAD83 geographic tile n37w116 (2026-06-10 file) extends the terrain toward the valley. Continuous reprojection uses bilinear interpolation; the local model uses a 5 m working grid and the regional horizon/valley uses 20 m. Raw metadata dates, bounds and checksums are in inputs/sources.json. [1,2]')
    b.p('Local member rays are tested at ≤5 m intervals with Earth radius multiplied by 4/3. Ground is bilinearly interpolated. Road/trail intersections use segment midpoints at ≤40 m. Land uses 80 m cell centers, independent of road samples. Backbone edges use native 1 m surfaces at ≤1 m intervals and the regional extension outside tile coverage. The DEM extends beyond the reporting polygon.')
    b.h('Candidate search and route definition')
    b.p(f"Search {len(s)} station/candidate locations including 7 full-road shoulder searches. New stop-centered candidates use a 250 m terrain search; each nominal repeater then uses a 20 m circle sampled at 5 m with road, roof, mapped helipad, closure-buffer and steep-slope exclusions. A score combines sample visibility, gateway attachment and other infrastructure edges. Station shifts remain zero. Distinguishable micro-topography can still hide a tree, cliff edge or building.")
    b.p('Start from the two fire stations. Add up to three forwarding repeaters per packet, test all singleton additions, then greedy construction and one-for-one exchanges from multiple seeds. Scored classes are roads 56%, trails 18%, camps/resort 18%, land 8%, with a 10% Lee preference inside the route classes. Campgrounds and ski runs get equal facility-group weight before the Lee preference. Weight-binned bitsets accelerate ranking. This is a searched layout, with no global-optimality claim.')
    b.p('Local link plausibility uses positive terrain clearance at the verified profile, subject to the Fresnel sensitivity run. Gain, feeder loss, receiver threshold, clutter, body shielding, snow burial, polarization and interference remain site-specific unknowns. At 910.625 MHz the free-space loss in dB is 91.63 + 20 log10(distance in km). At 10 dBm a 5 km path gives about −95.6 dBm with an assumed pair of 0 dBi antennas and no cable loss. This reference budget cannot predict packet reliability.')
    b.p('US / LONG_FAST, channel 35, 10 dBm, SF11, 250 kHz, CR 4/5 and hop limit 3 come from bench/receive records. A zero-hop reference board is excluded. No special zero-cost forwarding is credited. Physical board assignments, field role, frequency and antenna fit require final readback. [11]',8.7)
    b.end()
    b.begin('Sources and files','Evidence carried into the field copy','Source details were checked 13 November 2026. The source manifest preserves exact public download URLs, dates and SHA-256 digests. USGS elevation is public domain; map geometry is © OpenStreetMap contributors, ODbL.')
    sources=[
        ('1','USGS 3DEP 1 metre DEM collection','https://data.usgs.gov/datacatalog/data/USGS%3A77ae0551-c61e-4979-aedd-d797abdcde0e'),
        ('2','USGS elevation coordinate systems and resolution','https://www.usgs.gov/faqs/what-projection-horizontal-datum-vertical-datum-and-resolution-a-usgs-digital-elevation-model'),
        ('3','Geofabrik Nevada extract, data through 12 Nov 2026','https://download.geofabrik.de/north-america/us/nevada.html'),
        ('4','Nevada DOT winter parking and traction rules','https://www.dot.nv.gov/safety/safe-winter-driving/mt-charleston-winter-safety'),
        ('5','USFS storm-damage closure order and Exhibit A','https://www.fs.usda.gov/r04/humboldt-toiyabe/alerts/area-road-and-trail-closures-spring-mountains-national-recreation-area'),
        ('6','Spring Mountains weekly recreation update','https://www.gomtcharleston.com/spring-mountains-weekly-update/'),
        ('7','Spring Mountains conditions and closures','https://www.gomtcharleston.com/current-condition-closures/'),
        ('8','Lee Canyon resort parking / facilities','https://www.leecanyonlv.com/where-do-i-park/'),
        ('9','NASA POWER climatology API, solar resource','https://power.larc.nasa.gov/docs/services/api/temporal/climatology/'),
        ('10','NOAA solar position calculation','https://gml.noaa.gov/grad/solcalc/solareqns.PDF'),
        ('11','Meshtastic managed flood and hop-limit semantics','https://meshtastic.org/docs/overview/mesh-algo/'),
        ('12','Recreation.gov McWilliams including Dolomite loops','https://www.recreation.gov/camping/campgrounds/232168'),
        ('13','Nevada DOT state-maintained highway description index','https://www.dot.nv.gov/home/showpublisheddocument/23124/638718361041470000')]
    for idx,label,url in sources:
        b.text(36,b.y-9,idx,8,b.bold,TEAL);b.text(57,b.y-9,label,9,b.font)
        b.c.linkURL(url,(55,b.y-12,574,b.y+1),relative=0);b.y-=18
    b.h('Project records')
    b.p('PROJECT.md and records/deployment-nodes.md govern equipment identity and mission. records/inventory.md and docs/hardware/enclosures.md describe fitted panels. The R001 commissioning, B003 member, screenless gateway and airtime-sniffer records support the radio assumptions. Nine board-level RAK passes and a held R003 are recorded; the field labels in this atlas assign no devices.')
    b.h('Offline files')
    b.p('navigation.gpx contains the eleven radio search points and eleven staging/rendezvous points. gis/ contains WGS84 GeoJSON and projected GeoTIFFs. The route-status layer gives three classes at segment scale. tables/results.json includes every pair, tested height, covered length and loss. tables/profiles/ holds terrain and Fresnel data. inputs/study.json controls the next run.')
    b.p('For a field correction, retain packet IDs and anonymous measured results privately. Update the editable inputs with surveyed ground point, antenna AGL and access evidence; regenerate the model and compare the same road, trail and facility denominators.')
    b.end()
    candidates=[v for v in r['sites'] if v['id'] not in r['gateways']]
    for page in range(0,len(candidates),17):
        b.begin('Candidate register','Mounting-point comparisons','All candidate radios use 4 m AGL. Road km here are individual terrain footprints. An isolated radio can see a road without delivering its packets to either station.')
        subset=candidates[page:page+17]
        b.table(['Code / location','Nominal WGS84','Selected WGS84','Offset m','Road km nominal / selected'],
                [[v['id']+' / '+v['name'],ll(v['nom_ll']),ll(v['ll']),f"{v['shift']:.0f}",f"{v['nominal_footprint']['road_km']:.1f} / {v['selected_footprint']['road_km']:.1f}"] for v in subset],
                [138,124,124,50,104],8)
        b.p('Supplied sites retain the original nominal pin. For new candidates the nominal point comes from a terrain search near a mapped stop or from road-corridor sampling. The table gives the subsequent 20 m refinement. All proposed final trees, funding and permissions remain unassigned.')
        b.end()
