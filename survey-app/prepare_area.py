"""Build a private offline map from local OSM linework, AO polygon and USGS DEM."""

import argparse
import base64
import io
import json
import os
import shutil
import tempfile
from pathlib import Path


def build(boundary, roads, dem, out, budget_mib, size):
    import numpy as np
    import rasterio
    from PIL import Image
    from rasterio.transform import from_bounds
    from rasterio.warp import Resampling, reproject, transform_bounds
    from shapely.geometry import shape
    from shapely.ops import unary_union

    limit = budget_mib * 1024**2
    out.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(out).free < limit:
        raise ValueError("Insufficient free space for the selected map budget")
    area = unary_union(
        [shape(f["geometry"]) for f in json.loads(boundary.read_bytes())["features"]]
    )
    bounds = area.bounds
    if not (
        -180 <= bounds[0] < bounds[2] <= 180
        and -80 <= bounds[1] < bounds[3] <= 80
        and bounds[2] - bounds[0] <= 2
        and bounds[3] - bounds[1] <= 2
    ):
        raise ValueError("Use a local WGS84 AO under two degrees per axis")
    print(
        f"Bounds W/S/E/N {bounds}; display zooms 9–16; relief {size}px; maximum {budget_mib} MiB. Ctrl+C cancels.",
        flush=True,
    )
    lines = []
    features = json.loads(roads.read_bytes())["features"]
    estimate = min(limit, roads.stat().st_size + size * size * 4)
    print(
        f"Estimated upper working output {estimate:,} bytes. Clipping roads…",
        flush=True,
    )
    for i, feature in enumerate(features):
        p = feature["properties"]
        if not p.get("highway") or feature["geometry"]["type"] not in (
            "MultiLineString",
            "LineString",
        ):
            continue
        geom = shape(feature["geometry"]).intersection(area)
        for line in getattr(geom, "geoms", [geom]):
            if line.geom_type == "LineString" and not line.is_empty:
                pts = [
                    [round(x, 5), round(y, 5)]
                    for x, y, *_ in line.simplify(0.00002).coords
                ]
                lines.append([p.get("name", ""), p["highway"], pts])
        if i and i % 400 == 0:
            print(f"Read {i}/{len(features)} features", flush=True)
    print("Shading local elevation raster…", flush=True)
    extent = transform_bounds("EPSG:4326", "EPSG:3857", *bounds)
    width, height = extent[2] - extent[0], extent[3] - extent[1]
    w, h = (
        max(2, int(size * width / max(width, height))),
        max(2, int(size * height / max(width, height))),
    )
    grid = np.full((h, w), np.nan, np.float32)
    with rasterio.open(dem) as dataset:
        reproject(
            rasterio.band(dataset, 1),
            grid,
            dst_transform=from_bounds(*extent, w, h),
            dst_crs="EPSG:3857",
            dst_nodata=np.nan,
            resampling=Resampling.bilinear,
        )
    north, east = np.gradient(grid, height / h, width / w)
    shade = np.nan_to_num(np.clip(0.6 * north - 0.85 * east, -0.65, 0.65), nan=0)
    # Warm relief and subtle elevation contours, with explicit missing-raster background.
    bands = np.nan_to_num(grid, nan=0) % 100
    tint = np.where((bands < 2.8) & np.isfinite(grid), -6, 0)
    rgb = np.stack(
        [np.clip(base + shade * 55 + tint, 0, 255) for base in (222, 222, 197)], axis=-1
    ).astype("uint8")
    buf = io.BytesIO()
    Image.fromarray(rgb).save(buf, "JPEG", quality=86)
    package = {
        "version": 1,
        "bounds": bounds,
        "zoom": [9, 16],
        "roads": lines,
        "terrain": "data:image/jpeg;base64,"
        + base64.b64encode(buf.getvalue()).decode(),
        "attribution": "USGS 3DEP · © OpenStreetMap contributors, ODbL",
    }
    payload = json.dumps(package, separators=(",", ":"), allow_nan=False).encode()
    if len(payload) > limit:
        raise ValueError("Map exceeds byte budget. Reduce raster size or area.")
    name = None
    try:
        with tempfile.NamedTemporaryFile(dir=out, delete=False) as f:
            name = f.name
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, out / "area.json")
    finally:
        if name:
            Path(name).unlink(missing_ok=True)
    print(
        f"Ready: {len(lines)} road segments, {w}×{h} relief, {len(payload):,} bytes.",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("boundary", "roads", "dem", "out"):
        parser.add_argument("--" + key, required=True, type=Path)
    parser.add_argument(
        "--budget-mib", type=int, default=16, choices=range(1, 129), metavar="1..128"
    )
    parser.add_argument(
        "--size", type=int, default=1600, choices=range(256, 3073), metavar="256..3072"
    )
    args = parser.parse_args()
    build(**vars(args))
