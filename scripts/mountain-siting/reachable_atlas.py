"""Print the access-constrained field atlas using the same map and profile scales."""
from atlas_maps import *
from reachable_search import ANGEL, ESC, LEE, MACK, SHOW, VEGAS
from summary_pages import executive_summary, facility_results, method_and_acceptance, plan_and_routes, scenario_results
from viewshed_pages import angel_valley_viewshed, individual_viewsheds, network_spreads
import pymupdf


def pair(a,b):
    return graph[a][b]


def coord(k):
    lat,lon=lonlat(k)
    return f"{lat:.6f}, {lon:.6f}"


def signed(a,b):
    return f"{pair(a,b)['clear']:+.1f} m"


def marked_site(ax,k,title,at,color):
    ax.scatter(*xy[k],s=46,color=color,edgecolor="white",linewidth=1.4,zorder=9)
    ax.annotate(title,xy[k],xytext=at,textcoords="axes fraction",fontsize=9,weight="bold",
                color=color,ha="center",va="center",zorder=10,
                bbox=dict(boxstyle="round,pad=.34",fc="#fffef8",ec=color,lw=.7),
                arrowprops=dict(arrowstyle="-",color=color,lw=1,shrinkA=2,shrinkB=4,
                                path_effects=[pe.withStroke(linewidth=2.7,foreground="white")]))


def waypoint_maps(scout,trail):
    fig=page("Survey waypoints  /  Angel Peak","Angel Peak",
             "Four survey positions on the summit ridge. The proposed Vegas site and the conditional road scout are 154 m apart.")
    ax=axis([.045,.155,.635,.635])
    x,y=xy[VEGAS]
    mapbase(ax,(x-735,y-480,x+405,y+335))
    deployed="#15585a"
    proposed="#8a304f"
    marked_site(ax,"Angel Mountain","Deployed Angel Mountain",(.21,.71),deployed)
    marked_site(ax,"Angel Vegas","Deployed Angel Vegas",(.80,.19),deployed)
    marked_site(ax,VEGAS,"Vegas alternative",(.79,.78),proposed)
    marked_site(ax,scout,"Road scout",(.40,.33),proposed)
    fig.text(.71,.755,"WGS84 waypoints",fontsize=12,weight="bold",color="#185c53")
    for i,(title,k) in enumerate([("Deployed Angel Mountain","Angel Mountain"),("Deployed Angel Vegas","Angel Vegas"),
                                  ("Vegas alternative",VEGAS),("Road scout",scout)]):
        y=.70-i*.085
        fig.text(.71,y,title,fontsize=10,weight="bold",color=deployed if i<2 else proposed)
        fig.text(.71,y-.029,coord(k),fontsize=9)
    fig.text(.71,.327,"Check before the visit",fontsize=11,weight="bold",color="#185c53")
    fig.text(.71,.296,"Confirm access to the road scout.\nThe mapped road passes through\nthe Angel Peak facility area.",
             va="top",fontsize=9.5,linespacing=1.45)
    fig.text(.045,.100,"Contours every 10 m  •  Index contours every 50 m  •  Elevation in metres above sea level",fontsize=9)
    save("angel-peak-map.png")

    fig=page("Survey waypoints  /  Kyle Canyon","Escarpment trail",
             "The trail map shows the 4.67 km mapped footway. The enlargement locates the supplied pin and its nearby survey offset.")
    line=next(g for g,p in features if p.get("osm_id")==search["trail_id"])
    l,b,r,t=line.bounds
    ax=axis([.045,.235,.555,.50])
    mapbase(ax,(l-120,b-160,r+115,t+160))
    ax.plot(*line.xy,color="#176f67",lw=1.9,path_effects=[pe.withStroke(linewidth=3.4,foreground="white")],zorder=5)
    x,y=xy[ESC]
    close=(x-73,y-75,x+98,y+65)
    ax.add_patch(Rectangle(close[:2],close[2]-close[0],close[3]-close[1],fill=False,ec=proposed,
                           lw=1.6,zorder=7,path_effects=[pe.withStroke(linewidth=3,foreground="white")]))
    ax.annotate("Survey area",(x,y),xytext=(22,-19),textcoords="offset points",weight="bold",
                color=proposed,fontsize=9,bbox=dict(fc="white",ec="none",pad=2),zorder=8)
    ax=axis([.625,.235,.33,.50])
    mapbase(ax,close)
    ax.plot(*line.xy,color="#176f67",lw=1.9,path_effects=[pe.withStroke(linewidth=3.4,foreground="white")],zorder=5)
    marked_site(ax,ESC,"Supplied pin",(.28,.73),deployed)
    marked_site(ax,trail,"Survey 3",(.73,.24),proposed)
    fig.text(.045,.763,"Trail overview",fontsize=12,weight="bold",color="#185c53")
    fig.text(.625,.763,"Waypoint detail",fontsize=12,weight="bold",color="#185c53")
    fig.text(.045,.166,"Teal   mapped Escarpment footway     •     10 m contours",fontsize=9)
    fig.text(.625,.166,"2 m contours     •     Pins about 21 m apart",fontsize=9)
    fig.text(.045,.103,"Supplied pin   "+coord(ESC)+"       Survey 3   "+coord(trail),fontsize=10)
    save("escarpment-trail-map.png")


