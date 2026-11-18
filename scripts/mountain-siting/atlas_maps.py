"""Produce the offline field atlas, geographic view rasters and micro-site checks."""
from survey import *
from basemaps import CACHE, MAPS
from PIL import Image
from functools import lru_cache
from textwrap import fill
from matplotlib.patches import Rectangle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from rasterio.transform import from_origin
from terrain import write_raster
import rasterio

plt.rcParams.update({"font.size":10,"font.family":"DejaVu Sans","axes.titleweight":"bold","pdf.fonttype":42})
L,B,R,T=boundary.bounds
step=35
xs=np.arange(L+step/2,R,step)
ys=np.arange(T-step/2,B,-step)
XX,YY=np.meshgrid(xs,ys)
ground=points(grid,meta,np.c_[XX.ravel(),YY.ravel()],1.2)
extent=[L,L+len(xs)*step,T-len(ys)*step,T]
display=export()
displaysites=set(display)
views={}
def site_view(k):
    origin=points(grid,meta,[xy[k]],wh(k))[0]
    folder=OUT/"viewsheds"
    folder.mkdir(exist_ok=True)
    path=folder/(label(k)+".tif")
    signature=json.dumps([*origin,L,T,step,*XX.shape,1.2,5.,wave,radius,
                          (DATA/"cache/terrain-local.tif").stat().st_mtime_ns])
    if path.is_file():
        with rasterio.open(path) as raster:
            if raster.tags().get("model_inputs")==signature:
                return raster.read(1).astype(bool)
    view=sight(grid,meta,origin,ground,5.,wave,radius).reshape(XX.shape)
    write_raster(path,view,from_origin(L,T,step,step))
    with rasterio.open(path,"r+") as raster:
        raster.update_tags(model_inputs=signature)
    return view.astype(bool)
for k in display:
    views[k]=site_view(k)
c1,c2,both="#ef9b19","#3f94dd","#13866e"
path_color="#ab0755"
fig=None
pdf=PdfPages(OUT/"mountain-field-atlas.pdf")
def page(section,title,sub):
    global fig
    fig=plt.figure(figsize=(11.7,8.3),facecolor="#faf9f4")
    fig.text(.045,.952,section.upper(),fontsize=10,color="#19736b",weight="bold")
    fig.text(.045,.897,title,fontsize=23,fontfamily="DejaVu Serif")
    fig.text(.045,.855,sub,fontsize=10,color="#42535a")
    return fig
def save():
    fig.text(.045,.035,"SNORR MeshLink   /   Mount Charleston     •     17 November 2026     •     Topography: USGS The National Map",fontsize=8,color="#465254")
    fig.text(.955,.035,str(pdf.get_pagecount()+1),ha="right",fontsize=8)
    pdf.savefig(fig,dpi=190)
    plt.close(fig)
def axis(rect):
    return fig.add_axes(rect)
@lru_cache(maxsize=4)
def basemap(name):
    suffix=".jpg" if name=="aerial" else ".png"
    with Image.open(CACHE/(name+suffix)) as image:
        return np.asarray(image.convert("RGB"))

def mapbase(ax,bounds=None,name="regional"):
    l,b,r,t=bounds or (L,B,R,T)
    west,south,east,north=MAPS[name][0]
    ax.imshow(basemap(name),extent=(west,east,south,north),interpolation="lanczos",zorder=0)
    ax.set(xlim=(l,r),ylim=(b,t),aspect="equal",xticks=[],yticks=[])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_color("#73837d")
    boxstyle=dict(facecolor="white",edgecolor="none",alpha=.92,pad=2.5)
    ax.text(.025,.97,"N ↑",transform=ax.transAxes,va="top",fontsize=9,weight="bold",bbox=boxstyle,zorder=12)
    width=r-l
    bar=next(d for d in [2000,1000,500,200,100,50,20,10] if d<width*.23)
    x=l+.04*width
    y=b+.052*(t-b)
    ax.plot([x,x+bar],[y,y],c="#243237",lw=2,zorder=10,path_effects=[pe.withStroke(linewidth=4,foreground="white")])
    ax.text(x,y+.014*(t-b),f"{bar/1000:g} km" if bar>=1000 else f"{bar} m",fontsize=8,color="#142324",bbox=boxstyle,zorder=10)

