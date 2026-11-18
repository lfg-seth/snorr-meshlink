"""Draw the edition cover with a georeferenced aerial draped over local terrain."""
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from functools import lru_cache
from io import BytesIO

import numpy as np
from PIL import Image, ImageEnhance
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling
from reportlab.lib.colors import HexColor
from scipy.ndimage import map_coordinates

from node_model import (CACHE, DATA, SITES, CODE, LEE, SHADY, A5, ANGEL, UP, MACK, ESC, CAT,
                        KYLE_FIRE, KEPT_PAIRS, road_inventory, xy)
from node_drawing import W,H,fillbox,txt,para,rule,link
from node_cartography import clip,mark,line,project

SOURCE=(613000,4009000,635000,4029000)
FRAME=(614650,4010250,633650,4027450)
RECT=(247,24,595,571)
TILT=.56
RES=7.5


def aerial():
    path=CACHE/"cover-naip.jpg"
    if not path.exists():
        query=urlencode(dict(bbox=",".join(map(str,SOURCE)),bboxSR=26911,imageSR=26911,size="3300,3000",
                             format="jpg",bandIds="0,1,2",f="image"))
        service="https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage"
        with urlopen(Request(service+"?"+query,headers={"User-Agent":"SNORR-MeshLink study"}),timeout=90) as r:
            raw=r.read()
        assert Image.open(BytesIO(raw)).size==(3300,3000)
        path.write_bytes(raw)
    return path


@lru_cache(1)
def drape():
    import rasterio
    l,b,r,t=SOURCE
    cols,rows=round((r-l)/RES),round((t-b)/RES)
    tr=from_bounds(*SOURCE,cols,rows)
    dem=np.zeros((rows,cols),dtype="float32")
    with rasterio.open(DATA/"cache/terrain-regional.tif") as ds:
        reproject(rasterio.band(ds,1),dem,dst_transform=tr,dst_crs="EPSG:26911",resampling=Resampling.bilinear)
    assert dem.min()>0
    def lifted(x,y):
        x,y=np.broadcast_arrays(x,y)
        coords=np.asarray([(t-y)/-tr.e-.5,(x-l)/tr.a-.5]).reshape(2,-1)
        z=map_coordinates(dem,coords,order=1,mode="nearest").reshape(x.shape)
        return x,y+TILT*(z-2200)

    path=CACHE/"cover-oblique.jpg"
    if not path.exists():
        photo=Image.open(aerial()).convert("RGB").resize((cols,rows),Image.Resampling.LANCZOS)
        texture=np.asarray(ImageEnhance.Color(photo).enhance(1.17))
        west,bottom,east,top=FRAME
        outw,outh=round((east-west)/RES),round((top-bottom)/RES)
        image=np.empty((outh,outw,3),np.uint8)
        source_y=t+(np.arange(rows)+.5)*tr.e
        dest_y=top-(np.arange(outh)+.5)*(top-bottom)/outh
        for j in range(outw):
            x=west+(j+.5)*(east-west)/outw
            col=int((x-l)/tr.a)
            y=(source_y+TILT*(dem[:,col]-2200))[::-1]
            # Scan from the camera toward the north. Hide terrain behind closer ridges.
            visible=np.r_[True,y[1:]>np.maximum.accumulate(y[:-1])]
            for channel in range(3):
                image[:,j,channel]=np.interp(dest_y,y[visible],texture[::-1,col,channel][visible])
        Image.fromarray(image).save(path,quality=93,subsampling=0)
    return path,lifted


def draw_cover(c,links):
    path,lifted=drape()
    fillbox(c,0,0,W,H,"#122E32")
    c.drawImage(str(path),*RECT)
    def pos(x,y):
        xx,yy=lifted(x,y)
        return project((xx,yy),FRAME,RECT)
    clip(c,RECT)
    for geometry,_ in road_inventory:
        pts=np.asarray(geometry.coords)
        px,py=pos(*pts.T)
        road=c.beginPath()
        road.moveTo(px[0],py[0])
        for x,y in zip(px[1:],py[1:]):
            road.lineTo(x,y)
        c.setStrokeColor(HexColor("#BFA878"));c.setLineWidth(.8);c.drawPath(road)
    c.restoreState()
    offsets={UP:(-11,-13,"right"), LEE:(-7,9,"right"), MACK:(1,12,"center"),
             ESC:(-6,-15,"right"),SHADY:(8,9,"left"),CAT:(-7,-14,"right"),
             KYLE_FIRE:(7,9,"left"), A5:(-9,13,"right"), ANGEL:(10,-14,"left")}
    for k in SITES:
        x,y=pos(*xy[k]);dx,dy,align=offsets[k]
        xx,yy=x+dx,y+dy
        name=k.replace("'","’")
        width=c.stringWidth(name,"Bold",8.6)
        line(c,(x,y),(xx,yy+2),"#F7EED8",.9)
        xx-=width if align=="right" else width/2 if align=="center" else 0
        c.setFillColor(HexColor("#19383A"));c.roundRect(xx-3.6,yy-2.8,width+7.2,13,2.3,fill=1,stroke=0)
        txt(c,xx,yy,name,8.6,"Bold","#FFFFF3")
        mark(c,(x,y),"#AC4829","diamond" if k==LEE else "circle",3.6)
    fillbox(c,243,0,4,H,"#CFB589")
    txt(c,26,555,"SNORR  /  MESHLINK",10,"Bold","#C1DCD0")
    rule(c,26,535,217,"#688982")
    txt(c,24,439,"Mount",35,"Serif","#FAF6E7")
    txt(c,24,395,"Charleston",35,"Serif","#FAF6E7")
    txt(c,26,357,"Repeater field study",16,"Sans","#DFEBDA")
    para(c,26,304,"Member GPS routes to Lee Fire and fixed-radio coverage across the Las Vegas Valley.",189,11.8,18,"#E0EADF")
    txt(c,26,206,"FAVORITE-ROUTER EDITION",8,"Bold","#CBB38A")
    txt(c,26,183,f"{len(SITES)} sites   /   {len(KEPT_PAIRS)} direct links",11,"Bold","#FEF9E9")
    rule(c,26,149,217,"#688982")
    txt(c,26,126,"Prepared for the SNORR field team",9.1,"Sans","#DFEBDA")
    txt(c,26,106,"Codex for SNORR MeshLink",9.1,"Sans","#DFEBDA")
    txt(c,26,76,"18 November 2026",11,"Bold","#FFF9E8")
    txt(c,26,39,"Open contents   →   p. 5",9,"Bold","#C1DCD0");link(links,24,32,133,18,5)
    txt(c,260,9,"Mount Charleston operating area   /   USGS NAIP aerial imagery and 3DEP elevation",8,"Sans","#E0EADF")
