"""Verify the final PDF, field packet, displayed masks and directional evidence against GIS inputs."""
from collections import Counter
from itertools import permutations
from pathlib import Path
from io import BytesIO
import csv
import json
import re
import zipfile
from xml.etree import ElementTree as ET
import pymupdf
from node_model import *
from node_valley import WSEN
from node_report import PDF
from node_chapters import region
from node_drawing import psite,ppath
from scipy.ndimage import binary_erosion, map_coordinates
from PIL import Image, ImageDraw

def compact(value):
    return " ".join(value.split())


def displayed_mask(page,mask,eligible=None,with_neighbors=False):
    images=[im for im in page.get_image_info() if (im["height"],im["width"])==mask.shape]
    assert len(images)==1,(page.number,len(images))
    box=images[0]["bbox"]
    if with_neighbors:
        image,=(im for im in page.get_images() if (im[3],im[2])==mask.shape)
        alpha=Image.open(BytesIO(page.parent.extract_image(image[1])["image"]))
        assert np.array_equal(np.asarray(alpha)>0,mask),page.number+1
    agreement(page,box,mask,eligible,with_neighbors)


def agreement(page,box,mask,eligible=None,with_neighbors=False):
    pix=page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3),alpha=False)
    pixels=np.frombuffer(pix.samples,"uint8").reshape(pix.height,pix.width,3).astype("int16")
    teal=(pixels[:,:,1]-pixels[:,:,0]>35)&(pixels[:,:,2]-pixels[:,:,0]>19)
    # Text badges, pin symbols and link strokes intentionally cover some visible cells.
    # Verify unobscured printed pixels separately from the full embedded alpha mask.
    occluded=Image.new("1",(pix.width,pix.height))
    if with_neighbors:
        pen=ImageDraw.Draw(occluded)
        for path in page.get_drawings():
            rect=path["rect"]
            if path.get("fill") is not None and rect.width<142 and rect.height<24:
                pen.rectangle((rect.x0*1.3-2,rect.y0*1.3-2,rect.x1*1.3+2,rect.y1*1.3+2),fill=1)
            if any(abs((path.get("width") or 0)-width)<.01 for width in (1.65,.85)):
                for item in path["items"]:
                    if item[0]=="l":
                        pen.line([tuple(np.asarray(pt)*1.3) for pt in item[1:3]],fill=1,width=5)
    occluded=np.asarray(occluded)
    l,t,r,b=np.array(box)*1.3
    if eligible is None:eligible=np.ones_like(mask,dtype=bool)
    for val in [False,True]:
        rr,cc=np.nonzero(binary_erosion((mask==val)&eligible))
        step=max(1,len(rr)//1800)
        py=((rr[::step]+.5)*(b-t)/mask.shape[0]+t).astype(int)
        px=((cc[::step]+.5)*(r-l)/mask.shape[1]+l).astype(int)
        valid=(px>=0)&(px<teal.shape[1])&(py>=0)&(py<teal.shape[0])
        inside=np.flatnonzero(valid)
        valid[inside]=~occluded[py[inside],px[inside]]
        assert valid.sum()>5 and (teal[py[valid],px[valid]]==val).mean()>.86,(page.number+1,val)


def check_valley(doc):
    from model import grid as local_dem,meta as local_transform
    with rasterio.open(VALLEY_CACHE/"vegas-henderson-20m.tif") as ds:
        regiondem=ds.read(1);aff=ds.transform
        assert np.isfinite(regiondem).all() and regiondem.min()>-500 and aff.a==20
        for name,lon,lat in [("Southern Henderson",-115.105,35.913),("Eastern Henderson",-114.923,36.105),
                             ("North Las Vegas",-115.16,36.32),("Mount Charleston",-115.67,36.25)]:
            x,y=forward.transform(lon,lat)
            assert ds.bounds.left<x<ds.bounds.right and ds.bounds.bottom<y<ds.bounds.top,name
    def sample(dem,x0,y0,res,xx,yy):
        return map_coordinates(dem,[(y0-yy)/res-.5,(xx-x0)/res-.5],order=1,prefilter=False,output=np.float64)
    for i,k in enumerate(REGIONAL,6):
        page=doc[i]
        with rasterio.open(VALLEY_CACHE/(k+"-valley.tif")) as ds:
            mask=ds.read(1).astype(bool);tr=ds.transform;assert tr.a==120 and tr.e==-120
        displayed_mask(page,mask)
        rr,cc=np.mgrid[8:mask.shape[0]:61,8:mask.shape[1]:53]
        x0,y0=xy[k]
        z0=sample(local_dem,*local_transform,np.array([x0]),np.array([y0]))[0]+4
        for i,j in zip(rr.ravel(),cc.ravel()):
            x,y=tr*(j+.5,i+.5);distance=np.hypot(x-x0,y-y0)
            tt=np.linspace(0,1,max(2,int(np.ceil(distance/20)))+1)
            z=sample(regiondem,aff.c,aff.f,aff.a,x0+tt*(x-x0),y0+tt*(y-y0))
            ray=z0+(z[-1]+4-z0)*tt
            clearance=ray-z-distance**2*tt*(1-tt)/(2*6371000*4/3)
            assert (clearance[1:-1].min()>=0)==mask[i,j],(k,i,j)
        text=compact(page.get_text());assert "Henderson" in text and "Las Vegas" in text and "4 m" in text
        assert f"{mask.sum()*.0144:,.0f} km²" in text


def check_close_profiles(doc):
    from model import grid,meta
    from node_cartography import extent_for
    from node_chapters import PAIR_PALETTE
    colors=np.asarray(PAIR_PALETTE)[:,:3]
    count=0
    for a,b in permutations(SITES,2):
        if b not in neighbors(a):continue
        l,bottom,r,t=extent_for([xy[a],xy[b]],398/383,.23,min_span=120)
        if r-l>=1500:continue
        count+=1
        spacing=2.5 if r-l<500 else 5
        pg=doc[ppath(a,b)-1]
        assert f"{spacing:g} m cells" in pg.get_text()
        nxpix,nypix=int(np.ceil((r-l)/spacing)),int(np.ceil((t-bottom)/spacing))
        img,=(im for im in pg.get_images() if im[2:4]==(nxpix,nypix))
        pixels=np.asarray(Image.open(BytesIO(doc.extract_image(img[0])["image"])).convert("RGB"))
        def z(xs,ys):
            return map_coordinates(grid,[(meta[1]-ys)/meta[2]-.5,(xs-meta[0])/meta[2]-.5],order=1,prefilter=False,output=np.float64)
        for row in range(1,nypix,max(2,nypix//7)):
            for col in range(1,nxpix,max(2,nxpix//7)):
                x,y=l+(col+.5)*spacing,t-(row+.5)*spacing
                code=0
                for bit,k in enumerate((a,b)):
                    x0,y0=xy[k];d=np.hypot(x-x0,y-y0)
                    ts=np.linspace(0,1,max(2,int(np.ceil(d/5)))+1)
                    zz=z(x0+ts*(x-x0),y0+ts*(y-y0))
                    line=zz[0]+wh(k)+(zz[-1]+1.2-zz[0]-wh(k))*ts
                    clear=line-zz-d*d*ts*(1-ts)/(2*6371000*4/3)
                    code+=(1<<bit)*int(clear[1:-1].min()>=0)
                assert np.array_equal(pixels[row,col],colors[code]),(a,b,row,col)
    return count


def check_angel_inset(doc):
    from node_cartography import extent_for
    from node_front import INSET
    from model import grid,meta
    l,b,r,t=extent_for([xy[k] for k in REGIONAL],INSET[2]/INSET[3],.38)
    spacing=2.5
    width,height=int(np.ceil((r-l)/spacing)),int(np.ceil((t-b)/spacing))
    item,=(im for im in doc[2].get_images() if im[2:4]==(width,height))
    alpha=np.asarray(Image.open(BytesIO(doc.extract_image(item[1])["image"])))>0
    def terrain(x,y):
        return map_coordinates(grid,[(meta[1]-y)/meta[2]-.5,(x-meta[0])/meta[2]-.5],order=1,
                               prefilter=False,output=np.float64)
    for row in range(3,height,17):
        for col in range(2,width,17):
            x,y=l+(col+.5)*spacing,t-(row+.5)*spacing
            visible=False
            for k in SITES:
                xx,yy=xy[k]
                distance=np.hypot(x-xx,y-yy)
                frac=np.linspace(0,1,max(2,int(np.ceil(distance/5)))+1)
                z=terrain(xx+frac*(x-xx),yy+frac*(y-yy))
                ray=z[0]+wh(k)+(z[-1]+1.2-z[0]-wh(k))*frac
                if np.all((ray-z-distance**2*frac*(1-frac)/(2*6371000*4/3))[1:-1]>=0):
                    visible=True
                    break
            assert visible==alpha[row,col],(row,col)


def check_network(doc,records):
    # Traverse packet states independently of the report's simple-path enumeration.
    for first in SITES:
        stack=[(first,None,3)]
        seen=set()
        costs=[]
        while stack:
            current,prev,remaining=stack.pop()
            state=(current,prev,remaining)
            if state in seen:
                continue
            seen.add(state)
            if current==LEE:
                costs.append(3-remaining)
                continue
            if not remaining:
                continue
            consumed=int(prev is None or current==KYLE_FIRE or prev==KYLE_FIRE)
            for nxt in SITES:
                if nxt in (prev,current):
                    continue
                edge=frozenset((current,nxt))
                if float(records[edge]["native LOS clearance m"])>=0 or edge in OBSERVED:
                    stack.append((nxt,current,remaining-consumed))
        assert costs and min(costs)==ROUTES[first][1],first
    union=footprint(SITES)
    assert set(ROUTES)==set(SITES)
    assert ROUTES[KYLE_FIRE][1]==2 and all(ROUTES[k][1]==1 for k in ROUTERS)
    with rasterio.open(REPORT/"combined-mountain-viewshed.tif") as ds:
        assert ds.nodata==255 and np.array_equal(ds.read(1),np.where(INSIDE,union,255))
        assert ds.transform==GEO
    displayed_mask(doc[2],union,INSIDE,with_neighbors=True)
    assert sorted(im["bbox"] for im in doc[1].get_image_info() if im["width"]>=1400)==sorted(
        im["bbox"] for im in doc[2].get_image_info() if im["width"]>=1400)
    assert f"{union.sum()*AREA:.2f} km²" in compact(doc[2].get_text())
    target_mask=masks[[ix[k] for k in SITES]].any(axis=0)
    assert f"{roadkm(target_mask):.2f} of " in compact(doc[2].get_text())


def check_neighbors_on_map(page,site,sisters):
    from node_cartography import project
    rect=(32,58,520,436)
    bounds=region(rect)
    def pdf_point(k):
        x,y=project(xy[k],bounds,rect)
        return np.array((x,page.rect.height-y))
    focal=pdf_point(site)
    segments=[]
    focal_rings=[]
    for path in page.get_drawings():
        if abs((path.get("width") or 0)-.85)<.01:
            segments.extend((np.array(item[1]),np.array(item[2])) for item in path["items"] if item[0]=="l")
        box=path["rect"]
        if abs(box.width-14.6)<.05 and abs(box.height-14.6)<.05:
            focal_rings.append(np.array(((box.x0+box.x1)/2,(box.y0+box.y1)/2)))
    assert any(np.linalg.norm(at-focal)<.03 for at in focal_rings),site
    drawn={other for other in SITES if other!=site and any(
        np.linalg.norm(p-focal)<.03 and np.linalg.norm(q-pdf_point(other))<.03 for p,q in segments)}
    assert drawn==sisters,(site,drawn,sisters)
    for b in sisters:
        assert b in page.get_text(),(site,b)


def verify():
    with (OUT/"pair-overlap.csv").open(encoding="utf-8-sig") as f:
        records={frozenset((row["site A"],row["site B"])):row for row in csv.DictReader(f)}
    with pymupdf.open(PDF) as doc:
        assert len(doc)==46 and "Codex" in doc.metadata["author"]
        pages=[compact(p.get_text()) for p in doc]
        assert all(name not in t for t in pages for name in ("Vegas alternative","Kyle Junction","Showgirl","Angel road survey 1","Angel road survey 3","Angel road survey 6","Three separate Angel scout trials","Executive summary"))
        links=lambda p:{d["page"]+1 for d in doc[p-1].get_links() if d["kind"]==pymupdf.LINK_GOTO}
        assert set(psite(k) for k in SITES)<=links(5)&links(6)
        assert {2,3,4,6,7,8}<=links(5)
        examples=[records[frozenset((SHADY,b))] for b in (CAT,"Kyle Junction")]
        thresholds={key:min(float(r[key]) for r in examples) for key in ("native LOS clearance m","min first Fresnel fraction")}
        expected={pair for pair,r in records.items() if pair<=set(SITES) and (
            all(float(r[key])>=lo for key,lo in thresholds.items()) or pair in OBSERVED)}
        assert expected==KEPT_PAIRS and len(expected)==10
        physical=Counter()
        for k in SITES:
            for text in (pages[0],pages[1],pages[2],pages[3],pages[5]):
                assert k.replace("’","'") in text.replace("’","'"),k
            sisters={b for b in SITES if frozenset((k,b)) in expected}
            assert set(neighbors(k))==sisters
            assert set(ppath(k,b) for b in neighbors(k))<=links(psite(k))
            with rasterio.open(OUT/"viewsheds"/(k+".tif")) as ds:vis=ds.read(1).astype(bool)
            displayed_mask(doc[psite(k)],vis&INSIDE,INSIDE,with_neighbors=True)
            check_neighbors_on_map(doc[psite(k)],k,sisters)
            for b in neighbors(k):
                n=ppath(k,b);text=pages[n-1]
                assert compact(f"{k} to {b}") in text,(n,k,b)
                assert ppath(b,k) in links(n) and psite(k) in links(n)
                row=records[frozenset((k,b))]
                value=float(row["native LOS clearance m"])
                assert f"{value:+.2f} m" in text and f"{wh(k)} m at A / {wh(b)} m at B" in text,(n,k,b)
                assert ("Historical field record: G002 at Shady" in text)==observed(k,b)
                if value<0:
                    label=("Marginal · recorded" if {k,b} == {SHADY,CAT} else
                           "Recorded" if observed(k,b) else "Marginal · unverified")
                    assert label in text and "Blocked / recorded" not in text,(k,b)
                assert ("Terrain intersects the ray." in text)==(value<0)
                assert f"Reverse profile p. {ppath(b,k)}" in text
                physical[frozenset((k,b))]+=1
        assert set(physical)==expected and set(physical.values())=={2}
        assert all(all(link["kind"]==pymupdf.LINK_URI or 0<=link.get("page",-1)<len(doc) for link in p.get_links()) for p in doc)
        assert all({5,6}<=links(i) for i in range(2,len(doc)+1))
        check_network(doc,records);check_valley(doc);check_angel_inset(doc)
        close_count=check_close_profiles(doc)
    with zipfile.ZipFile(REPORT/"favorite-router-field-packet.zip") as ar:
        assert len(ar.namelist())==16 and ar.testzip() is None and ar.read(PDF.name)==PDF.read_bytes()
        assert set(n for n in ar.namelist() if n.endswith(".tif")) == {"mountain-viewsheds/"+s+".tif" for s in SITES} | {"valley-viewsheds/"+s+".tif" for s in REGIONAL} | {"mountain-viewsheds/combined-mountain-viewshed.tif"}
        for filename in ("node-waypoints.kml","node-waypoints.gpx"):
            root=ET.fromstring(ar.read(filename));tag="Placemark" if filename.endswith("kml") else "wpt"
            assert {p.findtext("{*}name") for p in root.findall(".//{*}"+tag)}==set(SITES)
        viewer=json.loads(re.search(r"^const db=(.*);\r?$",ar.read("radio-paths.html").decode("utf8"),re.M)[1])
        assert set(viewer["points"])==set(viewer["views"])==set(SITES)
        assert {frozenset((p["a"],p["b"])) for p in viewer["paths"]}==expected
        assert all(p["fieldClass"]==status(p["a"],p["b"]) for p in viewer["paths"])
    print(f"Verified 46 pages, 20 oriented profiles ({close_count} fine-grid overlays), nine annotated viewsheds, the combined mountain map, favorite-router paths, two valley maps and the 16-file packet.")


if __name__=="__main__":
    verify()
