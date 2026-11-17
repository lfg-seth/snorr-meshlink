"""Produce the offline field atlas, geographic view rasters and micro-site checks."""
from survey import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import ListedColormap, LightSource
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from rasterio.transform import from_origin
from terrain import write_raster

plt.rcParams.update({"font.size":10,"font.family":"DejaVu Sans","axes.titleweight":"bold","pdf.fonttype":42})
L,B,R,T=boundary.bounds
step=90
xs=np.arange(L+step/2,R,step)
ys=np.arange(T-step/2,B,-step)
XX,YY=np.meshgrid(xs,ys)
ground=points(grid,meta,np.c_[XX.ravel(),YY.ravel()],1.2)
shade=LightSource(azdeg=315,altdeg=40).hillshade(ground[:,2].reshape(XX.shape),dx=step,dy=step)
extent=[L,L+len(xs)*step,T-len(ys)*step,T]
display=export()
displaysites=set(display)
views={}
for k in display:
    origin=points(grid,meta,[xy[k]],wh(k))[0]
    view=sight(grid,meta,origin,ground,5.,wave,radius).reshape(XX.shape)
    views[k]=view.astype(bool)
    folder=OUT/"viewsheds"
    folder.mkdir(exist_ok=True)
    write_raster(folder/(label(k)+".tif"),view,from_origin(L,T,step,step))
c1,c2,both="#e4a444","#5794be","#027967"
fig=None
pdf=PdfPages(OUT/"mountain-field-atlas.pdf")
def page(section,title,sub):
    global fig
    fig=plt.figure(figsize=(11.7,8.3),facecolor="#faf9f4")
    fig.text(.045,.952,section.upper(),fontsize=10,color="#19736b",weight="bold")
    fig.text(.045,.897,title,fontsize=23,fontfamily="DejaVu Serif")
    fig.text(.045,.855,sub,fontsize=10,color="#42535a")
def save():
    fig.text(.045,.035,"SNORR MeshLink   /   Mount Charleston     •     17 November 2026",fontsize=8,color="#465254")
    fig.text(.955,.035,str(pdf.get_pagecount()+1),ha="right",fontsize=8)
    pdf.savefig(fig)
    plt.close(fig)
def axis(rect):
    return fig.add_axes(rect)
def mapbase(ax,bounds=None):
    ax.imshow(shade,extent=extent,cmap="Greys",alpha=.32,interpolation="nearest",vmin=0,vmax=1)
    for line,ref in road_inventory:
        x,y=line.xy
        ax.plot(x,y,c="#464d50",lw=1,zorder=3)
    l,b,r,t=bounds or (L,B,R,T)
    ax.set(xlim=(l,r),ylim=(b,t),aspect="equal",xticks=[],yticks=[])
    ax.text(.02,.97,"N ↑",transform=ax.transAxes,va="top",fontsize=9,weight="bold",bbox=dict(fc="white",ec="none",alpha=.85))
    km=200 if r-l<3500 else 2000
    x=l+.05*(r-l);y=b+.05*(t-b)
    ax.plot([x,x+km],[y,y],c="black",lw=2,zorder=5)
    ax.text(x,y+.015*(t-b),f"{km/1000:g} km",fontsize=7,backgroundcolor="white",zorder=7)
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
    ax.plot(d/1000,l,c="#bc4834",lw=1.7)
    ax.scatter([0,d[-1]/1000],[l[0],l[-1]],c=["#174f82","#246e4e"],zorder=4,s=30)
    ax.grid(axis="y",alpha=.23)
    ax.set(xlabel="Distance from A (km)",ylabel="Elevation (m)",xlim=(0,d[-1]/1000))
    return (l-z)[1:-1].min(),((l-z)[1:-1]/f[1:-1]).min()
def overlay(ax,arr,colors):
    ax.imshow(np.ma.masked_equal(arr,0),extent=extent,cmap=ListedColormap(colors),interpolation="nearest",vmin=.5,vmax=len(colors)+.5,alpha=.77,zorder=2)

page("Field atlas   /   Lee Fire backhaul","Mount Charleston repeater study","Terrain-screened survey plan for SR 156, SR 157, SR 158 and their member GPS targets.")
ax=axis([.035,.12,.56,.69]);mapbase(ax);roadstatus(ax,plan)
for j,k in enumerate(["Lee Fire",*plan]):
    pin(ax,k,str(j+1))
