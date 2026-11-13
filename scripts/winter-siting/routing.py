"""Sink-only gateways; graph search works on live nodes after each failure."""


def routes_to_gateways(ids, gateways, links, hops, failed=None):
    active=set(ids)-{failed}
    paths={g:[g] for g in gateways if g in active}
    for _ in range(hops):
        previous=dict(paths)
        for i in sorted(active-previous.keys()):
            neighbors=[j for j in previous if links[i,j]]
            if neighbors:
                j=min(neighbors,key=lambda k:(len(previous[k]),k))
                paths[i]=[i]+previous[j]
    assert all(failed not in path and len(path)-1<=hops for path in paths.values())
    return paths


def union_mask(indices, masks):
    result=0
    for i in indices:
        result |= masks[i]
    return result


def choose(sites, gateways, links, hops, masks, weights, limit, excluded=(), forced=(), resilience_weight=.07):
    """Deterministic multi-start greedy construction and one-for-one local exchange."""
    candidates=[i for i in range(len(sites)) if i not in set(gateways)|set(excluded)]
    cache={}
    def feasible(chosen):
        names={sites[i]['id'] for i in chosen}
        return not {'CL','CH'}<=names
    def merit(chosen):
        key=tuple(sorted(chosen))
        if key in cache:return cache[key]
        active=list(gateways)+list(key)
        paths=routes_to_gateways(active,gateways,links,hops)
        mask=union_mask(paths,masks)
        coverage=sum((mask & s).bit_count()*w for s,w in weights)
        # Coverage first; resilience and shorter approaches distinguish similar layouts.
        survive=mask
        for i in active:
            survive &= union_mask(routes_to_gateways(active,gateways,links,hops,i),masks)
        resilience=sum((survive & s).bit_count()*w for s,w in weights)
        difficulty=sum(sites[i]['difficulty'] for i in chosen)
        value=coverage+resilience_weight*resilience-.00022*difficulty
        cache[key]=value
        return value
    def fill(seed):
        chosen=list(seed)
        while len(chosen)<limit:
            options=[i for i in candidates if i not in chosen and feasible(chosen+[i])]
            chosen.append(max(options,key=lambda i:merit(chosen+[i])))
        while True:
            old=merit(chosen)
            swaps=[([i for i in chosen if i!=a]+[b]) for a in chosen if a not in forced
                   for b in candidates if b not in chosen and feasible([i for i in chosen if i!=a]+[b])]
            if not swaps:break
            best=max(swaps,key=merit)
            if merit(best)<=old+1e-10:break
            chosen=best
        return chosen
    # Include seeds with a second bridge; greedy singleton addition can miss these.
    seeds=[list(forced)]+[list(forced)+[i] for i in candidates if i not in forced and feasible(list(forced)+[i])]
    layouts=[fill(seed) for seed in seeds]
    winner=max(layouts,key=merit)
    ordered=[]
    while len(ordered)<limit:
        ordered.append(max((i for i in winner if i not in ordered),key=lambda i:merit(ordered+[i])))
    return ordered,merit
