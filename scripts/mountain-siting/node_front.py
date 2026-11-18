"""Report front matter, labeled mountain networks and five matched metropolitan viewsheds."""
from itertools import combinations
from collections import Counter
from node_model import *
from node_cartography import *
from node_chapters import region, SHED_PALETTE
from node_drawing import *
from reportlab.lib.colors import HexColor, white

NETRECT=(26,75,499,416)
INSET=(535,146,278,293)
NAMES={UP:"Upper Bristlecone",MACK:"Mack’s alternative",ESC:"Escarpment trail"}
OFF={UP:(-4,-18),LEE:(-9,11),MACK:(-8,12),SHOW:(-8,-16),SHADY:(15,5),ESC:(23,-17),CAT:(-4,-18),KYLE:(-19,11)}
ANG_POS={SCOUTS[3]:(.27,.91),SCOUTS[1]:(.67,.74),SCOUTS[2]:(.23,.57),SCOUTS[0]:(.26,.26),ANGEL:(.77,.095)}
TOC_FRONT=[("All study nodes",2),("Potential links and field evidence",3),("Coordinate and purpose directory",5),
           ("Executive summary",6),("Deployed and shortlist coverage",7),("Shady forwarding trial",8),
           ("Four separate scout scenarios",9)]
OV_COLORS={"Strong":"#00786A","Marginal":"#AE6A13","Recorded":"#A52670"}


def cover(c,links):
    fillbox(c,0,0,W,H,"#143A3C")
    rect=(413,0,W-413,H)
    bounds=extent_for([xy[s] for s in SITES],rect[2]/rect[3],.14)
    # An unlabelled relief illustration belongs only on this title page.
    mapbounds=extent_for([xy[SCOUTS[2]],xy[SHOW],xy[ESC]],rect[2]/rect[3],.2)
    mountain(c,rect,mapbounds,wpx=1650)
    fillbox(c,400,0,13,H,"#B9BE9A")
    txt(c,34,541,"SNORR  /  MESHLINK",11,"Bold","#C7DFCE")
    txt(c,34,445,"Mount Charleston",33,"Serif","#FFFFF5")
    txt(c,34,398,"repeater study",34,"Serif","#FFFFF5")
    txt(c,35,347,"Node coverage and direct radio paths",14,"Sans","#DCEDDC")
    para(c,35,288,"A field planning report for passive member GPS delivery to Lee Fire and fixed outdoor radio coverage across the Las Vegas Valley.",327,13,21,"#F0F4E9")
    rule(c,35,185,367,"#789B8F")
    txt(c,35,161,"PREPARED FOR",8,"Bold","#BDDAC9")
    txt(c,35,140,"SNORR MeshLink field team",13,"Sans","#FFFDF1")
    txt(c,35,108,"PREPARED BY",8,"Bold","#BDDAC9")
    txt(c,35,88,"Codex for SNORR MeshLink",12,"Sans","#FFFDF1")
    txt(c,35,54,"18 November 2026   ·   Survey waypoints dated 17 November",9,"Sans","#E0EEDC")
    fillbox(c,433,25,367,53,"#FBFAF2")
    txt(c,446,55,"13 study sites   /   78 physical links   /   156 directional profiles",10,"Bold",TEAL)
    txt(c,446,37,"Open contents  p. 4                  Open executive summary  p. 6",9,"Sans",INK)
    link(links,441,28,142,20,4);link(links,608,28,178,20,6)


def draw_edges(c,rect,bounds,sites,valid=None):
    for typ in ("Strong","Marginal","Recorded"):
        for a,b in combinations(sites,2):
            group=rating(a,b)
            if group=="Blocked" and observed(a,b):group="Recorded"
            if group!=typ:continue
            p,q=project(xy[a],bounds,rect),project(xy[b],bounds,rect)
            line(c,p,q,"#FAFAF1",2.9)
            line(c,p,q,OV_COLORS[typ],1.3,{"Strong":None,"Marginal":[6,3],"Recorded":[1.7,3]}[typ])


def labelsite(c,xy0,end,name,anch="center",size=8.3):
    line(c,xy0,end,"#59665D",.7)
    tag(c,end[0],end[1],name,anch,size,strong=True)