notes(.61,.785,[("First field test","Test the nearest passing shoulder on foot with Angel\nMountain and its Lee-side neighbor. Check a fresh\nGPS packet at Lee Fire before relocating R006."),
                 ("Four estimated assemblies","One for legacy Fletcher and one to replace Shady.\nApply the other two to the additional relay sites.\nWaypoint assignments are in the study brief."),
                 ("Gateway","Lee Fire is the sole uplink. Kyle Fire appears only\nin the optional dual-station comparison.")],.11)
for j,k in enumerate(["Lee Fire",*plan]):
    fig.text(.614,.445-j*.027,f"{j+1:>2}    {label(k)}",fontsize=9.1)
fig.text(.06,.082,"Green  modeled path to Lee Fire      Red  highway gap      Dark points  proposed layout",fontsize=9)
save()
page("Layout comparison","What each placement buys","Percent of sampled highway length or facility probes with a path to Lee Fire through at most three forwarding radios.")
ax=axis([.045,.38,.91,.42]);ax.axis("off")
rows=[]
for sc,short in [("Deployed","Deployed"),("First Lee bridge trial","Move Lee Junction only"),("Keep Kyle, Angel and Shady","Keep Kyle, Angel and Shady pins"),("Closer to highways","New search points within 1.2 km of road"),("No Fletcher","Full search without Fletcher"),("Legacy Fletcher","Full search with legacy swap"),("Fletcher intermediate","Full search with intermediate Fletcher"),("Fletcher Peak","Full search with summit")]:
    v=D[sc];s=v["scores"];rows.append([short,f"{len(set(v['layout']) & set(v['reach']))}/{len(v['layout'])}"]+
                    [f"{s[k]:.1f}" for k in ("SR 156","SR 157","SR 158","Trailheads","Other parking","Resort parking","Lodge / base")])
table=ax.table(cellText=rows,colLabels=["Layout","RF to Lee*","156","157","158","Heads","Lots","Ski lot","Base"],cellLoc="center",colWidths=[.34,.09,.07,.07,.07,.08,.07,.09,.09],bbox=[0,0,1,1]);table.auto_set_font_size(False);table.set_fontsize(9)
for (r,c),cell in table.get_celld().items():
    cell.set_edgecolor("#d1d8d3")
    if not r:cell.set_facecolor("#d5e9e2")
    if c==0:cell.set_text_props(ha="left")
notes(.05,.32,[("Reading the scores","*Count of selected relay first hops usable by a member under the three-forwarder limit. Highways span 39.61 km within the study bounds.\nFacility percentages average sampled fractions per mapped feature. Some trailheads have both a point and a lot."),
                ("Fletcher on an unchanged backbone","The preferred backbone reaches 93.1% without Fletcher, 94.6% with legacy, 93.1% partway up and 94.2% at the summit.\nThe full-search rows also allow companion sites to move. The individual viewsheds show direct member visibility.\nThe highway and facility scores require an eligible route to Lee Fire.")],.11)
save()
page("Hardware and routes","Where each radio goes","Four new assemblies support the complete option. G001 stays at Lee Fire. Arrows follow modeled RF legs at 1 m / 4 m nominal heights.")
roles=["Keep R010","Keep R001","Keep R005","Keep R011","Move R008","Move R006","Shady replacement","Fletcher swap","Additional relay","Additional relay"]
rows=[]
for role,k in zip(roles,plan):
    p=route(k,plan,.6)
    rows.append([role,label(k),f"{lonlat(k)[0]:.5f}, {lonlat(k)[1]:.5f}"," → ".join(label(j) for j in p[1:])])
ax=axis([.045,.32,.91,.49]);ax.axis("off")
tab=ax.table(cellText=rows,colLabels=["Hardware","Waypoint","Latitude, longitude","One path from waypoint to station"],cellLoc="left",colWidths=[.14,.26,.22,.38],bbox=[0,0,1,1]);tab.auto_set_font_size(False);tab.set_fontsize(8)
for (r,c),cell in tab.get_celld().items():
    cell.set_edgecolor("#d1d8d3")
    if not r:cell.set_facecolor("#d5e9e2")
notes(.05,.25,[("Where a few metres matter","Upper Lee south ridge is about 706 m above the nearest mapped parking center. At the proposed pin the path to Lee Fire clears bare earth\nby 1.47 m. A 20 m move south blocks it by 16.04 m. Use a portable radio before carrying the full assembly."),
               ("If the climb or Fletcher trip falls through","Test the northwest shoulder via Upper Bristlecone first. On the full backbone all nine other relays keep a route to Lee without Fletcher.\nIf moving Shady or Kyle is impractical, the layout that retains both pins still reaches 83.1% of sampled highway.")],.10)
