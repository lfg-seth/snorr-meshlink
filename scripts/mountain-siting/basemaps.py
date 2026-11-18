"""Download, validate and cache projected USGS basemaps used by the offline field packet."""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import json

CACHE = Path("private/winter-siting/cache/mountain-basemaps")
TOPO = "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/export"
NAIP = "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage"
MOUNTAIN = (614000, 4010000, 634000, 4028000)
RESORT = (618040, 4018110, 619480, 4020400)
MAPS = {
    "regional": (MOUNTAIN, (1000, 900)),
    "detail": (MOUNTAIN, (2500, 2250)),
    "resort": (RESORT, (720, 1145)),
    "junction": ((618900,4021000,622500,4024600),(1800,1800)),
    "aerial": (RESORT, (1440, 2290)),
}

def fetch(name):
    bounds, size = MAPS[name]
    params = dict(bbox=",".join(map(str,bounds)), bboxSR=26911, imageSR=26911,
                  size=",".join(map(str,size)), format="png32", transparent="false", f="image")
    service = TOPO
    if name == "aerial":
        service = NAIP
        params.update(format="jpg", bandIds="0,1,2", mosaicRule=json.dumps(
            {"mosaicMethod":"esriMosaicLockRaster","lockRasterIds":[134752]}))
    path = CACHE / (name + (".jpg" if name == "aerial" else ".png"))
    if not path.exists():
        with urlopen(service + "?" + urlencode(params), timeout=90) as response:
            image = Image.open(BytesIO(response.read())).convert("RGB")
        if image.size != size or max(hi-lo for lo,hi in image.getextrema())<90:
            raise ValueError("Unexpected USGS raster for " + name)
        CACHE.mkdir(parents=True, exist_ok=True)
        if name == "aerial":
            image.save(path, quality=95)
        else:
            image.save(path)
    return path

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(fetch, MAPS):
            print(result)
