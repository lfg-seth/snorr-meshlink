"""Labeled mountain maps and two matched valley viewsheds for the favorite-router edition."""
from itertools import combinations
from node_model import *
from node_cartography import *
from node_chapters import region, SHED_PALETTE
from node_drawing import *
from reportlab.lib.colors import HexColor, white

NETRECT=(26,75,499,416)
INSET=(535,146,278,293)
NAMES={UP:"Upper Bristlecone",MACK:"Mack’s alternative",ESC:"Escarpment trail"}
OFF={UP:(-4,-18),LEE:(-9,11),MACK:(0,12),SHADY:(12,7),ESC:(10,-15),CAT:(-5,-16),KYLE_FIRE:(10,9)}
ANG_POS={A5:(.25,.78),ANGEL:(.74,.22)}
TOC_FRONT=[("All study nodes",2),("Combined mountain viewshed",3),("Potential direct links",4),("Coordinate and purpose directory",6)]
OV_COLORS={"Strong":"#00786A","Marginal":"#AE6A13","Recorded":"#A52670"}


def cover(c,links):
    from favorite_cover import draw_cover
    draw_cover(c,links)


def draw_edges(c,rect,bounds,sites,focus=()):
    for typ in ("Strong","Marginal","Recorded"):
        for a,b in combinations(sites,2):
            if focus and a not in focus and b not in focus:
                continue
            group=line_class(a,b)
            if group!=typ:continue
            p,q=project(xy[a],bounds,rect),project(xy[b],bounds,rect)
            line(c,p,q,"#FAFAF1",2.9)
            line(c,p,q,OV_COLORS[typ],1.3,{"Strong":None,"Marginal":[6,3],"Recorded":[1.7,3]}[typ])


def labelsite(c,xy0,end,name,anch="center",size=8.3):
    line(c,xy0,end,"#59665D",.7)
    tag(c,end[0],end[1],name,anch,size,strong=True)


def overview(c,links,n):
    showlinks=n==4
    combined=n==3
    title={2:"All study nodes",3:"Combined mountain viewshed",4:"Potential direct links"}[n]
    sub={2:"The nine-site plan spans Lee Canyon, Kyle Canyon and Angel Peak. Page 6 lists coordinates, roles and chapter pages.",
         3:"Teal marks bare-earth line of sight from a 1.2 m member antenna to at least one study radio. Overlapping cells count once.",
         4:"Each line connects a pair retained for field testing. Open either site chapter for its terrain profile and reception evidence."}[n]
    start(c,n,"Study maps   /   Mountain network",title,sub)
    bounds=region(NETRECT)
    overlay=overlay_file("combined",footprint(SITES).astype("uint8"),SHED_PALETTE) if combined else None
    mountain(c,NETRECT,bounds,overlay,wpx=2150)
    study_edge(c,NETRECT,bounds)
    if showlinks:draw_edges(c,NETRECT,bounds,SITES)
    detail_labels(c,NETRECT,bounds)
    for k in SITES:
        if k in REGIONAL:continue
        p=project(xy[k],bounds,NETRECT);dx,dy=OFF[k]
        end=(p[0]+dx,p[1]+dy)
        align="left" if k in (SHADY,ESC,KYLE_FIRE) else "center"
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
    txt(c,535,453,"Deployed Angel Vegas and proposed survey 5",9,"Sans",SOFT)
    bounds=extent_for([xy[k] for k in REGIONAL],INSET[2]/INSET[3],.38)
    detail,extent=None,EXTENT
    if combined:
        masks0,extent,spacing=local_member_masks(SITES,bounds)
        detail=overlay_file("combined-angel-detail",np.logical_or.reduce(masks0).astype("uint8"),SHED_PALETTE)
    mountain(c,INSET,bounds,detail,wpx=1410,overlay_bounds=extent)
    if showlinks:
        clip(c,INSET)
        draw_edges(c,INSET,bounds,SITES,focus=REGIONAL)
        c.restoreState()
    for k in REGIONAL:
        p=project(xy[k],bounds,INSET);u,v=ANG_POS[k]
        end=(INSET[0]+u*INSET[2],INSET[1]+v*INSET[3])
        labelsite(c,p,end,k,size=8)
        mark(c,p,"#153D40" if k==ANGEL else "#846627",radius=3.8)
    frame(c,INSET,bounds)
    if showlinks:
        for i,(kind,label) in enumerate([("Strong","Strong · at least 60% Fresnel clearance"),("Recorded","Recorded · former G002 at Shady Hollow")]):
            y=122-i*18
            line(c,(536,y+2),(563,y+2),OV_COLORS[kind],2,{"Strong":None,"Recorded":[1.7,3]}[kind])
            txt(c,572,y,label,8.7)
        txt(c,535,83,"Survey 5 links to Mack’s and Escarpment.",8.7)
        txt(c,535,68,"Angel Vegas links to Escarpment and Shady.",8.7)
        txt(c,30,54,"Eight terrain-clear pairs. Shady–Cathedral is marginal and recorded. Retest both historical receptions with the Shady RAK.",9)
    elif combined:
        mask=footprint(SITES)
        highway=roadkm(masks[[ix[k] for k in SITES]].any(axis=0))
        txt(c,535,122,f"{mask.sum()*AREA:.2f} km² of mountain terrain",12,"Bold",TEAL)
        txt(c,535,103,f"{highway:.2f} of {weights[groups=='Highway'].sum()/1000:.2f} highway km  ·  {100*highway/(weights[groups=='Highway'].sum()/1000):.1f}%",9.6,"Bold")
        txt(c,535,84,f"35 m mountain grid · {spacing:g} m Angel detail",8.6,"Sans",SOFT)
        assert set(ROUTES)==set(SITES)
        txt(c,30,54,"All nine sites have a modeled route to Lee Fire under the favorite-router assumption. Packet delivery requires a field check.",8.7)
    else:
        para(c,535,122,"Angel Vegas and survey 5 operate together. Confirm access and a usable mount at the road scout before placement.",266,9.2,14)
        txt(c,30,54,"Diamond = Lee Fire uplink. Circles = seven routers and the G002 forwarding CLIENT at Kyle Fire.",9)
    nav(c,links)