save()
page("Resort and access","Ski base, parking and approach","Outdoor probes only. The upper 1.72 km of SR 156 approaching the resort is scored separately from the rest of the highway.")
ax=axis([.04,.15,.58,.65]);x,y=resort.coords[0];mapbase(ax,(x-950,y-650,x+950,y+1250))
for g,p in features:
    if g.geom_type=="Polygon" and g.distance(resort)<1000 and (p.get("building") or p.get("amenity")=="parking"):
        ax.fill(*g.exterior.xy,color="#b3c4cc",zorder=3,alpha=.7)
for cat,color,marker in [("Resort parking","#a04d15","s"),("Lodge / base","#213d83","^"),("Resort approach",both,".")]:
    take=groups==cat;ax.scatter(*targets[take].T,c=color,s=26,marker=marker,zorder=5,label=cat)
ax.legend(loc="upper right",fontsize=8)
notes(.65,.76,[("Resort parking","22 probes in the mapped surface lot.\nDeployed model 22.7% • legacy plan 100%."),
               ("Lodge and base","7 probes including the lodge-area building\nand two Ponderosa base proxies.\nDeployed model 0% • legacy plan 100%."),
               ("Approach road","46 centerline probes within 1.9 km of the\nresort marker. Deployed 88.7% • plan 100%."),
               ("Coverage limits","The map extract delineates one resort lot.\nWalk both Bristlecone and Ponderosa lots,\nthe lodge entrance and base plazas.\nBuilding penetration remains unmeasured.")],.145)
save()
page("Changes from deployment","What the moves gain and lose","Direct highway visibility before and after each move, using the same 1.2 m member tracker.")
ax=axis([.045,.22,.48,.58]);mapbase(ax);roadstatus(ax,plan)
with (OUT/"highway-gaps.csv").open(encoding="utf-8-sig") as source:
    gaps=list(csv.DictReader(source))
for j,gap in enumerate(gaps[:3]):
    pt=forward.transform(float(gap["start longitude"]),float(gap["start latitude"]))
    ax.scatter(*pt,c="#b7332d",s=85,edgecolor="white",zorder=8)
    ax.annotate(str(j+1),pt,xytext=(6,4),textcoords="offset points",weight="bold",zorder=9)
changes=[]
highway=groups=="Highway"
for old,new in zip(["Lee Junction","Kyle Junction","Angel Mountain","Shady Hollow"],[plan[5],plan[4],plan[3],plan[6]]):
    ma,mb=masks[ix[old]],masks[ix[new]]
    lost=weights[highway & ma & ~mb].sum()/1000
    gained=weights[highway & mb & ~ma].sum()/1000
    changes.append(f"{old}    {lost:.2f} km lost / {gained:.2f} km gained")
live=lambda sc:masks[[ix[k] for k in D[sc]["reach"]]].any(axis=0)
loss=weights[highway & live("Deployed") & ~live(key)].sum()
gaptext="\n".join(f"{i+1}   {g['road']}   {g['length m']} m   •   {float(g['start latitude']):.5f}, {float(g['start longitude']):.5f}" for i,g in enumerate(gaps[:3]))
notes(.56,.75,[("Individual highway footprints","\n".join(changes)),
               ("End-to-end impact",f"The full layout loses {loss:.0f} m of previously Lee-reachable highway.\nTest the changed segments in member-probes.csv before\nmoving the deployed radios."),
               ("Longest gaps on mapped centerlines",gaptext)],.19)
fig.text(.055,.13,"Green  Lee-reachable      Red  blind      Numbers  gap starts",fontsize=9)
save()
# Neighbor viewsheds and individual field profiles.
southeast=next(v["layout"][-1] for n,v in D.items() if n.startswith("Lee trial J"))
first="J1"
nextleg=next(k for k in ("Lee Fire","Upper Bristlecone") if k in strong[first])
presentations=[("C16","Upper Bristlecone"),("C16","Angel Mountain"),("Lee Junction","Upper Bristlecone"),("Across SR 156","Angel Mountain"),("Across SR 158","Lee Fire"),
               (first,"Angel Mountain"),(first,nextleg),(southeast,"Angel Mountain"),(southeast,"Lee Fire"),
               ("Upper Bristlecone","Lee Fire"),("Shady Hollow","Kyle Junction")]
for scenario in ("Legacy Fletcher","No Fletcher","Fletcher intermediate","Fletcher Peak"):
    for k in D[scenario]["layout"]:
        path=route(k,D[scenario]["layout"],.6) or route(k,D[scenario]["layout"])
        if len(path)>1 and not any({k,path[1]}==set(pair) for pair in presentations):
            presentations.append((k,path[1]))
