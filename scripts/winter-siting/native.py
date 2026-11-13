"""Vectorized bilinear profiles in native one-metre tiles, falling back outside their footprint."""
from functools import lru_cache
import math
import numpy as np
import rasterio
from rasterio.windows import Window
from terrain import elevation

class Profiles:
    def __init__(self,files,grid,meta,wav,radius):
        self.tiles=[rasterio.open(f) for f in sorted(files)]
        self.grid,self.meta,self.wav,self.radius=grid,meta,wav,radius

    @lru_cache(maxsize=1800)
    def block(self,t,r,c):
        ds=self.tiles[t]
        return ds.read(1,window=Window(c*256,r*256,min(257,ds.width-c*256),min(257,ds.height-r*256)))

    def ground(self,x,y):
        x,y=np.atleast_1d(x),np.atleast_1d(y)
        z=np.full(len(x),np.nan)
        for ti,ds in enumerate(self.tiles):
            w,s,e,n=ds.bounds
            ix=np.flatnonzero((x>w+1)&(x<e-1)&(y>s+1)&(y<n-1)&~np.isfinite(z))
            if not len(ix):continue
            col=(x[ix]-w)/ds.transform.a-.5
            row=(n-y[ix])/(-ds.transform.e)-.5
            r,c=row.astype(int),col.astype(int)
            groups=(r//256)*1000+c//256
            for key in np.unique(groups):
                loc=np.flatnonzero(groups==key);v=self.block(ti,int(key//1000),int(key%1000))
                rr,cc=r[loc]%256,c[loc]%256
                a,b=col[loc]-c[loc],row[loc]-r[loc]
                corners=np.stack([v[rr,cc],v[rr,cc+1],v[rr+1,cc],v[rr+1,cc+1]])
                ok=np.min(corners,axis=0)>-1000
                values=(corners[0]*(1-a)+corners[1]*a)*(1-b)+(corners[2]*(1-a)+corners[3]*a)*b
                z[ix[loc[ok]]]=values[ok]
        for i in np.flatnonzero(~np.isfinite(z)):z[i]=elevation(self.grid,self.meta,x[i],y[i])
        return z

    def trace(self,a,b):
        distance=math.dist(a[:2],b[:2])
        t=np.linspace(0,1,max(3,math.ceil(distance)+1))
        ground=self.ground(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
        bulge=distance**2*t*(1-t)/(2*self.radius)
        line=ground[0]+a[2]+(ground[-1]+b[2]-ground[0]-a[2])*t
        f1=np.sqrt(self.wav*distance*t*(1-t))
        return distance*t,ground+bulge,line,f1

    def stats(self,a,b):
        d,z,line,f1=self.trace(a,b)
        clearance=(line-z)[1:-1]
        return float(clearance.min()),float((clearance/f1[1:-1]).min()),float(d[1:-1][np.argmin(clearance)])