def link_bounds(a,b):
    x1,y1=xy[a]; x2,y2=xy[b]
    span=max(abs(x2-x1),abs(y2-y1),2800)*1.60
    cx,cy=(x1+x2)/2,(y1+y2)/2
    return cx-span*.55,cy-span*.50,cx+span*.55,cy+span*.50

def endpoint(ax,x,y,letter):
    ax.scatter(x,y,s=180,marker="o" if letter=="A" else "D",c=path_color,
               edgecolors="white",linewidths=2.3,zorder=9,clip_on=False)
    ax.annotate(letter,(x,y),ha="center",va="center",color="white",weight="bold",fontsize=9,zorder=10)

def map_labels(ax,a=None,b=None):
    """Place a few readable reference names without covering endpoints or the radio ray."""
    x0,x1=ax.get_xlim()
    y0,y1=ax.get_ylim()
    width,height=x1-x0,y1-y0
    occupied=[]
    if a:
        link=np.array([xy[a],xy[b]])
        occupied.extend((x,y,.080,.050) for x,y in (link-[x0,y0])/[width,height])
    shown=set()
    for name,x,y,kind in sorted(reference_labels(),key=lambda row:row[-1]!="road"):
        u,v=(x-x0)/width,(y-y0)/height
        rw=.052 if kind=="road" else .012*len(name)/2
        if name in shown or not (.04+rw<u<.96-rw and .13<v<.9):
            continue
        if any(abs(u-ou)<rw+ow and abs(v-ov)<.033+oh for ou,ov,ow,oh in occupied):
            continue
        if a:
            start,end=(link-[x0,y0])/[width,height]
            vector=end-start
            t=np.clip(np.dot(np.array([u,v])-start,vector)/np.dot(vector,vector),0,1)
            if np.linalg.norm(np.array([u,v])-(start+t*vector))<rw*.85:
                continue
        if kind=="road":
            ax.text(x,y,name,ha="center",va="center",fontsize=7.2,weight="bold",color="#283b41",
                    bbox=dict(boxstyle="round,pad=.20",fc="#fffefa",ec="#47575a",lw=.65),zorder=5)
        else:
            ax.text(x,y,name,ha="center",va="center",fontsize=8.2,style="italic",color="#283b37",
                    path_effects=[pe.withStroke(linewidth=3,foreground="#fffefa")],zorder=5)
        occupied.append((u,v,rw,.032))
        shown.add(name)

def radio_line(ax,x,y):
    ax.plot(x,y,color=path_color,lw=2.8,solid_capstyle="round",zorder=7,
            path_effects=[pe.withStroke(linewidth=5.5,foreground="white")])

def roadstatus(ax,layout):
    reach=network(set(layout))
    mask=masks[[ix[k] for k in reach]].any(axis=0)
    h=groups=="Highway"
    for val,col in [(True,both),(False,"#bd483e")]:
        v=h & (mask==val)
        ax.scatter(*targets[v].T,s=6,c=col,zorder=4,linewidths=0)
def pin(ax,k,txt=None,delta=(5,4)):
    x,y=xy[k]
    ax.scatter(x,y,s=42,c="#182a35",ec="white",lw=.8,zorder=6)
    if txt:
        ax.annotate(txt,(x,y),xytext=delta,textcoords="offset points",fontsize=8,weight="bold",zorder=7,
                    path_effects=[pe.withStroke(linewidth=3,foreground="white")])
def notes(x,y,sections,spacing=.11):
    for title,body in sections:
        fig.text(x,y,title,weight="bold",fontsize=11,color="#154d49")
        fig.text(x,y-.022,body,va="top",fontsize=9.5,linespacing=1.4)
        y-=spacing
