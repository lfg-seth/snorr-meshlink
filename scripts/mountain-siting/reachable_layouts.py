"""Rank fieldable layouts by weighted member coverage at Lee within three forwarders."""
from itertools import product
from layouts import baseline, fletcher, groups, ix, masks, metrics, network, np, OUT, search, strong, weights
from reachable_search import ANGEL, ESC, LEE, MACK, SHOW, VEGAS
from functools import lru_cache
import json

families=search["families"]
priorities={"Highway":.50,"Other parking":.16,"Trailheads":.14,"Lodge / base":.10,
            "Resort approach":.05,"Resort parking":.05}
importance=np.zeros(len(weights))
for name,weight in priorities.items():
    take=groups==name
    importance[take]=weight*weights[take]/weights[take].sum()


@lru_cache(None)
def service(nodes):
    covered=masks[[ix[k] for k in nodes]].any(axis=0)
    return float(importance[covered].sum())


def build():
    layouts={"Deployed":baseline, "Shady replacement only":baseline+["Shady Hollow"],
             "Move R006 to Lee Alternative":baseline[:-1]+[LEE],
             "Move R006 to Mack":baseline[:-1]+[MACK],
             "Keep deployed + Mack":baseline+[MACK],
             "Mack + alternative Vegas":[k for k in baseline if k!="Angel Vegas"]+[MACK,VEGAS],
             "Mack + both Vegas sites":baseline+[MACK,VEGAS]}
    best={}
    count=0
    # Retain Cathedral, Upper Bristlecone and Angel Mountain. Reuse a moved radio;
    # four additional assemblies are available across all remaining field positions.
    fixed=["Upper Bristlecone","Cathedral Rock","Angel Mountain"]
    choices=[
        ["Angel Vegas",VEGAS,*families[ANGEL]], ["Kyle Junction",None],
        [None,"Lee Junction",LEE,*families[LEE]], [None,MACK],
        [None,"Shady Hollow"],[None,*fletcher], [None,SHOW,*families[SHOW]],
        [None,ESC,*families[ESC]]
    ]
    for selections in product(*choices):
        layout=fixed+[k for k in selections if k]
        if len(layout)>len(baseline)+4:
            continue
        # Radios may stay deployed when an added site would provide no member service.
        members=frozenset(layout)
        reach=frozenset(network(members))
        robust=frozenset(network(members,strong))
        rank=(round(.7*service(robust)+.3*service(reach),10),
              len(members.intersection(baseline)), -len(members),
              len(members.intersection(search["source_pins"])))
        count+=1
        mapped_angel=selections[0] in families[ANGEL]
        for label,allowed in [("Reachable plan",not mapped_angel),("Map-only Angel comparison",mapped_angel),
                              ("Hold deployed Angel Vegas", "Angel Vegas" in members),
                              ("Owner pins only",members.issubset(search["source_pins"])),
                              ("Move R006; no new assembly",not mapped_angel and len(layout)<=6 and "Lee Junction" not in members)]:
            if allowed and (label not in best or rank>best[label][0]):
                best[label]=(rank,layout)
    layouts.update({name:value[1] for name,value in best.items()})
    preferred=layouts["Reachable plan"]
    scout=next(k for k in layouts["Map-only Angel comparison"] if k in families[ANGEL])
    for name,label in [("Hold deployed Angel Vegas","Keep R005 + Angel scout"),
                       ("Reachable plan","Plan + Angel scout")]:
        if len(layouts[name])<10:
            layouts[label]=layouts[name]+[scout]
    layouts["Move R011 to Angel scout"]=[scout if k=="Angel Mountain" else k
                                        for k in layouts["Hold deployed Angel Vegas"]]
    for k in fletcher+["Shady Hollow",SHOW,ESC]:
        if k not in preferred and len(preferred)<10:
            layouts["Plan + "+k]=preferred+[k]
    out={}
    for label,layout in layouts.items():
        reach,scores=metrics(layout)
        out[label]=dict(layout=layout,reach=reach,scores=scores,robust=metrics(layout,adj=strong)[1],
                        kyle=metrics(layout,True)[1])
        print(label, scores["Highway"],out[label]["robust"]["Highway"],reach,flush=True)
    (OUT/"layouts.json").write_text(json.dumps(out,indent=2))
    print(f"Scored {count} layouts; preferred {preferred}")


if __name__=="__main__":
    build()
