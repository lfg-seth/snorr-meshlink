"""Decision, deployment and coverage results for the self-contained reachable field atlas."""
import csv
from textwrap import fill

from atlas_maps import (D, OUT, field_table, groups, ix, key, masks, names, np,
                        page, plan, save, search, weights)
from reachable_search import MACK, VEGAS


def road_km(scenario,road=None):
    take=groups=="Highway"
    if road:
        take=take & (names==road)
    selected=masks[[ix[k] for k in D[scenario]["reach"]]].any(axis=0)
    return weights[take & selected].sum()/1000


def paragraph(fig,x,y,title,body,width=55):
    fig.text(x,y,title,fontsize=11.4,color="#155c57",weight="bold")
    fig.text(x,y-.034,fill(body,width),fontsize=9.8,va="top",linespacing=1.43)


def executive_summary():
    title="Mount Charleston repeater study"
    fig=page("Study summary  /  Reachable survey waypoints",title,
             "Passive member GPS to Lee Fire • 17 supplied waypoints • 15 terrain-derived alternatives • 39.61 km of sampled highway")
    stages=[("Deployed","Deployed"),("Keep deployed + Mack","Add Mack’s only"),
            (key,"Reachable plan"),("Keep R005 + Angel scout","Conditional Angel scout")]
    for i,(scenario,name) in enumerate(stages):
        x=.046+i*.236
        fig.text(x,.72,f"{D[scenario]['scores']['Highway']:.1f}%",fontsize=28,weight="bold",color="#075e5b")
        fig.text(x,.667,name,fontsize=11,weight="bold")
        fig.text(x,.629,f"{road_km(scenario):.2f} km of highway reaches Lee",fontsize=8.8)
    paragraph(fig,.047,.535,"First outing","Take a portable to Mack’s alternative at 4 m. Test Angel Mountain → Mack’s → Upper Bristlecone → Lee Fire. At a 2 m Mack’s mount the modeled Upper Bristlecone clearance falls to 0.06 m.",58)
    paragraph(fig,.527,.535,"Keep R005 as the control","The proposed Vegas pin clears Mack’s by 4.04 m and sees 20/36 valley probes. Shady’s modeled direct ray is blocked by 124 m. Its recorder previously heard deployed R005 through a similar obstruction.",56)
    paragraph(fig,.047,.325,"If the trial succeeds","Add one assembly at Mack’s. Compare R006 at the Lee Alternative center and the 7 m offset. Trial R005 at the Vegas alternative only after checking Shady and a stationary valley receiver.",58)
    paragraph(fig,.527,.325,"What still needs coverage","The reachable plan serves 83.9% of SR 156, 2.4% of SR 157 and 30.0% of SR 158. The longest remaining gap on a mapped part is 6.94 km on SR 157. The Angel scout needs access confirmation.",57)
    fig.text(.047,.104,"Open a section",fontsize=9.4,color="#365652",weight="bold")
    for x,txt in [(.19,"Network viewsheds"),(.39,"Full layout results"),(.60,"Site viewshed index"),(.81,"Direct link profiles")]:
        fig.text(x,.104,txt,fontsize=9.4,color="#056c65",weight="bold")
    save()


def plan_and_routes():
    fig=page("Study summary  /  Deployment","Where each radio fits",
             "Five of the seven proposed relays have a member first-hop route to the Lee Fire uplink within the three-forwarder budget.")
    station="Lee Fire"
    lee=next(k for k in plan if k in search["families"]["Lee Alternative"])
    actions={station:("G001","Keep uplink"),"Upper Bristlecone":("R010","Keep"),
             "Cathedral Rock":("R001","Keep as control"),"Angel Mountain":("R011","Keep"),
             VEGAS:("R005","Portable comparison before move"),"Kyle Junction":("R008","Keep as control"),
             lee:("R006","Compare center and offset"),MACK:("One additional assembly","Attend first")}
    with (OUT/"station-routes.csv").open(encoding="utf-8-sig") as f:
        routes={row["origin"]:row for row in csv.DictReader(f) if row["scenario"]==key}
    rows=[]
    for k in [station,*plan]:
        hardware,action=actions[k]
        via="Gateway receiver"
        if k!=station:
            via=" → ".join(routes[k]["route (60% preferred)"].split(" > ")[1:]) if k in D[key]["reach"] else "No eligible route at nominal heights"
        rows.append([hardware,k,action,via])
    field_table([.045,.383,.91,.413],["Hardware","Waypoint","Field action","Next hops to Lee Fire"],rows,
                [.16,.215,.265,.36],8.4)
    paragraph(fig,.046,.302,"South-side options","At Escarpment survey 3 the Kyle Junction, Shady and both deployed Angel rays clear terrain. Showgirl has a clear Angel Mountain ray. A tracker first heard at either site would use a fourth forwarder on that route.",58)
    paragraph(fig,.528,.302,"Other assemblies","G002 records offline at Shady. A Shady repeater and the legacy, intermediate and summit Fletcher options each add zero highway length on this backbone. A Kyle Fire uplink would raise reach to 50.4% if Wi-Fi becomes available.",55)
    fig.text(.047,.105,"Using six assemblies gives the same 33.2% highway result if Kyle Junction is vacated to supply the extra radio. The seven-relay plan keeps that control.",size=8.7)
    save()


