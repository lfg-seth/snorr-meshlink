"""Print the access-constrained field atlas using the same map and profile scales."""
from atlas_maps import *
from reachable_search import ANGEL, ESC, LEE, MACK, SHOW, VEGAS


def field_table(rect, columns, rows, widths, size=9):
    ax=axis(rect)
    ax.axis("off")
    table=ax.table(cellText=rows,colLabels=columns,cellLoc="left",colLoc="left",
                   colWidths=widths,bbox=[0,0,1,1])
    table.auto_set_font_size(False)
    table.set_fontsize(size)
    for (row,col),cell in table.get_celld().items():
        cell.set_edgecolor("#c2cec7")
        cell.set_linewidth(.55)
        cell.set_facecolor("#d8eae2" if row==0 else ("#ffffff" if row%2 else "#f1f4ef"))
        if row==0:
            cell.set_text_props(weight="bold",color="#254e49")


def pair(a,b):
    return graph[a][b]


def coord(k):
    lat,lon=lonlat(k)
    return f"{lat:.6f}, {lon:.6f}"


def signed(a,b):
    return f"{pair(a,b)['clear']:+.1f} m"


def main():
    offset_lee=next(k for k in plan if k in search["families"][LEE])
    scout=next(k for k in D["Map-only Angel comparison"]["layout"] if k in search["families"][ANGEL])
    # The closest screened trail point with clear rays to all four field endpoints.
    trail=min((k for k in search["families"][ESC] if all(pair(k,b)["clear"]>0 for b in
              ("Shady Hollow","Kyle Junction","Angel Vegas","Angel Mountain"))),
              key=lambda k:math.dist(xy[k],xy[ESC]))
    fig=page("Return survey  /  Lee Fire uplink","Start at Mack’s alternative",
             "Compare the new pins against the deployed radios with a 1.2 m member tracker and the existing three-forwarder limit.")
    ax=axis([.035,.15,.55,.65])
    mapbase(ax)
    roadstatus(ax,plan)
    map_labels(ax)
    field=["Lee Fire","Upper Bristlecone",MACK,"Angel Mountain",VEGAS,offset_lee]
    for a,b in [(field[0],field[1]),(field[1],field[2]),(field[2],field[3]),(field[2],field[4])]:
        ax.plot(*np.array([xy[a],xy[b]]).T,color="#962351",lw=1.7,zorder=5,
                path_effects=[pe.withStroke(linewidth=3.5,foreground="white")])
    for i,k in enumerate(field,1):
        pin(ax,k,str(i),(-12,-12) if i==4 else (5,5))
    fig.text(.61,.775,"First portable trial",size=13,weight="bold",color="#185c53")
    fig.text(.61,.735,"Keep the deployed radios in place. A portable at\nMack’s opens a modeled route for Angel Mountain\nvia Upper Bristlecone to Lee Fire.",va="top",linespacing=1.5)
    fig.text(.61,.598,"Test from each end",size=13,weight="bold",color="#185c53")
    fig.text(.61,.557,"Use the intended 4 m height at Mack’s. At 2 m,\nits path to Upper clears terrain by only 0.06 m.\nTest both directions and log the actual height.",va="top",linespacing=1.5)
    fig.text(.61,.416,"Survey waypoints",size=13,weight="bold",color="#185c53")
    for i,k in enumerate(field,1):
        fig.text(.615,.413-i*.034,f"{i}    {k}",size=10)
    fig.text(.05,.095,"Green road   modeled member delivery       Red road   gap       Magenta   trial relay path",size=9)
    save()

    fig=page("Layouts  /  same 39.61 km of highway","What each change buys",
             "Every percentage requires a path to Lee Fire. Strict reach also requires 60% first-Fresnel clearance on every backbone link.")
    variants=[("Deployed","Deployed"),("Move R006 to Lee Alternative","Move R006 to Lee Alternative center"),
              ("Move R006 to Mack","Move R006 to Mack’s"),("Keep deployed + Mack","Keep all deployed + Mack’s"),
              ("Hold deployed Angel Vegas","Mack’s + Lee offset, keep R005"),
              ("Owner pins only","Mack’s + Lee center + new Vegas pin"),
              ("Reachable plan","Mack’s + Lee offset + new Vegas pin"),
              ("Keep R005 + Angel scout","Mack’s + Lee offset + Angel scout, keep R005")]
    rows=[]
    for k,title in variants:
        v=D[k]
        rows.append([title,*[f"{v['scores'][g]:.1f}%" for g in ("Highway","SR 156","SR 157","SR 158")],
                     f"{v['robust']['Highway']:.1f}%"])
    field_table([.045,.41,.91,.39],["Trial","All roads","SR 156","SR 157","SR 158","Strict roads"],
                rows,[.42,.115,.11,.11,.11,.135])
    fig.text(.047,.336,"What limits the south side",size=12,weight="bold",color="#185c53")
    fig.text(.047,.303,"From a member heard at Angel Mountain, Angel → Mack’s → Upper Bristlecone already uses all three forwarders. A tracker\nfirst heard by another relay behind Angel needs an extra forwarder. A two-radio ping can succeed while that tracker still misses Lee.",
             va="top",size=10,linespacing=1.5)
    fig.text(.047,.168,"The previous 94.6% layout used ridge sites outside this KML. The map-only Angel scout needs access confirmation.\nA regular Shady repeater and each of the three Fletcher choices individually add zero highway reach on the revised backbone.",
             va="top",size=10,linespacing=1.5)
    save()

    fig=page("Angel Peak  /  R005 comparison","Can one Vegas site reach all three?",
             "Mack’s and Shady columns show native mountain terrain clearance. Valley columns count clear rays to nine 4 m probes per sector.")
    rows=[]
    angels=["Angel Vegas",VEGAS,"Angel Mountain",*search["families"][ANGEL]]
    for k in angels:
        rows.append([k,signed(k,MACK),signed(k,"Shady Hollow"),*[f"{n}/9" for n in search["valley"][k]]])
    field_table([.045,.375,.91,.43],["Angel location","Mack’s","Shady","Centennial","Lone Mtn","Providence","N. LV west"],
                rows,[.24,.12,.12,.135,.12,.13,.135])
    fig.text(.05,.309,"Keep the current R005 as the control",size=12,weight="bold",color="#185c53")
    fig.text(.05,.273,"Your alternative improves the Mack’s path and retains the valley sectors. The model blocks its direct Shady ray. G002’s card\nrecorded direct packets from deployed R005 and R011 despite modeled obstructions. Test a portable against G002 and a fixed\nvalley receiver in the same time window before choosing a mount.",va="top",size=10,linespacing=1.45)
    fig.text(.05,.117,f"{scout} links Mack’s and Escarpment. Its 0/36 valley result makes it a mountain-side survey option.",size=10)
    save()

    fig=page("Navigation  /  Google Earth and GPX","Where to carry the portable",
             "The KML groups the owner’s pins and generated survey points. Coordinates below are WGS84 latitude, longitude.")
    sites=[(MACK,"First outing. Test Upper Bristlecone and both Angel choices."),
           (LEE,"Center of the owner’s 20 m search. Test the Upper Bristlecone leg."),
           (offset_lee,"5 m east, 5 m south of center. Compare at the same height."),
           (VEGAS,"Compare Shady and valley reception against deployed R005."),
           (scout,"Map-only shoulder. Confirm local access, then test Mack’s and Escarpment."),
           (ESC,"Trail control. The owner’s placemark falls on the mapped footway."),
           (trail,"Near the control. Test Kyle Junction, Shady and both deployed Angels."),
           (SHOW,"Legacy pin. Test the Angel Mountain leg before considering an offset.")]
    field_table([.045,.42,.91,.385],["Waypoint","Latitude, longitude","At the waypoint"],
                [[k,coord(k),t] for k,t in sites],[.245,.255,.5],8.4)
    notes(.05,.342,[("Escarpment and Showgirl",
        "The Escarpment screen followed the 4.67 km mapped footway past the supplied pin. Survey 3 is about 21 m from the pin and has\nclear direct paths to Shady and Kyle Junction and both deployed Angels. At Showgirl the strongest first comparison is Angel Mountain."),
        ("Measure ordinary GPS delivery",
        "Record the sender, packet ID, send count, GPS fix time, Lee receipt time and antenna heights. Repeat the existing control before\nand after each trial. Inspect Shady’s offline SD card. Compare body-worn and in-vehicle results against the 15-minute freshness limit.")],.16)
    save()

    fig=page("Waypoint detail  /  USGS topography","Angel Peak and the Escarpment trail",
             "Compare the three owner-supplied Angel pins with the optional shoulder. The traced footway anchors the Escarpment search.")
    ax=axis([.046,.26,.43,.51])
    x,y=xy[VEGAS]
    mapbase(ax,(x-680,y-550,x+480,y+480),"detail")
    for n,(k,disp) in enumerate([("Angel Vegas",(6,-13)),("Angel Mountain",(5,-13)),(VEGAS,(5,7)),(scout,(-12,-12))],1):
        pin(ax,k,str(n),disp)
    fig.text(.045,.788,"Angel Peak",weight="bold",size=12)
    fig.text(.048,.214,"1   Deployed Angel Vegas       2   Deployed Angel Mountain",size=8.6)
    fig.text(.048,.178,"3   Owner’s Vegas alternative   4   Conditional road scout",size=8.6)
    fig.text(.048,.126,"Confirm access to the scout. The mapped road passes\nthrough the Angel Peak facility area.",size=9,linespacing=1.45)
    ax=axis([.522,.26,.43,.51])
    line=next(g for g,p in features if p.get("osm_id")==search["trail_id"])
    l,b,r,t=line.bounds
    mapbase(ax,(l-200,b-200,r+200,t+200),"detail")
    ax.plot(*line.xy,color="#176f67",lw=2,path_effects=[pe.withStroke(linewidth=4,foreground="white")])
    pin(ax,ESC,"Owner pin",(-55,8))
    pin(ax,trail,"Survey 3",(8,-14))
    fig.text(.522,.788,"Escarpment trail",weight="bold",size=12)
    fig.text(.523,.214,"Teal   mapped footway     •     OSM way "+search["trail_id"][1:],size=8.6)
    fig.text(.523,.162,"The supplied point lies about 1 m from the mapped way.\nThe trial offset is about 21 m from the supplied pin.",size=9,linespacing=1.45)
    save()
    resort_page()
    pairs=[(MACK,"Upper Bristlecone"),(MACK,"Angel Mountain"),(MACK,VEGAS),(MACK,"Lee Fire"),
           ("Upper Bristlecone","Lee Fire"),(offset_lee,"Upper Bristlecone"),(VEGAS,"Shady Hollow"),
           (scout,MACK),(scout,ESC),(trail,"Shady Hollow"),(trail,"Kyle Junction"),(SHOW,"Angel Mountain")]
    for a,b in pairs:
        direct_page(a,b)
    pdf.close()
    offsets=[]
    for a,b in pairs:
        for dx,dy in [(0,0),(-20,0),(20,0),(0,-20),(0,20)]:
            if a in search["families"][LEE] and math.dist((xy[a][0]+dx,xy[a][1]+dy),xy[LEE])>20:
                continue
            c,f,_=profile.stats((xy[a][0]+dx,xy[a][1]+dy,wh(a)),coords(b))
            offsets.append([a,b,dx,dy,round(c,3),round(f,3)])
    write_csv("mount-offsets.csv",["moving site","fixed neighbor","east m","north m","clear m","min F1 fraction"],offsets)


if __name__=="__main__":
    main()
