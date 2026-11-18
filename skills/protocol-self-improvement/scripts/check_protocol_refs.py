#!/usr/bin/env python3
"""Check that every cross-reference in the planning protocol resolves.

Reads the core file and every module file. Defined anchors are the numbered headings (`### 3.7.1`),
the numbered items under a heading (`2E.4`) and under Rule 0 (`0.6`), the bold sub-sections (`0.3.1`),
the Global Rules, the phases, the appendices and the research steps (R0 to R7). Reports every reference
to an anchor that is not defined, and every module whose version line is missing.
Exit status 0 means no unresolved reference.
"""
import argparse
import pathlib
import re
import sys

NUMBER = re.compile(r"(?<![\w.@/-])(\d[A-Z]?(?:\.\d+){1,2})(?![\w-])")
HEADING = re.compile(r"^#{2,4} (\d[A-Z]?(?:\.\d+)*)\b")
ITEM = re.compile(r"^(\d+)\. ")
BOLD_SECTION = re.compile(r"^\*\*(\d[A-Z]?(?:\.\d+)+)\b")
PHASE = re.compile(r"^## Phase (\d)")
APPENDIX = re.compile(r"^## Appendix ([A-Z])")
RESEARCH_STEP = re.compile(r"^\*\*(R\d)b? ")
GLOBAL_RULE = re.compile(r"^(\d+)\. \*\*")
VERSION_LINE = re.compile(r"^# Planning protocol module: [\w-]+ \(v\d+\.\d+\)")


def collect(files):
    anchors = {"section": set(), "rule": set(), "phase": set(), "appendix": set(), "step": set()}
    for path in files:
        heading, region, fenced = None, None, False
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("```"):
                fenced = not fenced
            if fenced:
                continue
            if line.startswith("## Rule 0"):
                region, heading = "rule0", None
                anchors["rule"].add("0")
            elif line.startswith("## Global Rules"):
                region, heading = "global", None
            elif line.startswith("## "):
                region, heading = None, None
            if (m := HEADING.match(line)):
                heading = m.group(1)
                anchors["section"].add(heading)
            elif (m := ITEM.match(line)):
                if region == "rule0":
                    anchors["section"].add(f"0.{m.group(1)}")
                    anchors["rule"].add(f"0.{m.group(1)}")
                elif region == "global" and GLOBAL_RULE.match(line):
                    anchors["rule"].add(m.group(1))
                elif heading:
                    anchors["section"].add(f"{heading}.{m.group(1)}")
            if (m := BOLD_SECTION.match(line)):
                anchors["section"].add(m.group(1))
            if (m := PHASE.match(line)):
                anchors["phase"].add(m.group(1))
                heading = m.group(1)
            if (m := APPENDIX.match(line)):
                anchors["appendix"].add(m.group(1))
            if (m := RESEARCH_STEP.match(line)):
                anchors["step"].add(m.group(1))
    return anchors


def references(path):
    fenced = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced
        if fenced or line.startswith("#"):
            continue
        plain = re.sub(r"`[^`]*`", "``", line)
        for m in re.finditer(r"\b(?:Global )?Rules? (\d+(?:\.\d+)?)", plain):
            yield number, "rule", m.group(1)
        for m in re.finditer(r"\bPhases? (\d)", plain):
            yield number, "phase", m.group(1)
        for m in re.finditer(r"\bAppendices (?:[A-Z] to )?([A-Z])\b|\bAppendix ([A-Z])\b", plain):
            yield number, "appendix", m.group(1) or m.group(2)
        for m in NUMBER.finditer(plain):
            yield number, "section", m.group(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("protocols", type=pathlib.Path, help="the protocols directory (holds planning-protocol.md and modules/)")
    args = parser.parse_args()
    core = args.protocols / "planning-protocol.md"
    modules = sorted((args.protocols / "modules").glob("*.md"))
    anchors = collect([core, *modules])
    problems = []
    for path in [core, *modules]:
        for number, kind, value in references(path):
            if value not in anchors[kind]:
                problems.append(f"{path.name}:{number}: unresolved {kind} reference {value}")
    for path in modules:
        if not VERSION_LINE.match(path.read_text(encoding="utf-8").splitlines()[0]):
            problems.append(f"{path.name}:1: module version line missing")
    print("\n".join(problems) or f"all references resolve ({sum(len(v) for v in anchors.values())} anchors)")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
