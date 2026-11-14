"""Check station routing, scoped drive-up roads, navigation and the rendered packet."""
import argparse
from pathlib import Path
import json
import math
import xml.etree.ElementTree as ET
from study import configure


def verify(root):
    import networkx as nx
    import numpy as np
    import rasterio
    import pymupdf
    from PIL import Image,ImageDraw
    from terrain import forward
    from field_names import field_code, field_name, navigation_name
    from cartography import Maps
    r=json.loads((root/'tables/results.json').read_bytes())
    cfg=json.loads((root/'inputs/study.json').read_bytes())
    active=r['gateways']+r['selected']
    sites={v['id']:v for v in r['sites']}
    assert len(set(active))==11
    assert len({field_code(k) for k in sites})==len(sites)
    def data(name):
        with rasterio.open(root/'gis'/(name+'.tif')) as ds:
            assert ds.crs.to_epsg()==26911 and ds.nodata==255
            return ds.read(1)
    field=data('reachability');inside=field!=255
    footprints={k:data('viewshed-'+k)==1 for k in active}
    assert np.array_equal(data('terrain-union')==1,np.logical_or.reduce(list(footprints.values())))
    assert np.array_equal(data('relay-overlap')[inside],sum(footprints[k].astype('uint8') for k in r['selected'])[inside])
    graph=nx.Graph();graph.add_nodes_from(active)
    graph.add_edges_from((p['a'],p['b']) for p in r['pairs'] if p['active'] and p['los'])
    maps=Maps(root,r)
    station_masks=maps.station_masks(cfg['hop_limit'])
    assert set(np.unique(field))=={0,1,255}
    assert np.array_equal(np.logical_or.reduce(list(station_masks.values())),field==1)
    for station,mask in station_masks.items():
        g=graph.copy();g.remove_nodes_from(set(r['gateways'])-{station})
        nodes=nx.single_source_shortest_path_length(g,station,cutoff=cfg['hop_limit'])
        assert np.array_equal(mask,np.logical_or.reduce([footprints[k] for k in nodes]))
    from shapely.geometry import Point
    from shapely.ops import unary_union
    road=unary_union([g for g,n in maps.roads if n=='Angel Peak'])
    highway=unary_union([g for g,n in maps.roads if n=='SR 158'])
    assert road.distance(highway)<1
    pins=[Point(sites[k]['nx'],sites[k]['ny']) for k in cfg['angel_approach']['destinations']]
    assert all(road.distance(p)<50 for p in pins)
    assert road.bounds[2]<max(p.x for p in pins)+60
    segments=[(g,p['status']) for g,p in maps.status if p['name']=='Angel Peak']
    assert abs(sum(g.length for g,_ in segments)-road.length)<1
    percent=100*sum(g.length for g,cl in segments if cl=='reachable')/road.length
    assert abs(percent-r['scenarios']['Recommended']['Angel Peak'])<.01
    for name in ('Macks Canyon','Angel Peak'):
        gap=maps.longest_gap[name]
        if gap is None:
            assert not r['roads'][name]
            continue
        model=r['roads'][name][0]
        assert abs(gap.length/1000-model['km'])<.001
        for point,key in ((gap.coords[0],'a'),(gap.coords[-1],'b')):
            assert math.dist(point,forward.transform(*model[key]))<.02
    pin_data=json.loads((root/'gis/sites.geojson').read_bytes())['features']
    points={f['properties']['id']:f for f in pin_data if f['properties']['selected']}
    assert set(points)==set(active)
    nav=ET.parse(root/'navigation.gpx')
    ns={'g':'http://www.topografix.com/GPX/1/1'}
    waypoints={w.findtext('g:name',namespaces=ns):[float(w.get('lon')),float(w.get('lat'))] for w in nav.findall('g:wpt',ns)}
    extra=set(cfg['drive_up_sites'])-set(active)
    assert len(waypoints)==2*len(active)+len(extra)
    for k in cfg['drive_up_sites']:
        label=navigation_name(k)+(' - drive-up test' if k in extra else ' - stage')
        assert math.dist(waypoints[label],sites[k]['nom_ll'])<1e-6
    doc=pymupdf.open(root/'Mount-Charleston-winter-field-plan.pdf')
    pages=[p.get_text() for p in doc]
    assert len(doc.get_toc())==len(doc)
    assert 'Winter mesh field plan' in pages[0] and 'Deployment order' in pages[1]
    assert sum('Navigation and mounting' in p for p in pages)==len(active)
    for phrase in ('Where the roads reach dispatch','Which fire station gets the packet?',
                   'Where each repeater stands alone','Which repeater covers which slope?',
                   'Angel Peak to the Las Vegas valley',
                   'Kyle Canyon terrain profiles','Lee Canyon terrain profiles'):
        assert any(phrase in page for page in pages),phrase
    content=' '.join(pages).lower()
    for stale in ('single-node','outage','survives','lucky strike','where the named places sit'):
        assert stale not in content,stale
    for k in active:
        s=sites[k];lon,lat=s['ll'];coord=f'{lat:.5f}, {lon:.5f}'
        site_page=[p for p in pages if 'Navigation and mounting' in p and 'Selected WGS84' in p and coord in p and navigation_name(k) in p]
        assert len(site_page)==1,(k,'PDF sheet')
        stage=s['stop_ll'];assert f'{stage[1]:.5f}, {stage[0]:.5f}' in site_page[0]
        assert math.dist(forward.transform(*points[k]['geometry']['coordinates']),(s['x'],s['y']))<.01
        assert points[k]['properties']['field_code']==field_code(k) and points[k]['properties']['field_name']==field_name(k)
        assert math.dist(forward.transform(*waypoints[navigation_name(k)]),(s['x'],s['y']))<.03
        assert math.dist(waypoints[navigation_name(k)+' - stage'],stage)<1e-6
        assert round(s['shift'],1)<=20.1 and s['h']==(cfg['gateway_m'] if k in r['gateways'] else cfg['repeater_m'])
    render=root/'cache/render';render.mkdir(exist_ok=True)
    thumbs=[]
    for i,page in enumerate(doc):
        pix=page.get_pixmap(matrix=pymupdf.Matrix(1.4,1.4),alpha=False)
        im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        im.save(render/f'page-{i+1:02}.png')
        im.thumbnail((245,320));thumbs.append(im)
    for start in range(0,len(thumbs),8):
        sheet=Image.new('RGB',(1000,680),'#dce1df')
        for idx,im in enumerate(thumbs[start:start+8]):
            x=(idx%4)*250;y=(idx//4)*340
            sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+8,y+319),str(start+idx+1),fill='black')
        sheet.save(render/f'contact-{start//8+1}.png')
    print(f'{len(doc)} pages rendered. The 11 site sheets and {len(waypoints)} waypoints match the model. Both station masks and the scoped Angel Peak road pass independent checks.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    root=parser.parse_args().directory.resolve();configure(root);verify(root)
