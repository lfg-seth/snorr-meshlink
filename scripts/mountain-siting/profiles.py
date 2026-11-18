"""Write the self-contained path viewer and exact critical-link height sweep."""
import base64
from io import BytesIO
from PIL import Image
from basemaps import CACHE, MAPS
from survey import *
import rasterio

def build():
    sites=export()
    paths=[]
    sensitivity=[]
    for a,b in combinations(sites,2):
        d,z,line,f1=profile.trace(coords(a),coords(b))
        if not np.isfinite(z).all():
            raise ValueError((a,b))
        labela,labelb=label(a),label(b)
        t=d/d[-1]
        for ah in ([.5,1,2,4,6] if a.endswith("Fire") else [2,4,6,8]):
            for bh in ([.5,1,2,4,6] if b.endswith("Fire") else [2,4,6,8]):
                clear=(line-z+(ah-wh(a))*(1-t)+(bh-wh(b))*t)[1:-1]
                sensitivity.append([labela,labelb,ah,bh,round(clear.min(),3),round((clear/f1[1:-1]).min(),4)])
        q=np.rint((z-z.min())*100).astype("int32")
        raw=np.diff(q,prepend=q[0]).astype("<i2")
        assert np.array_equal(q,raw.astype("int32").cumsum()+q[0])
        paths.append(dict(a=labela,b=labelb,d=round(d[-1],3),z0=float(z.min()+q[0]/100),aH=wh(a),bH=wh(b),
                          data=base64.b64encode(raw.tobytes()).decode("ascii")))
    write_csv("height-sweep.csv",["site A","site B","A m AGL","B m AGL","minimum terrain clearance m","min first Fresnel fraction"],sensitivity)
    payload=dict(paths=paths,points={label(k):xy[k] for k in sites},roads=[list(line.simplify(25).coords) for line,_ in road_inventory],
                 start=[label("C16"),"Angel Mountain"])
    packed_views={}
    for k in sites:
        with rasterio.open(OUT/"viewsheds"/(label(k)+".tif")) as ds:
            data=ds.read(1)
            packed_views[label(k)]=base64.b64encode(np.packbits(data,bitorder="little").tobytes()).decode("ascii")
            raster=[ds.bounds.left,ds.bounds.top,ds.transform.a,ds.width,ds.height]
    payload.update(views=packed_views,raster=raster)
    payload["referenceLabels"]=reference_labels()
    payload["topo"]={}
    for name in ("regional","detail","junction"):
        with Image.open(CACHE/(name+".png")) as image:
            buf=BytesIO()
            image.convert("RGB").save(buf,"JPEG",quality=91,optimize=True)
            payload["topo"][name]=dict(bounds=MAPS[name][0],image=base64.b64encode(buf.getvalue()).decode("ascii"))
    template=Path(__file__).with_name("viewer.html").read_text(encoding="utf8")
    (OUT/"radio-paths.html").write_text(template.replace("PAYLOAD_HERE",json.dumps(payload,separators=(",",":"))),encoding="utf8")
if __name__=="__main__":
    build()
