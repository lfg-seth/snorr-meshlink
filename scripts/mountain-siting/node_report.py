"""Assemble the dated node report and a private offline packet for the same roster."""
import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import pymupdf
from node_model import SITES, CODE, REGIONAL, KEPT_PAIRS, UP, MACK, OUT, REPORT, CACHE, lonlat, status
from node_drawing import H, psite, ppath, chapter_end
from node_chapters import chapter
from node_model import neighbors, footprint, SITE_INFO, VALLEY_CACHE, INSIDE
import numpy as np
import rasterio
from node_front import front

PDF=REPORT/"mount-charleston-favorite-router-study.pdf"


def assemble():
    result=pymupdf.open()
    annotations=[]
    for file in [CACHE/"front.pdf",*[CACHE/"chapters"/(CODE[k]+".pdf") for k in SITES]]:
        with pymupdf.open(file) as section:result.insert_pdf(section)
        annotations+=json.loads(file.with_suffix(".json").read_bytes())
    assert len(result)==len(annotations)==chapter_end(SITES[-1])
    toc=[[1,"Mount Charleston repeater field study",1],[2,"All study nodes",2],[2,"Combined mountain viewshed",3],
         [2,"Potential direct links",4],[2,"Table of contents",5],[2,"Node directory",6],
         [1,"Las Vegas Valley | Fixed outdoor receivers at 4 m",7]]
    toc += [[2,k,i] for i,k in enumerate(REGIONAL,7)]
    for k in SITES:
        toc.extend([[1,k,psite(k)],[2,"Single-site viewshed",psite(k)+1]])
        toc.extend([2,f"{k} → {b}",ppath(k,b)] for b in neighbors(k))
    result.set_toc(toc)
    for i,page_links in enumerate(annotations):
        p=result[i]
        if i:
            p.insert_text((327,H-19),"USGS 3DEP terrain   /   © OpenStreetMap contributors",fontname="helv",fontsize=7.0,color=(.32,.40,.41))
        for x,y,w,h,number in page_links:
            p.insert_link({"kind":pymupdf.LINK_GOTO,"from":pymupdf.Rect(x,H-y-h,x+w,H-y),"page":number-1})
    result.set_metadata({"title":"Mount Charleston repeater field study | Favorite-router edition",
                         "author":"Codex for SNORR MeshLink","subject":f"{len(SITES)} sites, {2*len(KEPT_PAIRS)} directional profiles and {len(REGIONAL)} Las Vegas Valley viewsheds",
                         "creationDate":"D:20261118080000-08'00'"})
    temp=PDF.with_suffix(".building.pdf")
    result.save(temp,garbage=4,deflate=True,use_objstms=1);result.close();temp.replace(PDF)
    print(f"Assembled {PDF} ({PDF.stat().st_size:,} bytes)",flush=True)


def packet():
    # Reuse the original high-resolution offline map engine; supply only this report's sites and pairs.
    source=(OUT/"radio-paths.html").read_text(encoding="utf8")
    match=re.search(r"^const db=(.*);$",source,re.M)
    data=json.loads(match[1])
    for key in ("views","points"):data[key]={k:data[key][k] for k in SITES}
    data["paths"]=[dict(v,fieldClass=status(v["a"],v["b"])) for v in data["paths"]
                   if frozenset((v["a"],v["b"])) in KEPT_PAIRS]
    data["start"]=[MACK,UP]
    assert len(data["paths"])==len(KEPT_PAIRS)
    template=Path(__file__).with_name("viewer.html").read_text(encoding="utf8")
    viewer=template.replace("PAYLOAD_HERE",json.dumps(data,separators=(",",":")))
    (REPORT/"radio-paths.html").write_text(viewer,encoding="utf8")
    gpx=ET.Element("gpx",xmlns="http://www.topografix.com/GPX/1/1",version="1.1",creator="SNORR MeshLink")
    kml=ET.Element("kml",xmlns="http://www.opengis.net/kml/2.2");doc=ET.SubElement(kml,"Document")
    ET.SubElement(doc,"name").text="Mount Charleston • Favorite-router edition"
    for k in SITES:
        lat,lon=lonlat(k)
        role,purpose,*_=SITE_INFO[k]
        details=f"{role}. {purpose}."
        wp=ET.SubElement(gpx,"wpt",lat=f"{lat:.8f}",lon=f"{lon:.8f}")
        ET.SubElement(wp,"name").text=k
        ET.SubElement(wp,"desc").text=details
        place=ET.SubElement(doc,"Placemark")
        ET.SubElement(place,"name").text=k
        ET.SubElement(place,"description").text=details
        pt=ET.SubElement(place,"Point")
        ET.SubElement(pt,"coordinates").text=f"{lon:.8f},{lat:.8f},0"
    for name,root in (("gpx",gpx),("kml",kml)):
        ET.ElementTree(root).write(REPORT/("node-waypoints."+name),encoding="utf-8",xml_declaration=True)
    union=REPORT/"combined-mountain-viewshed.tif"
    with rasterio.open(OUT/"viewsheds"/(UP+".tif")) as sample:
        meta=sample.profile.copy()
    meta.update(dtype="uint8",nodata=255,compress="deflate")
    with rasterio.open(union,"w",**meta) as out:
        out.write(np.where(INSIDE,footprint(SITES),255).astype("uint8"),1)
        out.set_band_description(1,"Member at 1.2 m visible to any study site (1 visible, 0 shadow)")
    files={p.name:p for p in (PDF,REPORT/"radio-paths.html",REPORT/"node-waypoints.kml",REPORT/"node-waypoints.gpx")}
    files["mountain-viewsheds/"+union.name]=union
    files.update({"mountain-viewsheds/"+k+".tif":OUT/"viewsheds"/(k+".tif") for k in SITES})
    files.update({"valley-viewsheds/"+k+".tif":VALLEY_CACHE/(k+"-valley.tif") for k in REGIONAL})
    dest=REPORT/"favorite-router-field-packet.zip";temp=dest.with_suffix(".building.zip")
    with zipfile.ZipFile(temp,"w",zipfile.ZIP_DEFLATED) as ar:
        for name,path in files.items():ar.write(path,name)
    with zipfile.ZipFile(temp) as ar:
        assert ar.testzip() is None and set(ar.namelist())==set(files)
        for name,path in files.items():assert ar.read(name)==path.read_bytes(),name
    temp.replace(dest)
    print(f"Verified {len(files)} files in {dest}",flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assemble",action="store_true",help="Use already rendered chapters and front matter")
    parser.add_argument("--packet",action="store_true",help="Build the offline field packet after PDF assembly")
    args=parser.parse_args()
    if not args.assemble:
        front()
        for site in SITES:chapter(site)
    assemble()
    if args.packet:packet()