def overview(c,links,showlinks):
    n=3 if showlinks else 2
    start(c,n,"Study maps   /   Mountain network","Potential direct links" if showlinks else "All study nodes",
          "The inset separates five closely spaced Angel Peak sites. Page 5 lists their coordinates, purposes and chapters.")
    bounds=extent_for([xy[s] for s in SITES],NETRECT[2]/NETRECT[3],.17)
    mountain(c,NETRECT,bounds,wpx=2150)
    if showlinks:draw_edges(c,NETRECT,bounds,SITES)
    detail_labels(c,NETRECT,bounds)
    for k in SITES:
        if k in REGIONAL:continue
        p=project(xy[k],bounds,NETRECT);dx,dy=OFF[k]
        end=(p[0]+dx,p[1]+dy)
        align="left" if k in (SHADY,ESC) else "right" if k==KYLE else "center"
        labelsite(c,p,end,NAMES.get(k,k),align)
        mark(c,p,shape="diamond" if k==LEE else "circle")
    pts=[project(xy[k],bounds,NETRECT) for k in REGIONAL]
    center=np.mean(pts,axis=0)
    c.setStrokeColor(HexColor("#234D4B"));c.setLineWidth(.8);c.setDash([2,2])
    c.rect(min(p[0] for p in pts)-4,min(p[1] for p in pts)-4,
           max(p[0] for p in pts)-min(p[0] for p in pts)+8,max(p[1] for p in pts)-min(p[1] for p in pts)+8)
    c.setDash([])
    for p in pts:mark(c,p,radius=2.4)
    tag(c,center[0]-18,center[1]+15,"Angel Peak  →  inset","right",7.8,strong=True)
    frame(c,NETRECT,bounds)
    txt(c,535,473,"Angel Peak detail",15,"Serif")
    txt(c,535,453,"One deployed radio and four road scouts",9,"Sans",SOFT)
    bounds=extent_for([xy[k] for k in REGIONAL],INSET[2]/INSET[3],.38)
    mountain(c,INSET,bounds,wpx=1410)
    if showlinks:draw_edges(c,INSET,bounds,REGIONAL)
    for k in REGIONAL:
        p=project(xy[k],bounds,INSET);u,v=ANG_POS[k]
        end=(INSET[0]+u*INSET[2],INSET[1]+v*INSET[3])
        labelsite(c,p,end,k,size=8)
        mark(c,p,"#153D40" if k==ANGEL else "#846627",radius=3.8)
    frame(c,INSET,bounds)
    if showlinks:
        for i,(kind,label) in enumerate([("Strong","At least 60% first Fresnel clearance"),("Marginal","Terrain clear, less than 60% Fresnel"),("Recorded","Observed through terrain obstruction")]):
            y=124-i*19
            line(c,(536,y+2),(563,y+2),OV_COLORS[kind],2,{"Strong":None,"Marginal":[6,3],"Recorded":[1.7,3]}[kind])
            txt(c,572,y,label,8.6)
        txt(c,30,55,"Each remaining blocked pair has a profile in both directions. Inter-scout lines describe portable tests between alternative sites.",8.8)
    else:
        para(c,535,122,"The road sites are alternative survey positions. Access and usable antenna mounts need on-site confirmation.",266,9.2,14)
        txt(c,30,54,"Diamond = Lee Fire gateway. Mountain site names refer to the supplied pins. The road sites were derived from the terrain search.",8.7)
    nav(c,links)


def contents(c,links):
    start(c,4,"Report navigation","Table of contents","Select a chapter or section. Each node chapter starts with its brief, then its viewshed and twelve direct path profiles.")
    txt(c,33,470,"Study maps and findings",14,"Bold",TEAL)
    rows=TOC_FRONT+[(f"Valley viewshed · {k}",i) for i,k in enumerate(REGIONAL,10)]
    for i,(s,p) in enumerate(rows):
        y=437-i*28;txt(c,34,y,s,10.2);txt(c,365,y,p,10.2,"Bold",TEAL,True);rule(c,33,y-8,367);link(links,31,y-7,336,23,p)
    txt(c,408,470,"Node chapters",14,"Bold",TEAL)
    for i,k in enumerate(SITES):
        y=437-i*28;startp=psite(k)
        txt(c,409,y,CODE[k],9.5,"Bold",TEAL);txt(c,447,y,k,10.5)
        txt(c,803,y,f"{startp}–{startp+13}",10.2,"Bold",TEAL,True);rule(c,408,y-8,804);link(links,407,y-7,397,23,startp)
    nav(c,links)


