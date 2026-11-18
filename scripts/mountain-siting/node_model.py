"""Node roster, direct link evidence, and role-aware Lee Fire scenarios for the field report."""
from functools import lru_cache
from itertools import combinations
from math import dist
from survey import (DATA, OUT, baseline, boundary, coords, features, forward, graph, groups,
                    ix, lonlat, masks, names, profile, road_inventory, weights, wh, xy)
import networkx as nx
import numpy as np
import rasterio
from shapely import contains_xy

from node_valley import CACHE as VALLEY_CACHE

REPORT = VALLEY_CACHE.parent.with_name("mountain-node-study-20261118-favorites")
CACHE = REPORT / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

UP="Upper Bristlecone"
LEE="Lee Fire"
MACK="Mack's alternative"
SHADY="Shady Hollow"
ESC="Escarpment trail"
CAT="Cathedral Rock"
ANGEL="Angel Vegas"
KYLE_FIRE="Kyle Fire"
A5="Angel road survey 5"
REGIONAL=[ANGEL,A5]
SITES=[UP,LEE,MACK,SHADY,ESC,CAT,A5,ANGEL,KYLE_FIRE]
CODE=dict(zip(SITES,("UB","LF","MA","SH","ES","CR","A5","AV","KF")))
ROUTERS=set(SITES)-{LEE,KYLE_FIRE}
OBSERVED={frozenset((SHADY,k)) for k in (CAT,ANGEL)}
SITE_INFO={
    UP:("R010 · deployed router","Lee Canyon backbone","Upper is the western anchor for the proposed Mack’s link. The model connects it directly to Lee Fire.","Test reciprocal packet IDs from Mack’s, then match the member fix time at Lee Fire."),
    LEE:("G001 · gateway","Lee Fire uplink","Lee Fire is the sole dispatch uplink. A tracker can reach the gateway directly or through the favorite-router chain.","Check gateway power and uplink. Match the member ID, GPS fix time and gateway receipt time."),
    MACK:("Owner waypoint · proposed router","Bridge into Lee Canyon","This supplied pin connects the Angel road site to Upper Bristlecone. Both modeled links are needed to carry south-side traffic to Lee.","Set the portable at the intended 4 m. Repeat the Upper link at 2 m to measure mount sensitivity."),
    SHADY:("RAK · proposed router","Shady Hollow relay","A RAK router takes the former recorder position. G002 heard Cathedral Rock and Angel Vegas here before its proposed move. These receptions belong to the original hardware and mount.","At the RAK, repeat the Cathedral and Angel tests and check the Escarpment link. Match a member GPS fix at Lee Fire."),
    ESC:("Owner waypoint · proposed router","Escarpment footway","The supplied pin sits beside the mapped footway. It joins the southern sites to Angel road survey 5.","Keep the portable at the supplied pin first. Compare the Angel and south-side links with the same antenna."),
    CAT:("R001 · deployed router","Cathedral Rock control","Cathedral has a terrain-clear path to Kyle Fire and Escarpment. The historical Shady recorder heard Cathedral across a marginal terrain profile.","Test G002 at the station, then verify the new RAK at Shady with numbered packets in both directions."),
    A5:("Road scout · proposed router","Mountain-facing Angel relay","Survey 5 clears Mack’s and Escarpment. It operates alongside Angel Vegas in this plan. Their valley maps use the same 4 m receiver.","Confirm access and the 4 m mount. Test Mack’s and Escarpment, then compare valley reception against Angel Vegas."),
    ANGEL:("R005 · deployed router","Valley-facing Angel control","This installed Vegas-side radio has a clear path to Escarpment. G002 at the former Shady recording position also heard it directly.","Keep R005 operating. Compare against road survey 5 at the same fixed valley receiver and repeat the Shady test."),
    KYLE_FIRE:("G002 · forwarding CLIENT","Kyle Canyon station","G002 moves to the station pin as a forwarding CLIENT with local SD recording. Its modeled neighbor is Cathedral Rock. Backhaul remains at Lee Fire.","Check the actual antenna height and CLIENT rebroadcast setting. Log direct Cathedral packets and match a tracker fix at Lee Fire."),
}
COLORS={"Strong":"#08776F","Marginal":"#A36406","Blocked":"#68757B","Recorded":"#973B72"}


