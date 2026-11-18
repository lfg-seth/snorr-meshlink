"""Georeferenced topography, vector annotations and full-metro map layers for the node report."""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from math import ceil, hypot
import json
import numpy as np
from PIL import Image, ImageDraw
import rasterio
from rasterio.enums import Resampling
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.utils import ImageReader
from shapely.geometry import LineString

from node_model import CACHE, GEO, EXTENT, INSIDE, SITES, ANGEL, SCOUTS, CODE, features, xy
from terrain_maps import landscape, contour_lines, contour_interval, feature_paths, relief


def extent_for(points,aspect,pad=.15,min_span=180):
    pts=np.array(points)
    low,high=pts.min(axis=0),pts.max(axis=0)
    cx,cy=(low+high)/2
    width=max((high[0]-low[0])*(1+2*pad),(high[1]-low[1])*(1+2*pad)*aspect,min_span)
    h=width/aspect
    return cx-width/2,cy-h/2,cx+width/2,cy+h/2


def project(pt,bounds,rect):
    l,b,r,t=bounds
    x,y,w,h=rect
    return x+(pt[0]-l)*w/(r-l), y+(pt[1]-b)*h/(t-b)


def clip(c,rect):
    c.saveState()
    p=c.beginPath()
    p.rect(*rect)
    c.clipPath(p,stroke=0)


def projected_image(c,path,bounds,rect,source_bounds):
    l,b,r,t=source_bounds
    x,y=project((l,b),bounds,rect)
    right,top=project((r,t),bounds,rect)
    c.drawImage(str(path),x,y,right-x,top-y,mask="auto")


def base_path(bounds,wpx,mode):
    version=4 if bounds[2]-bounds[0]<wpx else 3
    key=sha256(repr((tuple(round(v,2) for v in bounds),wpx,mode,version)).encode()).hexdigest()[:20]
    return CACHE/"maps"/(key+".jpg")


def topo(bounds,wpx=1650,mode="detail"):
    path=base_path(bounds,wpx,mode)
    if path.is_file(): return path
    path.parent.mkdir(exist_ok=True,parents=True)
    l,b,r,t=bounds
    res=max(1,(r-l)/wpx)
    x,y,z=landscape(bounds,res)
    img=Image.fromarray(relief(z,res))
    img=Image.blend(img,Image.new("RGB",img.size,"#f8f7ed"),.26)
    if img.width<wpx:
        img=img.resize((wpx,round(wpx*(t-b)/(r-l))),Image.Resampling.LANCZOS)
    d=ImageDraw.Draw(img)
    sx,sy=img.width/(r-l),img.height/(t-b)
    def pix(a):
        return list(map(tuple,np.column_stack(((a[:,0]-l)*sx,(t-a[:,1])*sy)).round().astype(int)))
    interval=contour_interval(max(r-l,t-b))
    if mode!="shade":
        for level,coords in contour_lines(x,y,z,interval,max(.45,res*.7)):
            d.line(pix(coords),fill="#b9af9b" if level%(5*interval) else "#a19580",width=1 if level%(5*interval) else 2)
    paths=list(feature_paths(features,bounds))
    for kind,paint,width in [("building","#b0ada4",1),("parking","#c6bfb0",1),("stream","#94b1b4",1),
                             ("trail","#998771",1),("road","#a49c8b",3),("highway","#807562",5),
                             ("road","#fbf9ec",1),("highway","#f7d8a1",3)]:
        for k,_,coords in paths:
            if k!=kind: continue
            pts=pix(coords)
            if k in ("building","parking") and len(pts)>3 and pts[0]==pts[-1]:
                d.polygon(pts,fill=paint)
            elif len(pts)>1:
                d.line(pts,fill=paint,width=width)
    img.save(path,quality=88,subsampling=0)
    return path


