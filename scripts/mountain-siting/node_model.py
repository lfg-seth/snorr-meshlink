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

from node_valley import CACHE, REPORT

UP="Upper Bristlecone"
LEE="Lee Fire"
MACK="Mack's alternative"
SHOW="Showgirl"
SHADY="Shady Hollow"
ESC="Escarpment trail"
CAT="Cathedral Rock"
ANGEL="Angel Vegas"
KYLE="Kyle Junction"
SCOUTS=[f"Angel road survey {i}" for i in (1,3,5,6)]
SITES=[UP,LEE,MACK,SHOW,SHADY,ESC,CAT,SCOUTS[2],ANGEL,KYLE,SCOUTS[0],SCOUTS[1],SCOUTS[3]]
CODE=dict(zip(SITES,("UB","LF","MA","SG","SH","ES","CR","A5","AV","KJ","A1","A3","A6")))
# November study records G002 direct packets and reciprocal neighbor reports. G002 is a passive recorder.
OBSERVED={frozenset((SHADY,k)) for k in (CAT,ANGEL,KYLE,"Angel Mountain")}
SITE_INFO={
    UP:("R010 · deployed repeater","Lee Canyon backbone","Upper is the western anchor for the proposed Mack’s link. The model connects it directly to Lee Fire.","Test reciprocal packet IDs from Mack’s, then match the member fix time at Lee Fire."),
    LEE:("G001 · gateway","Lee Fire uplink","This is the report’s only dispatch gateway. A member transmission can arrive directly or through up to three forwarders.","Confirm gateway power and uplink before a trial. Match tracker ID, fix time and gateway receipt time."),
    MACK:("Owner waypoint · proposed repeater","Bridge into Lee Canyon","This supplied pin can join the Angel-side sites to Upper Bristlecone. Direct terrain toward Lee Fire is obstructed.","Set the portable at the intended 4 m. Repeat the Upper link at 2 m to measure mount sensitivity."),
    SHOW:("Owner waypoint · former site","Southern mountain coverage","Use the supplied Showgirl pin. Its direct terrain ray to deployed Angel Vegas has limited Fresnel clearance.","Compare Angel Vegas and the Angel road scouts at equal antenna height. Record both directions."),
    SHADY:("G002 · offline recorder","Witness receiver and relay trial","The recovered SD record includes direct packets from Cathedral, Angel Vegas and Kyle Junction. G002 currently has forwarding disabled.","For the forwarding trial, use the same site and log the relay identity plus a matched GPS receipt at Lee."),
    ESC:("Owner waypoint · proposed repeater","Escarpment footway","The supplied pin sits beside the mapped footway. Its near neighbors include Shady and the Kyle side of the network.","Keep the portable at the supplied pin first. Compare the Angel and south-side links with the same antenna."),
    CAT:("R001 · deployed repeater","Cathedral Rock control","Cathedral is an installed south-side control. Shady’s recorder provides evidence of a direct radio reception.","Use numbered packets toward Shady and Escarpment. Verify a gateway receipt separately."),
    ANGEL:("R005 · deployed repeater","Valley-facing Angel control","This is the installed Vegas-side radio. It provides a fixed reference for each separate road-scout trial and was heard at Shady.","Keep R005 operating and compare a fixed valley receiver with each candidate during the same test window."),
    KYLE:("R008 · deployed repeater","Kyle Canyon control","Use the corrected Kyle Junction position. Shady recorded direct packets from this radio despite the terrain obstruction.","Compare the Shady and Escarpment paths from the installed antenna. Check member GPS delivery separately."),
    SCOUTS[0]:("Road scout · access unconfirmed","Showgirl and Escarpment option","Survey 1 cleared Showgirl and Escarpment in the native-terrain screen. Its valley footprint is compared with the other Angel sites.","Confirm access and stand location. Test both mountain links and compare the same fixed valley receiver."),
    SCOUTS[1]:("Road scout · access unconfirmed","Mack’s and valley option","Survey 3 clears Mack’s and offers a valley-facing position. Survey 2 was about 20 m away and duplicated that role in the earlier screen.","Confirm access, compare the Mack’s link with survey 5 and repeat the valley test at the same receiver."),
    SCOUTS[2]:("Road scout · access unconfirmed","Mountain-facing Angel option","Survey 5 clears Mack’s, Showgirl and the supplied Escarpment pin. Its whole-valley page shows the trade-off at a fixed 4 m receiver.","Confirm access. Favor the Mack’s and Escarpment tests and keep deployed Angel Vegas as the control."),
    SCOUTS[3]:("Road scout · access unconfirmed","Mack’s and survey 5 link option","Survey 6 clears Mack’s and survey 5 at the 60% Fresnel threshold. The network comparisons place one scout at a time.","Confirm access and test Mack’s first. A separate portable can test the inter-scout path without assuming two installations."),
}
BASE_LINKS=[frozenset((a,b)) for a,b in combinations(SITES,2)]
REGIONAL=[ANGEL,SCOUTS[0],SCOUTS[1],SCOUTS[2],SCOUTS[3]]
ROLE_RELAY=[UP,MACK,SHOW,ESC,CAT,ANGEL,KYLE]
COLORS={"Strong":"#08776F","Marginal":"#A36406","Blocked":"#68757B","Recorded":"#973B72"}


def observed(a,b):
    return frozenset((a,b)) in OBSERVED


def rating(a,b):
    v=graph[a][b]
    return "Blocked" if v["clear"]<0 else "Strong" if v["f1"]>=.6 else "Marginal"


def neighbors(site):
    order={"Strong":0,"Marginal":1,"Recorded":2,"Blocked":3}
    def sort(k):
        rank="Recorded" if observed(site,k) and rating(site,k)=="Blocked" else rating(site,k)
        return order[rank],dist(xy[site],xy[k])
    return sorted((k for k in SITES if k!=site),key=sort)


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


def radio_network(relays,allow_recorded=False):
    selected=[LEE,*relays]
    g=nx.Graph()
    g.add_nodes_from(selected)
    for a,b in combinations(selected,2):
        if rating(a,b)!="Blocked" or (allow_recorded and observed(a,b)):
            g.add_edge(a,b)
    routes=nx.single_source_shortest_path(g,LEE,cutoff=3)
    serving=list(routes)
    targets=masks[[ix[s] for s in serving]].any(axis=0)
    footprint_mask=footprint(serving)
    scores={}
    for n in ["Highway","SR 156","SR 157","SR 158"]:
        take=(groups=="Highway") if n=="Highway" else (groups=="Highway")&(names==n)
        scores[n]=100*weights[take&targets].sum()/weights[take].sum()
    return dict(relays=relays,routes=routes,zone=footprint_mask,area=footprint_mask.sum()*AREA,
                km=roadkm(targets),scores=scores)


DEPLOYED=radio_network(baseline)
CASES={s:radio_network([*ROLE_RELAY,s]) for s in SCOUTS}
TRIALS={s:radio_network([*ROLE_RELAY,s,SHADY],True) for s in SCOUTS}