def observed(a,b):
    return frozenset((a,b)) in OBSERVED


def rating(a,b):
    v=graph[a][b]
    return "Blocked" if v["clear"]<0 else "Strong" if v["f1"]>=.6 else "Marginal"


FIELD_EXAMPLES=("Kyle Junction",CAT)
CLEARANCE_FLOOR=min(graph[SHADY][k]["clear"] for k in FIELD_EXAMPLES)
FRESNEL_FLOOR=min(graph[SHADY][k]["f1"] for k in FIELD_EXAMPLES)


def status(a,b):
    """Field classification at nominal mounts. Routing still uses the modeled terrain rating."""
    terrain=rating(a,b)
    if terrain!="Blocked":
        return terrain
    path=graph[a][b]
    comparable=path["clear"]>=CLEARANCE_FLOOR and path["f1"]>=FRESNEL_FLOOR
    if observed(a,b):
        return "Marginal · recorded" if comparable else "Recorded"
    return "Marginal · unverified" if comparable else "Blocked"


def line_class(a,b):
    if observed(a,b):
        return "Recorded"
    return "Marginal" if status(a,b).startswith("Marginal") else status(a,b)


KEPT_PAIRS={frozenset((a,b)) for a,b in combinations(SITES,2) if status(a,b)!="Blocked"}


def neighbors(site):
    order={"Strong":0,"Marginal":1,"Marginal · recorded":2,"Recorded":3,"Marginal · unverified":4}
    eligible=(k for k in SITES if frozenset((site,k)) in KEPT_PAIRS)
    return sorted(eligible,key=lambda k:(order[status(site,k)],dist(xy[site],xy[k])))


@lru_cache(None)
def view(site):
    with rasterio.open(OUT/"viewsheds"/(site+".tif")) as ds:
        return ds.read(1).astype(bool)


with rasterio.open(OUT/"viewsheds"/(LEE+".tif")) as sample:
    GEO=sample.transform
    SHAPE=sample.shape
    EXTENT=tuple(sample.bounds)
rows,cols=np.indices(SHAPE)
INSIDE=contains_xy(boundary,GEO.c+(cols+.5)*GEO.a,GEO.f+(rows+.5)*GEO.e)
AREA=abs(GEO.a*GEO.e)/1e6


def footprint(sites):
    return np.logical_or.reduce([view(k) for k in sites]) & INSIDE


def roadkm(mask):
    return weights[(groups=="Highway") & mask].sum()/1000


def charged_forwards(route, budget=3):
    """Charge each rebroadcast at the receiving relay. Lee is the destination."""
    charged = 0
    for i, site in enumerate(route[:-1]):
        if charged == budget:
            return None
        if i == 0 or site not in ROUTERS or route[i-1] not in ROUTERS:
            charged += 1
    return charged


def favorite_routes():
    network = nx.Graph()
    network.add_nodes_from(SITES)
    for a,b in combinations(SITES,2):
        if rating(a,b) != "Blocked" or observed(a,b):
            network.add_edge(a,b)
    routes = {LEE: ([LEE], 0)}
    for site in SITES:
        if site == LEE:
            continue
        choices = []
        for route in nx.all_simple_paths(network,site,LEE):
            cost = charged_forwards(route)
            if cost is not None:
                historical = sum(observed(a,b) for a,b in zip(route,route[1:]))
                choices.append((cost,historical,len(route),route))
        if choices:
            cost,_,_,route = min(choices)
            routes[site] = (route,cost)
    return routes


ROUTES = favorite_routes()
