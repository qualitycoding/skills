#!/usr/bin/env python3
"""Check that a proposed protocol text weakens none of the protected rules (Rule 17).

Compares the core file of the unchanged protocol with the proposed one. For each protected block, every
non-empty line of the unchanged block must still appear in the proposed block, in the same order; lines
may be added between them. A changed or removed line is reported. A block that is absent from the
unchanged file (a rule added since) is skipped. Exit status 0 means no protected line was changed or removed.
"""
import argparse
import pathlib
import re
import sys

GLOBAL_RULES = (6, 9, 10, 14, 15, 16, 17)


def region(lines, start, stop):
    begin = next((i for i, l in enumerate(lines) if re.match(start, l)), None)
    if begin is None:
        return None
    end = next((i for i in range(begin + 1, len(lines)) if re.match(stop, lines[i])), len(lines))
    return lines[begin:end]


def blocks(text):
    lines = text.splitlines()
    found = {}
    rules = region(lines, r"^## Global Rules", r"^## Phase 0") or []
    for n in GLOBAL_RULES:
        found[f"Rule {n}"] = region(rules, rf"^{n}\. \*\*", r"^(\d+\. \*\*|---)")
    found["Rule 4, Critical lines"] = region(rules, r"^\s*\* \*\*Critical:\*\*", r"^\s*\* \*\*High:\*\*")
    for name, start, stop in (("2B item 5, Red Verification", r"^5\. \*\*Red Verification\*\*", r"^### "),
                              ("2E, Traceability and Freeze", r"^### 2E ", r"^(### |## )"),
                              ("3.6, Cold-Read Gate", r"^### 3\.6 ", r"^(### |## )"),
                              ("Phase 4, Pre-Mortem and 4.7 Audit", r"^## Phase 4", r"^## Phase 5")):
        found[name] = region(lines, start, stop)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("unchanged", type=pathlib.Path, help="planning-protocol.md before the change")
    parser.add_argument("proposed", type=pathlib.Path, help="planning-protocol.md with the change")
    args = parser.parse_args()
    old, new = blocks(args.unchanged.read_text(encoding="utf-8")), blocks(args.proposed.read_text(encoding="utf-8"))
    problems = []
    for name, old_lines in old.items():
        if old_lines is None:
            continue
        if new[name] is None:
            problems.append(f"{name}: block removed")
            continue
        remaining = iter(l.strip() for l in new[name] if l.strip())
        for line in (l.strip() for l in old_lines if l.strip()):
            if line not in remaining:
                problems.append(f"{name}: line changed or removed: {line[:90]}")
                break
    print("\n".join(problems) or "no protected line changed or removed")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
