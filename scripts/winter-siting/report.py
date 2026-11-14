"""Offline letter-size field atlas. Values and plotted pins use the model output."""
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from cartography import Maps
from field_names import field_name, field_code, navigation_name
from briefing import cover, briefing_pages, profile_pages, solar_windows, legend

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
    b=Book(root/'Mount-Charleston-winter-field-plan.pdf')
    maps=Maps(root,r);order=r['selected'];active=r['gateways']+order
    scen=r['scenarios'];rec=scen['Recommended']
    cover(b,maps)
    briefing_pages(b,maps,r,cfg)
    def coverage_rows(labels):
        return [[k,num(scen[k]['road_km']),num(scen[k]['trail_km']),num(scen[k]['land_km2'])] for k in labels]
    b.begin('Alternatives','Where a change of site pays off','Each alternate row moves one of the nine and keeps the other eight. The reported alternative is the highest-scoring equal-or-easier access class tested for that slot.')
    b.table(['Field code','Replacement','Alternative roads','Alternative trails'],
            [[field_code(k),navigation_name(r['alternatives'][k]['easy']),num(r['alternatives'][k]['metrics']['road_km'])+' km',num(r['alternatives'][k]['metrics']['trail_km'])+' km'] for k in order],[85,185,135,135])
    b.table(['Layout or sensitivity test','Road km','Trail km','Land km²'],coverage_rows(['Direct','Starting / lower','Starting / higher','Starting / no Angel Vegas','Starting / no Angel mountain','Starting / neither Angel','Higher / no Vegas','Higher / no mountain','Higher / neither','Recommended','60 percent F1 backbone','Fletcher unavailable','Tenth candidate']),[267,91,91,91],8.1)
    b.p(f"Without Fletcher, use {', '.join(map(field_code,r['no_fletcher']))}. The strongest tenth candidate was {field_name(r['extra'])}, adding {scen['Tenth candidate']['road_km']-rec['road_km']:.2f} road km. Keep the nine; the gap trials and 3 m mast test come first. The register at the back gives coordinates for every alternate site.",9.2)
    b.end()
    more_pages(b,maps,root,cfg,r,active)
    b.c.save()


