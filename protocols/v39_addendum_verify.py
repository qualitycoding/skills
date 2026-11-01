#!/usr/bin/env python3
"""Mechanical checks for the qualitycoding planning-protocol v3.9 addenda."""
import argparse
import json
import pathlib
import re
import sys

SECRET = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----")


def read(path, problems):
    if not path.is_file():
        problems.append(f"missing file: {path}")
        return ""
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        problems.append(f"empty file: {path}")
    return text


def artifact(repo, problems):
    path = repo / "ADDENDUM-PLAN-V3.9.md"
    text = read(path, problems)
    for token in ("Target protocol:** **v3.9**", "Audited source commit:", "S-ADD-000", "S-ADD-001", "S-ADD-090", "S-ADD-100", "planning-v3.9-addendum-control.md"):
        if token not in text:
            problems.append(f"{path}: missing addendum marker {token!r}")
    if SECRET.search(text):
        problems.append(f"{path}: possible secret")


def final(repo, plan_root, problems):
    artifact(repo, problems)
    root = repo / plan_root
    required = [
        repo / "HANDOFF.md",
        root / "PROFILE.md",
        root / "PLAN.md",
        root / "ASSUMPTIONS.md",
        root / "DECISIONS.md",
        root / "GATES.md",
        root / "ENVIRONMENT.md",
        root / "TRACEABILITY.md",
        root / "ADDENDUM-V3.9-GAP.md",
        repo / "research" / "PRIOR_KNOWLEDGE.md",
        repo / "premortem" / "RISK_REGISTER.md",
        repo / "premortem" / "ASSUMPTION_AUDIT.md",
        repo / "reviews" / "CODE_REVIEW.md",
        repo / "reviews" / "ADVERSARIAL_REVIEW.md",
        repo / ".checkpoints" / "state.json",
        repo / "ADDENDUM-V3.9-STATUS.md",
        repo / "ADDENDUM-RETROSPECTIVE.md",
        repo / "EXECUTION_LOG.md",
        repo / "DEVIATIONS.md",
    ]
    if plan_root != "plan":
        # Nested planning trees may keep shared research/review/state artifacts at
        # their own level; require those beside the nested plan instead.
        base = root.parent
        required = [root / "PROFILE.md", root / "PLAN.md", root / "ASSUMPTIONS.md", root / "DECISIONS.md", root / "GATES.md", root / "ENVIRONMENT.md", root / "TRACEABILITY.md", root / "ADDENDUM-V3.9-GAP.md", base / "HANDOFF.md", base / "research" / "PRIOR_KNOWLEDGE.md", base / "premortem" / "RISK_REGISTER.md", base / "premortem" / "ASSUMPTION_AUDIT.md", base / "reviews" / "CODE_REVIEW.md", base / "reviews" / "ADVERSARIAL_REVIEW.md", base / ".checkpoints" / "state.json", repo / "ADDENDUM-V3.9-STATUS.md", repo / "ADDENDUM-RETROSPECTIVE.md", repo / "EXECUTION_LOG.md", repo / "DEVIATIONS.md"]
    texts = {p: read(p, problems) for p in required}
    plan = texts.get(root / "PLAN.md", "")
    for token in ("S-000", "S-RETRO", "S-KNOW", "S-REVIEW", "S-ADVERSARIAL", "v3.9"):
        if token not in plan:
            problems.append(f"{root / 'PLAN.md'}: missing {token}")
    if plan.rfind("S-RETRO") > plan.rfind("S-KNOW") or plan.rfind("S-KNOW") < 0:
        problems.append(f"{root / 'PLAN.md'}: closing steps are not ordered S-RETRO then S-KNOW")
    gates = texts.get(root / "GATES.md", "")
    for token in ("G-003", "Lessons", "knowledge", "do-not-push"):
        if token not in gates:
            problems.append(f"{root / 'GATES.md'}: missing split-store gate marker {token}")
    decisions = texts.get(root / "DECISIONS.md", "")
    mutation = read(repo / "reviews" / "MUTATION.md", []) if plan_root == "plan" else read(root.parent / "reviews" / "MUTATION.md", [])
    if not mutation and "D-980" not in decisions:
        problems.append("mutation design missing: reviews/MUTATION.md or D-980 opt-out")
    state_path = repo / ".checkpoints" / "state.json" if plan_root == "plan" else root.parent / ".checkpoints" / "state.json"
    try:
        state = json.loads(texts.get(state_path, ""))
        for key in ("execution_context", "active_variables", "artifacts", "lesson_store", "knowledge_store"):
            if key not in state:
                problems.append(f"{state_path}: missing field {key}")
    except json.JSONDecodeError as exc:
        problems.append(f"{state_path}: invalid JSON: {exc}")
    status = texts.get(repo / "ADDENDUM-V3.9-STATUS.md", "")
    rows = [line for line in status.splitlines() if line.startswith("| S-ADD-")]
    if not rows:
        problems.append("ADDENDUM-V3.9-STATUS.md: no step rows")
    for row in rows:
        if not re.search(r"\|\s*pass\s*\|", row, re.I):
            problems.append(f"ADDENDUM-V3.9-STATUS.md: step not passed: {row}")
    for path, text in list(texts.items()) + [(repo / "ADDENDUM-PLAN-V3.9.md", (repo / "ADDENDUM-PLAN-V3.9.md").read_text(encoding="utf-8"))]:
        if SECRET.search(text):
            problems.append(f"{path}: possible secret")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("artifact", "final"))
    parser.add_argument("--repo", default=".", help="target repository root")
    parser.add_argument("--plan-root", default="plan", help="planning directory relative to repository root")
    args = parser.parse_args()
    repo = pathlib.Path(args.repo).resolve()
    problems = []
    if args.mode == "artifact":
        artifact(repo, problems)
    else:
        final(repo, args.plan_root, problems)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"{args.mode} verification passed: {repo} (plan root: {args.plan_root})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