def lineplot(ax,a,b):
    d,z,l,f=profile.trace(coords(a),coords(b))
    ax.fill_between(d/1000,z,z.min()-20,color="#a4b0a9")
    ax.fill_between(d/1000,l-.6*f,l+.6*f,color="#76b6d4",alpha=.65)
    radio_line(ax,d/1000,l)
    endpoint(ax,0,l[0],"A")
    endpoint(ax,d[-1]/1000,l[-1],"B")
    ax.grid(axis="y",alpha=.23)
    ax.set(xlabel="Distance from A (km)",ylabel="Elevation (m)",xlim=(-d[-1]*.00006,d[-1]*.00106))
    return (l-z)[1:-1].min(),((l-z)[1:-1]/f[1:-1]).min()
def overlay(ax,arr,colors):
    ax.imshow(np.ma.masked_equal(arr,0),extent=extent,cmap=ListedColormap(colors),interpolation="nearest",vmin=.5,vmax=len(colors)+.5,alpha=.52,zorder=2)


def direct_page(a,b):
    bothv=views[a] & views[b]
    arr=views[a].astype(int)+2*views[b].astype(int)
    page("Viewshed and direct path",label(a)+"  /  "+label(b),"Member antenna 1.2 m above ground. The map frames this link; overlap totals use the full study area.")
    ax=axis([.042,.21,.525,.59])
    mapbase(ax,link_bounds(a,b),"detail")
    overlay(ax,arr,[c1,c2,both])
    map_labels(ax,a,b)
    radio_line(ax,*np.array([xy[a],xy[b]]).T)
    endpoint(ax,*xy[a],"A")
    endpoint(ax,*xy[b],"B")
    for site,other in ((a,b),(b,a)):
        above=xy[site][1]>=xy[other][1]
        ax.annotate(fill(label(site),width=21),xy[site],xytext=(0,11 if above else -12),
                    textcoords="offset points",ha="center",va="bottom" if above else "top",
                    fontsize=8.6,color="#5b1238",weight="bold",zorder=9,
                    bbox=dict(boxstyle="round,pad=.18",facecolor="white",edgecolor="none",alpha=.92))
    ax.legend(handles=[Patch(color=c1,label="A only"),Patch(color=c2,label="B only"),Patch(color=both,label="Both")],
              loc="upper center",bbox_to_anchor=(.56,1.015),ncol=3,framealpha=.96,fontsize=8,handlelength=1,columnspacing=1)
    ax2=axis([.60,.48,.345,.26]);clear,f1=lineplot(ax2,a,b)
    shared=(groups=="Highway") & masks[ix[a]] & masks[ix[b]]
    km=weights[shared].sum()/1000
    notes(.57,.36,[("Direct antenna path",f"{math.dist(xy[a],xy[b])/1000:.2f} km   •   {clear:+.1f} m minimum clearance\nMinimum first Fresnel clearance {100*f1:.0f}%   •   A {wh(a)} m / B {wh(b)} m"),
                    ("Member overlap",f"{km:.2f} km of shared highway and {bothv.sum()*step**2/1e6:.1f} km² of shared\nterrain on the 35 m plotting grid. Shared tracker visibility\nand an antenna-to-antenna link are separate tests.")],.11)
    fig.text(.057,.14,f"A   {label(a)}    {lonlat(a)[0]:.5f}, {lonlat(a)[1]:.5f}\nB   {label(b)}    {lonlat(b)[0]:.5f}, {lonlat(b)[1]:.5f}",fontsize=9,linespacing=1.6)
    fig.text(.57,.108,"Magenta   direct ray       Blue band   inner 60% Fresnel zone\nGray   curvature-adjusted bare earth",fontsize=9,linespacing=1.5)
    save()

