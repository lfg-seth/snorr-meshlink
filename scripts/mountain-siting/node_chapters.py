"""Each chapter keeps its own site at A, including every blocked and reciprocal path."""
import json
import math
from node_model import *
from node_cartography import (clipped_overlay,close_pair_overlay,detail_labels,extent_for,frame,line,mark,mountain,overlay_file,
                             project,study_edge,tag)
from node_drawing import *
from reportlab.lib.colors import HexColor

SHED_PALETTE=[(0,0,0,0),(0,118,108,187)]
PAIR_PALETTE=[(0,0,0,0),(224,144,36,131),(65,139,191,132),(22,125,100,175)]


def region(rect):
    l,b,r,t=EXTENT
    return extent_for([(l,b),(r,t)],rect[2]/rect[3],0)


def status(a,b):
    if observed(a,b) and rating(a,b)=="Blocked":return "Blocked / recorded"
    return rating(a,b)


def source(k):
    return "Generated road shoulder" if k in SCOUTS else "Supplied survey waypoint"


def summary(c,k,links):
    n=psite(k)
    role,purpose,context,test=SITE_INFO[k]
    start(c,n,"Node "+CODE[k]+"   /   Site brief",k+"   /   Site brief",purpose+"   ·   "+role)
    rect=(32,228,340,262)
    bounds=extent_for([xy[k]],rect[2]/rect[3],min_span=1200 if k in REGIONAL else 1600)
    mountain(c,rect,bounds,wpx=1570)
    pos=project(xy[k],bounds,rect)
    mark(c,pos,shape="diamond" if k==LEE else "circle",radius=5)
    tag(c,pos[0],pos[1]+10,k, size=9,strong=True)
    frame(c,rect,bounds)
    lat,lon=lonlat(k)
    txt(c,32,210,f"{lat:.5f}, {lon:.5f}   ·   WGS84   ·   antenna {wh(k)} m above ground",9.3,"Bold")
    txt(c,32,192,source(k),9,"Sans",SOFT)
    txt(c,32,164,"Site context",11,"Bold",TEAL)
    para(c,32,146,context,338,9.6,13.7)
    txt(c,32,97,"Field check",11,"Bold",TEAL)
    para(c,32,80,test,343,9.2,12.8)
    txt(c,393,480,"Direct sister nodes",13,"Bold",TEAL)
    txt(c,393,462,"Select a row to open this node’s A-first profile.",9,"Sans",SOFT)
    rows=[]
    for b in neighbors(k):
        rows.append([b,f"{math.dist(xy[k],xy[b])/1000:.2f}",status(k,b),str(ppath(k,b))])
    mids=table(c,["Sister B","km","Terrain / evidence","Page"],[142,42,151,60],rows,390,445,23,8.6)
    for b,y in zip(neighbors(k),mids):link(links,390,y-6,395,21,ppath(k,b))
    txt(c,392,118,"Strong ≥60% first Fresnel clearance. Marginal = positive terrain",8.8)
    txt(c,392,104,"clearance below 60%. Recorded = direct reception in the field.",8.8)
    txt(c,392,69,f"Open single-site viewshed   →   p. {n+1}",10,"Bold",TEAL)
    link(links,390,62,240,19,n+1)
    nav(c,links)


