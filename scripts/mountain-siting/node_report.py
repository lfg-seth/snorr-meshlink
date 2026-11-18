"""Assemble the dated node report and a private offline packet for the same roster."""
import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import pymupdf
from node_model import SITES, CODE, REGIONAL, UP, MACK, OUT, REPORT, CACHE, lonlat
from node_drawing import H, psite, ppath
from node_chapters import chapter
from node_model import neighbors
from node_front import front

PDF=REPORT/"mount-charleston-node-report.pdf"


def assemble():
    result=pymupdf.open()
    annotations=[]
    for file in [CACHE/"front.pdf",*[CACHE/"chapters"/(CODE[k]+".pdf") for k in SITES]]:
        with pymupdf.open(file) as section:result.insert_pdf(section)
        annotations+=json.loads(file.with_suffix(".json").read_bytes())
    assert len(result)==len(annotations)==196
    toc=[[1,"Mount Charleston repeater study",1],[2,"All study nodes",2],[2,"Potential direct links",3],
         [2,"Table of contents",4],[2,"Node directory",5],[1,"Executive summary",6],
         [2,"Deployed and shortlist coverage",7],[2,"Shady forwarding trial",8],[2,"Scout scenarios",9],
         [1,"Las Vegas Valley | Fixed outdoor receivers at 4 m",10]]
    toc += [[2,k,i] for i,k in enumerate(REGIONAL,10)]
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
    result.set_metadata({"title":"Mount Charleston repeater study | Node coverage and direct radio paths",
                         "author":"Codex for SNORR MeshLink","subject":"13 sites, 156 directional profiles and five Las Vegas Valley viewsheds",
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
    data["paths"]=[v for v in data["paths"] if v["a"] in SITES and v["b"] in SITES]
    data["start"]=[MACK,UP]
    assert len(data["paths"])==78
    viewer=source[:match.start(1)]+json.dumps(data,separators=(",",":"))+source[match.end(1):]
    (REPORT/"radio-paths.html").write_text(viewer,encoding="utf8")
    gpx=ET.parse(OUT/"survey-waypoints.gpx").getroot()
    for element in list(gpx):
        if element.findtext("{*}name") not in SITES:gpx.remove(element)
    ET.ElementTree(gpx).write(REPORT/"node-waypoints.gpx",encoding="utf-8",xml_declaration=True)
    kml=ET.Element("kml",xmlns="http://www.opengis.net/kml/2.2");doc=ET.SubElement(kml,"Document")
    ET.SubElement(doc,"name").text="Mount Charleston • 13 study nodes"
    for k in SITES:
        p=ET.SubElement(doc,"Placemark");ET.SubElement(p,"name").text=k
        pt=ET.SubElement(p,"Point");lat,lon=lonlat(k);ET.SubElement(pt,"coordinates").text=f"{lon:.8f},{lat:.8f},0"
    ET.ElementTree(kml).write(REPORT/"node-waypoints.kml",encoding="utf-8",xml_declaration=True)
    files={p.name:p for p in (PDF,REPORT/"radio-paths.html",REPORT/"node-waypoints.kml",REPORT/"node-waypoints.gpx")}
    files.update({"mountain-viewsheds/"+k+".tif":OUT/"viewsheds"/(k+".tif") for k in SITES})
    files.update({"valley-viewsheds/"+k+".tif":CACHE/(k+"-valley.tif") for k in REGIONAL})
    dest=REPORT/"node-field-packet.zip";temp=dest.with_suffix(".building.zip")
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
