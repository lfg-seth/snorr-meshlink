"""Cross-check the field packet against independently traversed relay graphs and the height sweep."""
import base64
import re
from survey import *

html=(OUT/"radio-paths.html").read_text(encoding="utf8")
payload=json.loads(re.search(r"^const db=(.*);$",html,re.MULTILINE).group(1))
gpx=ET.parse(OUT/"survey-waypoints.gpx")
waypoints={w.find("{*}name").text for w in gpx.getroot()}
assert waypoints==set(payload["points"])==set(payload["views"])
assert set(payload["start"])<=waypoints and len(set(payload["start"]))==2
assert len(payload["paths"])==math.comb(len(waypoints),2)
sweeps=defaultdict(list)
with (OUT/"height-sweep.csv").open(encoding="utf-8-sig") as f:
    for row in list(csv.reader(f))[1:]:
        a,b,ha,hb,clear,f1=row
        sweeps[a,b].append(tuple(map(float,(ha,hb,clear,f1))))
for path in payload["paths"]:
    z=np.frombuffer(base64.b64decode(path["data"]),dtype="<i2").astype(float).cumsum()/100+path["z0"]
    t=np.linspace(0,1,len(z))
    zone=np.sqrt(wave*path["d"]*t[1:-1]*(1-t[1:-1]))
    for ha,hb,expected,expected_f1 in sweeps[path["a"],path["b"]]:
        clear=(z[0]+ha)*(1-t)+(z[-1]+hb)*t-z
        assert abs(clear[1:-1].min()-expected)<.021
        assert abs((clear[1:-1]/zone).min()-expected_f1)<.045
for scenario,v in D.items():
    selected={"Lee Fire",*v["layout"]}
    graph2=nx.Graph()
    graph2.add_nodes_from(selected)
    graph2.add_edges_from((a,b) for a,b,p in graph.edges(data=True) if a in selected and b in selected and p["clear"]>=0)
    connected=set(nx.single_source_shortest_path_length(graph2,"Lee Fire",cutoff=3))
    assert connected==set(v["reach"]),scenario
    rows=groups=="Highway"
    served=masks[[ix[k] for k in connected]].any(axis=0)
    assert round(100*weights[rows & served].sum()/weights[rows].sum(),1)==v["scores"]["Highway"]
if "source_pins" in search:
    from reachable_search import ANGEL, ESC, LEE, SHOW, load_waypoints
    owner=load_waypoints(OUT/"owner-waypoints.kml")
    assert set(owner)==set(search["source_pins"])
    kml={p.findtext("{*}name"):p.findtext("{*}Point/{*}coordinates") for p in
         ET.parse(OUT/"survey-waypoints.kml").findall(".//{*}Placemark") if p.find("{*}Point") is not None}
    assert set(kml)==waypoints
    for wp in gpx.getroot():
        k=wp.findtext("{*}name")
        lon,lat=map(float,kml[k].split(",")[:2])
        assert max(abs(lon-float(wp.get("lon"))),abs(lat-float(wp.get("lat"))))<1e-7
        if k in owner:
            assert math.dist(forward.transform(lon,lat),owner[k][0])<.02
    for group,r in [(LEE,20),(SHOW,100)]:
        assert all(math.dist(xy[k],xy[group])<=r+1e-6 for k in search["families"][group])
    trail=next(g for g,p in features if p.get("osm_id")==search["trail_id"])
    assert all(trail.distance(Point(xy[k]))<10.01 for k in search["families"][ESC])
    for scenario,record in D.items():
        assert len(record["layout"])<=10
        if scenario in ("Reachable plan","Owner pins only"):
            assert not set(record["layout"]).intersection(search["families"][ANGEL])
        strict=nx.Graph()
        strict.add_nodes_from(["Lee Fire",*record["layout"]])
        strict.add_edges_from((a,b) for a,b,p in graph.edges(data=True)
                              if a in strict and b in strict and p["f1"]>=.6)
        good=nx.single_source_shortest_path_length(strict,"Lee Fire",cutoff=3)
        served=masks[[ix[k] for k in good]].any(axis=0)
        assert round(100*weights[rows & served].sum()/weights[rows].sum(),1)==record["robust"]["Highway"]
else:
    assert set(plan)==set(D[key]["reach"])-{"Lee Fire"}
    assert np.allclose(lonlat("Kyle Junction"),pins["Kyle Junction"])
    assert xy["J1"][1]>xy["Lee Junction"][1] and xy["J6"][1]<xy["Lee Junction"][1]
print(f"PASS: {len(D)} layouts, {len(waypoints)} mapped sites, {len(payload['paths'])} radio paths and {sum(map(len,sweeps.values()))} height pairs")
