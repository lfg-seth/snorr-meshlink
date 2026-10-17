#!/usr/bin/env python3
"""Provision repository tracking metadata; never touch application deployments."""

import argparse
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


CONFIG = Path(__file__).resolve().parents[2] / ".github" / "tracking.json"
REPOSITORY = "lfg-seth/snorr-meshlink"


def read_config():
    config = json.loads(CONFIG.read_text())
    labels = config["labels"]
    milestones = config["milestones"]
    assert labels and milestones, "Labels and milestones must be nonempty"
    assert len({item["name"] for item in labels}) == len(labels), "Duplicate label"
    assert len({item["title"] for item in milestones}) == len(milestones), "Duplicate milestone"
    for label in labels:
        assert re.fullmatch(r"[0-9a-fA-F]{6}", label["color"]), "Invalid label color"
        assert 0 < len(label["name"]) <= 50, "Invalid label name"
        assert len(label["description"]) <= 100, "Label description too long"
    titles = {item["title"] for item in milestones}
    for number, title in config["initial_issue_milestones"].items():
        assert number.isdecimal() and int(number) > 0, "Invalid issue number"
        assert title in titles, "Unknown milestone"
    return config


def apply(config):
    assert os.environ.get("GITHUB_REPOSITORY") == REPOSITORY, "Unexpected repository"
    token = os.environ["GITHUB_TOKEN"]
    root = f"https://api.github.com/repos/{REPOSITORY}"

    def request(method, path, data=None):
        payload = None if data is None else json.dumps(data).encode()
        req = Request(
            root + path,
            data=payload,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "snorr-tracking-bootstrap",
            },
        )
        try:
            with urlopen(req, timeout=30) as response:
                return json.load(response)
        except HTTPError as exc:
            # Report endpoint and status only; do not dump responses or credentials.
            raise RuntimeError(f"GitHub {method} {path}: HTTP {exc.code}") from None

    def collection(path):
        items = []
        page = 1
        while True:
            separator = "&" if "?" in path else "?"
            batch = request("GET", f"{path}{separator}per_page=100&page={page}")
            items.extend(batch)
            if len(batch) < 100:
                return items
            page += 1

    existing = {item["name"]: item for item in collection("/labels")}
    for label in config["labels"]:
        previous = existing.get(label["name"])
        if previous is None:
            request("POST", "/labels", label)
        elif any(str(previous.get(key) or "").lower() != str(label[key]).lower()
                 for key in ("color", "description")):
            request("PATCH", "/labels/" + quote(label["name"], safe=""), label)
    print(f"Labels verified: {len(config['labels'])}")

    existing = {item["title"]: item for item in collection("/milestones?state=all")}
    numbers = {}
    for milestone in config["milestones"]:
        previous = existing.get(milestone["title"])
        if previous is None:
            previous = request("POST", "/milestones", milestone)
        # Preserve owner-edited descriptions, dates and closed states on reruns.
        numbers[milestone["title"]] = previous["number"]
        print(f"Milestone {previous['number']}: {previous['title']}")

    for number, title in config["initial_issue_milestones"].items():
        issue = request("GET", f"/issues/{number}")
        if issue.get("milestone") is None:
            request("PATCH", f"/issues/{number}", {"milestone": numbers[title]})
            print(f"Initial milestone assigned: issue {number}")
        else:
            print(f"Existing milestone preserved: issue {number}")
    print("Tracking bootstrap complete; issue status and application services unchanged.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply through GitHub API")
    args = parser.parse_args()
    configuration = read_config()
    print("Tracking configuration valid.")
    if args.apply:
        apply(configuration)