def contents(c,links):
    start(c,5,"Report navigation","Table of contents","Select a chapter or section. Each node chapter starts with its brief, then its viewshed and direct profiles for the mapped neighbors.")
    txt(c,33,470,"Study maps and directory",14,"Bold",TEAL)
    rows=TOC_FRONT+[(f"Valley viewshed · {k}",i) for i,k in enumerate(REGIONAL,7)]
    for i,(s,p) in enumerate(rows):
        y=437-i*28;txt(c,34,y,s,10.2);txt(c,365,y,p,10.2,"Bold",TEAL,True);rule(c,33,y-8,367);link(links,31,y-7,336,23,p)
    txt(c,408,470,"Node chapters",14,"Bold",TEAL)
    for i,k in enumerate(SITES):
        y=437-i*28;startp=psite(k)
        txt(c,409,y,CODE[k],9.5,"Bold",TEAL);txt(c,447,y,k,10.5)
        txt(c,803,y,f"{startp}–{chapter_end(k)}",10.2,"Bold",TEAL,True);rule(c,408,y-8,804);link(links,407,y-7,397,23,startp)
    nav(c,links)


def directory(c,links):
    start(c,6,"Report navigation","Node directory","Select a row for the site brief and direct links. Coordinates use WGS84. Heights are assumed antenna heights above local ground.")
    rows=[]
    for k in SITES:
        a,b=lonlat(k)
        role,purpose,*_=SITE_INFO[k]
        rows.append([CODE[k],k,f"{a:.5f}, {b:.5f}",purpose,role,f"{psite(k)}–{chapter_end(k)}"])
    mids=table(c,["ID","Node","Latitude, longitude","Purpose","Equipment / status","Pages"],[36,134,126,160,219,91],rows,32,481,25,8.8)
    for k,y in zip(SITES,mids):link(links,31,y-7,766,23,psite(k))
    txt(c,33,201,"How the routes are modeled",12,"Bold",TEAL)
    para(c,33,178,"Lee Fire is the sole uplink. A member starts with three hops. The first forward uses one. A router preserves the remaining budget when it forwards a packet received from a favorite neighboring router. The plan assumes reciprocal favorites on every eligible router pair.",755,10,15)
    para(c,33,133,"G002 at Kyle Fire is a forwarding CLIENT. Its rebroadcast costs one hop, and the next router’s rebroadcast also costs one. Both station antennas use 1 m and the seven routers use 4 m. The Shady observations were made with G002 before its proposed move.",755,10,15)
    para(c,33,88,"Terrain follows USGS 3DEP at 910.625 MHz with 4/3 effective Earth radius. Buildings, canopy and channel conditions need field tests. Record the actual mount and match a member GPS fix at Lee Fire.",755,9,13)
    nav(c,links)


def valley(c,links,k,n):
    start(c,n,"Regional viewsheds   /   Fixed outdoor receiver",k+"   /   Las Vegas Valley",
          "Same full-valley frame on both maps. Both ends use 4 m above ground. Color shows direct bare-earth visibility to this Angel site.")
    path,bb=metro_base()
    width=431*(bb[2]-bb[0])/(bb[3]-bb[1])
    rect=(27+(625-width)/2,66,width,431)
    bounds=bb
    with rasterio.open(VALLEY_CACHE/(k+"-valley.tif")) as ds:
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
    actions=[(cover,()),(overview,(2,)),(overview,(3,)),(overview,(4,)),(contents,()),(directory,())]
    actions += [(valley,(k,i)) for i,k in enumerate(REGIONAL,7)]
    records=[]
    for fn,args in actions:
        links=[]
        if args:fn(c,links,*args)
        else:fn(c,links)
        c.showPage();records.append(links)
    c.save();(CACHE/"front.json").write_text(json.dumps(records),encoding="utf8")


if __name__=="__main__":
    front()
