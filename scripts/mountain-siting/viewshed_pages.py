"""Full-extent, site-by-site and gateway-connected viewsheds for the printable study."""
from functools import lru_cache

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
from shapely import contains_xy

from atlas_maps import (D, DATA, XX, YY, axis, boundary, display, extent,
                        forward, grid, groups, ix, key, lonlat, masks,
                        meta, network, page, pdf, pe, plan, points, radius, read,
                        reference_labels, road_inventory, save, search, sight, step, strong,
                        views, wave, weights, wh, xy)
from reachable_search import MACK, VEGAS
from terrain_maps import landscape, relief

VISIBLE="#00786f"
STRICT="#006d67"
MARGINAL="#e0a124"
ISOLATED="#9a6da8"
SHADOW="#eeede8"
OUTSIDE="#fbfaf6"
DEPLOYED="Deployed"
FULL=tuple(extent)
INSIDE=contains_xy(boundary,XX,YY)
CELL_KM2=step**2/1e6


@lru_cache(maxsize=1)
def background():
    l,r,b,t=FULL
    resolution=max(r-l,t-b)/1850
    _,_,ground=landscape((l,b,r,t),resolution)
    # Subdue relief so a small patch of direct visibility is still conspicuous.
    return (relief(ground,resolution)*.43+np.array([248,248,245])*.57).astype("uint8")


def count_area(mask):
    return np.count_nonzero(mask & INSIDE)*CELL_KM2


def raster_layer(ax,classes,colors,bounds,inside=None):
    palette=np.asarray([to_rgba(color,alpha) for color,alpha in colors])
    rgba=np.rint(palette[classes]*255).astype("uint8")
    if inside is not None:
        rgba[~inside]=np.array(to_rgba(OUTSIDE))*255
    ax.imshow(rgba,extent=bounds,interpolation="none",zorder=1,origin="upper")


def map_frame(ax,bounds,bar):
    l,r,b,t=bounds
    ax.set(xlim=(l,r),ylim=(b,t),aspect="equal",xticks=[],yticks=[])
    for edge in ax.spines.values():
        edge.set_color("#969e99")
    ax.text(.02,.975,"N ↑",transform=ax.transAxes,ha="left",va="top",size=7.6,
            weight="bold",bbox=dict(fc="white",ec="none",pad=2),zorder=8)
    x=l+.035*(r-l)
    y=b+.05*(t-b)
    ax.plot([x,x+bar],[y,y],lw=2,color="#283737",zorder=8,
            path_effects=[pe.withStroke(linewidth=4,foreground="white")])
    ax.text(x,y+.014*(t-b),f"{bar/1000:g} km",size=7.6,color="#253838",
            bbox=dict(fc="white",ec="none",pad=1.4),zorder=8)


def mountain_panel(rect,classes,colors,sites=()):
    ax=axis(rect)
    ax.imshow(background(),extent=FULL,interpolation="none",zorder=0)
    raster_layer(ax,classes,colors,FULL,INSIDE)
    roads=[np.asarray(line.coords) for line,_ in road_inventory]
    for width,color in [(1.9,"#fffdf5"),(.75,"#665d51")]:
        ax.add_collection(LineCollection(roads,linewidths=width,colors=color,zorder=3))
    ax.plot(*boundary.exterior.xy,color="#9caaa5",lw=.55,zorder=2)
    # One shield per road; keep these out of the site markers.
    used=set()
    for name,x,y,kind in reference_labels():
        if kind!="road" or name in used or any(np.hypot(x-xy[k][0],y-xy[k][1])<950 for k in sites):
            continue
        ax.text(x,y,name,size=6.1,color="#413e38",ha="center",va="center",
                bbox=dict(boxstyle="round,pad=.15",fc="#fffef9",ec="#a49d90",lw=.45),zorder=4)
        used.add(name)
    for k in sites:
        ax.scatter(*xy[k],marker="D" if k=="Lee Fire" else "o",s=44,
                   color="#211f36",edgecolor="white",linewidth=1.1,zorder=6)
    map_frame(ax,FULL,2000)
    return ax


def legend(fig,y,items):
    x=.048
    for text,color,space in items:
        fig.text(x,y,"■",color=color,size=13,va="center")
        fig.text(x+.02,y,text,size=9,va="center",color="#263f40")
        x+=space


def union(sites):
    return np.logical_or.reduce([views[k] for k in sites])


