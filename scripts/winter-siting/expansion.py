"""Compare every screened one- and two-site addition while the ten core sites stay fixed."""
from itertools import combinations
import numpy as np
from road_runs import road_runs


def compare_expansion(ids, sites, gateway, core, excluded, score, samples, weights, baseline, merit):
    target=np.array([s['kind']=='road' and s['name'] in ('SR 156','Macks Canyon') for s in samples])
    roads=np.array([s['kind']=='road' for s in samples])
    candidates=[i for i in range(len(sites)) if i not in gateway+core+excluded]
    rows=[]
    for count in (1,2):
        for extra in combinations(candidates,count):
            chosen=core+list(extra)
            if {'CL','CH'}<={ids[i] for i in chosen}:continue
            visible,_,paths=score(gateway+chosen)
            if any(i not in paths for i in extra):continue
            gain=visible & ~baseline
            rows.append(dict(sites=[ids[i] for i in extra],
                             lee_road_gain_km=float(weights[target & gain].sum()/1000),
                             road_gain_km=float(weights[roads & gain].sum()/1000),
                             score=merit(chosen)))
    def key(row):return (round(row['lee_road_gain_km'],5),round(row['road_gain_km'],5),row['score'])
    # Compare all pairs, including pairs where one site supplies the forwarding path.
    singles=[r for r in rows if len(r['sites'])==1]
    best_single=max(singles,key=key)
    pairs=[r for r in rows if len(r['sites'])==2 and any(single['sites'][0] in r['sites'] for single in singles)]
    if not pairs:raise ValueError('No connected, independently stageable pair. Review the candidate inputs.')
    best_pair=max(pairs,key=key)
    first=max((r for r in singles if r['sites'][0] in best_pair['sites']),key=key,default=None)
    if first:
        best_pair=dict(best_pair,sites=first['sites']+[k for k in best_pair['sites'] if k!=first['sites'][0]])
    def detail(row):
        seq=gateway+core+[ids.index(k) for k in row['sites']]
        visible,_,paths=score(seq)
        result=dict(row)
        result['paths']={k:[ids[i] for i in paths[ids.index(k)]] for k in row['sites']}
        result['sisters_path']=[ids[i] for i in paths.get(core[-1],[])]
        result['corridors']={}
        for name in ('SR 156','Macks Canyon'):
            ix=np.array([s['kind']=='road' and s['name']==name for s in samples])
            runs=road_runs(samples,name,~visible)
            prior=road_runs(samples,name,~baseline)
            original=prior[0][1] if prior else []
            result['corridors'][name]=dict(gain_km=weights[ix & visible & ~baseline].sum()/1000,
                                            former_gap_recovered_km=weights[original][visible[original]].sum()/1000,
                                            reachable_pct=100*weights[ix & visible].sum()/weights[ix].sum(),
                                            gap_km=runs[0][0].length/1000 if runs else 0.)
        return result
    return dict(rank_rule='New SR 156 and Macks Canyon road length, then all scored roads, then weighted merit.',
                compared=rows,best_single=detail(best_single),step_one=detail(first) if first else None,
                pair=detail(best_pair))
