#!/usr/bin/env python3
"""Run selected local checks; default to changed documentation only."""

import argparse
from collections import Counter
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"\n]*")?\)')


def prose(markdown):
    """Exclude fenced examples; preserve original line numbers for errors."""
    fence = None
    for line in markdown.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            yield ""
        else:
            yield line if fence is None else ""


def heading_ids(markdown):
    counts = Counter()
    ids = set()
    for line in prose(markdown):
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        label = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", match[1])
        slug = re.sub(r"[^\w\- ]", "", label.lower()).replace(" ", "-")
        count = counts[slug]
        counts[slug] += 1
        ids.add(f"{slug}-{count}" if count else slug)
    return ids


def link_errors(path):
    errors = []
    for number, line in enumerate(prose(path.read_text(encoding="utf-8")), 1):
        # Inline code examples are not rendered Markdown links.
        line = re.sub(r"(`+).*?\1", "", line)
        for match in LINK.finditer(line):
            target = match[1] or match[2]
            url = urlsplit(target)
            if url.scheme or url.netloc or target.startswith("/"):
                continue
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not destination.exists():
                errors.append(f"{path}:{number}: missing file: {target}")
            elif url.fragment and destination.suffix.lower() == ".md":
                if unquote(url.fragment) not in heading_ids(destination.read_text(encoding="utf-8")):
                    errors.append(f"{path}:{number}: missing heading: {target}")
    return errors


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8")


def changed_markdown(base):
    # Resolve a commit first so an invalid revision cannot become a path filter.
    commit = git("rev-parse", "--verify", f"{base}^{{commit}}").strip()
    changed = git("diff", "--name-only", "-z", "--diff-filter=ACMR", commit, "--")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z")
    names = set(changed.split("\0") + untracked.split("\0"))
    return sorted(ROOT / name for name in names if name.lower().endswith(".md"))


def check_docs(base):
    # Whitespace check covers tracked changes; links also include untracked docs.
    subprocess.run(["git", "diff", "--check", base, "--"], cwd=ROOT, check=True)
    paths = changed_markdown(base)
    errors = [error for path in paths for error in link_errors(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS docs: {len(paths)} changed/untracked Markdown files; whitespace and local inline links.", flush=True)
    return 0


def commands():
    return {
        "bench": [sys.executable, "-m", "unittest", "discover", "-s", "scripts/bench/tests", "-v"],
        "firmware-release": [sys.executable, "-m", "unittest", "discover", "-s", "firmware/bin", "-p", "test_*snorr_release.py", "-v"],
        "portal": [shutil.which("npm") or "npm", "--prefix", "portal", "run", "check"],
        "backend": [sys.executable, "backend/manage.py", "check"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scopes", nargs="*", help="docs, bench, firmware-release, portal, backend (default: docs)")
    parser.add_argument("--base", default="HEAD", help="Git comparison for docs, e.g. origin/main")
    parser.add_argument("--list", action="store_true", help="Describe scopes without running checks")
    args = parser.parse_args(argv)
    available = commands()
    scopes = list(dict.fromkeys(args.scopes or ["docs"]))
    if any(scope not in {"docs", *available} for scope in scopes):
        parser.error("Unknown scope; choose docs, bench, firmware-release, portal or backend")
    if args.base.startswith("-"):
        parser.error("--base must name a Git commit/ref")
    if args.list:
        print("docs: changed Markdown local links and git diff --check")
        for scope, command in available.items():
            print(f"{scope}: {subprocess.list2cmdline(command)}")
        return 0
    try:
        for scope in scopes:
            print(f"Checking {scope}...", flush=True)
            if scope == "docs":
                if check_docs(args.base):
                    return 1
            else:
                if scope == "firmware-release" and not (ROOT / "firmware/bin/test_verify_snorr_release.py").is_file():
                    raise FileNotFoundError("Initialize the pinned firmware submodule before firmware-release checks")
                subprocess.run(available[scope], cwd=ROOT, check=True)
                print(f"PASS {scope}: selected local suite completed.", flush=True)
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