def network_spreads():
    fig=page("Network viewsheds","Where member GPS can reach Lee Fire",
             "Each colored cell can see Lee Fire directly or a relay with a terrain-clear route to it within three forwarders.")
    maps=[(DEPLOYED,"Deployed network"),(key,"Reachable plan")]
    for i,(scenario,title) in enumerate(maps):
        x=.045+i*.485
        record=D[scenario]
        footprint=union(record["reach"])
        mountain_panel([x,.255,.435,.49],footprint.astype("uint8"),
                       [(SHADOW,0),(VISIBLE,.85)],record["reach"])
        fig.text(x,.770,title,size=13,weight="bold",color="#174b49")
        fig.text(x,.210,f"{count_area(footprint):.2f} km² connected  •  {record['scores']['Highway']:.1f}% of highway",size=10,weight="bold")
    legend(fig,.143,[("Reachable terrain",VISIBLE,.205),("Terrain without a modeled route","#c2c6bf",.35)])
    fig.text(.047,.082,"Same bounds, 35 m grid and 1.2 m member antenna on both maps. Dots mark eligible relays. The diamond marks the gateway.",size=9)
    save()

    fig=page("Network viewsheds","Which parts of the plan have a route?",
             "All seven proposed relay positions and the Lee Fire receiver contribute to the direct-visibility comparison.")
    connected=union(D[key]["reach"])
    strict=union(network(set(plan),strong))
    physical=union(["Lee Fire",*plan])
    classes=np.select([strict,connected,physical],[3,2,1],default=0).astype("uint8")
    mountain_panel([.045,.14,.53,.65],classes,
                   [(SHADOW,0),(ISOLATED,.82),(MARGINAL,.88),(STRICT,.85)],["Lee Fire",*plan])
    fig.text(.61,.755,"Area inside the study boundary",size=12,weight="bold",color="#174b49")
    categories=[(3,STRICT,"Strict route to Lee","Every backbone leg clears 60% of the first Fresnel zone."),
                (2,MARGINAL,"Terrain-clear route only","At least one required backbone leg falls below 60%."),
                (1,ISOLATED,"Visible to an isolated relay","A first hop is possible. The Lee route exceeds the budget or is blocked."),
                (0,"#9b9f97","Terrain shadow","No direct terrain ray to any selected radio or Lee Fire.")]
    from textwrap import fill
    for i,(code,color,title,body) in enumerate(categories):
        y=.674-i*.123
        fig.text(.61,y,"■",color=color,size=13)
        fig.text(.632,y,title,size=10.2,weight="bold")
        fig.text(.95,y,f"{count_area(classes==code):.2f} km²",ha="right",size=9.4)
        fig.text(.632,y-.023,fill(body,49),size=8.6,va="top",linespacing=1.3)
    fig.text(.61,.147,f"Total mapped area   {count_area(INSIDE):.2f} km²",size=10,weight="bold")
    fig.text(.047,.075,"The member hop uses bare-earth visibility in both route classes. Trees, buildings, radio noise and packet delivery require field checks.",size=9)
    save()


def site_order():
    # Start with the return-visit decisions. Follow with every remaining site in source order.
    first=[MACK,"Upper Bristlecone","Angel Vegas",VEGAS,"Angel Mountain","Angel road survey 5",
           "Lee Alternative","Lee Alternative survey 2","Lee Junction","Lee Fire",
           "Escarpment trail","Escarpment trail survey 3","Shady Hollow","Kyle Junction",
           "Showgirl","Cathedral Rock","Legacy Fletcher","Fletcher intermediate","Fletcher Peak","Kyle Fire"]
    return list(dict.fromkeys([k for k in first if k in display]+list(display)))


