"""Build the full-valley 4 m line-of-sight rasters from USGS 3DEP terrain."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
import argparse
import hashlib
import json
import shutil
import sys

ROOT = Path.cwd()
DATA = ROOT / "private/winter-siting"
REPORT = ROOT / "private/mountain-node-study-20261118"
CACHE = REPORT / "cache"
TILES = {"n37w115":445709830, "n36w115":432922435, "n36w116":417100345}
ANGELS = ["Angel Vegas", *[f"Angel road survey {i}" for i in (1,3,5)]]
# The mountain and metro margins include North Las Vegas, Lake Las Vegas and southern Henderson.
WSEN = (-115.745,35.865,-114.84,36.445)
SPACING = 120
sys.path[:0] = [str(DATA/"envpkgs"),str(Path(__file__).resolve().parents[1]/"winter-siting")]


def acquire(tile):
    import rasterio
    directory=CACHE/"source"
    directory.mkdir(parents=True,exist_ok=True)
    filename=f"USGS_13_{tile}.tif"
    target=directory/filename
    date="20260610" if tile=="n36w116" else "20261023"
    url=f"https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/TIFF/historical/{tile}/USGS_13_{tile}_{date}.tif"
    if not target.exists():
        temp=target.with_suffix(".part")
        with urlopen(Request(url,headers={"User-Agent":"SNORR-MeshLink-study/1.0"}),timeout=150) as src, temp.open("wb") as dst:
            shutil.copyfileobj(src,dst,1024*1024)
        if temp.stat().st_size!=TILES[tile]:
            raise ValueError(f"Incomplete or revised USGS tile: {filename}")
        with rasterio.open(temp) as ds:
            assert ds.count==1 and ds.width>=10800
        temp.replace(target)
    with target.open("rb") as src:
        digest=hashlib.file_digest(src,"sha256").hexdigest()
    return {"file":filename,"url":url,"bytes":target.stat().st_size,"sha256":digest}


def mosaic():
    import numpy as np
    import rasterio as rio
    from rasterio.transform import from_origin
    from rasterio.warp import reproject, Resampling, transform_bounds
    from terrain import write_raster, CRS
    from math import floor,ceil
    dst=CACHE/"vegas-henderson-20m.tif"
    if dst.exists():
        return dst
    west,south,east,north=transform_bounds("EPSG:4326",CRS,*WSEN,densify_pts=31)
    l,b=(floor(v/SPACING)*SPACING-SPACING for v in (west,south))
    r,t=(ceil(v/SPACING)*SPACING+SPACING for v in (east,north))
    trans=from_origin(l,t,20,20)
    z=np.full(((t-b)//20,(r-l)//20),-9999.,dtype="float32")
    tiles=[next((DATA/"source").glob("USGS_13_n37w116*.tif")),*sorted((CACHE/"source").glob("*.tif"))]
    for path in tiles:
        with rio.open(path) as ds:
            reproject(rio.band(ds,1),z,dst_crs=CRS,dst_transform=trans,dst_nodata=-9999,
                      init_dest_nodata=False,resampling=Resampling.bilinear,num_threads=4)
    assert np.isfinite(z).all() and z.min()>-500,"Whole-valley source coverage incomplete"
    temp=dst.with_suffix(".part.tif")
    write_raster(temp,z,trans,-9999)
    temp.replace(dst)
    return dst


def calculate():
    import numpy as np
    import rasterio
    from terrain import load_dem, points, sight, write_raster
    from rasterio.transform import from_origin
    from model import grid as mountain, meta as mountain_transform, OUT, wave, radius
    data=json.loads((OUT/"search.json").read_bytes())
    path=mosaic()
    dem,transform=load_dem(path)
    with rasterio.open(path) as src:
        left,bottom,right,top=src.bounds
    gx,gy=np.meshgrid(np.arange(left+SPACING/2,right,SPACING),np.arange(top-SPACING/2,bottom,-SPACING))
    ends=points(dem,transform,np.column_stack((gx.ravel(),gy.ravel())),4)
    assert np.isfinite(ends).all()
    for k in ANGELS:
        dest=CACHE/(k+"-valley.tif")
        start=points(mountain,mountain_transform,[data["xy"][k]],4)[0]
        if not dest.exists():
            visibility=sight(dem,transform,start,ends,20,wave,radius).reshape(gx.shape)
            temp=dest.with_suffix(".part.tif")
            write_raster(temp,visibility,from_origin(left,top,SPACING,SPACING))
            temp.replace(dest)
        print(f"Valley 4 m viewshed ready: {k}",flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch",action="store_true",help="Download the three missing source tiles and record their digests")
    args=parser.parse_args()
    if args.fetch:
        with ThreadPoolExecutor(max_workers=3) as pool:
            manifest=list(pool.map(acquire,TILES))
        (CACHE/"source"/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf8")
    else:
        calculate()
