"""Geographic names, waypoint roles and comparable field evidence for the atlas."""
from layouts import *
import xml.etree.ElementTree as ET

D=read(OUT/"layouts.json")
key="Legacy Fletcher"
plan=D[key]["layout"]
labels={"C01":"Upper Lee south ridge","C04":"Lee Meadows east ridge","C10":"Lower Bristlecone east spur",
        "C16":"Lee Junction northwest shoulder","C24":"Kyle Junction south ridge","C35":"Kyle Junction north ridge",
        "C46":"Kyle Junction south shoulder","C65":"Upper Lee southwest ridge",
        "J1":"Lee Junction near northwest","J3":"Lee Junction upper northwest","J6":"Lee Junction southeast bridge",
        "J10":"Lee Junction south bridge"}
def label(k):
    return labels.get(k,k)
def lonlat(k):
    lon,lat=inverse.transform(*xy[k])
    return lat,lon
def wh(k):
    return 1 if k.endswith("Fire") else 4
def coords(k):
    return (*xy[k],wh(k))
def route(k,layout,threshold=0):
    adj=normal if threshold==0 else strong
    G=nx.Graph()
    for a in ["Lee Fire",*layout]:
        G.add_node(a)
        for b in adj[a].intersection(["Lee Fire",*layout]):
            G.add_edge(a,b)
    paths=list(nx.all_shortest_paths(G,k,"Lee Fire")) if nx.has_path(G,k,"Lee Fire") else []
    return max(paths,key=lambda p:min([graph[a][b]["f1"] for a,b in zip(p,p[1:])] or [100])) if paths else []
def write_csv(name,header,rows):
    with (OUT/name).open("w",newline="",encoding="utf-8-sig") as file:
        w=csv.writer(file)
        w.writerow(header)
        w.writerows(rows)
def reference_labels():
    """Named features and highway shield anchors in the same CRS as the path maps."""
    wanted=["Lee Canyon","Desert View Overlook","Fletcher Peak","Mummy Mountain",
            "The Sisters","Upper Bristlecone Trailhead","Harris Mountain","Stanley B Springs"]
    labels=[]
    for name in wanted:
        point=next((g for g,p in features if g.geom_type=="Point" and p.get("name")==name),None)
        if point is not None:
            labels.append((name,*point.coords[0],"landmark"))
    for ref in ("SR 156","SR 157","SR 158"):
        line=max((g for g,n in road_inventory if n==ref),key=lambda g:g.length)
        for distance in (.6,.27,.83):
            labels.append((ref,*line.interpolate(distance,normalized=True).coords[0],"road"))
    return labels

def export():
    display=list(dict.fromkeys(["Lee Fire",*existing,"Shady Hollow",*fletcher,"Kyle Fire"]+
                              [k for v in D.values() for k in v["layout"]]))
    root=ET.Element("gpx",version="1.1",creator="SNORR MeshLink",xmlns="http://www.topografix.com/GPX/1/1")
    for k in display:
        lat,lon=lonlat(k)
        wp=ET.SubElement(root,"wpt",lat=f"{lat:.7f}",lon=f"{lon:.7f}")
        ET.SubElement(wp,"name").text=label(k)
        ET.SubElement(wp,"desc").text=f"{k}. Survey point. Verify access and actual antenna position on site."
    ET.ElementTree(root).write(OUT/"survey-waypoints.gpx",encoding="utf-8",xml_declaration=True)
    write_csv("candidates.csv",["key","field name","latitude","longitude","ground m","highway offset m","direct highway km","selected in"],(
        [k,label(k),*lonlat(k),round(elevation(grid,meta,*xy[k])),round(roads.distance(Point(xy[k]))),
         round(weights[(groups=="Highway") & masks[ix[k]]].sum()/1000,3)," | ".join(n for n,v in D.items() if k in v["layout"])] for k in ids))
    rows=[]
    for a,b in combinations(ids,2):
        shared=masks[ix[a]]&masks[ix[b]]
        edge=graph[a].get(b,{})
        rows.append([label(a),label(b),round(math.dist(xy[a],xy[b])/1000,3),edge.get("clear"),edge.get("f1"),round(weights[(groups=="Highway")&shared].sum()/1000,3)]+
                    [int(shared[groups==g].sum()) for g in ("Trailheads","Other parking","Resort parking","Lodge / base")])
    write_csv("pair-overlap.csv",["site A","site B","km","native LOS clearance m","min first Fresnel fraction","shared highway km","shared trailhead probes","shared other parking probes","shared resort lot probes","shared lodge/base probes"],rows)
    rows=[]
    for scenario,v in D.items():
        for site in v["layout"]:
            p=route(site,v["layout"],.6) or route(site,v["layout"])
            rows.append([scenario,label(site)," > ".join(map(label,p)),len(p)-1 if p else "",site in v["reach"]])
    write_csv("station-routes.csv",["scenario","origin","route (60% preferred)","radio links","member path within 3 repeats"],rows)
    reach=D[key]["reach"]
    mask=masks[[ix[k] for k in reach]].any(axis=0)
    base=masks[[ix[k] for k in D["Deployed"]["reach"]]].any(axis=0)
    rows=[]
    for i,(x,y) in enumerate(targets):
        lon,lat=inverse.transform(x,y)
        rows.append([groups[i],names[i],round(lat,6),round(lon,6),weights[i],int(base[i]),int(mask[i]),
                     " | ".join(label(k) for k in reach if masks[ix[k],i])])
    write_csv("member-probes.csv",["type","name","latitude","longitude","weight (road m or facility share)","deployed reachable","plan reachable","plan visible connected sites"],rows)
    gaps=[]
    for idx,(line,ref) in enumerate(road_inventory):
        samples=np.flatnonzero(part==idx)
        runs=np.split(samples[~mask[samples]],np.flatnonzero(np.diff(samples[~mask[samples]])>1)+1)
        for run in runs:
            if not len(run):
                continue
            a=line.interpolate(max(0,offset[run[0]]-weights[run[0]]/2))
            b=line.interpolate(min(line.length,offset[run[-1]]+weights[run[-1]]/2))
            gaps.append([ref,round(weights[run].sum()),*inverse.transform(a.x,a.y)[::-1],*inverse.transform(b.x,b.y)[::-1]])
    write_csv("highway-gaps.csv",["road","length m","start latitude","start longitude","end latitude","end longitude"],sorted(gaps,key=lambda v:-v[1]))
    return display
if __name__=="__main__":
    export()