def more_pages(b,maps,root,cfg,r,active):
    sites=maps.sites;rec=r['scenarios']['Recommended'];order=r['selected'];scen=r['scenarios']
    profile_pages(b,maps,root,cfg,r)
    b.begin('Antenna height','Test a mast before moving a radio','Both station pins stay fixed on the supplied premises. The baseline antenna is 1 m above local ground. Each height trial changes a single endpoint and repeats member and infrastructure visibility.')
    b.table(['Location','AGL tested (m)','Reachable road km at each height','New backbone links'],[
        [field_code(k),'1, '+', '.join(str(v['height']) for v in r['heights'] if v['id']==k),
         f"{rec['road_km']:.2f}, "+', '.join(f"{v['road_km']:.2f}" for v in r['heights'] if v['id']==k),
         ', '.join(field_code(j) for j in sorted({j for v in r['heights'] if v['id']==k for j in v['new']})) or 'None'] for k in r['gateways']],[68,100,275,97])
    b.table(['Repeater','4 to 7 m: roads gained','Trails gained','New backbone links'],[
        [navigation_name(v['id']),f"{v['road_km']-rec['road_km']:+.2f} km",f"{v['trail_km']-rec['trail_km']:+.2f} km",', '.join(map(field_code,v['new'])) or 'None']
        for v in r['heights'] if v['id'] in order],[102,153,135,150])
    for k in r['gateways']:
        rows=[v for v in r['heights'] if v['id']==k]
        first=next((v for v in rows if v['new'] or v['road_km']-rec['road_km']>=.25),None)
        note=(f"The first tested height gaining a new link or at least 250 m of road is {first['height']} m (+{first['road_km']-rec['road_km']:.2f} road km)." if first else 'No tested height through 12 m gains a new link or 250 m of road.')
        b.p(field_name(k)+'. '+note,9.6,4)
    b.p('Measure the station antenna AGL and roof lip. Use the same remote radio, antenna and cable when comparing heights.',9.5,5)
    b.h('Member carried, in a vehicle and on the roof')
    b.p(f"The 1.2 m on-person and in-cabin screens both reach {rec['road_km']:.2f} km before body and vehicle loss. An assumed 2.2 m external roof antenna reaches {scen['Roof antenna']['road_km']:.2f} km. Metal, cabin orientation, whip gain, jacket position and foliage have no measured local loss distribution. Paired packets at the same stop can separate height from shielding.")
    b.end()
    b.begin('Owner access and placement','The helipad and the two Angel Peak pins','The owner confirms agency authority to access the mountain and place equipment, easy access at Upper Bristlecone and vehicle access to both Angel Peak pins. Use these locations as the starting points for the field checks.')
    b.h('Upper Bristlecone Helipad  /  UB')
    sk=sites['SK']
    b.p(f"The supplied trailhead pin is {ll(sk['nom_ll'])}. The earlier screen removed its whole 20 m circle using a public trail-closure buffer. With agency access, {sk['tested_cells']} cells pass the physical screen. The modeled mount is {sk['shift']:.0f} m from the pin at {sk['bearing']}° true. UB has a direct terrain path to Lee and receives the Lee Junction relay.")
    b.p('Start with ten numbered packets from the selected 4 m test mount. Check the landing area, trail surface, plow clearance and actual branch shade when choosing the tree.')
    b.h('Angel Peak  /  compare the drive-up pins')
    trials=r['drive_up_trials']
    for k in ('AM','AV'):
        t=trials[k]['metrics'];site=sites[k]
        b.p(f"{navigation_name(k)}   /   {ll(site['nom_ll'])}. With this site included and the other eight places re-optimized, {t['road_km']:.2f} km of road and {t['trail_km']:.2f} km of trail can reach a station. The SR 158 approach scores {t['Angel Peak']:.1f}%.",9.8,5)
    b.p('Use AM for mountain tracking and take a portable to AV for the valley trial. Drive to the supplied coordinates. The 20 m search circles account for where the antenna can actually be mounted. Snow and ice on the day determine the last few metres.')
    b.h('Conditional Kyle branch')
    fallback=scen['Higher Cathedral unavailable']
    b.p(f"If the higher Cathedral pin or access route fails, reallocate the nine to {', '.join(map(field_code,r['no_high_cathedral']))}. That layout reaches {fallback['road_km']:.1f} road km and {fallback['trail_km']:.1f} trail km. If Fletcher alone is inaccessible, use the separate Fletcher fallback on the alternatives page. Do not transfer a result from the upper pin to the lower one.")
    b.p('On the site sheets, a solid rust line follows a mapped centerline. Dashes mark the estimated connectors. Where only a direct estimate exists the whole approach is dashed. Positive ascent sums the climbs along that estimate. Snow, cliffs, driveway restrictions and unrepresented switchbacks can make a short estimate unusable.')
    b.end()
    b.begin('Optional valley gateway','Angel Peak to the Las Vegas valley','Follow the rays east from the supplied drive-up point to the named city neighborhoods. Each square is a 1 km test area. Teal lines lead to a sector with at least one clear terrain sample from the Vegas-side radio.')
    b.image(maps.valley_image(cfg),268)
    legend(b,[('At least one clear sample','#00746d','line'),('No clear sample','#a6344a','dash'),('Freeway','#c5a04b','line')])
    rows=[]
    for idx,(name,lon,lat) in enumerate(cfg['valley_sectors'],1):
        vals={v['angel']:v for v in r['valley_drive_up'] if v['sector']==name}
        rows.append([str(idx)+'  '+name,f"{vals['AV']['clear']}/9",f"{vals['AM']['clear']}/9",f"{vals['AV']['km']:.1f} km"])
    b.table(['Test sector','Vegas pin (AV)','Mountain pin (AM)','From AV'],rows,[210,110,125,95])
    b.h('First city test   /   western North Las Vegas')
    b.p('Place a receiver in sector 4 with the antenna 4 m above ground. From the supplied Vegas-side drive-up point, send ten numbered packets, then repeat from the mountain-side point at the same antenna height. Match packet IDs at the receiver and at dispatch. Record RSSI/SNR and actual AGL. Repeat in Centennial Hills.')
    b.p('The two columns use the exact vehicle pins at 4 m antenna height. Each count is the number of terrain-clear points on a 3 × 3 grid spaced 500 m apart. Buildings, trees and the receiving address can change the result. Streets and highways © OpenStreetMap contributors, Nevada extract dated 12 November 2026.',9.1,6)
    h=r['home'];nine=h['nine']
    b.p(f"A verified home uplink with the nine-radio valley option would cover {nine['road_km']:.1f} km of mountain roads. The deployment recommendation uses the two fire stations.",9.2,5)
    b.end()
    b.begin('Winter energy','Panel orientation at the tree','Azimuth is clockwise from true north. Tilt is degrees above horizontal. Terrain windows use Pacific local time, PST in November through February and PDT for the March and April dates.')
    solar_windows(b,sites,active)
    gains=[sites[k]['solar']['dec_gain'] for k in active]
    b.p(f'Adjusting each mount solely for December yields {min(gains):.1f}–{max(gains):.1f}% more modeled December energy. The field sheets give each December-only bearing and tilt.',9.6)
    b.p('For each site, trace a terrain horizon every 2° in azimuth out to 30 km at an assumed panel height of 2 m. The model combines NOAA sun angles at five-minute intervals with NASA POWER monthly DNI and diffuse climatology for 2001–2025. A representative day is weighted by days in its month. The orientation grid is 5°. Terrain-only windows assume clear sky. Solar resource is regional and does not resolve a specific tree. [9,10]')
    b.p('For a single fitted face, point its normal at the listed bearing. For the two angled v4 faces, center their outward normals around that bearing if the case geometry allows. Check both faces with an inclinometer and compass set to true. V3 has one fitted panel; v1 has three with unverified angles. Cases 10 and 11 have external 5 W pass-throughs. Panel nameplate current alone cannot establish winter charging.')
    b.p('At each tree, sight the solstice arc from panel height. Mark branch or trunk shade at the beginning, middle and end of the listed window. Check snow shedding and log panel input, battery temperature, voltage and overnight draw across an actual storm cycle before relying on autonomy.')
    b.p('Far-horizon rays stop at the regional DEM edge where it falls within 30 km. Near-field terrain gets finer sampling. A single regional climatology and approximate sky-view factor limit orientation precision to a practical range around the listed bearing.',8.5)
    b.end()
    for index,k in enumerate(active):
        s=sites[k];station=k in r['gateways'];solar=s['solar'];alt=r['alternatives'].get(k)
        b.begin('Station gateway' if station else f'Repeater field sheet  /  {order.index(k)+1} of 9',navigation_name(k),
                ('Station survey rendezvous. ' if station else 'Search circle 20 m. ')+s['note'])
        b.image(maps.site_image(k),198)
        map_key=[('Member can see this radio','#61ad99','fill')]
        if not station:
            if s['approach'].startswith('mapped'):map_key.append(('Mapped approach','#a95033','line'))
            map_key.extend([('Estimated connector','#a95033','dash'),('20 m search circle','#af502e','point')])
        legend(b,map_key)
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
        b.p('Modeled chain: '+' → '.join(map(field_name,r['paths'][k]))+
            "."+
            (f" Closest equal-or-easier alternative: {navigation_name(alt['easy'])}." if alt else ''),9.2,5)
        if not station:
            step=order.index(k)+1
            before=scen['Direct' if step==1 else f'Order {step-1}']
            after=scen[f'Order {step}']
            b.p(f"Deployment step {step} adds {after['road_km']-before['road_km']:.2f} km of gateway-reachable road and {after['trail_km']-before['trail_km']:.2f} km of trail over the preceding step.",9.2,5)
        if 'nominal_footprint' in s:
            b.p(f"Local pin comparison: individual road footprint {s['nominal_footprint']['road_km']:.2f} km nominal and {s['selected_footprint']['road_km']:.2f} km selected. Routing and weighted member coverage also influence the choice.",8.3,4)
        b.p(f"Winter solar: face {solar['az']}° true at {solar['tilt']}° above horizontal. December-only optimum {solar['dec_az']}° / {solar['dec_tilt']}°. Check branches at the actual fitted panel.",9.1,5)
        b.table(list(solar['windows']),[list(solar['windows'].values())],[90]*6,7.8)
        b.p('Field selection: use a stable tree or approved mount with the radio path clear at antenna height. Map precision is a navigation aid; allow the full search radius and re-test a moved mount. Record actual AGL, coordinate and dated two-way observations.',8.3)
        b.end()
    field_and_sources(b,root,cfg,r)