for a,b in presentations:
    bothv=views[a] & views[b]
    arr=views[a].astype(int)+2*views[b].astype(int)
    page("Viewshed and direct path",label(a)+"  /  "+label(b),"Member antenna 1.2 m above ground. North-up viewsheds cover the same extent throughout the atlas.")
    ax=axis([.035,.20,.50,.58]);mapbase(ax);overlay(ax,arr,[c1,c2,both]);pin(ax,a,"A");pin(ax,b,"B")
    ax.plot(*np.array([xy[a],xy[b]]).T,c="#1d3041",ls="--",lw=1,zorder=4)
    ax.legend(handles=[Patch(color=c1,label="A only"),Patch(color=c2,label="B only"),Patch(color=both,label="Shared")],loc="lower right",fontsize=8)
    ax2=axis([.60,.48,.345,.26]);clear,f1=lineplot(ax2,a,b)
    shared=(groups=="Highway") & masks[ix[a]] & masks[ix[b]]
    km=weights[shared].sum()/1000
    notes(.57,.36,[("Direct antenna path",f"{math.dist(xy[a],xy[b])/1000:.2f} km   •   {clear:+.1f} m minimum clearance\nMinimum first Fresnel clearance {100*f1:.0f}%   •   A {wh(a)} m / B {wh(b)} m"),
                    ("Member overlap",f"{km:.2f} km of shared highway and {bothv.sum()*step**2/1e6:.1f} km² of shared\nterrain on the 90 m plotting grid. Shared tracker visibility\nand an antenna-to-antenna link are separate tests.")],.11)
    fig.text(.057,.14,f"A   {label(a)}    {lonlat(a)[0]:.5f}, {lonlat(a)[1]:.5f}\nB   {label(b)}    {lonlat(b)[0]:.5f}, {lonlat(b)[1]:.5f}",fontsize=9,linespacing=1.6)
    fig.text(.57,.108,"Red line   direct ray       Blue band   inner 60% Fresnel zone\nGray   curvature-adjusted bare earth",fontsize=9,linespacing=1.5)
    save()
page("Field verification","Where to take the radios","Use the GPX waypoint names in this atlas. A survey point and a road offset do not establish a usable winter approach.")
notes(.055,.77,[("1   Establish the control before moving R006","Verify Lee Fire power and Wi-Fi, then send unique GPS packets by Upper Bristlecone and confirm their IDs at dispatch. Record actual\nantenna heights and direct-neighbor telemetry. At the current Lee Junction mount repeat on foot and from the parked vehicle."),
("2   Test the shortest Lee-to-Angel bridge","Use a portable at the current pin, the closest passing shoulder and then the south-side alternative. Test Angel Mountain and the Lee-side\nneighbor in both directions. Match a normal GPS packet at Lee Fire. The owner confirms the wildlife fence can be crossed."),
("3   Test both ends before relocating the Kyle sites","At Upper Lee south ridge test Lee Fire and Cathedral Rock. Verify the legacy Fletcher first hop in station-routes.csv and trace a GPS\npacket to the station. Compare the proposed Shady and Kyle moves while their deployed radios are available."),
("4   Drive and walk the target gaps","Carry the tracker at body height, then repeat in the vehicle. Drive SR 158 through the gaps in highway-gaps.csv. Walk both ski lots and\nlodge approaches. Log sent/received IDs, GPS-fix age and route evidence at Lee Fire; repeat the existing route to catch lost coverage."),
("5   Decide on hardware after the trial","A relay hearing another relay proves only that leg. Require repeatable end-to-end receipts and check the 15-minute freshness boundary.\nThe summit, legacy and intermediate Fletcher points are alternatives for one assembly. Verify access, mount, foliage and winter power.")],.142)
save()
pdf.close()
# Export physical micro-site sensitivity at sample offsets across a 20 m radius.
micro=[]
for a,b in presentations:
    if a not in candidates+fletcher:continue
    for dx,dy in [(0,0),(-20,0),(20,0),(0,-20),(0,20),(-10,-10),(-10,10),(10,-10),(10,10)]:
        x,y=np.array(xy[a])+[dx,dy]
        c,f,_=profile.stats((x,y,wh(a)),coords(b))
        micro.append([label(a),label(b),dx,dy,round(c,3),round(f,3)])
write_csv("mount-offsets.csv",["moving site","fixed neighbor","east m","north m","clear m","min F1 fraction"],micro)
