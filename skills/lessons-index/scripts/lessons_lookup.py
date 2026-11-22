#!/usr/bin/env python3
"""Look up lessons from the qualitycoding/Lessons generated index.

Fetches lessons/INDEX.md (tag -> lesson entries), selects entries whose
section tag matches the requested tags plus applies:all, ranks them by
severity then recency, and optionally downloads the full lesson files.

Auth: the repo is private. Provide a token via the GITHUB_TOKEN
environment variable (never as a command-line argument, never hardcoded).

Examples:
  GITHUB_TOKEN=... python3 lessons_lookup.py --tags domain:audio tech:python
  GITHUB_TOKEN=... python3 lessons_lookup.py --tags tech:git --fetch --top 10
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time

REPO = "qualitycoding/Lessons"
BRANCH = "main"
API = "https://api.github.com"
ENTRY_RE = re.compile(
    r"^- \[(?P<id>[^\]]+)\]\((?P<path>[^)]+)\) (?P<title>.*?)(?: \((?P<sev>High|Medium|Low)\))?$"
)
SEV_RANK = {"High": 0, "Medium": 1, "Low": 2}


def github_get(path, token, retries=4):
    """GET a repo content path via the GitHub API; return decoded bytes."""
    url = f"{API}/repos/{REPO}/contents/{path}?ref={BRANCH}"
    last = None
    for attempt in range(retries):
        try:
            r = subprocess.run(
                ["curl", "-sS", "--max-time", "40",
                 "-H", f"Authorization: Bearer {token}", url],
                capture_output=True, text=True, timeout=60,
            )
            d = json.loads(r.stdout)
            if "content" in d:
                return base64.b64decode(d["content"])
            last = d.get("message", r.stdout[:200])
        except Exception as e:  # noqa: BLE001 - network flakiness
            last = str(e)
        time.sleep(2 * (attempt + 1))
    raise SystemExit(f"failed to fetch {path}: {last}")


def parse_index(index_text):
    """Return {tag: [entry, ...]} keyed by section heading."""
    sections, tag = {}, None
    for line in index_text.splitlines():
        if line.startswith("## "):
            tag = line[3:].strip()
            sections.setdefault(tag, [])
        elif line.startswith("- ") and tag:
            m = ENTRY_RE.match(line)
            if m:
                sections[tag].append(m.groupdict())
    return sections


def select_and_rank(sections, tags, top):
    """Merge requested tags + applies:all, dedupe, rank, truncate."""
    picked = {}
    for tag in ["applies:all", *tags]:
        for e in sections.get(tag, []):
            picked.setdefault(e["id"], e)
    ranked = sorted(
        picked.values(),
        key=lambda e: (
            SEV_RANK.get(e["sev"], 3),
            re.sub(r"^L-", "", e["id"]),  # ISO timestamp: newest first
        ),
    )
    return ranked[:top] if top else ranked


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tags", nargs="+", required=True,
                    help="task tags, e.g. domain:audio tech:python")
    ap.add_argument("--fetch", action="store_true",
                    help="download full lesson files and print their text")
    ap.add_argument("--top", type=int, default=0,
                    help="limit to the first N ranked lessons (0 = all)")
    ap.add_argument("--out-dir", default=os.path.join(tempfile.gettempdir(), "lessons"),
                    help="where fetched lesson files are written")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set; export it first (do not pass it as an argument).")

    sections = parse_index(github_get("lessons/INDEX.md", token).decode("utf-8"))
    ranked = select_and_rank(sections, args.tags, args.top)
    if not ranked:
        print(f"no lessons matched tags: {args.tags}")
        return

    print(f"{len(ranked)} lesson(s) matched (severity, then newest first):")
    for i, e in enumerate(ranked, 1):
        print(f"{i:3}. [{e['sev'] or '?'}] {e['id']}\n      {e['title']}\n      {e['path']}")

    if not args.fetch:
        return
    os.makedirs(args.out_dir, exist_ok=True)
    for e in ranked:
        raw = github_get(e["path"], token).decode("utf-8")
        if re.search(r"^status:\s*(superseded|retired)\s*$", raw, re.M):
            print(f"\n### SKIPPED (not active): {e['id']}")
            continue
        dest = os.path.join(args.out_dir, os.path.basename(e["path"]))
        with open(dest, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"\n{'=' * 72}\n{dest}\n{'=' * 72}\n{raw}")


if __name__ == "__main__":
    main()
