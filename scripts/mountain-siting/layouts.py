"""Compare hardware-constrained layouts and export route, overlap and height evidence."""
from functools import lru_cache
import networkx as nx
from model import *

search=read(OUT/"search.json")
xy={k:tuple(v) for k,v in search["xy"].items()}
data=np.load(OUT/"targets.npz")
ids=list(data["ids"])
masks=data["masks"].astype(bool)
ix={k:i for i,k in enumerate(ids)}
baseline=["Upper Bristlecone","Cathedral Rock","Angel Vegas","Angel Mountain","Kyle Junction","Lee Junction"]
movable=baseline[-3:]
existing=["Lee Fire",*baseline]
fletcher=["Legacy Fletcher","Fletcher intermediate","Fletcher Peak"]
candidates=[k for k in ids if (k.startswith("C") and k!="Cathedral Rock") or k.startswith(("J","Across "))]
graph=nx.Graph()
graph.add_nodes_from(ids)
for edge,(clear,f1) in search["links"].items():
    a,b=edge.split("|")
    graph.add_edge(a,b,clear=clear,f1=f1)
def packed(arr):
    return int.from_bytes(np.packbits(arr,bitorder="little").tobytes(),"little")
bitmask={k:packed(masks[ix[k]]) for k in ids}
classes={g:packed(groups==g) for g in sorted(set(groups))}
def links_for(threshold):
    return {k:{l for l in graph[k] if graph[k][l]["f1"]>=threshold} for k in ids}
normal=links_for(0.0)
strong=links_for(.6)
road_distance={k:float(disttree.query(xy[k])[0]) for k in candidates}
def network(layout,adj=normal,kyle=False):
    covered={"Lee Fire"}
    if kyle:
        covered.add("Kyle Fire")
    frontier=covered.copy()
    for _ in range(3):
        frontier={l for k in frontier for l in adj[k] if l in layout}-covered
        covered.update(frontier)
    return covered

def union_mask(nodes):
    bits=0
    for k in nodes:
        bits|=bitmask[k]
    return bits
@lru_cache(maxsize=50000)
def fractions(bits):
    return {g:(bits & m).bit_count()/m.bit_count() for g,m in classes.items()}
def quality(layout):
    physical=set(layout)
    reach=network(physical)
    robust=network(physical,strong)
    m=fractions(union_mask(reach))
    mr=fractions(union_mask(robust))
    # Serve every selected relay, then prefer road and facility delivery on clear-Fresnel paths.
    utility=lambda f: .50*f["Highway"]+.16*f["Other parking"]+.14*f["Trailheads"]+.10*f["Lodge / base"]+.05*f["Resort approach"]+.05*f["Resort parking"]
    return (len(reach)-1-len(physical), .70*utility(mr)+.30*utility(m)-
            .0009*sum(k not in physical for k in movable)-
            .00000015*sum(road_distance.get(k,0) for k in physical))
def solve(fsite,mode="free"):
    initial=baseline+["Shady Hollow"]+([fsite] if fsite else [])
    eligible_sites=[k for k in candidates if mode!="close" or road_distance[k]<1200]
    layouts=sorted((tuple(initial+[a,b]) for a,b in combinations(eligible_sites,2)),
                   key=lambda x:(quality(x),x),reverse=True)[:18]
    # Beam search two new slots and refine all movable positions. Keep identical physical sets once.
    for idx in [5,3,4,6,len(initial),len(initial)+1,5,6]:
        if mode=="retain" and idx in (3,4,6):
            continue
        pool={}
        for layout in layouts:
            if idx in (3,4,5):
                choices=[initial[idx]]+[k for k in eligible_sites if math.dist(xy[k],xy[initial[idx]])<=2600]
            elif idx==6:
                choices=["Shady Hollow"]+eligible_sites
            else:
                choices=eligible_sites
            for k in choices:
                updated=list(layout)
                if len(updated)==idx:
                    updated.append(k)
                else:
                    updated[idx]=k
                if len(set(updated))!=len(updated):
                    continue
                key=frozenset(updated)
                if key not in pool:
                    pool[key]=tuple(updated)
        layouts=sorted(pool.values(),key=lambda x:(quality(x),x),reverse=True)[:12]
    return list(layouts[0])

def metrics(layout,kyle=False,adj=normal):
    reach=network(set(layout),adj,kyle)
    count=masks[[ix[k] for k in reach]].sum(axis=0)
    mask=count>0
    summary={}
    for label in sorted(set(groups)|set(names[groups=="Highway"])):
        idx=(groups==label) if label in classes else (names==label)&(groups=="Highway")
        summary[label]=round(100*weights[idx & mask].sum()/weights[idx].sum(),1)
    return sorted(reach),summary
def output():
    layouts={"Deployed":baseline,"Shady swap only":baseline+["Shady Hollow"]}
    for f in [None,*fletcher]:
        layouts[f or "No Fletcher"]=solve(f)
    layouts["Keep Kyle, Angel and Shady"]=solve("Legacy Fletcher","retain")
    layouts["Closer to highways"]=solve("Legacy Fletcher","close")
    layouts["First Lee bridge trial"]=[*baseline[:-1],"J1"]
    south=min((k for k in candidates if k.startswith("J") and xy[k][1]<xy["Lee Junction"][1] and "Lee Fire" in strong[k]),key=lambda k:math.dist(xy[k],xy["Lee Junction"]))
    for k in ("Across SR 156","Across SR 158",south):
        layouts["Lee trial "+k]=[*baseline[:-1],k]
    for tag,k in [("Retain closest bridge","J1"),("South-facing alternative",south)]:
        alternative=list(layouts["Legacy Fletcher"])
        if k not in alternative or alternative[5]==k:
            alternative[5]=k
            layouts[tag]=alternative
    for f in fletcher:
        layouts["Same backbone + "+f]=layouts["No Fletcher"]+[f]
    primary=layouts["Legacy Fletcher"]
    # The moved R006 and Shady's replacement are both nominal 4 m repeaters.
    # Assign the closer of their two field positions to the deployed R006.
    if math.dist(xy[primary[6]],xy["Lee Junction"])<math.dist(xy[primary[5]],xy["Lee Junction"]):
        primary[5],primary[6]=primary[6],primary[5]
    layouts["First northwest shoulder trial"]=[*baseline[:-1],primary[5]]
    common=[k for k in primary if k not in fletcher]
    layouts["Primary without Fletcher"]=common
    for f in fletcher:
        layouts["Primary with "+f]=common+[f]
    summaries={}
    for label,layout in layouts.items():
        reach,summary=metrics(layout)
        summaries[label]=dict(layout=layout,reach=reach,scores=summary,robust=metrics(layout,adj=strong)[1],kyle=metrics(layout,True)[1])
    (OUT/"layouts.json").write_text(json.dumps(summaries,indent=2))
    for k,v in summaries.items():
        print(k,v["layout"],v["scores"],v["robust"]["Highway"])
if __name__=="__main__":
    output()