def individual_viewsheds():
    ordered=site_order()
    pairs=[ordered[i:i+2] for i in range(0,len(ordered),2)]
    index=page("Individual site viewsheds","Find a site viewshed",
               "Every owner waypoint and model-generated survey point has its own direct-visibility map, shown at the same scale.")
    first_page=pdf.get_pagecount()+2
    for i,pair in enumerate(pairs):
        col,row=divmod(i,(len(pairs)+1)//2)
        x=.05+.48*col
        y=.735-.066*row
        index.text(x,y,str(first_page+i),size=11,weight="bold",color="#08786f")
        index.text(x+.043,y,"  /  ".join(pair),size=9.0)
    index.text(.05,.138,"Each site map gives direct terrain area, sampled highway length and its role in the proposed network.",size=10)
    index.text(.05,.095,"A large direct viewshed can still be isolated from Lee. The network maps at the front apply the forwarding limit.",size=9.5)
    save()
    for pair in pairs:
        fig=page("Individual site viewsheds","  /  ".join(pair),
                 "Direct bare-earth line of sight between each named radio and a member antenna 1.2 m above ground.")
        for i,k in enumerate(pair):
            x=.045+.485*i
            area=count_area(views[k])
            direct_km=weights[(groups=="Highway") & masks[ix[k]]].sum()/1000
            mountain_panel([x,.285,.435,.46],views[k].astype("uint8"),[(SHADOW,0),(VISIBLE,.85)],[k])
            fig.text(x,.767,k,size=12.5,weight="bold",color="#164e4d")
            fig.text(x,.246,f"{area:.2f} km² visible    •    {direct_km:.2f} km of highway visible",size=9.8,weight="bold")
            lat,lon=lonlat(k)
            fig.text(x,.206,f"{lat:.5f}, {lon:.5f}   •   {wh(k)} m antenna above ground",size=9)
            status=("Lee Fire uplink" if k=="Lee Fire" else "Eligible member first hop to Lee" if k in D[key]["reach"]
                    else "Selected relay with no route within three forwarders" if k in plan else "Comparison site outside the selected layout")
            fig.text(x,.171,status,size=8.8)
        legend(fig,.104,[("Visible to the marked radio",VISIBLE,.33),("Terrain shadow","#c2c6bf",.2)])
        save()


def angel_valley_viewshed():
    from city_streets import streets
    from reachable_search import valley_probes
    regional,trans,sectors,receivers=valley_probes()
    cfg=read(DATA/"inputs/study.json")
    x,y=receivers[:,:2].T
    spacing=60
    left,bottom=np.floor([(x.min()-1800)/spacing,(y.min()-2300)/spacing])*spacing
    right,top=np.ceil([(x.max()+1800)/spacing,(y.max()+2300)/spacing])*spacing
    gx,gy=np.meshgrid(np.arange(left+spacing/2,right,spacing),np.arange(top-spacing/2,bottom,-spacing))
    ends=points(regional,trans,np.c_[gx.ravel(),gy.ravel()],4)
    footprints=[]
    for k in ("Angel Vegas",VEGAS):
        start=points(grid,meta,[xy[k]],4)[0]
        sampled=sight(regional,trans,start,receivers,20,wave,radius).reshape(-1,9)
        if sampled.sum(axis=1).tolist()!=search["valley"][k]:
            raise ValueError(f"Valley probes disagree with the study at {k}")
        footprints.append(sight(regional,trans,start,ends,20,wave,radius).reshape(gx.shape))
    classes=footprints[0].astype("uint8")+2*footprints[1].astype("uint8")
    fig=page("Regional viewsheds","Angel Peak to northwest Las Vegas",
             "Direct visibility to outdoor 4 m receivers around the four comparison sectors. All rays use the regional 20 m elevation model.")
    ax=axis([.045,.21,.67,.57])
    bounds=(left,right,bottom,top)
    _,_,z=landscape((left,bottom,right,top),20)
    ax.imshow(relief(z,20),extent=bounds,interpolation="none",zorder=0)
    colors=[(SHADOW,.22),("#bb672e",.92),("#5a60ac",.9),(VISIBLE,.82)]
    raster_layer(ax,classes,colors,bounds)
    roads=[]
    for kind,ref,name,pts in streets(DATA,cfg["valley_map_wsen"]):
        if kind in ("motorway","trunk","primary","secondary"):
            coords=np.column_stack(forward.transform(*np.asarray(pts).T))
            if (coords[:,0].max()>=left and coords[:,0].min()<=right and
                    coords[:,1].max()>=bottom and coords[:,1].min()<=top):
                roads.append(coords)
    ax.add_collection(LineCollection(roads,linewidths=.45,colors="#566169",alpha=.65,zorder=3))
    for i,sector in enumerate(sectors):
        xx,yy=receivers[i*9:(i+1)*9,:2].T
        ax.scatter(xx,yy,s=12,fc="white",ec="#303c41",lw=.6,zorder=4)
        ax.annotate(str(i+1),(xx.mean(),yy.max()),xytext=(0,5),textcoords="offset points",ha="center",
                    weight="bold",size=9,bbox=dict(fc="white",ec="#435653",pad=1.4),zorder=6)
    map_frame(ax,bounds,2000)
    fig.text(.738,.74,"Clear sector probes",weight="bold",size=12,color="#174b49")
    fig.text(.738,.693,"Deployed  /  proposed",size=9.5)
    for i,sector in enumerate(sectors):
        py=.627-i*.092
        fig.text(.738,py,f"{i+1}   {sector}",size=9.1,weight="bold")
        fig.text(.759,py-.033,f"{search['valley']['Angel Vegas'][i]}/9   /   {search['valley'][VEGAS][i]}/9",size=10)
    legend(fig,.151,[("Deployed only","#bb672e",.18),("Alternative only","#5a60ac",.19),
                     ("Both",VISIBLE,.12),("Neither","#afafa6",.15)])
    fig.text(.047,.082,"Color samples the terrain on a 60 m grid. Circles locate the 36 independently tested probe positions. Buildings and indoor reception are unmodeled.",size=8.9)
    save()
