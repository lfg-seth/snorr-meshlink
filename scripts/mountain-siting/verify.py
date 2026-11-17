"""Cross-check the field packet against independently traversed relay graphs and the height sweep."""
import base64
import re
from survey import *

html=(OUT/"radio-paths.html").read_text(encoding="utf8")
payload=json.loads(re.search(r"const db=(.*);\nconst by=",html).group(1))
gpx=ET.parse(OUT/"survey-waypoints.gpx")
waypoints={w.find("{*}name").text for w in gpx.getroot()}
assert waypoints==set(payload["points"])==set(payload["views"])
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
    for ha,hb,expected,_ in sweeps[path["a"],path["b"]]:
        clear=(z[0]+ha)*(1-t)+(z[-1]+hb)*t-z
        assert abs(clear[1:-1].min()-expected)<.021
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
assert set(plan)==set(D[key]["reach"])-{"Lee Fire"}
assert lonlat("Kyle Junction")==pins["Kyle Junction"] or np.allclose(lonlat("Kyle Junction"),pins["Kyle Junction"])
assert xy["J1"][1]>xy["Lee Junction"][1] and xy["J6"][1]<xy["Lee Junction"][1]
print(f"PASS: {len(D)} layouts, {len(waypoints)} mapped sites, {len(payload['paths'])} radio paths and {sum(map(len,sweeps.values()))} height pairs")