def single(c,k,links):
    n=psite(k)+1
    start(c,n,"Node "+CODE[k]+"   /   Direct member visibility",k+"   /   Single-site viewshed",
          "Bare-earth line of sight to a 1.2 m member antenna across the mountain study area.")
    rect=(32,58,520,436);bounds=region(rect)
    mask=view(k)&INSIDE
    ov=overlay_file("site-"+CODE[k],mask.astype("uint8"),SHED_PALETTE)
    mountain(c,rect,bounds,ov,wpx=1950,mode="shade")
    study_edge(c,rect,bounds)
    detail_labels(c,rect,bounds);pos=project(xy[k],bounds,rect)
    mark(c,pos,shape="diamond" if k==LEE else "circle",radius=4.5)
    tag(c,pos[0],pos[1]+10,k,size=8,strong=True);frame(c,rect,bounds)
    summary_stat(c,575,444,f"{mask.sum()*AREA:.2f} km²","Directly visible mountain terrain")
    summary_stat(c,575,369,f"{roadkm(masks[ix[k]]):.2f} km","Directly visible sampled highway")
    fillbox(c,575,303,13,10,"#177F75");txt(c,596,303,"Visible to the marked site",9.8)
    fillbox(c,575,278,13,10,"#D8DCD2");txt(c,596,278,"Terrain shadow within study area",9.8)
    para(c,575,232,"The map shows a member’s first hop. Delivery to dispatch also requires an eligible forwarding route to Lee Fire.",226,10.1,15.5)
    lat,lon=lonlat(k)
    txt(c,575,145,f"{lat:.5f}, {lon:.5f}",11,"Bold")
    txt(c,575,123,f"Site antenna {wh(k)} m AGL   ·   map cells 35 m",9.1)
    txt(c,575,80,f"Site brief  p. {n-1}    /    First path  p. {n+1}",9,"Bold",TEAL)
    link(links,573,72,85,21,n-1);link(links,662,72,92,21,n+1)
    nav(c,links)


def chart(c,rect,a,b):
    d,z,los,f=profile.trace(coords(a),coords(b))
    if not np.isfinite(z).all():raise ValueError((a,b))
    vi=int(np.argmin((los-z)[1:-1]))+1
    minz=min(z.min(),(los-.6*f).min());maxz=max(z.max(),(los+.6*f).max())
    pad=max(3,(maxz-minz)*.09);lo=minz-pad;hi=maxz+pad
    x,y,w,h=rect
    tx=lambda dx:x+w*dx/d[-1]
    ty=lambda zz:y+h*(zz-lo)/(hi-lo)
    for i in range(4):
        elev=lo+(hi-lo)*(i+1)/5;ly=ty(elev)
        line(c,(x,ly),(x+w,ly),"#D3DBD7",.5);txt(c,x-4,ly-2,f"{elev:.0f}",7,"Sans",SOFT,True)
    ii=np.unique(np.r_[np.linspace(0,len(d)-1,min(800,len(d)),dtype=int),vi])
    def shape(xs,ys,color):
        p=c.beginPath();p.moveTo(xs[0],ys[0])
        for px,py in zip(xs[1:],ys[1:]):p.lineTo(px,py)
        p.close();c.setFillColor(HexColor(color));c.drawPath(p,fill=1,stroke=0)
    xs=tx(d[ii]);gz=ty(z[ii]);lower=ty(los[ii]-.6*f[ii]);upper=ty(los[ii]+.6*f[ii])
    shape(np.r_[xs,x+w,x],np.r_[gz,y,y],"#A8B4A8")
    c.saveState();c.setFillAlpha(.57);shape(np.r_[xs,xs[::-1]],np.r_[lower,upper[::-1]],"#86B8D1");c.restoreState()
    line(c,(x,ty(los[0])),(x+w,ty(los[-1])),"#B32369",1.7)
    for dx,s in ((0,"A"),(-1,"B")):
        pt=(tx(d[dx]),ty(los[dx]));mark(c,pt,"#92245D",radius=4)
        tag(c,pt[0]+(8 if dx==0 else -8),min(y+h-7,pt[1]+5),s,size=7,strong=True)
    for frac in (0,.5,1):
        txt(c,x+w*frac-(10 if frac else 0),y-12,f"{frac*d[-1]/1000:.2f}",6.9)
    txt(c,x+78,y-24,"Distance from A (km)",8,"Sans",SOFT)
    return float((los-z)[vi]),float(((los-z)[1:-1]/f[1:-1]).min()),d[vi]/1000


