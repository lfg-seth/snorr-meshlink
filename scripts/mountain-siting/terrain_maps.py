"""Topographic layers in EPSG:26911, derived at the extent of the map being drawn."""
import base64
import math
from contextlib import ExitStack
from io import BytesIO
from pathlib import Path

import contourpy
import numpy as np
import rasterio
from PIL import Image
from rasterio.enums import Resampling
from rasterio.merge import merge
from rasterio.transform import from_bounds
from rasterio.warp import reproject
from scipy.ndimage import gaussian_filter
from shapely.geometry import LineString, box

from basemaps import MOUNTAIN

DATA = Path("private/winter-siting")
TILE = 1024


def landscape(bounds, resolution):
    """Read the lidar tiles at the requested ground sampling distance before shading."""
    with ExitStack() as stack:
        datasets = []
        for path in sorted((DATA / "source").glob("USGS_1M*.tif")):
            ds = stack.enter_context(rasterio.open(path))
            if box(*ds.bounds).intersects(box(*bounds)):
                datasets.append(ds)
        left,bottom,right,top = bounds
        cols = max(3,round((right-left)/resolution))
        rows = max(3,round((top-bottom)/resolution))
        transform = from_bounds(*bounds, cols, rows)
        ground = np.full((rows,cols),np.nan,np.float32)
        if datasets:
            merged,_ = merge(datasets,bounds=bounds,res=(transform.a,-transform.e),
                             indexes=[1],resampling=Resampling.bilinear,nodata=np.nan,dtype="float32")
            ground[:] = merged[0]
        if not np.isfinite(ground).all():
            with rasterio.open(DATA/"cache/terrain-regional.tif") as coarse:
                fallback = np.full_like(ground,np.nan)
                reproject(rasterio.band(coarse,1),fallback,dst_transform=transform,
                          dst_crs="EPSG:26911",dst_nodata=np.nan,resampling=Resampling.bilinear)
            ground = np.where(np.isfinite(ground),ground,fallback)
        if not np.isfinite(ground).all():
            raise ValueError(f"Incomplete elevation coverage for map {bounds}")
    x = left + (np.arange(cols)+.5)*transform.a
    y = top + (np.arange(rows)+.5)*transform.e
    return x,y,ground


def relief(ground, resolution):
    # Light from the northwest; the upper edge of a raster faces north.
    south,east = np.gradient(ground,resolution)
    light = (east+south)*.49 + .72
    light /= np.sqrt(1+east**2+south**2)
    tone = np.clip((light+.22)/1.28,0,1)
    shadow,sun = np.array([139,153,143]),np.array([251,248,231])
    return (shadow + tone[:,:,None]*(sun-shadow)).astype(np.uint8)


def contour_lines(x,y,ground,interval,tolerance):
    generator=contourpy.contour_generator(x=x,y=y,z=gaussian_filter(ground,.9))
    first=math.ceil(ground.min()/interval)*interval
    for level in range(first,math.ceil(ground.max()),interval):
        for coords in generator.lines(level):
            if len(coords)<3:
                continue
            line=LineString(coords).simplify(tolerance,preserve_topology=False)
            if line.length>tolerance*8:
                yield level,np.asarray(line.coords)


def feature_paths(features,bounds):
    area=box(*bounds)
    for geom,props in features:
        highway=props.get("highway")
        if highway in ("motorway","trunk","primary","secondary","tertiary"):
            kind="highway"
        elif highway in ("footway","path","bridleway","steps","cycleway","track"):
            kind="trail"
        elif highway and geom.geom_type.endswith("LineString"):
            kind="road"
        elif props.get("building"):
            kind="building"
        elif props.get("amenity")=="parking":
            kind="parking"
        elif props.get("waterway") in ("stream","river"):
            kind="stream"
        else:
            continue
        if not geom.intersects(area):
            continue
        name=props.get("ref") or props.get("name") or ""
        if name=="Angel Peak Placce":
            name="Angel Peak Place"
        clipped=geom.intersection(area)
        for piece in getattr(clipped,"geoms",[clipped]):
            if piece.geom_type=="Polygon":
                if kind not in ("building","parking"):
                    continue
                piece=piece.exterior
            if piece.geom_type in ("LineString","LinearRing") and len(piece.coords)>1:
                yield kind,name,np.asarray(piece.coords)


def contour_interval(width):
    if width<=350:
        return 2
    if width<=2600:
        return 10
    return 20 if width<=9000 else 40


