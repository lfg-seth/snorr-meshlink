"""Projected bare-earth surfaces and sampled straight-ray terrain profiles."""
from math import ceil, hypot
import numpy as np
import rasterio as rio
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_origin
from pyproj import Transformer
from numba import njit, prange

CRS = "EPSG:26911"
forward = Transformer.from_crs(4326, CRS, always_xy=True)
inverse = Transformer.from_crs(CRS, 4326, always_xy=True)


def write_raster(path, data, transform, nodata=None):
    with rio.open(path, 'w', driver='GTiff', width=data.shape[1], height=data.shape[0],
                  count=1, dtype=data.dtype, crs=CRS, transform=transform, nodata=nodata,
                  tiled=True, compress='deflate', BIGTIFF='IF_SAFER') as dst:
        dst.write(data, 1)


def mosaic(source, destination, bounds, resolution, local):
    west, south, east, north = bounds
    transform = from_origin(west, north, resolution, resolution)
    array = np.full((ceil((north-south)/resolution), ceil((east-west)/resolution)), -9999., 'float32')
    files = sorted(source.glob('USGS_13*.tif'))
    sources = files + (sorted(source.glob('USGS_1M*.tif')) if local else [])
    for f in sources:
        with rio.open(f) as ds:
            reproject(rio.band(ds,1), array, dst_crs=CRS, dst_transform=transform,
                      dst_nodata=-9999, init_dest_nodata=False, resampling=Resampling.bilinear,
                      num_threads=4)
    if not files or array.min() <= -9999:
        raise ValueError('Incomplete terrain coverage: '+str(destination))
    write_raster(destination,array,transform,-9999.)


@njit
def elevation(grid, meta, x, y):
    col = (x-meta[0])/meta[2]-.5
    row = (meta[1]-y)/meta[2]-.5
    if col < 0 or row < 0 or col >= grid.shape[1]-1 or row >= grid.shape[0]-1:
        return np.nan
    i, j = int(row), int(col)
    a,b = col-j,row-i
    return (grid[i,j]*(1-a)+grid[i,j+1]*a)*(1-b)+(grid[i+1,j]*(1-a)+grid[i+1,j+1]*a)*b


def load_dem(path):
    with rio.open(path) as ds:
        return ds.read(1), np.array([ds.transform.c, ds.transform.f, ds.transform.a])


@njit
def ray(grid, meta, origin, target, step, wavelength, radius, quick=False):
    """Endpoint vectors are metric x, y, absolute antenna z. Exclude endpoints."""
    dx,dy=target[0]-origin[0],target[1]-origin[1]
    d=hypot(dx,dy)
    n=max(2,int(ceil(d/step)))
    minimum, fraction, at = 1e9,1e9,0.
    for i in range(1,n):
        t=i/n
        ground=elevation(grid,meta,origin[0]+dx*t,origin[1]+dy*t)
        if not np.isfinite(ground):
            return -1e6,-1e6,0.
        clearance=origin[2]+(target[2]-origin[2])*t-ground-d*d*t*(1-t)/(2*radius)
        if quick and clearance<0:
            return clearance,-1.,d*t
        if clearance<minimum:
            minimum,at=clearance,d*t
        fraction=min(fraction,clearance/max(.0001,(wavelength*d*t*(1-t))**.5))
    return minimum,fraction,at


@njit(parallel=True)
def sight(grid,meta,origin,targets,step,wavelength,radius):
    result=np.zeros(len(targets),np.uint8)
    for i in prange(len(targets)):
        result[i]=ray(grid,meta,origin,targets[i],step,wavelength,radius,True)[0]>=0
    return result


def points(grid,meta,xy,height):
    return np.array([[x,y,elevation(grid,meta,x,y)+height] for x,y in xy],dtype='float64')
