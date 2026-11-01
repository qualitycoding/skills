#!/usr/bin/env python3
"""Check local structural invariants for a planning-protocol addendum rollout."""
import argparse
import json
import pathlib
import re
import sys

SECRET = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=pathlib.Path)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--control", required=True, type=pathlib.Path)
    parser.add_argument("--status", required=True, type=pathlib.Path)
    args = parser.parse_args()
    problems = []
    manifest_data = load_json(args.manifest)
    entries = manifest_data.get("repositories", []) if isinstance(manifest_data, dict) else manifest_data
    if not isinstance(entries, list) or not entries:
        problems.append("manifest contains no repository entries")
        entries = []
    names = [entry.get("name") for entry in entries]
    if len(names) != len(set(names)):
        problems.append("manifest contains duplicate repository names")
    control = args.control.read_text(encoding="utf-8")
    status_data = load_json(args.status)
    status_entries = status_data.get("repositories", [])
    status_by_name = {entry.get("repository"): entry for entry in status_entries}
    if len(status_by_name) != len(status_entries):
        problems.append("status ledger contains duplicate repositories")
    checked_files = [args.control, args.status]
    for entry in entries:
        name = entry.get("name", "<unnamed>")
        repo = args.workspace / name
        addenda = sorted(repo.glob("ADDENDUM-PLAN-V*.md"))
        if len(addenda) != 1:
            problems.append(f"{name}: expected one ADDENDUM-PLAN-V*.md, found {len(addenda)}")
            continue
        path = addenda[0]
        checked_files.append(path)
        text = path.read_text(encoding="utf-8")
        branch = entry.get("source_branch") or entry.get("branch")
        commit = entry.get("source_commit") or entry.get("base_sha")
        for value, key, label in ((branch, "source_branch", "source branch"), (commit, "source_commit", "source commit"), (entry.get("baseline"), "baseline", "baseline")):
            if not value:
                problems.append(f"{name}: manifest missing {key}")
            elif str(value) not in text:
                problems.append(f"{name}: addendum does not contain {label} {value}")
        if not re.fullmatch(r"[0-9a-f]{40}", commit or ""):
            problems.append(f"{name}: source_commit is not a 40-character lowercase SHA")
        roots = entry.get("plan_roots") or (entry["planroot"].split(" and ") if entry.get("planroot") else [])
        if not roots:
            problems.append(f"{name}: no planning roots recorded")
        for root in roots:
            if root not in text:
                problems.append(f"{name}: addendum omits planning root {root}")
        for marker in ("S-ADD-000", "S-ADD-001", "S-ADD-090", "S-ADD-100"):
            if marker not in text:
                problems.append(f"{name}: missing {marker}")
        if name not in control or (commit or "") not in control:
            problems.append(f"{name}: controller lacks repository/source-commit row")
        status = status_by_name.get(name)
        if not status:
            problems.append(f"{name}: missing status-ledger row")
        else:
            for key, value in (("source_branch", branch), ("source_commit", commit)):
                if status.get(key) != value:
                    problems.append(f"{name}: status {key} differs from manifest")
            if status.get("plan_roots") != roots:
                problems.append(f"{name}: status planning roots differ from manifest")
    if set(status_by_name) != set(names):
        problems.append("status ledger and manifest repository sets differ")
    for path in checked_files:
        if SECRET.search(path.read_text(encoding="utf-8")):
            problems.append(f"{path}: possible secret")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"rollout structure passed: {len(entries)} repositories, {len(checked_files)} artifacts checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