def facility_results():
    fig=page("Study summary  /  Service and gaps","Roads, trailheads and the resort",
             "Scores count a member first hop only when the receiver has an eligible route to Lee. Distances are confined to the study window.")
    metrics=["Highway","SR 156","SR 157","SR 158","Resort approach","Resort parking","Lodge / base","Trailheads","Other parking"]
    rows=[]
    for m in metrics:
        take=groups==m if m not in ("SR 156","SR 157","SR 158") else ((groups=="Highway") & (names==m))
        length=m in ("Highway","SR 156","SR 157","SR 158","Resort approach")
        unit={"Resort parking":"lot","Lodge / base":"probes","Trailheads":"trailheads","Other parking":"lots"}
        scope=f"{weights[take].sum()/1000:.2f} km" if length else f"{weights[take].sum():.0f} {unit[m]}"
        rows.append([m,scope,*[f"{D[case]['scores'][m]:.1f}%" for case in ("Deployed","Keep deployed + Mack",key)],
                     f"{D[key]['robust'][m]:.1f}%"])
    field_table([.045,.35,.91,.45],["Target","Scored extent","Deployed","Add Mack’s","Reachable plan","Strict plan"],
                rows,[.185,.175,.14,.15,.18,.17])
    with (OUT/"highway-gaps.csv").open(encoding="utf-8-sig") as stream:
        gaps=list(csv.DictReader(stream))
    longest={road:max((int(r["length m"]) for r in gaps if r["road"]==road),default=0)/1000 for road in ("SR 156","SR 157","SR 158")}
    gaptext="   •   ".join(f"{r}   {length:.2f} km" for r,length in longest.items())
    fig.text(.048,.277,"Longest blind stretch on one mapped road part",fontsize=11.5,weight="bold",color="#155c57")
    fig.text(.048,.227,gaptext,fontsize=11.2)
    fig.text(.048,.156,"Parking and trailhead probes share each mapped feature’s weight. Each lodge/base probe has unit weight.",fontsize=9.3)
    fig.text(.048,.115,"Strict plan requires 60% of the first Fresnel zone to clear terrain on every backbone leg. Normal member rays use bare-earth visibility.",fontsize=9.1)
    save()


def scenario_results():
    items=list(D.items())
    for start in range(0,len(items),11):
        portion=items[start:start+11]
        fig=page("All layout results",f"Reported layouts {start+1}–{start+len(portion)} of {len(items)}",
                 "Percent of target served at nominal heights. Kyle shows the hypothetical second uplink. All other columns require Lee Fire.")
        rows=[]
        for scenario,v in portion:
            layout=v["layout"]
            row=[scenario.replace(";"," /"),f"{len(set(layout)&set(v['reach']))}/{len(layout)}"]
            row += [f"{v['scores'][m]:.1f}" for m in ("Highway","SR 156","SR 157","SR 158","Resort approach",
                                                      "Resort parking","Lodge / base","Trailheads","Other parking")]
            row += [f"{v['robust']['Highway']:.1f}",f"{v['kyle']['Highway']:.1f}"]
            rows.append(row)
        field_table([.036,.295,.928,.50],["Layout","Relays¹","Roads","156","157","158","Approach","Resort lot","Lodge","Heads","Lots","Strict²","Kyle³"],
                    rows,[.255,.065,.06,.05,.05,.05,.08,.081,.065,.059,.055,.065,.065],8.0)
        fig.text(.047,.231,"¹ Eligible first-hop relays / selected relays. Roads = all sampled highway. 156, 157 and 158 are individual state routes.",size=9.1)
        fig.text(.047,.192,"Approach, resort lot and lodge are the ski-area targets. Heads = trailheads. Lots = other mapped parking.",size=9.1)
        fig.text(.047,.150,"² Highway coverage with 60% first-Fresnel clearance on every backbone leg.  ³ Highway coverage with both Lee and Kyle Fire as uplinks.",size=9.1)
        fig.text(.047,.102,"The search evaluated 36,480 combinations, with six deployed repeaters and up to four additional assemblies.",size=9.2)
        save()


def method_and_acceptance():
    fig=page("Study summary  /  Field verification","Assumptions and field acceptance",
             "The terrain model predicts radio visibility. A field decision needs a measured GPS fix and a matching receipt at the gateway.")
    paragraph(fig,.046,.735,"What the model sampled","USGS 3DEP bare-earth elevations, 910.625 MHz and a 4/3 effective Earth radius. Mountain profiles use native 1 m samples with mosaic fallback. Member rays use 5 m terrain sampling and are plotted on 35 m cells.",57)
    paragraph(fig,.527,.735,"What was searched","The 17 KML pins were retained. Offset screens tested 31 positions inside Lee’s 20 m radius, 272 inside Showgirl’s 100 m radius, 349 beside the Escarpment footway and 908 near the three Angel pins. The main plan uses reachable sites.",56)
    paragraph(fig,.046,.482,"How the plan was chosen","Use 1.2 m for a member, 4 m for relays and 1 m at stations. Rank 70% on strict service and 30% on terrain-clear service. Highway length carries half the objective. Parking, trailheads and resort probes carry the other half.",57)
    paragraph(fig,.527,.482,"How to test it","Confirm G001 power and Wi-Fi. At Mack’s, match direct packet IDs in both directions at Upper Bristlecone and Angel Mountain. Send an ordinary GPS packet across the route and record fix and receipt times. Target freshness is under 15 minutes.",56)
    paragraph(fig,.046,.224,"What can change in the field","Canopy, buildings, snow, body or vehicle shielding, interference and actual antenna height can change delivery. Shady’s recorded receptions are especially important when evaluating a blocked model ray.",57)
    paragraph(fig,.527,.224,"Control the comparison","Keep the current R005 on air during the portable test. Check the same Shady SD recorder and stationary valley receiver at both sites. Repeat the previously working route on foot and in the vehicle before moving a case.",56)
    save()
