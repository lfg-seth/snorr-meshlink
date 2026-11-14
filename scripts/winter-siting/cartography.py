"""North-up field maps drawn from the projected model grid and measured road geometry."""
import json
from io import BytesIO
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, ListedColormap, BoundaryNorm, LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from matplotlib import patheffects as effects
import rasterio
from shapely.geometry import shape, Point
from shapely.ops import transform, unary_union
from terrain import forward
from field_names import field_name, field_code

INK='#193742'
TEAL='#00746d'
GOLD='#e4ad50'
RED='#a6344a'
BLANK='#eeede7'
MUTE='#526970'
ROAD_NAMES=('SR 156','SR 157','SR 158','Macks Canyon','Angel Peak','Champion')
SITE_COLORS=['#227e85','#a7cf58','#d383a4','#a171b0','#5d9cd0','#bd973d','#539e61','#ce7850','#7883bb']
SHARED='#435a63'
OFFSETS={'GK':(7,8),'CH':(7,-11),'GL':(7,6),'LF':(-7,-10),'LC':(-7,6),'CM':(7,7),
         'EL':(6,7),'SG':(6,-9),'FL':(-7,6),'AL':(6,7),'KJ':(7,7),'CL':(-7,8),'SK':(-6,-7),'AM':(6,7),'DC':(-5,8)}

def finish(fig):
    buf=BytesIO()
    fig.savefig(buf,format='png',dpi=190,facecolor=fig.get_facecolor(),bbox_inches='tight',pad_inches=.045)
    plt.close(fig);buf.seek(0)
    return buf

def label(ax,x,y,text,offset=(4,4),size=10,color=INK):
    return ax.annotate(text,(x,y),xytext=offset,textcoords='offset points',fontsize=size,
                       ha='right' if offset[0]<0 else 'left',va='center',color=color,
                       fontweight='bold',annotation_clip=True,zorder=12,
                       path_effects=[effects.withStroke(linewidth=3.8,foreground='white')])

def features(root,name):
    result=json.loads((root/'gis'/(name+'.geojson')).read_bytes())
    return [(transform(forward.transform,shape(f['geometry'])),f['properties']) for f in result['features']]

def frame(bounds,pad=.10,min_span=650):
    x,y,z,w=bounds
    dx=max(z-x,min_span);dy=max(w-y,min_span)
    return [(x+z)/2-dx*(.5+pad),(x+z)/2+dx*(.5+pad),(y+w)/2-dy*(.5+pad),(y+w)/2+dy*(.5+pad)]

