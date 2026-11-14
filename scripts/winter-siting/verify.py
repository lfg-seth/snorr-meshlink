"""Independent graph/outage, GIS, navigation and rendered field-sheet consistency checks."""
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
    assert len(set(active))==11 and len(r['failures'])==11
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
    survived=inside.copy()
    def independently_reachable(failed):
        g=graph.copy()
        if failed:g.remove_node(failed)
        connected=set()
        for target in r['gateways']:
            if target in g:
                # Stop at the other sink; do not forward through it.
                gg=g.copy();gg.remove_nodes_from(set(r['gateways'])-{target})
                connected.update(nx.single_source_shortest_path_length(gg,target,cutoff=cfg['hop_limit']))
        assert failed not in connected
        return np.logical_or.reduce([footprints[k] for k in connected])
    intact=independently_reachable(None)
    for k in active:
        m=independently_reachable(k)
        assert np.array_equal(intact & ~m,data('loss-'+k)==1)
        survived &= m
    assert np.array_equal(intact,inside & (field>=1)) and np.array_equal(survived,field==2)
    maps=Maps(root,r)
    station_masks=maps.station_masks(cfg['hop_limit'])
    assert np.array_equal(np.logical_or.reduce(list(station_masks.values())),intact)
    for station,mask in station_masks.items():
        other,=set(r['gateways'])-{station}
        assert np.array_equal(mask,independently_reachable(other))
    for name in ('Macks Canyon','Lucky Strike'):
        gap=maps.longest_gap[name]
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
    assert len(waypoints)==22
    doc=pymupdf.open(root/'Mount-Charleston-winter-mesh.pdf')
    pages=[p.get_text() for p in doc]
    assert len(doc.get_toc())==len(doc)
    assert 'Winter mesh field plan' in pages[0] and 'Deployment order' in pages[1]
    assert sum('Navigation and mounting' in p for p in pages)==len(active)
    for phrase in ('Two road gaps to drive first','Which fire station gets the packet?',
                   'Where each repeater stands alone','Which repeater covers which slope?',
                   'Where the named places sit','Where a single failure cuts service',
                   'Kyle Canyon terrain profiles','Lee Canyon terrain profiles'):
        assert any(phrase in page for page in pages),phrase
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
    print(f'{len(doc)} pages rendered; 11 site sheets and all 22 GPX waypoints match GIS. Eleven independent network removals match every raster cell.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    root=parser.parse_args().directory.resolve();configure(root);verify(root)
