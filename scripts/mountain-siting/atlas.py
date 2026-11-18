"""Render the unrestricted November 17 field study."""
from atlas_maps import *

fig=page("Field atlas   /   Lee Fire backhaul","Mount Charleston repeater study","Terrain-screened survey plan for SR 156, SR 157, SR 158 and their member GPS targets.")
ax=axis([.035,.12,.56,.69]);mapbase(ax);roadstatus(ax,plan);map_labels(ax)
for j,k in enumerate(["Lee Fire",*plan]):
    pin(ax,k,str(j+1))
notes(.61,.785,[("First field test","Test the nearest passing shoulder on foot with Angel\nMountain and its Lee-side neighbor. Check a fresh\nGPS packet at Lee Fire before relocating R006."),
                 ("Four estimated assemblies","One for legacy Fletcher and one to replace Shady.\nApply the other two to the additional relay sites.\nWaypoint assignments are in the study brief."),
                 ("Gateway","Lee Fire is the sole uplink. Kyle Fire appears only\nin the optional dual-station comparison.")],.11)
for j,k in enumerate(["Lee Fire",*plan]):
    fig.text(.614,.445-j*.027,f"{j+1:>2}    {label(k)}",fontsize=9.1)
fig.text(.06,.082,"Green  modeled path to Lee Fire      Red  highway gap      Numbered sites  proposed layout",fontsize=9)
save()
fig=page("Layout comparison","What each placement buys","Percent of sampled highway length or facility probes with a path to Lee Fire through at most three forwarding radios.")
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
fig=page("Hardware and routes","Where each radio goes","Four new assemblies support the complete option. G001 stays at Lee Fire. Arrows follow modeled RF legs at 1 m / 4 m nominal heights.")
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
resort_page()
fig=page("Changes from deployment","What the moves gain and lose","Direct highway visibility before and after each move, using the same 1.2 m member tracker.")
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
    direct_page(a,b)
fig=page("Field verification","Where to take the radios","Use the GPX waypoint names in this atlas. A survey point and a road offset do not establish a usable winter approach.")
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