class Maps:
    def __init__(self,root,result):
        self.root=root;self.r=result
        self.sites={s['id']:s for s in result['sites']}
        self.order=result['selected'];self.active=result['gateways']+self.order
        self.routes=features(root,'routes');self.gaps=features(root,'road-gaps')
        self.approaches=features(root,'approaches');self.facilities=features(root,'facilities')
        self.boundary=features(root,'boundary')[0][0]
        local=json.loads((root/'source/local-osm.geojson').read_bytes())['features']
        self.local_lines=[]
        for f in local:
            props=f['properties']
            if f['geometry']['type']=='LineString' and props.get('highway'):
                geom=transform(forward.transform,shape(f['geometry']))
                self.local_lines.append((geom,props.get('highway')))
        self.roads=[(g,p['name']) for g,p in self.routes if p['kind']=='road']
        self.status=features(root,'route-status')
        with rasterio.open(root/'gis/reachability.tif') as ds:
            b=ds.bounds;self.extent=[b.left,b.right,b.bottom,b.top]
        with rasterio.open(root/'cache/terrain-local.tif') as ds:
            self.elev=ds.read(1,out_shape=(730,810),resampling=rasterio.enums.Resampling.bilinear)
            b=ds.bounds;self.rel_extent=[b.left,b.right,b.bottom,b.top]
            self.relief=LightSource(azdeg=310,altdeg=35).hillshade(self.elev,dx=(b.right-b.left)/810,dy=(b.top-b.bottom)/730)
        self.longest_gap={k:max((g for g,p in self.gaps if p['name']==k),key=lambda g:g.length,default=None) for k in ROAD_NAMES}

    def values(self,key):
        with rasterio.open(self.root/'gis'/(key+'.tif')) as ds:return ds.read(1)

    def base(self,ax,extent=None,detail=True):
        ext=extent if extent is not None else frame(self.boundary.bounds,.045)
        ax.set_facecolor('#fafaf6');ax.imshow(self.relief,cmap='Greys_r',extent=self.rel_extent,alpha=.24,vmin=-.3,vmax=1.3)
        if detail:
            ax.add_collection(LineCollection([np.asarray(g.coords) for g,p in self.routes if p['kind']=='trail'],
                                            colors='#8b9389',linewidths=.42,alpha=.46,zorder=2))
        ax.add_collection(LineCollection([np.asarray(g.coords) for g,n in self.roads],
                                        colors='white',linewidths=2.2 if detail else 1.3,zorder=3))
        ax.add_collection(LineCollection([np.asarray(g.coords) for g,n in self.roads],colors='#617473',
                                        linewidths=.8 if detail else .5,zorder=3.1))
        ax.plot(*self.boundary.exterior.xy,c='#a6afa8',lw=.65,zorder=2)
        ax.set_xlim(ext[:2]);ax.set_ylim(ext[2:]);ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
        for sp in ax.spines.values():sp.set_visible(False)

    def scale(self,ax,small=False):
        x0,x1=ax.get_xlim();y0,y1=ax.get_ylim()
        length=max(v for v in (10,25,50,100,250,500,1000,2000,5000) if v<=(x1-x0)*.20)
        x=x0+.035*(x1-x0);y=y0+.046*(y1-y0)
        ax.plot([x,x+length],[y,y],color=INK,lw=1.8,zorder=11,path_effects=[effects.withStroke(linewidth=3.8,foreground='white')])
        label(ax,x,y,f'{length/1000:g} km' if length>=1000 else f'{length} m',(0,5),7 if small else 8)
        ax.text(.98,.965,'N ↑',transform=ax.transAxes,ha='right',va='top',fontsize=8 if small else 10,
                weight='bold',color=INK,zorder=11,bbox=dict(fc='white',ec='none',alpha=.9,pad=1))

    def layer(self,ax,values,colors):
        count=len(colors)
        ax.imshow(np.ma.masked_where(values==255,values),extent=self.extent,
                  cmap=ListedColormap(colors),norm=BoundaryNorm(np.arange(-.5,count+.5),count),
                  interpolation='nearest',zorder=1.5)

    def sites_on(self,ax,keys,style='code',size=10):
        for k in keys:
            s=self.sites[k];gateway=k in self.r['gateways']
            ax.scatter(s['x'],s['y'],s=36 if gateway else 34,marker='D' if gateway else '^',
                       facecolor=INK,edgecolor='white',lw=.85,zorder=9)
            if style:
                label(ax,s['x'],s['y'],field_name(k) if style=='name' else field_code(k),OFFSETS.get(k,(6,5)),size)

    def labels_roads(self,ax,which=ROAD_NAMES):
        frac={'SR 156':.78,'SR 157':.45,'SR 158':.34,'Macks Canyon':.67,'Angel Peak':.30,'Champion':.28}
        for name in which:
            g=max((g for g,n in self.roads if n==name),key=lambda g:g.length)
            pt=g.interpolate(frac[name],normalized=True)
            pretty={'Macks Canyon':'Macks Canyon Rd','Angel Peak':'Angel Peak approach','Champion':'Champion Rd'}.get(name,name)
            off={'Angel Peak':(-6,-11),'Macks Canyon':(-2,10),'SR 158':(8,-8),'Champion':(12,-9),'SR 156':(8,-10)}.get(name,(4,-10))
            label(ax,pt.x,pt.y,pretty,off,9,'#3e5159')

    def path(self,ax,sequence,color=TEAL,dash=False):
        xy=np.array([(self.sites[k]['x'],self.sites[k]['y']) for k in sequence])
        ax.plot(*xy.T,color=color,ls='--' if dash else '-',lw=2.5,zorder=6,
                path_effects=[effects.withStroke(linewidth=4.5,foreground='white')])

    def overview(self,mode):
        fig,ax=plt.subplots(figsize=(8.1,6.5));self.base(ax)
        if mode=='union':self.layer(ax,self.values('terrain-union'),[BLANK,'#72bca9'])
        elif mode=='overlap':
            counts=self.values('relay-overlap')
            classes=np.zeros_like(counts)
            for index,k in enumerate(self.order,1):
                classes[(self.values('viewshed-'+k)==1)&(counts==1)]=index
            classes[counts>1]=len(self.order)+1
            classes[counts==255]=255
            self.layer(ax,classes,[BLANK]+SITE_COLORS[:len(self.order)]+[SHARED])
        elif mode=='deployment':
            edges={tuple(sorted((a,b))) for seq in self.r['paths'].values() for a,b in zip(seq,seq[1:])}
            for edge in sorted(edges):self.path(ax,edge)
            for name,offset in [('Macks Canyon',(-8,12))]:
                g=self.longest_gap[name]
                if g is not None:
                    ax.plot(*g.xy,color=RED,lw=3,zorder=6)
                    p=g.interpolate(.45,normalized=True)
                    label(ax,p.x,p.y,name+' gap',offset,10,RED)
        self.sites_on(ax,self.order if mode=='overlap' else self.active,style='code',size=11)
        if mode!='deployment':self.labels_roads(ax,('SR 156','SR 157','SR 158','Angel Peak','Macks Canyon'))
        self.scale(ax);fig.tight_layout(pad=.05)
        return finish(fig)

    def mini_grid(self,keys):
        cols=3 if len(keys)>4 else 2;rows=(len(keys)+cols-1)//cols
        fig,axes=plt.subplots(rows,cols,figsize=(8.1,2.45*rows),squeeze=False)
        for ax,k in zip(axes.flat,keys):
            self.base(ax,detail=False)
            self.layer(ax,self.values('viewshed-'+k),[BLANK,'#4a9f8f'])
            subtitle=f"{self.sites[k]['selected_footprint']['road_km']:.1f} km of road visible"
            self.sites_on(ax,[k],style=None)
            title={'SK':'Upper Bristlecone (UB)','AM':'Angel Peak (AM)','AV':'Angel Peak (AV)'}.get(k,field_name(k))
            ax.set_title(title,fontsize=10,loc='left',fontweight='bold',color=INK,pad=4)
            ax.set_xlabel(subtitle,fontsize=9,labelpad=1,color=MUTE)
        for ax in list(axes.flat)[len(keys):]:ax.axis('off')
        fig.subplots_adjust(wspace=.13,hspace=.30)
        return finish(fig)

    def operating_roads(self,trails=False):
        fig,ax=plt.subplots(figsize=(8.1,6.3))
        self.base(ax,detail=False)
        for cls,color in [('reachable',TEAL),('blind',RED)]:
            seg=[np.asarray(g.coords) for g,p in self.status
                 if (p['name'] not in ROAD_NAMES)==trails and p['status']==cls]
            ax.add_collection(LineCollection(seg,colors=color,linewidths=1.8 if trails else 4,
                                            zorder=5,capstyle='round'))
        self.sites_on(ax,self.r['gateways'],'code',10)
        self.labels_roads(ax,('SR 156','SR 157','SR 158','Macks Canyon','Champion'))
        if not trails:
            for name,ends in self.r['highways'].items():
                for end in ends:
                    x,y=forward.transform(*end)
                    ax.scatter(x,y,s=38,fc='white',ec=INK,lw=1.2,zorder=6)
            for k,short,offset in [('SK','Upper Bristlecone',(-5,-12)),('AM','Mountain pin',(-6,11)),('AV','Vegas pin',(7,-6))]:
                v=self.sites[k];ax.scatter(v['nx'],v['ny'],s=32,marker='^',fc=INK,ec='white',lw=.9,zorder=8)
                label(ax,v['nx'],v['ny'],short,offset,9)
            self.labels_roads(ax,('Angel Peak',))
            gap=self.longest_gap['Macks Canyon']
            if gap:
                for tag,xy in zip('AB',[gap.coords[0],gap.coords[-1]]):
                    ax.scatter(*xy,s=28,fc='white',ec=RED,zorder=6);label(ax,*xy,tag,(2,-9),9,RED)
        self.scale(ax);fig.tight_layout(pad=.05)
        return finish(fig)

    def locator(self,ax,keys,edges=()):
        points=[Point(self.sites[k]['x'],self.sites[k]['y']) for k in keys]
        bounds=unary_union(points).bounds
        ext=frame(bounds,.27,1500)
        # Keep room beside the chain for readable names in these portrait-oriented canyons.
        width=max(ext[1]-ext[0],1.18*(ext[3]-ext[2]))
        cx=(ext[0]+ext[1])/2
        ext[:2]=[cx-width/2,cx+width/2]
        self.base(ax,ext)
        for start,end,blocked in edges:self.path(ax,(start,end),RED if blocked else TEAL,blocked)
        self.sites_on(ax,keys,'code',12);self.scale(ax,True)
        return ext

    def location_image(self,keys,edges):
        fig,(overview,ax)=plt.subplots(1,2,figsize=(8,3.05),gridspec_kw={'width_ratios':[1,1.3]})
        ext=self.locator(ax,keys,edges)
        self.base(overview,detail=False)
        overview.add_patch(Rectangle((ext[0],ext[2]),ext[1]-ext[0],ext[3]-ext[2],
                                     facecolor='#e4ad5030',edgecolor='#9a641e',lw=1.8,zorder=6))
        self.sites_on(overview,self.r['gateways'],None)
        for k,off in [('GL',(4,7)),('GK',(4,7))]:
            s=self.sites[k];label(overview,s['x'],s['y'],field_name(k),off,9)
        self.scale(overview,True)
        for panel,title in [(overview,'Mountain locator'),(ax,'Test links within the box')]:
            panel.set_title(title,loc='left',fontsize=11,weight='bold',color=INK,pad=3)
        fig.subplots_adjust(left=.01,right=.99,top=.91,bottom=.02,wspace=.09)
        return finish(fig)

    def station_masks(self,hops):
        import networkx as nx
        active_pairs=[(p['a'],p['b']) for p in self.r['pairs'] if p['active'] and p['los']]
        graph=nx.Graph();graph.add_nodes_from(self.active);graph.add_edges_from(active_pairs)
        masks={}
        for station in self.r['gateways']:
            g=graph.copy();g.remove_nodes_from(set(self.r['gateways'])-{station})
            receivers=nx.single_source_shortest_path_length(g,station,cutoff=hops)
            masks[station]=np.logical_or.reduce([self.values('viewshed-'+k)==1 for k in receivers])
        return masks

    def station_image(self,hops):
        masks=self.station_masks(hops);kyle,lee=masks['GK'],masks['GL']
        v=kyle.astype('uint8')+2*lee.astype('uint8')
        v[self.values('reachability')==255]=255
        fig,ax=plt.subplots(figsize=(8.1,6.5));self.base(ax)
        self.layer(ax,v,[BLANK,'#9e83b6','#77b6c9',TEAL])
        self.sites_on(ax,self.r['gateways'],'name',12)
        self.labels_roads(ax,('Macks Canyon','SR 156','SR 157','SR 158','Angel Peak'))
        self.scale(ax);fig.tight_layout(pad=.05)
        return finish(fig),v

    def valley_image(self,cfg):
        from city_streets import streets
        sectors=cfg['valley_sectors'];bounds=cfg['valley_map_wsen']
        fig,ax=plt.subplots(figsize=(10.3,4.4))
        terrain_file=self.root/'cache/terrain-regional.tif'
        with rasterio.open(terrain_file) as source:
            z=source.read(1,out_shape=(470,650),resampling=rasterio.enums.Resampling.bilinear)
            b=source.bounds
            relief=LightSource(azdeg=315,altdeg=38).hillshade(z,dx=(b.right-b.left)/650,dy=(b.top-b.bottom)/470)
            ax.imshow(relief,extent=[b.left,b.right,b.bottom,b.top],cmap='Greys_r',alpha=.28,vmin=-.2,vmax=1.3)
        roads=streets(self.root,bounds)
        layers={};label_roads=[]
        for kind,ref,name,coords in roads:
            x,y=forward.transform(*np.array(coords).T)
            xy=np.column_stack((x,y))
            layers.setdefault(kind,[]).append(xy)
            if kind=='motorway' or name in cfg['city_labels']:
                label_roads.append((ref,name,xy))
        for kinds,color,width in [(['residential','unclassified'],'#a8b8b4',.32),(['tertiary'],'#a2b3af',.5),
                                  (['secondary','primary'],'#718987',.76),(['motorway','trunk'],'#7b6332',2.4),
                                  (['motorway','trunk'],'#ffe79d',1.24)]:
            lines=[xy for k in kinds for xy in layers.get(k,())]
            ax.add_collection(LineCollection(lines,colors=color,linewidths=width,zorder=2))
        origin=self.sites['AV'];ox,oy=origin['nx'],origin['ny']
        for idx,(name,lon,lat) in enumerate(sectors,1):
            x,y=forward.transform(lon,lat)
            count=next(v['clear'] for v in self.r['valley_drive_up'] if v['sector']==name and v['angel']=='AV')
            col=TEAL if count else RED
            ax.plot([ox,x],[oy,y],c=col,lw=1.45,ls='-' if count else '--',zorder=3)
            ax.add_patch(Rectangle((x-500,y-500),1000,1000,facecolor='white',edgecolor=col,lw=1.45,zorder=4))
            short=('Centennial Hills','Lone Mountain','Providence','North Las Vegas')[idx-1]
            dx,dy=[(-3,-15),(3,-14),(-6,12),(-4,13)][idx-1]
            label(ax,x,y,f'{idx}  {short}',(dx,dy),9.6,col)
        for k in ('AV','AM'):
            s=self.sites[k];ax.scatter(s['nx'],s['ny'],s=35,marker='^',fc=INK,ec='white',lw=.85,zorder=9)
        label(ax,ox,oy,'Angel Peak · Vegas side',(1,-14),11)
        s=self.sites['AM'];label(ax,s['nx'],s['ny'],'Mountain side',(1,12),10)
        for street,info in cfg['city_labels'].items():
            short,lon,lat,dx,dy=info
            target=np.array(forward.transform(lon,lat))
            coords=[xy for ref,n,xy in label_roads if street==n or street in ref.split(';')]
            if not coords:raise ValueError('Missing city landmark: '+street)
            pts=np.concatenate(coords);near=pts[np.argmin(np.linalg.norm(pts-target,axis=1))]
            label(ax,*near,short,(dx,dy),8.8,'#594723' if street in ('US 95','CC 215') else '#3f5059')
        w,south=forward.transform(bounds[0],bounds[1]);east,n=forward.transform(bounds[2],bounds[3])
        ax.set_xlim(w,east);ax.set_ylim(south,n);ax.set_aspect('equal')
        ax.set_xticks([]);ax.set_yticks([])
        for s in ax.spines.values():s.set_visible(False)
        self.scale(ax);fig.tight_layout(pad=0)
        return finish(fig)

    def site_image(self,k):
        s=self.sites[k];fig,axes=plt.subplots(1,2,figsize=(8.1,3.15))
        ax,zoom=axes;self.base(ax,detail=False)
        self.layer(ax,self.values('viewshed-'+k),[BLANK,'#61ad99']);self.sites_on(ax,[k],None)
        self.scale(ax,True)
        px,py=forward.transform(*s['stop_ll'])
        bounds=unary_union([Point(px,py),Point(s['x'],s['y'])]+[g for g,p in self.approaches if p['id']==k]).bounds
        self.base(zoom,frame(bounds,.25,320))
        left,right=zoom.get_xlim();bottom,top=zoom.get_ylim()
        nearby={'trail':[],'road':[]}
        for geom,kind in self.local_lines:
            x0,y0,x1,y1=geom.bounds
            if x0<=right and x1>=left and y0<=top and y1>=bottom:
                group='trail' if kind in ('path','footway','steps','cycleway','bridleway') else 'road'
                nearby[group].append(np.asarray(geom.coords))
        for group,color,width,style in [('road','#718385',1.05,'solid'),('trail','#91a18d',.75,'dotted')]:
            zoom.add_collection(LineCollection(nearby[group],colors=color,linewidths=width,linestyles=style,zorder=4))
        for g,p in self.approaches:
            if p['id']==k:
                coords=np.asarray(g.coords)
                zoom.plot(*coords.T,color='#a95033',lw=2,ls='--',zorder=5)
                if p['method'].startswith('mapped') and len(coords)>3:
                    zoom.plot(*coords[1:-1].T,color='#a95033',lw=2,zorder=6)
        if k not in self.r['gateways']:
            zoom.scatter(px,py,s=38,marker='s',fc='white',ec=INK,zorder=8)
            label(zoom,px,py,'Stage',(-5,8) if px>s['x'] else (5,8),9)
            zoom.add_patch(plt.Circle((s['nx'],s['ny']),20,fill=False,color='#af502e',lw=1.5,zorder=7))
        self.sites_on(zoom,[k],'code');self.scale(zoom,True)
        for a,title in zip(axes,['Member-height footprint','Staging and final approach']):
            a.set_title(title,fontsize=11,loc='left',color=INK,fontweight='bold',pad=3)
        fig.subplots_adjust(wspace=.13);return finish(fig)

    def cover_art(self):
        fig,ax=plt.subplots(figsize=(9,5.4),facecolor=INK)
        z=self.elev
        colors=LinearSegmentedColormap.from_list('altitude',['#102e38','#285965','#55918c','#abc5ad','#eee9cf'])
        ax.imshow(z,extent=self.rel_extent,cmap=colors,aspect='equal',origin='upper')
        ax.imshow(self.relief,extent=self.rel_extent,cmap='Greys_r',alpha=.27)
        ax.contour(z,levels=np.arange(1500,4000,75),origin='upper',extent=self.rel_extent,colors='#fcf6da',linewidths=.37,alpha=.50)
        ax.add_collection(LineCollection([np.asarray(g.coords) for g,n in self.roads if n.startswith('SR')],colors='#fff8d9',linewidths=.72,alpha=.8))
        for k in self.active:
            s=self.sites[k];ax.scatter(s['x'],s['y'],s=23,marker='D' if k in self.r['gateways'] else '^',facecolor='#ffe8a6',edgecolor=INK,lw=.8,zorder=4)
        w,e,so,no=self.extent;ax.set_xlim(w,e);ax.set_ylim(so,no);ax.axis('off');fig.subplots_adjust(0,0,1,1)
        return finish(fig)
