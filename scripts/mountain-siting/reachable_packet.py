"""Write field navigation and valley evidence; package only the current revision's deliverables."""
import argparse
import posixpath
import re
import zipfile
from survey import *
from reachable_search import ANGEL, ESC, LEE, MACK, SHOW, VEGAS


def navigation():
    namespace="http://www.opengis.net/kml/2.2"
    root=ET.Element("kml",xmlns=namespace)
    doc=ET.SubElement(root,"Document")
    ET.SubElement(doc,"name").text="Mount Charleston | reachable repeater survey"
    descriptions=search["descriptions"]
    folders={}
    for title,color in [("First outing and controls","ff5e7717"),("Other supplied points","ffc16f17"),
                        ("Lee, Showgirl and Escarpment survey offsets","ff267cb3"),
                        ("Angel road scouts - access unconfirmed","ff91249e")]:
        style=ET.SubElement(doc,"Style",id=f"group{len(folders)}")
        icon=ET.SubElement(style,"IconStyle")
        ET.SubElement(icon,"color").text=color
        folder=ET.SubElement(doc,"Folder")
        ET.SubElement(folder,"name").text=title
        folders[title]=folder
    primary=[MACK,"Lee Fire","Upper Bristlecone","Angel Mountain","Angel Vegas",VEGAS,LEE]
    evidence={MACK:"First trial. Test Upper Bristlecone and Angel Mountain in both directions.",
              VEGAS:"Compare Mack's, Shady's offline receiver and a fixed valley receiver against deployed R005.",
              ESC:"Supplied pin on the mapped footway. Compare the nearby survey point against Kyle and Shady.",
              SHOW:"Owner's legacy location. Test Angel Mountain before moving within the circle."}
    for k in search["display"]:
        group=(0 if k in primary else 1 if k in search["source_pins"] else
               3 if k in search["families"][ANGEL] else 2)
        pm=ET.SubElement(list(folders.values())[group],"Placemark")
        ET.SubElement(pm,"name").text=k
        source="Owner-supplied pin." if k in search["source_pins"] else "Model-generated survey point."
        ET.SubElement(pm,"description").text=" ".join([source,descriptions[k],evidence.get(k,"")]).strip()
        ET.SubElement(pm,"styleUrl").text=f"#group{group}"
        lat,lon=lonlat(k)
        point=ET.SubElement(pm,"Point")
        ET.SubElement(point,"altitudeMode").text="clampToGround"
        ET.SubElement(point,"coordinates").text=f"{lon:.8f},{lat:.8f},0"
    limits=ET.SubElement(doc,"Folder")
    ET.SubElement(limits,"name").text="Survey areas and mapped Escarpment footway"
    trail=next(g for g,p in features if p.get("osm_id")==search["trail_id"])
    for name,line in [(LEE+" - 20 m circle",Point(xy[LEE]).buffer(20).exterior),
                      (SHOW+" - 100 m circle",Point(xy[SHOW]).buffer(100).exterior),
                      ("Mapped footway used for Escarpment search",trail)]:
        pm=ET.SubElement(limits,"Placemark")
        ET.SubElement(pm,"name").text=name
        shape=ET.SubElement(pm,"LineString")
        ET.SubElement(shape,"tessellate").text="1"
        ET.SubElement(shape,"coordinates").text=" ".join(
            f"{lon:.8f},{lat:.8f},0" for lon,lat in (inverse.transform(x,y) for x,y in line.coords))
    ET.indent(root)
    ET.ElementTree(root).write(OUT/"survey-waypoints.kml",encoding="utf-8",xml_declaration=True)
    write_csv("angel-valley.csv",["Angel site","sector","clear rays","probes","receiver height m"],
              ([k,sector,hits,9,4] for k,values in search["valley"].items()
               for sector,hits in zip(search["sectors"],values)))


def pack():
    # The packet travels independently of the repository. Keep field artifacts local
    # and give the brief's background references portable repository URLs.
    source=Path(__file__).resolve().parents[2]/"docs/research/mountain-siting-reachable-20261117.md"
    def repo_link(match):
        target=posixpath.normpath(posixpath.join("docs/research",match.group(1)))
        return "](https://github.com/lfg-seth/snorr-meshlink/blob/codex/mountain-siting-nov17/"+target+")"
    brief=re.sub(r"\]\((?!https?://)([^)]+)\)",repo_link,source.read_text(encoding="utf8"))
    title,body=brief.split("\n",1)
    field_files="[Field atlas](mountain-field-atlas.pdf) · [Angel Peak map](angel-peak-map.png) · [Escarpment trail map](escarpment-trail-map.png) · [Adjustable paths](radio-paths.html) · [Google Earth waypoints](survey-waypoints.kml) · [GPX](survey-waypoints.gpx)"
    (OUT/"study-brief.md").write_text(title+"\n\n"+field_files+"\n"+body,encoding="utf8")
    names=["mountain-field-atlas.pdf","angel-peak-map.png","escarpment-trail-map.png",
           "radio-paths.html","survey-waypoints.kml","survey-waypoints.gpx",
           "study-brief.md","owner-waypoints.kml","angel-valley.csv","candidates.csv","height-sweep.csv",
           "highway-gaps.csv","member-probes.csv","mount-offsets.csv","pair-overlap.csv","station-routes.csv",
           "search-screen.csv","layouts.json"]
    names += [f"viewsheds/{label(k)}.tif" for k in search["display"]]
    destination=OUT/"field-packet.zip"
    with zipfile.ZipFile(destination.with_suffix(".zip.tmp"),"w",zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(OUT/name,name)
    with zipfile.ZipFile(destination.with_suffix(".zip.tmp")) as archive:
        assert archive.testzip() is None and archive.namelist()==names
        for name in names:
            assert archive.read(name)==(OUT/name).read_bytes(),name
    destination.with_suffix(".zip.tmp").replace(destination)
    print(f"Verified {len(names)} field packet files")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip",action="store_true",help="Include the study brief and verified atlas in the packet")
    args=parser.parse_args()
    navigation()
    if args.zip:
        pack()