def directory(c,links):
    start(c,5,"Report navigation","Node directory","WGS84 decimal degrees. Select a row to open the chapter. AGL heights are model inputs above local ground.")
    purpose=["Lee Canyon relay","Dispatch gateway","Lee backbone trial","South-side trial","Recorder / relay trial",
             "Footway trial","South-side control","Mountain-facing trial","Valley-side control","Kyle-side control",
             "Showgirl / Escarpment trial","Mack’s / valley trial","Mack’s / A5 trial"]
    notes=["Deployed R010","G001 · 1 m AGL","Owner pin · 4 m","Owner pin · 4 m","G002 · offline",
           "Owner pin · 4 m","Deployed R001","Access unconfirmed","Deployed R005","Deployed R008",
           "Access unconfirmed","Access unconfirmed","Access unconfirmed"]
    rows=[]
    for k,p,note in zip(SITES,purpose,notes):
        a,b=lonlat(k);pn=psite(k)
        rows.append([CODE[k],k,f"{a:.5f}, {b:.5f}",p,note,f"{pn}–{pn+13}"])
    mids=table(c,["ID","Node","Latitude, longitude","Purpose","Field note","Pages"],[38,150,139,164,157,88],rows,32,481,26,9.1)
    for k,y in zip(SITES,mids):link(links,31,y-7,737,23,psite(k))
    txt(c,33,90,"Every non-gateway site uses a nominal 4 m antenna. Coordinates locate the study pin; record the actual test position and mount height.",9.1)
    nav(c,links)


def executive(c,links):
    s=SCOUTS[2];case=CASES[s]
    start(c,6,"Study findings","Executive summary","Primary objective: a member GPS fix reaching Lee Fire within three radio forwarders.")
    for x,num,title in [(34,f"{DEPLOYED['scores']['Highway']:.1f}%","Highway reachable · deployed"),
                        (302,f"{case['scores']['Highway']:.1f}%","Highway reachable · survey 5 case"),
                        (580,f"{case['area']:.2f} km²","Terrain reachable · survey 5 case")]:
        summary_stat(c,x,444,num,title)
    def section(x,y,h,body):
        txt(c,x,y,h,13,"Bold",TEAL);para(c,x,y-23,body,353,10.7,16)
    section(34,372,"First field decision","Test a 4 m portable at Mack’s against Upper Bristlecone, then have a member tracker send an ordinary GPS packet. Match its fix and receipt at Lee before relying on the mountain route.")
    section(422,372,"Which Angel scout to carry","Survey 5 provides the largest modeled member highway reach of the four one-scout cases. Surveys 1, 3 and 6 have different mountain neighbors and fixed-radio valley footprints. Deployed Angel Vegas stays in every scout case.")
    section(34,232,"What Shady changes","G002 heard Cathedral, Angel Vegas and Kyle directly through modeled obstructions. Enabling forwarding and admitting all three links adds zero eligible highway in these four cases. Shady still needs more forwarding steps to reach Lee, or a new link.")
    section(422,232,"Where coverage still falls short",f"Survey 5 reaches {case['scores']['SR 156']:.1f}% of SR 156, {case['scores']['SR 157']:.1f}% of SR 157 and {case['scores']['SR 158']:.1f}% of SR 158. Whole-valley maps assume a fixed outdoor receiver at 4 m. A field receipt is needed to establish radio delivery.")
    rule(c,34,118,807)
    areas=[]
    for k in REGIONAL:
        with rasterio.open(CACHE/(k+"-valley.tif")) as ds:
            areas.append(f"{CODE[k]}  {ds.read(1).sum()*abs(ds.transform.a*ds.transform.e)/1e6:,.0f}")
    txt(c,34,139,"Fixed-radio area across the full regional map (km²)     "+"     ·     ".join(areas),9.0,"Bold",TEAL)
    txt(c,34,92,"78 physical pairs",11,"Bold")
    count=Counter(rating(a,b) for a,b in combinations(SITES,2))
    txt(c,163,92,f"{count['Strong']} strong   ·   {count['Marginal']} marginal   ·   {count['Blocked']} terrain-blocked, including three directly recorded Shady links",10)
    txt(c,34,62,"Scouts are candidate test positions. The source waypoint set is dated 17 November 2026; deployment and SD evidence are identified in the chapters.",8.6)
    nav(c,links)


