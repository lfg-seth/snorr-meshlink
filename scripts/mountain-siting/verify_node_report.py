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
from PIL import Image

def compact(value):
    return " ".join(value.split())


def displayed_mask(page,mask,eligible=None):
    images=[im for im in page.get_image_info() if (im["height"],im["width"])==mask.shape]
    assert len(images)==1,(page.number,len(images))
    box=images[0]["bbox"]
    agreement(page,box,mask,eligible)


def agreement(page,box,mask,eligible=None):
    pix=page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3),alpha=False)
    pixels=np.frombuffer(pix.samples,"uint8").reshape(pix.height,pix.width,3).astype("int16")
    teal=(pixels[:,:,1]-pixels[:,:,0]>35)&(pixels[:,:,2]-pixels[:,:,0]>19)
    l,t,r,b=np.array(box)*1.3
    if eligible is None:eligible=np.ones_like(mask,dtype=bool)
    for val in [False,True]:
        rr,cc=np.nonzero(binary_erosion((mask==val)&eligible))
        step=max(1,len(rr)//1800)
        py=((rr[::step]+.5)*(b-t)/mask.shape[0]+t).astype(int)
        px=((cc[::step]+.5)*(r-l)/mask.shape[1]+l).astype(int)
        valid=(px>=0)&(px<teal.shape[1])&(py>=0)&(py<teal.shape[0])
        assert valid.sum()>5 and (teal[py[valid],px[valid]]==val).mean()>.86,(page.number+1,val)


def check_valley(doc):
    from model import grid as local_dem,meta as local_transform
    with rasterio.open(CACHE/"vegas-henderson-20m.tif") as ds:
        regiondem=ds.read(1);aff=ds.transform
        assert np.isfinite(regiondem).all() and regiondem.min()>-500 and aff.a==20
        for name,lon,lat in [("Southern Henderson",-115.105,35.913),("Eastern Henderson",-114.923,36.105),
                             ("North Las Vegas",-115.16,36.32),("Mount Charleston",-115.67,36.25)]:
            x,y=forward.transform(lon,lat)
            assert ds.bounds.left<x<ds.bounds.right and ds.bounds.bottom<y<ds.bounds.top,name
    def sample(dem,x0,y0,res,xx,yy):
        return map_coordinates(dem,[(y0-yy)/res-.5,(xx-x0)/res-.5],order=1,prefilter=False,output=np.float64)
    for k,page in zip(REGIONAL,list(doc)[9:14]):
        with rasterio.open(CACHE/(k+"-valley.tif")) as ds:
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


def check_network(doc,records):
    def recalc(relays,obs):
        graph0=nx.Graph(); selected=[LEE,*relays];graph0.add_nodes_from(selected)
        for a,b in combinations(selected,2):
            row=records[frozenset((a,b))]
            if float(row["native LOS clearance m"])>=0 or obs and observed(a,b):graph0.add_edge(a,b)
        reach=nx.single_source_shortest_path_length(graph0,LEE,cutoff=3)
        return list(reach)
    inputs=[(baseline,False,DEPLOYED)]
    for s in SCOUTS:
        inputs.extend([([*ROLE_RELAY,s],False,CASES[s]),([*ROLE_RELAY,s,SHADY],True,TRIALS[s])])
    for layout,obs,case in inputs:
        reach=recalc(layout,obs)
        assert set(case["routes"])==set(reach)
        mask=footprint(reach);assert np.array_equal(mask,case["zone"])
        assert np.isclose(roadkm(np.logical_or.reduce([masks[ix[k]] for k in reach])),case["km"])
    for page,scenarios in [(doc[6],[DEPLOYED,CASES[SCOUTS[2]]]),(doc[7],[CASES[SCOUTS[2]],TRIALS[SCOUTS[2]]])]:
        images=sorted([im for im in page.get_image_info() if (im["height"],im["width"])==SHAPE],key=lambda im:im["bbox"][0])
        assert len(images)==2
        for im,case in zip(images,scenarios):agreement(page,im["bbox"],case["zone"],INSIDE)


def verify():
    with (OUT/"pair-overlap.csv").open(encoding="utf-8-sig") as f:
        records={frozenset((row["site A"],row["site B"])):row for row in csv.DictReader(f)}
    with pymupdf.open(PDF) as doc:
        assert len(doc)==196 and "Codex" in doc.metadata["author"]
        pages=[compact(p.get_text()) for p in doc]
        assert all("Vegas alternative" not in t and "Lone Mountain foothills" not in t for t in pages)
        links=lambda p:{d["page"]+1 for d in doc[p-1].get_links() if d["kind"]==pymupdf.LINK_GOTO}
        assert set(psite(k) for k in SITES)<=links(4)&links(5)
        assert set(range(10,15))<=links(4)
        physical=Counter()
        for k in SITES:
            for text in (pages[1],pages[2],pages[4]):
                assert k.replace("’","'") in text.replace("’","'"),k
            assert len(neighbors(k))==12
            assert set(ppath(k,b) for b in neighbors(k))<=links(psite(k))
            with rasterio.open(OUT/"viewsheds"/(k+".tif")) as ds:vis=ds.read(1).astype(bool)
            displayed_mask(doc[psite(k)],vis&INSIDE,INSIDE)
            for b in neighbors(k):
                n=ppath(k,b);text=pages[n-1]
                assert compact(f"{k} to {b}") in text,(n,k,b)
                assert ppath(b,k) in links(n) and psite(k) in links(n)
                row=records[frozenset((k,b))]
                value=float(row["native LOS clearance m"])
                assert f"{value:+.2f} m" in text and f"{wh(k)} m at A / {wh(b)} m at B" in text,(n,k,b)
                assert ("Field record: Shady received" in text)==observed(k,b)
                assert ("Terrain intersects the ray." in text)==(value<0)
                assert f"Reverse profile p. {ppath(b,k)}" in text
                physical[frozenset((k,b))]+=1
        assert len(physical)==78 and set(physical.values())=={2}
        assert all(all(link["kind"]==pymupdf.LINK_URI or 0<=link.get("page",-1)<len(doc) for link in p.get_links()) for p in doc)
        assert len([link for link in doc[8].get_links() if link["kind"]==pymupdf.LINK_URI])==3
        check_network(doc,records);check_valley(doc)
        close_count=check_close_profiles(doc)
    with zipfile.ZipFile(REPORT/"node-field-packet.zip") as ar:
        assert len(ar.namelist())==22 and ar.testzip() is None and ar.read(PDF.name)==PDF.read_bytes()
        for filename in ("node-waypoints.kml","node-waypoints.gpx"):
            root=ET.fromstring(ar.read(filename));tag="Placemark" if filename.endswith("kml") else "wpt"
            assert {p.findtext("{*}name") for p in root.findall(".//{*}"+tag)}==set(SITES)
        viewer=json.loads(re.search(r"^const db=(.*);\r?$",ar.read("radio-paths.html").decode("utf8"),re.M)[1])
        assert set(viewer["points"])==set(viewer["views"])==set(SITES) and len(viewer["paths"])==78
    print(f"Verified 196 pages, 156 oriented profiles ({close_count} fine-grid overlays), 13 single-site maps, four network map panels, five regional rasters and the 22-file packet.")


if __name__=="__main__":
    verify()