def overlay_file(name,classes,palette):
    # Include pixel data and palette so a changed model never reuses an obsolete map.
    key=sha256(classes.tobytes()+repr((classes.shape,palette)).encode()).hexdigest()[:16]
    p=CACHE/"maps"/(name+"-"+key+".png")
    if not p.exists():
        p.parent.mkdir(parents=True,exist_ok=True)
        rgba=np.array(palette,dtype=np.uint8)[classes]
        Image.fromarray(rgba).save(p)
    return p


def line(c,start,end,color,width=1,dash=None):
    c.setStrokeColor(HexColor(color)); c.setLineWidth(width)
    c.setDash(dash or [])
    c.line(*start,*end); c.setDash([])


def tag(c,x,y,s,align="center",size=8,color="#293C3E",strong=False):
    font="Bold" if strong else "Sans"
    w=c.stringWidth(s,font,size)
    if align=="center": x-=w/2
    if align=="right": x-=w
    c.setFillColor(HexColor("#FFFDF6")); c.roundRect(x-2.4,y-2.3,w+4.8,size+4,2.2,stroke=0,fill=1)
    c.setFillColor(HexColor(color)); c.setFont(font,size); c.drawString(x,y,s)


def mark(c,at,color="#173A41",shape="circle",radius=3.6):
    x,y=at
    c.setStrokeColor(white); c.setLineWidth(1.2); c.setFillColor(HexColor(color))
    if shape=="diamond":
        p=c.beginPath();p.moveTo(x,y+radius*1.4);p.lineTo(x+radius*1.4,y);p.lineTo(x,y-radius*1.4);p.lineTo(x-radius*1.4,y);p.close()
        c.drawPath(p,stroke=1,fill=1)
    else: c.circle(x,y,radius,stroke=1,fill=1)


def frame(c,rect,bounds):
    x,y,w,h=rect
    c.setStrokeColor(HexColor("#819389"));c.setLineWidth(.6);c.rect(*rect)
    tag(c,x+9,y+h-14,"N ↑","left",8,strong=True)
    km=(bounds[2]-bounds[0])/1000
    bar=next(d for d in (20,10,5,2,1,.5,.2,.1,.05,.02,.01) if d<km*.26)
    span=bar*w/km
    sx=x+10;sy=y+11
    line(c,(sx,sy),(sx+span,sy),"#fffef8",4.6)
    line(c,(sx,sy),(sx+span,sy),"#283D3D",2)
    tag(c,sx,sy+4,f"{bar:g} km" if bar>=1 else f"{bar*1000:g} m","left",7)


def clipped_overlay(classes,bounds,palette):
    # Crop to the visible source pixels before drawing. A summit-to-summit inset
    # can otherwise ask a PDF viewer to expand the 17 km source to a 100 m scale.
    left,bottom,right,top=bounds
    ix0=max(0,int(np.floor((left-GEO.c)/GEO.a))-1)
    ix1=min(classes.shape[1],int(np.ceil((right-GEO.c)/GEO.a))+1)
    iy0=max(0,int(np.floor((top-GEO.f)/GEO.e))-1)
    iy1=min(classes.shape[0],int(np.ceil((bottom-GEO.f)/GEO.e))+1)
    sub=classes[iy0:iy1,ix0:ix1]
    x0,y1=GEO*(ix0,iy0)
    x1,y0=GEO*(ix1,iy1)
    return overlay_file("pair",sub,palette),(x0,y0,x1,y1)


def close_pair_overlay(a,b,bounds,palette):
    from model import grid,meta,wave,radius
    from survey import wh
    from terrain import points,sight
    l,bottom,r,t=bounds
    spacing=2.5 if r-l<500 else 5
    cols,rows=ceil((r-l)/spacing),ceil((t-bottom)/spacing)
    gx,gy=np.meshgrid(l+(np.arange(cols)+.5)*spacing,t-(np.arange(rows)+.5)*spacing)
    ends=points(grid,meta,np.column_stack((gx.ravel(),gy.ravel())),1.2)
    assert np.isfinite(ends).all()
    masks=[]
    for site in (a,b):
        origin=points(grid,meta,[xy[site]],wh(site))[0]
        masks.append(sight(grid,meta,origin,ends,5,wave,radius).reshape(rows,cols))
    classes=masks[0]+2*masks[1]
    return overlay_file("local-pair",classes,palette),(l,t-rows*spacing,l+cols*spacing,t),spacing


