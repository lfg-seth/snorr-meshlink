"""Check what the PDF actually shows against the independent georeferenced outputs."""
import unicodedata

import numpy as np
import rasterio
import pymupdf
from scipy.ndimage import binary_erosion
from shapely import contains_xy


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC",text).split())


def check_viewshed_pixels(page,expected_masks,inside):
    """Locate the map images on the printed page and sample their displayed colors."""
    images=page.get_image_info()
    rects=[]
    for im in sorted(images,key=lambda im:im["bbox"][0]):
        rect=np.array(im["bbox"])
        if rect[2]-rect[0]<120 or rect[3]-rect[1]<120:
            continue
        if not any(np.max(np.abs(rect-prev))<2 for prev in rects):
            rects.append(rect)
    assert len(rects)==len(expected_masks),(page.number+1,rects)
    pixels=page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False)
    image=np.frombuffer(pixels.samples,np.uint8).reshape(pixels.height,pixels.width,3).astype("int16")
    teal=(image[:,:,1]-image[:,:,0]>45) & (image[:,:,2]-image[:,:,0]>30)
    for rect,mask in zip(rects,expected_masks):
        left,top,right,bottom=rect*1.5
        for visible in [True,False]:
            chosen=binary_erosion(inside & (mask==visible))
            rr,cc=np.nonzero(chosen)
            assert len(rr)>0,(page.number+1,visible)
            stride=max(1,len(rr)//3000)
            y=(top+(rr[::stride]+.5)*(bottom-top)/mask.shape[0]).astype(int)
            x=(left+(cc[::stride]+.5)*(right-left)/mask.shape[1]).astype(int)
            agreement=np.mean(teal[y,x]==visible)
            assert agreement>.87,(page.number+1,visible,agreement)


def verify_coverage(atlas,folder,sites,layouts,boundary,primary):
    headings=atlas.get_toc()
    pages={title:atlas[number-1] for level,title,number in headings if level==2}
    assert len(atlas[0].get_links())==4
    assert all(dest["kind"]==1 and dest["page"]>0 for dest in atlas[0].get_links())
    results=[p for name,p in pages.items() if name.startswith("Reported layouts ")]
    case_text=normalized(" ".join(p.get_text() for p in results))
    metrics=("Highway","SR 156","SR 157","SR 158","Resort approach","Resort parking","Lodge / base","Trailheads","Other parking")
    for scenario,record in layouts.items():
        relay_count=len(set(record["layout"]) & set(record["reach"]))
        expected=[scenario.replace(";"," /"),f"{relay_count}/{len(record['layout'])}"]
        expected.extend(f"{record['scores'][metric]:.1f}" for metric in metrics)
        expected.extend(f"{record[group]['Highway']:.1f}" for group in ("robust","kyle"))
        assert normalized(" ".join(expected)) in case_text,scenario
    assert "Assumptions and field acceptance" in pages and "Where each radio fits" in pages
    masks={}
    for site in sites:
        with rasterio.open(folder/(site+".tif")) as ds:
            masks[site]=ds.read(1).astype(bool)
            transform=ds.transform
    rows,cols=np.indices(masks[sites[0]].shape)
    X=transform.c+(cols+.5)*transform.a
    Y=transform.f+(rows+.5)*transform.e
    inside=contains_xy(boundary,X,Y)
    pixel_area=abs(transform.a*transform.e)/1e6
    section=""
    mapped=[]
    for level,title,number in headings:
        if level==1:
            section=title
            continue
        if section!="Individual site viewsheds" or title=="Find a site viewshed":
            continue
        pair=title.split("  /  ")
        printed=normalized(atlas[number-1].get_text())
        for site in pair:
            area=np.count_nonzero(masks[site]&inside)*pixel_area
            assert normalized(f"{area:.2f} km² visible") in printed,(site,area)
        check_viewshed_pixels(atlas[number-1],[masks[k] for k in pair],inside)
        mapped.extend(pair)
    assert sorted(mapped)==sorted(sites)
    index=pages["Find a site viewshed"]
    assert sorted(link["page"] for link in index.get_links())==list(range(index.number+1,index.number+1+(len(sites)+1)//2))
    unions=[np.logical_or.reduce([masks[k] for k in layouts[scenario]["reach"]]) for scenario in ("Deployed",primary)]
    check_viewshed_pixels(pages["Where member GPS can reach Lee Fire"],unions,inside)
    assert "Angel Peak to northwest Las Vegas" in pages
    return len(mapped)