def field_and_sources(b,root,cfg,r):
    s={v['id']:v for v in r['sites']}
    b.begin('Model notes','Terrain, routing and uncertainty','The rankings compare feasible paths through sampled bare earth. No deployment reception, clearance of vegetation, winter parking inspection or battery-runtime test occurred in this study.')
    b.h('Terrain and footprints')
    b.p('Six USGS NV_Southern_D23 1 m bare-earth lidar tiles cover the mountain. Source NAD83 / UTM zone 11N, NAVD88 orthometric metres. A 1/3 arc-second NAD83 geographic tile n37w116 (2026-06-10 file) extends the terrain toward the valley. Continuous reprojection uses bilinear interpolation; the local model uses a 5 m working grid and the regional horizon/valley uses 20 m. Raw metadata dates, bounds and checksums are in inputs/sources.json. [1,2]')
    b.p('Local member rays are tested at ≤5 m intervals with Earth radius multiplied by 4/3. Ground is bilinearly interpolated. Road/trail intersections use segment midpoints at ≤40 m. Land uses 80 m cell centers, independent of road samples. Backbone edges use native 1 m surfaces at ≤1 m intervals and the regional extension outside tile coverage. The DEM extends beyond the reporting polygon.')
    b.h('Candidate search and route definition')
    b.p(f"Search {len(s)} station/candidate locations including 7 full-road shoulder searches. New stop-centered candidates use a 250 m terrain search; each nominal repeater then uses a 20 m circle sampled at 5 m with road, roof, mapped helipad, walking-surface and steep-slope exclusions. A score combines sample visibility, gateway attachment and other infrastructure edges. Station shifts remain zero. Distinguishable micro-topography can still hide a tree, cliff edge or building.")
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
        ('13','Nevada DOT state-maintained highway description index','https://www.dot.nv.gov/home/showpublisheddocument/23124/638718361041470000'),
        ('14','UK Government Analysis Function, chart and small-multiple guidance','https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/'),
        ('15','ColorBrewer, choosing color schemes for maps','https://colorbrewer2.org/learnmore/schemes.html')]
    for idx,label,url in sources:
        b.text(36,b.y-9,idx,8,b.bold,TEAL);b.text(57,b.y-9,label,9,b.font)
        b.c.linkURL(url,(55,b.y-12,574,b.y+1),relative=0);b.y-=18
    b.h('Project records')
    b.p('PROJECT.md and records/deployment-nodes.md govern equipment identity and mission. records/inventory.md and docs/hardware/enclosures.md describe fitted panels. The R001 commissioning, B003 member, screenless gateway and airtime-sniffer records support the radio assumptions. Nine board-level RAK passes and a held R003 are recorded; the field labels in this atlas assign no devices.')
    b.h('Offline files')
    b.p('navigation.gpx contains selected mounts, staging points and the alternate Angel Peak drive-up test. Use the AM stage and AV drive-up test for the two supplied vehicle coordinates. gis/ contains WGS84 GeoJSON and projected GeoTIFFs. tables/results.json holds every tested link, height and route comparison. tables/profiles/ holds terrain and Fresnel data. inputs/study.json controls the next run.')
    b.p('For a field correction, retain packet IDs and anonymous measured results privately. Update the editable inputs with surveyed ground point, antenna AGL and access evidence; regenerate the model and compare the same road, trail and facility denominators.')
    b.end()
    candidates=[v for v in r['sites'] if v['id'] not in r['gateways']]
    for page in range(0,len(candidates),17):
        b.begin('Candidate register','Mounting-point comparisons','All candidate radios use 4 m AGL. Road km here are individual terrain footprints. An isolated radio can see a road without delivering its packets to either station.')
        subset=candidates[page:page+17]
        b.table(['Code / location','Nominal WGS84','Selected WGS84','Offset m','Road km nominal / selected'],
                [[navigation_name(v['id']),ll(v['nom_ll']),ll(v['ll']),f"{v['shift']:.0f}",f"{v['nominal_footprint']['road_km']:.1f} / {v['selected_footprint']['road_km']:.1f}"] for v in subset],
                [138,124,124,50,104],8)
        b.p('Supplied sites retain the original nominal pin. For new candidates the nominal point comes from a terrain search near a mapped stop or from road-corridor sampling. The table gives the subsequent 20 m refinement. Exact trees and physical radio assignments are field decisions.')
        b.end()