def mountain(c,rect,bounds,overlay=None,wpx=1650,mode="detail",overlay_bounds=EXTENT):
    clip(c,rect)
    c.drawImage(str(topo(bounds,wpx,mode)),*rect)
    if overlay is not None:
        projected_image(c,overlay,bounds,rect,overlay_bounds)
    c.restoreState()


def detail_labels(c,rect,bounds):
    from survey import reference_labels
    prior=[]
    for name,x,y,kind in reference_labels():
        if kind!="road" or name in prior: continue
        px,py=project((x,y),bounds,rect)
        l,b,w,h=rect
        if l+21<px<l+w-21 and b+20<py<b+h-18:
            tag(c,px,py,name,size=6.6)
            prior.append(name)


def study_edge(c,rect,bounds):
    from node_model import boundary
    clip(c,rect)
    outline=c.beginPath()
    outline.rect(*rect)
    vertices=[project(point,bounds,rect) for point in boundary.exterior.coords]
    outline.moveTo(*vertices[0])
    for pt in vertices[1:]:outline.lineTo(*pt)
    outline.close()
    c.setFillColor(HexColor("#FAF9F4"));c.setFillAlpha(.81)
    c.drawPath(outline,stroke=0,fill=1,fillMode=0)
    c.setFillAlpha(1)
    for a,b in zip(vertices,vertices[1:]):line(c,a,b,"#97A69E",.55)
    c.restoreState()


def city_layers():
    from node_valley import WSEN
    from terrain import forward
    from city_streets import streets
    from node_model import DATA
    # Use a report-local copy of the urban street extract. Leave prior study cache untouched.
    name=CACHE/"metro-major-roads.json"
    if not name.exists():
        import osmium
        from shapely.geometry import box
        geom=box(*WSEN)
        road=[]
        class Major(osmium.SimpleHandler):
            def way(self,w):
                kind=w.tags.get("highway")
                if kind not in ("motorway","trunk","primary","secondary") or len(w.nodes)<2: return
                if not any(WSEN[0]-.04<n.lon<WSEN[2]+.04 and WSEN[1]-.04<n.lat<WSEN[3]+.04 for n in w.nodes): return
                obj=LineString([(n.lon,n.lat) for n in w.nodes]).intersection(geom)
                for g in getattr(obj,"geoms",[obj]):
                    if g.geom_type=="LineString" and not g.is_empty:
                        pts=np.asarray(g.simplify(.00014).coords)
                        road.append([kind,np.column_stack(forward.transform(*pts.T)).round().astype(int).tolist()])
        Major().apply_file(str(DATA/"source/nevada.osm.pbf"),locations=True)
        name.write_text(json.dumps(road,separators=(",",":")))
    return json.loads(name.read_bytes())


@lru_cache(1)
def metro_base():
    path=CACHE/"metro-relief-roads.jpg"
    with rasterio.open(CACHE/"vegas-henderson-20m.tif") as ds:
        bounds=tuple(ds.bounds)
        if path.exists(): return path,bounds
        w=2700
        h=round(w*ds.height/ds.width)
        z=ds.read(1,out_shape=(h,w),resampling=Resampling.bilinear)
    img=Image.fromarray(relief(z,(bounds[2]-bounds[0])/w))
    img=Image.blend(img,Image.new("RGB",img.size,"#faf8f0"),.32)
    d=ImageDraw.Draw(img)
    l,b,r,t=bounds
    for kind,points in city_layers():
        pts=[((x-l)*w/(r-l),(t-y)*h/(t-b)) for x,y in points]
        d.line(pts,fill="#8d9189" if kind in ("motorway","trunk") else "#b7bab0",width=2 if kind in ("motorway","trunk") else 1)
    img.save(path,quality=91)
    return path,bounds