def finish_atlas():
    pdf.close()
    output=atlas_path.with_suffix(".indexed.pdf")
    with pymupdf.open(render_path) as doc:
        toc=[]
        groups={}
        for section,title,number in page_index:
            if section not in groups:
                groups[section]=number
                toc.append([1,section,number])
            toc.append([2,title,number])
        doc.set_toc(toc)
        jumps={"Network viewsheds":"Network viewsheds","Full layout results":"All layout results",
               "Site viewshed index":"Individual site viewsheds","Direct link profiles":"Viewshed and direct path"}
        for text,section in jumps.items():
            where,=doc[0].search_for(text)
            doc[0].insert_link({"kind":pymupdf.LINK_GOTO,"from":where,"page":groups[section]-1})
        index=doc[groups["Individual site viewsheds"]-1]
        words=index.get_text("words")
        for section,title,number in page_index:
            if section=="Individual site viewsheds" and number>index.number+1:
                # The printed page number starts each two-site entry on the index.
                where,=(pymupdf.Rect(word[:4]) for word in words if word[4]==str(number) and word[1]<index.rect.height*.8)
                where.x1+=index.rect.width*.42
                index.insert_link({"kind":pymupdf.LINK_GOTO,"from":where,"page":number-1})
        doc.set_metadata({**doc.metadata,"title":"Mount Charleston repeater study | Coverage and viewshed atlas",
                          "subject":"Reachable survey waypoints, member GPS coverage and field trials"})
        doc.save(output,garbage=4,deflate=True,use_objstms=1)
    output.replace(atlas_path)
    render_path.unlink()


def main():
    offset_lee=next(k for k in plan if k in search["families"][LEE])
    scout=next(k for k in D["Map-only Angel comparison"]["layout"] if k in search["families"][ANGEL])
    # The closest screened trail point with clear rays to all four field endpoints.
    trail=min((k for k in search["families"][ESC] if all(pair(k,b)["clear"]>0 for b in
              ("Shady Hollow","Kyle Junction","Angel Vegas","Angel Mountain"))),
              key=lambda k:math.dist(xy[k],xy[ESC]))
    executive_summary()
    network_spreads()
    angel_valley_viewshed()
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

    plan_and_routes()
    facility_results()
    scenario_results()

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

    waypoint_maps(scout,trail)
    resort_page()
    method_and_acceptance()
    individual_viewsheds()
    pairs=[(MACK,"Upper Bristlecone"),(MACK,"Angel Mountain"),(MACK,VEGAS),(MACK,"Lee Fire"),
           ("Upper Bristlecone","Lee Fire"),(offset_lee,"Upper Bristlecone"),(VEGAS,"Shady Hollow"),
           (scout,MACK),(scout,ESC),(trail,"Shady Hollow"),(trail,"Kyle Junction"),(SHOW,"Angel Mountain")]
    for a,b in pairs:
        direct_page(a,b)
    finish_atlas()
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
