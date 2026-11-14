"""Contiguous runs of scored road segments in the original centerline order."""
from math import dist
from shapely.geometry import LineString


def road_runs(samples, name, include):
    runs = []
    indices = []
    coords = []
    for index, (sample, selected) in enumerate(zip(samples, include)):
        relevant = selected and sample['kind'] == 'road' and sample['name'] == name
        segment = list(sample['segment'].coords) if relevant else []
        if coords and (not segment or dist(coords[-1], segment[0]) > .01):
            runs.append((LineString(coords), indices))
            coords, indices = [], []
        if segment:
            coords.extend(segment[1:] if coords else segment)
            indices.append(index)
    if coords:
        runs.append((LineString(coords), indices))
    return sorted(runs, key=lambda item: -item[0].length)