def pdf_topography(ax,bounds,features):
    from matplotlib.collections import LineCollection, PolyCollection
    import matplotlib.patheffects as pe
    left,bottom,right,top=bounds
    span=max(right-left,top-bottom)
    resolution=max(1,span/2200)
    x,y,z=landscape(bounds,resolution)
    ax.imshow(relief(z,resolution),extent=(left,right,bottom,top),interpolation="antialiased",zorder=0)
    interval=contour_interval(span)
    contours=list(contour_lines(x,y,z,interval,max(.4,resolution*.42)))
    for major in (False,True):
        lines=[line for level,line in contours if (level%(5*interval)==0)==major]
        ax.add_collection(LineCollection(lines,colors="#8c7961" if major else "#af9f88",
                                        linewidths=.56 if major else .29,alpha=.86,zorder=.4))
    # Place a few index elevations on long, spatially separated contours.
    placed=[]
    for level,line in sorted(contours,key=lambda item:-len(item[1])):
        if level%(5*interval) or len(placed)>=4:
            continue
        j=len(line)//2
        px,py=line[j]
        u,v=(px-left)/(right-left),(py-bottom)/(top-bottom)
        if not (.1<u<.9 and .17<v<.85) or any(abs(u-a)<.22 and abs(v-b)<.22 for a,b in placed):
            continue
        d=line[min(len(line)-1,j+2)]-line[max(0,j-2)]
        angle=(math.degrees(math.atan2(d[1],d[0]))+90)%180-90
        ax.text(px,py,f"{level:,} m",rotation=angle,color="#625a4d",ha="center",va="center",fontsize=6.3,
                clip_on=True,path_effects=[pe.withStroke(linewidth=2.7,foreground="#f3f0dc")],zorder=1)
        placed.append((u,v))
    paths=list(feature_paths(features,bounds))
    for kind,face,edge in [("parking","#e3dfd4","#999487"),("building","#a6acaa","#626b67")]:
        polys=[line for k,_,line in paths if k==kind and np.array_equal(line[0],line[-1])]
        ax.add_collection(PolyCollection(polys,facecolors=face,edgecolors=edge,linewidths=.4,zorder=1.15))
    for kind,color,width,style in [("stream","#6698a4",.57,"solid"),("trail","#796448",.66,"dashed"),
                                   ("road","#747873",1.65,"solid"),("highway","#786548",2.6,"solid"),
                                   ("road","#fffef4",.89,"solid"),("highway","#f9d79a",1.6,"solid")]:
        ax.add_collection(LineCollection([p for k,_,p in paths if k==kind],colors=color,
                                        linewidths=width,linestyles=style,zorder=1.3))
    if span<5000:
        named=set()
        for kind,name,line in sorted(paths,key=lambda item:-LineString(item[2]).length):
            if not name or name in named or kind not in ("road","trail","highway") or len(named)>=4:
                continue
            geom=LineString(line)
            if geom.length<span*.22:
                continue
            for fraction in (.7,.35,.5):
                p=geom.interpolate(fraction,normalized=True)
                u,v=(p.x-left)/(right-left),(p.y-bottom)/(top-bottom)
                if not (.19<u<.80 and .15<v<.87) or any(abs(u-a)<.24 and abs(v-b)<.1 for a,b in placed):
                    continue
                before=geom.interpolate(fraction-.035,normalized=True)
                after=geom.interpolate(fraction+.035,normalized=True)
                angle=(math.degrees(math.atan2(after.y-before.y,after.x-before.x))+90)%180-90
                ax.text(p.x,p.y,name,ha="center",va="center",rotation=angle,fontsize=6.7,
                        color="#423e34",clip_on=True,path_effects=[pe.withStroke(linewidth=2.8,foreground="#fffcef")],zorder=1.6)
                placed.append((u,v))
                named.add(name)
                break
    return interval


def svg_paths(lines,origin):
    # Compact local metre coordinates keep the offline vectors small and precise.
    commands=[]
    for line in lines:
        coordinates=np.rint(line-origin).astype(int)
        keep=np.r_[True,np.any(np.diff(coordinates,axis=0),axis=1)]
        pts=coordinates[keep]
        if len(pts)>1:
            commands.append("M"+" ".join(f"{x},{y}" for x,y in pts))
    return "".join(commands)


def viewer_sheet(bounds,resolution,interval):
    x,y,ground=landscape(bounds,resolution)
    buf=BytesIO()
    Image.fromarray(relief(ground,resolution)).save(buf,"JPEG",quality=87,optimize=True)
    lines={}
    for elevation,line in contour_lines(x,y,ground,interval,resolution*.65):
        lines.setdefault(str(elevation),[]).append(line)
    return dict(bounds=bounds,resolution=resolution,
                image=base64.b64encode(buf.getvalue()).decode("ascii"),
                contours={level:svg_paths(group,bounds[:2]) for level,group in lines.items()})


def viewer_topography(positions,features):
    region=viewer_sheet(MOUNTAIN,6,20)
    # Detail tiles cover the vicinity of every selectable site. BBox overlap is
    # handled at draw time, so a short link across a tile boundary stays sharp.
    cells=set()
    for x,y in positions:
        for col in range(math.floor((x-500)/TILE),math.floor((x+500)/TILE)+1):
            for row in range(math.floor((y-500)/TILE),math.floor((y+500)/TILE)+1):
                cells.add((col,row))
    sheets=[viewer_sheet((c*TILE,r*TILE,(c+1)*TILE,(r+1)*TILE),1,5) for c,r in sorted(cells)]
    features_by_kind={}
    street_labels=[]
    for kind,name,line in feature_paths(features,MOUNTAIN):
        features_by_kind.setdefault(kind,[]).append(line)
        if kind in ("highway","road","trail") and name:
            geom=LineString(line)
            if geom.length>120:
                point=geom.interpolate(.5,normalized=True)
                street_labels.append([name,point.x,point.y,"street"])
    vectors={kind:svg_paths(lines,MOUNTAIN[:2]) for kind,lines in features_by_kind.items()}
    return dict(regional=region,tiles=sheets,vectors=vectors,streetLabels=street_labels)
