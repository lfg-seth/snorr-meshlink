#!/usr/bin/env python3
"""Check or synchronize the GitHub Project from issue status labels."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import time


CONFIG = Path(__file__).resolve().parents[2] / ".github" / "project.json"


def gh_json(*args, payload=None):
    executable = shutil.which("gh")
    if executable is None:
        raise RuntimeError("Install GitHub CLI and authorize it with the project scope.")
    command = [executable, *args]
    if payload is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(
        command,
        input=None if payload is None else json.dumps(payload),
        text=True,
        capture_output=True,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "GitHub CLI request failed")
    value = json.loads(result.stdout)
    if isinstance(value, dict) and value.get("errors"):
        raise RuntimeError("GitHub GraphQL request failed: " + str(value["errors"]))
    return value


def graphql(query, **variables):
    return gh_json("api", "graphql", payload={"query": query, "variables": variables})["data"]


def desired_status(issue, config):
    if issue["state"] == "closed":
        return config["closed_status"]
    statuses = [label["name"] for label in issue["labels"] if label["name"].startswith("status:")]
    if len(statuses) != 1 or statuses[0] not in config["status_labels"]:
        raise ValueError(f"Issue #{issue['number']} needs exactly one recognized status label.")
    return config["status_labels"][statuses[0]]


def project_items(config):
    query = """query($id:ID!, $after:String) {
      node(id:$id) { ... on ProjectV2 {
        items(first:100, after:$after) {
          pageInfo { hasNextPage endCursor }
          nodes { id
            fieldValueByName(name:"Status") {
              ... on ProjectV2ItemFieldSingleSelectValue { name }
            }
            content { ... on Issue { id repository { nameWithOwner } } }
          }
        }
      } }
    }"""
    result = {}
    cursor = None
    while True:
        page = graphql(query, id=config["id"], after=cursor)["node"]["items"]
        for item in page["nodes"]:
            content = item.get("content") or {}
            if content.get("repository", {}).get("nameWithOwner") == config["repository"]:
                result[content["id"]] = item
        if not page["pageInfo"]["hasNextPage"]:
            return result
        cursor = page["pageInfo"]["endCursor"]


def main(apply):
    config = json.loads(CONFIG.read_text())
    pages = gh_json(
        "api", f"repos/{config['repository']}/issues?state=all&per_page=100",
        "--paginate", "--slurp",
    )
    issues = [item for page in pages for item in page if "pull_request" not in item]
    # Validate every status before making any write; holds remain authoritative.
    desired = [(issue, desired_status(issue, config)) for issue in issues]
    project = graphql("""query($id:ID!) {
      node(id:$id) { ... on ProjectV2 {
        id title fields(first:100) { nodes {
          ... on ProjectV2SingleSelectField { id name options { id name } }
        } }
      } }
    }""", id=config["id"])["node"]
    field = next(f for f in project["fields"]["nodes"] if f.get("id") == config["status_field_id"])
    assert field["name"] == "Status", "Configured field is not Status"
    options = {option["name"]: option["id"] for option in field["options"]}
    for _, status in desired:
        if status not in options:
            raise ValueError(f"Project is missing the {status} status option.")

    items = project_items(config)
    changes = 0
    for issue, status in sorted(desired, key=lambda pair: pair[0]["number"]):
        item = items.get(issue["node_id"])
        current = (item.get("fieldValueByName") or {}).get("name") if item else None
        if item and current == status:
            continue
        changes += 1
        print(f"#{issue['number']}: {current or 'not on board'} -> {status}", flush=True)
        if not apply:
            continue
        if item is None:
            item = graphql("""mutation($input:AddProjectV2ItemByIdInput!) {
              addProjectV2ItemById(input:$input) { item { id } }
            }""", input={"projectId": config["id"], "contentId": issue["node_id"]})["addProjectV2ItemById"]["item"]
        graphql("""mutation($input:UpdateProjectV2ItemFieldValueInput!) {
          updateProjectV2ItemFieldValue(input:$input) { projectV2Item { id } }
        }""", input={
            "projectId": config["id"], "itemId": item["id"], "fieldId": field["id"],
            "value": {"singleSelectOptionId": options[status]},
        })

    if apply and changes:
        # Project reads can lag a successful mutation; retry reads, never writes.
        mismatches = []
        for delay in (0, 1, 2, 3, 4):
            if delay:
                time.sleep(delay)
            actual = project_items(config)
            mismatches = [
                issue["number"] for issue, status in desired
                if issue["node_id"] not in actual
                or (actual[issue["node_id"]].get("fieldValueByName") or {}).get("name") != status
            ]
            if not mismatches:
                break
        if mismatches:
            raise RuntimeError(f"Board readback differs for issues: {mismatches}.")
    print(f"Issues checked: {len(issues)}; {'applied' if apply else 'pending'} changes: {changes}.")
    return 0 if apply or not changes else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Add missing issues and update derived board status")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.apply))
