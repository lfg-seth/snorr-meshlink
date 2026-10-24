#!/usr/bin/env python3
"""Assign stable, labelled Las Vegas map placeholders to unlocated infrastructure."""

import copy
import math
import random

SOURCE = "random-las-vegas-placeholder"
LABEL = "Random Las Vegas map placement"
BOUNDS = {"latitude": (36.155, 36.190), "longitude": (-115.170, -115.120)}


def valid_coordinate(value, limit):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and abs(value) <= limit
    )


def has_location(configuration):
    return valid_coordinate(configuration.get("latitude"), 90) and valid_coordinate(
        configuration.get("longitude"), 180
    )


def place_missing(device, rng=None):
    """Return a new device; preserve member locations and all existing valid pairs."""
    result = copy.deepcopy(device)
    configuration = result.get("configuration") or {}
    if result.get("kind") not in ("repeater", "backhaul") or has_location(configuration):
        return result
    rng = rng or random.SystemRandom()
    configuration = copy.deepcopy(configuration)
    for field, (lower, upper) in BOUNDS.items():
        configuration[field] = round(rng.uniform(lower, upper), 6)
    original = configuration.get("name") or result.get("number") or result["key"]
    configuration.update(
        locationSource=SOURCE,
        locationLabel=LABEL + " · not a measured location",
        locationOriginalName=original,
        name=original + " · " + LABEL,
    )
    result["configuration"] = configuration
    return result