def direct(c,a,b,links):
    n=ppath(a,b); rev=ppath(b,a)
    start(c,n,"Node "+CODE[a]+"   /   Viewshed and direct path",a+"   to   "+b,
          "A is the chapter site. The map shows member visibility at 1.2 m. The profile tests the direct antenna path.")
    rect=(32,106,398,383)
    bounds=extent_for([xy[a],xy[b]],rect[2]/rect[3],.23,min_span=120)
    classes=(view(a).astype("uint8")+2*view(b).astype("uint8"))*INSIDE
    spacing=35
    if bounds[2]-bounds[0]<1500:
        ov,overlay_bounds,spacing=close_pair_overlay(a,b,bounds,PAIR_PALETTE)
    else:
        ov,overlay_bounds=clipped_overlay(classes,bounds,PAIR_PALETTE)
    mountain(c,rect,bounds,ov,wpx=1750,overlay_bounds=overlay_bounds);detail_labels(c,rect,bounds)
    pt,qt=(project(xy[k],bounds,rect) for k in (a,b))
    line(c,pt,qt,"#fffef9",4);line(c,pt,qt,"#9A245B",2.1)
    for k,other,ident in ((a,b,"A"),(b,a,"B")):
        pos=project(xy[k],bounds,rect)
        mark(c,pos,"#97215D","circle" if ident=="A" else "diamond",5.3)
        dy=11 if xy[k][1]>=xy[other][1] else -16
        ax=min(rect[0]+rect[2]-57,max(rect[0]+57,pos[0]))
        tag(c,ax,pos[1]+dy,ident+"   "+k,size=8.2,strong=True)
    frame(c,rect,bounds)
    for xx,col,s in [(32,"#D99A40","A only"),(113,"#6496BF","B only"),(190,"#348473","Both visible")]:
        fillbox(c,xx,84,11,8,col);txt(c,xx+16,84,s,8.7)
    txt(c,423,84,f"{spacing:g} m cells",8.5,"Sans",SOFT,True)
    la,oa=lonlat(a);lb,ob=lonlat(b)
    txt(c,32,62,f"A   {la:.5f}, {oa:.5f}       B   {lb:.5f}, {ob:.5f}",8.6)
    txt(c,460,475,"Terrain profile",13,"Bold",TEAL)
    txt(c,802,475,"Elevation (m)",8,"Sans",SOFT,True)
    clear,f1,at=chart(c,(486,331,309,120),a,b)
    txt(c,460,281,"Direct antenna path",12,"Bold",TEAL)
    txt(c,460,260,status(a,b),13,"Bold",COLORS["Recorded" if observed(a,b) else rating(a,b)])
    txt(c,460,239,f"{math.dist(xy[a],xy[b])/1000:.2f} km   ·   {wh(a)} m at A   /   {wh(b)} m at B",9.6)
    txt(c,460,221,f"Minimum terrain clearance {clear:+.2f} m at {at:.2f} km from A.",9.6)
    txt(c,460,203,("Terrain intersects the ray." if f1<0 else f"Minimum first Fresnel clearance {100*f1:.0f}%."),9.6)
    if observed(a,b):
        msg="Field record: Shady received this sister radio directly; the sister also reported hearing G002. Forwarding remains a trial."
    else:
        msg="Evidence: terrain model. No direct field receipt is cited for this pair in the study record."
    para(c,460,180,msg,338,9,12.7)
    shared=masks[ix[a]]&masks[ix[b]]
    txt(c,460,133,f"Member overlap   {roadkm(shared):.2f} km of highway   /   {((classes==3).sum()*AREA):.2f} km²",9.3,"Bold")
    txt(c,460,108,"Magenta = direct ray     Blue = inner 60% Fresnel zone",8.4)
    txt(c,460,92,"Gray = curvature-adjusted bare earth",8.4)
    txt(c,460,63,f"Reverse profile  p. {rev}      /      {CODE[a]} site brief  p. {psite(a)}",9.1,"Bold",TEAL)
    link(links,457,55,120,19,rev);link(links,586,55,145,19,psite(a))
    nav(c,links)


def chapter(k):
    directory=CACHE/"chapters";directory.mkdir(exist_ok=True,parents=True)
    path=directory/(CODE[k]+".pdf")
    c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
    destinations=[]
    actions=[(summary,(k,)),(single,(k,))]+[(direct,(k,b)) for b in neighbors(k)]
    for fn,args in actions:
        links=[];fn(c,*args,links);destinations.append(links);c.showPage()
    c.save()
    path.with_suffix(".json").write_text(json.dumps(destinations),encoding="utf8")
    print("Rendered chapter:",k,flush=True)


if __name__=="__main__":
    import sys
    for k in SITES:
        if len(sys.argv)==1 or CODE[k] in sys.argv[1:]:chapter(k)
