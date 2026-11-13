"""Printable maps on a common NAD83 / UTM zone 11N frame."""
import json
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LightSource
from matplotlib import patheffects
from matplotlib.collections import LineCollection
from shapely.geometry import shape
from shapely.ops import transform
from terrain import forward
import rasterio

PALETTE=['#3966ad','#bf4a30','#48892b','#914a9a','#098a88','#ca7b08','#a73964','#626b38','#35355c']


class Maps:
    def __init__(self,root,result):
        self.root=root
        self.sites={s['id']:s for s in result['sites']}
        self.order=result['selected']
        self.highways=result['highways']
        self.active=result['gateways']+self.order
        def read(name):
            return [(transform(forward.transform,shape(f['geometry'])),f['properties'])
                    for f in json.loads((root/'gis'/(name+'.geojson')).read_bytes())['features']]
        self.routes=read('routes')
        self.gaps=read('road-gaps')
        self.approaches=read('approaches')
        self.facilities=read('facilities')
        self.boundary=read('boundary')[0][0]
        with rasterio.open(root/'gis/reachability.tif') as ds:
            b=ds.bounds;self.extent=[b.left,b.right,b.bottom,b.top]
        with rasterio.open(root/'cache/terrain-local.tif') as ds:
            t=ds.read(1,out_shape=(700,750),resampling=rasterio.enums.Resampling.bilinear)
            b=ds.bounds;self.rel_extent=[b.left,b.right,b.bottom,b.top]
            self.gray=LightSource(azdeg=320,altdeg=42).hillshade(t,dx=(b.right-b.left)/750,dy=(b.top-b.bottom)/700)
        self.labelpoints={}
        for name in sorted({p['name'] for _,p in self.routes if p['kind']=='road'}):
            g=max((g for g,p in self.routes if p['name']==name),key=lambda g:g.length)
            frac={'SR 156':.81,'SR 157':.8,'SR 158':.27,'Macks Canyon':.7,'Champion':.4,'Lucky Strike':.22}.get(name,.5)
            self.labelpoints[name]=g.interpolate(frac,normalized=True).coords[0]

    def values(self,stem):
        with rasterio.open(self.root/'gis'/(stem+'.tif')) as ds:return ds.read(1)

    def paint(self,ax,mode,site=None,local=False):
        ax.imshow(self.gray,cmap='Greys_r',extent=self.rel_extent,alpha=.4,origin='upper',interpolation='bilinear',vmin=-.25,vmax=1.1)
        if mode=='overlay':
            for idx,code in enumerate(self.order):
                v=self.values('viewshed-'+code)==1
                yy,xx=np.indices(v.shape)
                # A tiled dot lattice retains every overlapping footprint's color and identity.
                mask=v & (yy%3==idx//3) & (xx%3==idx%3)
                ax.imshow(np.ma.masked_where(~mask,np.ones(v.shape)),cmap=ListedColormap([PALETTE[idx]]),
                          extent=self.extent,interpolation='nearest',alpha=.98)
        else:
            raster='viewshed-'+site if site else ('terrain-union' if mode=='union' else 'reachability')
            v=self.values(raster)
            cmap=ListedColormap(['#bd7339','#06766d'] if mode=='reach' and not site else ['#127d74'])
            ax.imshow(np.ma.masked_where((v==0)|(v==255),v),extent=self.extent,cmap=cmap,vmin=1,vmax=2 if cmap.N==2 else 1,
                      alpha=.70,interpolation='nearest')
        extent=self.extent
        if local:
            s=self.sites[site];px,py=forward.transform(*s['stop_ll'])
            pad=max(350,abs(px-s['x'])*.25,abs(py-s['y'])*.25)
            extent=[min(px,s['x'])-pad,max(px,s['x'])+pad,min(py,s['y'])-pad,max(py,s['y'])+pad]
            cx=(extent[0]+extent[1])/2;cy=(extent[2]+extent[3])/2
            span=max(extent[1]-extent[0],extent[3]-extent[2])
            extent=[cx-span/2,cx+span/2,cy-span/2,cy+span/2]
        for typ in ('trail','road'):
            segments=[np.asarray(g.coords) for g,p in self.routes if p['kind']==typ]
            ax.add_collection(LineCollection(segments,colors='#64706b' if typ=='trail' else '#30404a',linewidths=.3 if typ=='trail' else 1.05,alpha=.65 if typ=='trail' else .92))
        if mode=='reach' and not local:
            ax.add_collection(LineCollection([np.asarray(g.coords) for g,p in self.gaps],colors='#aa2143',linewidths=1.8))
        def label(x,y,text,color='#243641',size=7,off=(3,3)):
            obj=ax.annotate(text,(x,y),xytext=off,textcoords='offset points',fontsize=size,color=color,weight='bold',clip_on=True)
            obj.set_path_effects([patheffects.withStroke(linewidth=2.6,foreground='white',alpha=.98)])
        if not local and not site:
            if mode=='reach':
                for coords in self.highways.values():
                    for point in coords:
                        endx,endy=forward.transform(*point)
                        ax.scatter(endx,endy,s=42,marker='o',facecolor='none',edgecolor='#1c2532',linewidths=1.1,zorder=6)
            for name,(x,y) in self.labelpoints.items():
                label(x,y,name,size=7,off=(-40,-10) if name=='Lucky Strike' else (16,3) if name=='SR 157' else (2,-9))
            if mode=='union':
                for g,p in self.facilities:
                    if g.geom_type!='Polygon':continue
                    pos=g.representative_point();name=p['name'].replace(' Group Campground','').replace(' Campground','')
                    ax.scatter(pos.x,pos.y,s=14,facecolor='#fffefa',edgecolor='#635d49',zorder=5)
                    label(pos.x,pos.y,name,size=6,off={'Fletcher View':(-36,7),'Kyle Canyon':(0,-11),'Mahogany Grove':(-43,7),'Hilltop':(4,7),'McWilliams':(-37,-7)}.get(name,(2,6)))
                ski=[g for g,p in self.facilities if p['name']=='Lee ski terrain']
                if ski:
                    pos=max(ski,key=lambda g:g.length).interpolate(.5,normalized=True)
                    label(pos.x,pos.y,'Lee ski resort',size=7,off=(-32,-8))
        if local:
            for g,p in self.approaches:
                if p['id']==site:ax.plot(*g.xy,color='#ba4e2d',lw=2,ls='--')
            if site not in ('GK','GL'):
                ax.scatter(px,py,marker='s',s=32,c='#f8f5ec',edgecolor='#8a4926',zorder=7);label(px,py,'STAGE',off=(4,-9))
            ax.add_patch(plt.Circle((s['nx'],s['ny']),20,fill=False,color='#a4451e',lw=1.4,zorder=8))
        for code in ([site] if site else self.active):
            s=self.sites[code];x,y=s['x'],s['y'];gw=code in ('GK','GL')
            color=PALETTE[self.order.index(code)] if mode=='overlay' and not gw else '#202e3c'
            ax.scatter(x,y,marker='D' if gw else '^',color=color,s=32 if gw else 29,edgecolors='white',linewidths=.65,zorder=8)
            label(x,y,code,off={'GK':(4,4),'CH':(-17,-8),'CM':(3,4),'LC':(-14,-9),'DC':(-14,3),'FL':(-14,3)}.get(code,(4,4)))
        ax.plot(*self.boundary.exterior.xy,c='#61716b',lw=.65)
        ax.set_xlim(extent[:2]);ax.set_ylim(extent[2:]);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
        for sp in ax.spines.values():sp.set_color('#b8c4bf')
        length=2000 if not local else (100 if span<1600 else 500)
        x=extent[0]+(extent[1]-extent[0])*.045;y=extent[2]+(extent[3]-extent[2])*.055
        ax.plot([x,x+length],[y,y],color='#192a32',lw=2.4)
        label(x,y,(f'{length/1000:g} km' if length>=1000 else f'{length} m'),size=6,off=(0,3))
        ax.text(.97,.95,'N ↑',ha='right',va='top',fontsize=8,transform=ax.transAxes,bbox=dict(fc='white',ec='none',alpha=.85))

    def image(self,mode,site=None):
        if site:
            fig,axs=plt.subplots(1,2,figsize=(9,3.1))
            self.paint(axs[0],mode,site);self.paint(axs[1],mode,site,True)
            axs[0].set_title('Member-height footprint across the operating area',fontsize=9,loc='left')
            axs[1].set_title('Staging and final search area',fontsize=9,loc='left')
        else:
            fig,ax=plt.subplots(figsize=(8.3,6.7));self.paint(ax,mode)
        fig.tight_layout(pad=.25)
        out=BytesIO();fig.savefig(out,format='png',dpi=175,bbox_inches='tight',pad_inches=.03);plt.close(fig);out.seek(0)
        return out
