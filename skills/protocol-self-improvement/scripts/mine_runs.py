#!/usr/bin/env python3
"""Mine run records and lessons from a lesson-store checkout for the planning-protocol improvement loop.

Reads `<store>/runs/*.json` (Appendix D of the protocol) and `<store>/lessons/**/L-*.md`, and prints one JSON
report: lesson telemetry, lessons to strengthen or review or retire, candidate skills, evidence for protocol
changes, and per-protocol-version figures. It writes nothing. Every list is a lead for a reviewing agent to
judge, not a decision.
"""
import argparse
import collections
import json
import pathlib
import re
import sys

STOP = {"the", "a", "an", "of", "to", "and", "in", "for", "on", "with", "by", "from", "is", "are", "it", "at", "as"}
GROUP_KINDS = {"kind:process", "kind:tooling", "kind:environment", "kind:verification-gap"}
PROTECTED_TAGS = {"kind:security", "kind:integrity"}


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 0.0


def cluster(items, same):
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if same(items[i], items[j]):
                parent[find(i)] = find(j)
    groups = collections.defaultdict(list)
    for i, item in enumerate(items):
        groups[find(i)].append(item)
    return sorted(groups.values(), key=lambda g: (-len(g), g[0]["key"]))


def read_lesson(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    head = parts[1] if text.startswith("---") and len(parts) == 3 else ""
    fields = {}
    for key, value in re.findall(r"^(\w+):[ \t]*(.*)$", head, re.M):
        fields[key] = re.sub(r"\s+#.*$", "", value).strip()
    fields["tags"] = re.findall(r"[\w-]+:[\w.-]+", fields.get("tags", ""))
    return fields


def check_record(record, stem):
    """Raise when a record lacks what this script reads; the full schema check is in Appendix D of the protocol."""
    assert isinstance(record, dict) and record.get("run_id") == stem, "run_id does not match the file name"
    assert isinstance(record.get("planning"), dict) and isinstance(record.get("implementation"), dict), "planning or implementation missing"
    assert all(isinstance(e, dict) and e.get("id") and e.get("outcome") for e in record.get("lessons_loaded", [])), "malformed lessons_loaded"
    assert all(isinstance(p, dict) and p.get("phase") for p in record["implementation"].get("late_problems", [])), "late problem without a phase"
    assert all(isinstance(p, dict) and p.get("name") for p in record.get("procedures_by_hand", [])), "procedure without a name"


def mean(values):
    return round(sum(values) / len(values), 2) if values else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("store", type=pathlib.Path, help="checkout of the lesson store")
    parser.add_argument("--min-runs-skill", type=int, default=3, help="distinct runs for a candidate skill (default 3)")
    parser.add_argument("--min-runs-retire", type=int, default=5, help="runs that loaded a lesson before it is a retirement candidate (default 5)")
    parser.add_argument("--min-runs-protocol", type=int, default=2, help="distinct runs for the protocol evidence bar (default 2)")
    args = parser.parse_args()

    lessons, runs, invalid = {}, [], []
    for path in sorted(args.store.glob("lessons/**/L-*.md")):
        fields = read_lesson(path)
        lessons[path.stem] = fields
    for path in sorted(args.store.glob("runs/*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            check_record(record, path.stem)
            runs.append(record)
        except (ValueError, KeyError, TypeError, AssertionError) as error:
            invalid.append(f"{path.name}: {error!r}")
    runs.sort(key=lambda r: (r.get("recorded_at", ""), r["run_id"]))

    outcomes = collections.defaultdict(lambda: collections.Counter())
    for record in runs:
        for entry in record.get("lessons_loaded", []):
            outcomes[entry["id"]][entry["outcome"]] += 1
    children = collections.defaultdict(list)
    for lesson_id, fields in lessons.items():
        parent = fields.get("recurrence_of", "null")
        if parent not in ("", "null", "None"):
            children[parent].append(lesson_id)

    telemetry, strengthen, review, retire = [], [], [], []
    for lesson_id in sorted(set(lessons) | set(outcomes)):
        fields = lessons.get(lesson_id)
        counts = outcomes.get(lesson_id, collections.Counter())
        loaded = sum(counts.values())
        protected = bool(fields) and (fields.get("severity") == "Critical" or bool(PROTECTED_TAGS & set(fields["tags"])))
        row = {"id": lesson_id, "in_store": fields is not None, "status": fields.get("status") if fields else None,
               "severity": fields.get("severity") if fields else None, "protected": protected,
               "runs_loaded": loaded, "outcomes": dict(sorted(counts.items())), "recurrence_children": sorted(children.get(lesson_id, []))}
        telemetry.append(row)
        if not fields or fields.get("status") != "active":
            continue
        if counts["applied-recurred"] or children.get(lesson_id):
            strengthen.append({"id": lesson_id, "applied_recurred": counts["applied-recurred"], "recurrences": sorted(children.get(lesson_id, []))})
        if counts["applied-harmful"]:
            review.append({"id": lesson_id, "applied_harmful": counts["applied-harmful"], "runs_loaded": loaded})
        if loaded >= args.min_runs_retire and counts["not-applicable"] == loaded and not protected:
            retire.append({"id": lesson_id, "runs_loaded": loaded, "reason": "loaded in every run, never applicable"})

    procedures = [{"key": f"{r['run_id']}#{i}", "run": r["run_id"], "name": p.get("name", ""), "tags": set(p.get("tags", [])),
                   "steps": tokens(" ".join(p.get("steps", []))), "words": tokens(p.get("name", ""))}
                  for r in runs for i, p in enumerate(r.get("procedures_by_hand", []))]
    same_procedure = lambda a, b: bool(a["tags"] & b["tags"]) and (jaccard(a["words"], b["words"]) >= 0.5 or jaccard(a["steps"], b["steps"]) >= 0.6)
    procedure_candidates = [{"names": sorted({p["name"] for p in g}), "runs": sorted({p["run"] for p in g}), "tags": sorted(set().union(*[p["tags"] for p in g])),
                             "steps_seen": sorted({" ".join(sorted(p["steps"])) for p in g})}
                            for g in cluster(procedures, same_procedure) if len({p["run"] for p in g}) >= args.min_runs_skill]

    groups = collections.defaultdict(list)
    for lesson_id, fields in lessons.items():
        kinds = GROUP_KINDS & set(fields["tags"])
        subject = next((t for t in fields["tags"] if t.startswith(("tech:", "domain:"))), None)
        if fields.get("status") == "active" and kinds and subject:
            groups[(subject, sorted(kinds)[0])].append(lesson_id)
    lesson_groups = [{"tag": k[0], "kind": k[1], "lessons": sorted(v), "runs": sorted({lessons[i].get("run", "") for i in v})}
                     for k, v in sorted(groups.items()) if len(v) >= 3 and len({lessons[i].get("run", "") for i in v}) >= 2]

    protocol_lessons = [{"key": i, "id": i, "severity": f.get("severity"), "run": f.get("run"), "status": f.get("status"),
                         "words": tokens(f.get("title", ""))} for i, f in sorted(lessons.items()) if "kind:protocol" in f["tags"] and f.get("status") == "active"]
    evidence = []
    for g in cluster(protocol_lessons, lambda a, b: jaccard(a["words"], b["words"]) >= 0.5):
        distinct = len({p["run"] for p in g})
        critical = any(p["severity"] == "Critical" for p in g)
        evidence.append({"lessons": [p["id"] for p in g], "runs": distinct, "critical": critical,
                         "meets_evidence_bar": distinct >= args.min_runs_protocol or critical})

    late = collections.defaultdict(lambda: {"problems": 0, "runs": set()})
    nothing = collections.defaultdict(list)
    for record in runs:
        for problem in record.get("implementation", {}).get("late_problems", []):
            late[problem["phase"]]["problems"] += 1
            late[problem["phase"]]["runs"].add(record["run_id"])
        for check in record.get("checks_found_nothing", []):
            nothing[check].append(record["run_id"])
    ordered = [r["run_id"] for r in runs]
    checks = {}
    for check, ids in sorted(nothing.items()):
        trailing = 0
        for run_id in reversed(ordered):
            if run_id not in ids:
                break
            trailing += 1
        checks[check] = {"runs": len(ids), "of": len(ordered), "trailing_runs": trailing}

    by_version = collections.defaultdict(list)
    for record in runs:
        by_version[str(record.get("protocol", {}).get("core", "unknown"))].append(record)
    version_figures = {}
    for version, records in sorted(by_version.items()):
        impl = [r.get("implementation", {}) for r in records]
        version_figures[version] = {
            "runs": len(records),
            "mean_late_problems": mean([len(i.get("late_problems", [])) for i in impl]),
            "mean_failed_attempts": mean([i.get("failed_attempts", 0) for i in impl]),
            "mean_deviations": mean([i.get("deviations", 0) for i in impl]),
            "mean_first_cold_read_items": mean([r["planning"]["cold_read_items"][0] for r in records if r.get("planning", {}).get("cold_read_items")]),
            "mean_applied_recurred": mean([sum(e["outcome"] == "applied-recurred" for e in r.get("lessons_loaded", [])) for r in records]),
        }

    report = {
        "runs": {"count": len(runs), "ids": ordered, "invalid": invalid},
        "lessons": {"in_store": len(lessons), "telemetry": telemetry},
        "strengthen": strengthen, "review_harmful": review, "retire_candidates": retire,
        "skill_candidates": {"procedures": procedure_candidates, "lesson_groups": lesson_groups},
        "protocol": {"evidence": evidence,
                     "late_problems_by_phase": {k: {"problems": v["problems"], "runs": len(v["runs"])} for k, v in sorted(late.items())},
                     "checks_found_nothing": checks, "figures_by_core_version": version_figures},
    }
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    print()
    sys.exit(1 if invalid else 0)


if __name__ == "__main__":
    main()