def netmap(c,rect,record,label,caption,receivers):
    bounds=region(rect);mask=record["zone"]
    ov=overlay_file("net",mask.astype("uint8"),SHED_PALETTE)
    mountain(c,rect,bounds,ov,wpx=1810,mode="shade");study_edge(c,rect,bounds);detail_labels(c,rect,bounds)
    for k in receivers:
        p=project(xy[k],bounds,rect);mark(c,p,shape="diamond" if k==LEE else "circle",radius=3)
    if "Shady" in label:
        p=project(xy[SHADY],bounds,rect);mark(c,p,"#98366F",radius=3.8);tag(c,p[0],p[1]-12,"Shady",size=7,strong=True)
    frame(c,rect,bounds)
    txt(c,rect[0],466,label,14,"Bold",TEAL)
    txt(c,rect[0],133,f"{record['area']:.2f} km²    /    {record['km']:.2f} km of highway",11,"Bold")
    txt(c,rect[0],113,caption,8.9,"Sans",SOFT)


def comparison(c,links,shady):
    n=8 if shady else 7;s=SCOUTS[2]
    left=CASES[s] if shady else DEPLOYED;right=TRIALS[s] if shady else CASES[s]
    heading="Can Shady close the forwarding gap?" if shady else "Where member GPS can reach Lee Fire"
    sub=("Shady’s trial enables forwarding and admits both terrain-clear and directly recorded radio paths in one estimate." if shady else
         "Teal cells can reach Lee Fire directly or through an eligible relay. Dark dots mark eligible radios. The diamond marks Lee Fire.")
    start(c,n,"Network viewsheds",heading,sub)
    for i,(rec,label,cap) in enumerate([(left,"Shady recording only" if shady else "Documented deployment","Three-forwarder limit · 1.2 m member"),
                   (right,"Shady forwarding trial" if shady else "Shortlist with Angel road survey 5","Same boundary, grid and forwarding limit")]):
        netmap(c,(32+i*396,154,380,297),rec,label,cap,rec["routes"])
    msg=("In the survey 5 trial, the shortest path from Shady to Lee uses five radio links via Escarpment, survey 5, Mack’s and Upper. A tracker first heard at Shady needs five forwarders; the budget is three. The two footprints therefore coincide." if shady else
         "The deployed reference includes installed Angel Mountain and Lee Junction. The shortlist uses the named sites, retains Angel Vegas and evaluates one Angel road scout at a time. Shady remains an offline recorder here.")
    para(c,33,86,msg,765,10.1,15)
    nav(c,links)


def scenario_table(c,links):
    start(c,9,"Network comparison","Four separate Angel scout trials",
          "Each row gives one scout with the seven common relays. Shady is an offline receiver until the separate forwarding trial.")
    arr=[]
    for k in SCOUTS:
        rec=CASES[k];trial=TRIALS[k];sc=rec["scores"]
        arr.append([k,f"{rec['area']:.2f}",f"{rec['km']:.2f}",*[f"{sc[road]:.1f}%" for road in ("Highway","SR 156","SR 157","SR 158")],f"{trial['scores']['Highway']:.1f}%"])
    table(c,["Scout","Area km²","Road km","All roads","SR 156","SR 157","SR 158","Shady trial¹"],[151,79,77,90,80,80,80,118],arr,32,467,31,9.5)
    txt(c,33,281,"Common relays and equipment assumptions",12,"Bold",TEAL)
    para(c,33,259,"Upper Bristlecone, Mack’s alternative, Showgirl, Escarpment trail, Cathedral Rock, deployed Angel Vegas and Kyle Junction are present in each shortlist case. One road scout gives eight relay positions. The Shady trial adds a ninth forwarding position; installed G002 currently records offline.",755,10.3,15)
    txt(c,33,189,"Reading the estimates",12,"Bold",TEAL)
    para(c,33,168,"¹ Shady trial shows total highway coverage with recorded Shady links admitted and forwarding enabled. Percentages use 39.61 km of independently distance-weighted road samples. The terrain area uses 35 m mountain cells centered inside the common study boundary. Overlap between two site viewsheds alone does not establish a direct backbone path.",755,10.1,14)
    para(c,33,101,"Model: 910.625 MHz with 4/3 effective Earth radius. Mountain profiles use native 1 m terrain with mosaic fallback. Strong paths clear 60% of the first Fresnel zone. Member rays use a 1.2 m tracker. Field acceptance requires a matched member fix under 15 minutes old at Lee Fire.",755,9.2,13)
    txt(c,33,56,"Sources",8.5,"Bold")
    for x,title,url in [
        (84,"USGS 3DEP elevation","https://www.usgs.gov/3d-elevation-program"),
        (230,"OpenStreetMap cartography","https://www.openstreetmap.org/copyright"),
        (407,"Deployment and Shady SD evidence","https://github.com/lfg-seth/snorr-meshlink/blob/8b0f030/docs/research/mountain-siting-20261117.md#preferred-full-layout")]:
        txt(c,x,56,title,8.5,"Bold",TEAL)
        c.linkURL(url,(x,52,x+c.stringWidth(title,"Bold",8.5),66),relative=0,thickness=0)
    nav(c,links)