def resort_page():
    fig=page("Resort and access","Ski base, parking and approach","Outdoor probes only. The upper 1.72 km of SR 156 approaching the resort is scored separately from the rest of the highway.")
    # Field map of the complete approach and a separate, larger-scale view of the base.
    ax=axis([.042,.22,.385,.565])
    mapbase(ax,(618105,4018195,619465,4020305),"resort")
    ax.annotate("SR 156  •  Lee Canyon Road",xy=(618920,4019750),xytext=(618760,4020180),ha="center",
                fontsize=8.3,weight="bold",bbox=dict(fc="#fffefa",ec="#566669",boxstyle="round,pad=.25"),zorder=8)
    take=groups=="Resort approach"
    ax.scatter(*targets[take].T,s=10,c="#045e62",edgecolors="white",linewidths=.35,zorder=4)
    close=(618260,4018260,619155,4018980)
    ax.add_patch(Rectangle(close[:2],close[2]-close[0],close[3]-close[1],fill=False,edgecolor=path_color,
                           linewidth=1.6,zorder=6,path_effects=[pe.withStroke(linewidth=3.5,foreground="white")]))
    ax.text(.03,.13,"Base detail →",transform=ax.transAxes,fontsize=8,weight="bold",
            color=path_color,bbox=dict(facecolor="white",edgecolor="none",pad=2),zorder=8)
    fig.text(.055,.80,"SR 156   /   Resort approach",weight="bold",fontsize=12)
    detail=axis([.445,.22,.51,.565])
    mapbase(detail,close,"aerial")
    lot=next(g for g,p in features if p.get("osm_id")=="w1154358378")
    detail.fill(*lot.exterior.xy,color="#ffbe3d",alpha=.3,zorder=2)
    detail.plot(*lot.exterior.xy,color="#ffca4e",lw=1.7,zorder=3)
    take=groups=="Resort parking"
    detail.scatter(*targets[take].T,s=7,color="#ffcb39",edgecolors="#44311c",linewidths=.3,zorder=5)
    take=groups=="Lodge / base"
    detail.scatter(*targets[take].T,marker="^",s=32,c="#0c4477",edgecolors="white",linewidths=1,zorder=6)
    def callout(text,anchor,at):
        detail.annotate(text,xy=anchor,xytext=at,fontsize=8.2,color="#102d35",weight="bold",va="center",ha="center",
                        bbox=dict(boxstyle="round,pad=.34",fc="#fffefa",ec="#34464b",lw=.55),
                        arrowprops=dict(arrowstyle="-",color="white",lw=1.6,path_effects=[pe.withStroke(linewidth=2.8,foreground="#23343a")]),
                        zorder=7)
    callout("Mapped parking lot",lot.representative_point().coords[0],(618480,4018855))
    callout("Bristlecone lodge",targets[names=="Bristlecone lodge exterior"][0],(618450,4018360))
    callout("Ponderosa west",targets[names=="Ponderosa base west"][0],(618780,4018420))
    callout("Ponderosa east",targets[names=="Ponderosa base east"][0],(619005,4018730))
    fig.text(.445,.80,"Parking and base   /   Outdoor tracker probes",weight="bold",fontsize=12)
    fig.text(.055,.167,"Approach   46 probes",weight="bold",color="#045e62")
    fig.text(.055,.136,f"{D['Deployed']['scores']['Resort approach']:g}% deployed  /  {D[key]['scores']['Resort approach']:g}% proposed",fontsize=9)
    fig.text(.385,.167,"Mapped lot   22 probes",weight="bold",color="#804c05")
    fig.text(.385,.136,f"{D['Deployed']['scores']['Resort parking']:g}% deployed  /  {D[key]['scores']['Resort parking']:g}% proposed",fontsize=9)
    fig.text(.705,.167,"Lodge and base   7 probes",weight="bold",color="#124578")
    fig.text(.705,.136,f"{D['Deployed']['scores']['Lodge / base']:g}% deployed  /  {D[key]['scores']['Lodge / base']:g}% proposed",fontsize=9)
    fig.text(.055,.085,"USGS The National Map • USDA NAIP photograph, June 2022. Ponderosa markers locate outdoor probes; walk both lots to verify coverage.",fontsize=8)
    save()