def valley(c,links,k,n):
    start(c,n,"Regional viewsheds   /   Fixed outdoor receiver",k+"   /   Las Vegas Valley",
          "Same full-valley frame on all five maps. Both ends use 4 m above ground. Color shows direct bare-earth visibility to this Angel site.")
    path,bb=metro_base()
    width=431*(bb[2]-bb[0])/(bb[3]-bb[1])
    rect=(27+(625-width)/2,66,width,431)
    bounds=bb
    with rasterio.open(CACHE/(k+"-valley.tif")) as ds:
        arr=ds.read(1);ox=tuple(ds.bounds)
    ov=overlay_file("valley-"+CODE[k],arr,[(0,0,0,0),(3,123,111,161)])
    fillbox(c,*rect,"#F0F0E6");clip(c,rect);projected_image(c,path,bounds,rect,bb);projected_image(c,ov,bounds,rect,ox);c.restoreState()
    pos=project(xy[k],bounds,rect);mark(c,pos,"#85326A",radius=5);tag(c,pos[0]+5,pos[1]+9,"Angel Peak","left",8.5,strong=True)
    # Place-name annotations only; these are not survey or reception samples.
    for text,lon,lat in [("Mount Charleston",-115.668,36.248),("North Las Vegas",-115.131,36.235),
                         ("Las Vegas",-115.154,36.167),("Summerlin",-115.324,36.178),("Spring Valley",-115.262,36.086),
                         ("Henderson",-114.986,36.032),("Boulder Hwy",-115.047,36.088)]:
        p=project(forward.transform(lon,lat),bounds,rect);tag(c,*p,text,size=7.5)
    frame(c,rect,bounds)
    txt(c,669,457,"Fixed-radio",16,"Serif");txt(c,669,435,"visibility",16,"Serif")
    fillbox(c,669,391,12,10,"#398F83");txt(c,687,391,"Terrain clear",8.9)
    fillbox(c,669,367,12,10,"#CBCFC3");txt(c,687,367,"Terrain shadow",8.9)
    txt(c,669,318,"Area shown clear",9,"Bold",TEAL)
    txt(c,669,292,f"{arr.sum()*.12**2:,.0f} km²",17,"Bold")
    para(c,669,264,"Includes mountains and developed areas throughout the mapped rectangle.",139,9.2,13)
    para(c,669,189,"120 m map cells. Each ray samples the regional 20 m terrain grid. Buildings, trees and receiver sensitivity are unmodeled.",137,9.2,13)
    txt(c,669,82,f"Node brief  p. {psite(k)}",9.2,"Bold",TEAL);link(links,665,75,138,18,psite(k))
    nav(c,links)


def front():
    c=canvas.Canvas(str(CACHE/"front.pdf"),pagesize=(W,H),pageCompression=1)
    actions=[(cover,()),(overview,(False,)),(overview,(True,)),(contents,()),(directory,()),(executive,()),
             (comparison,(False,)),(comparison,(True,)),(scenario_table,())]
    actions += [(valley,(k,i)) for i,k in enumerate(REGIONAL,10)]
    records=[]
    for fn,args in actions:
        links=[]
        if args:fn(c,links,*args)
        else:fn(c,links)
        c.showPage();records.append(links)
    c.save();(CACHE/"front.json").write_text(json.dumps(records),encoding="utf8")


if __name__=="__main__":
    front()
