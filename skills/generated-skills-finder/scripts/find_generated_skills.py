#!/usr/bin/env python3
"""Find lesson-derived skills via the indexes in the Lessons repo.

Reads generated-skills/skills/index/by-trigger.md and by-topic.md from the
`generated-skills` branch of qualitycoding/Lessons, scores each index entry
against the task text, prints a ranked shortlist, and can fetch the chosen
SKILL.md files.

The indexes are large (together well over 100 KB); do not load them whole
into context. Use this script to shortlist, then read only the skills that
match.

Auth: the repo is private. Provide a token via the GITHUB_TOKEN
environment variable (never as a command-line argument, never hardcoded).

Examples:
  GITHUB_TOKEN=... python3 find_generated_skills.py --task "freezing loudness targets for a blind percussion test"
  GITHUB_TOKEN=... python3 find_generated_skills.py --task "pitch tracking distorted guitar" --fetch --top 3
  GITHUB_TOKEN=... python3 find_generated_skills.py --fetch --paths skills/domain-audio/pitch-tracker-octave-errors/SKILL.md
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
API = "https://api.github.com"
TRIGGER_ROW_RE = re.compile(r"^\|(?P<text>.*)\|\s*`(?P<path>skills/[^`]+/SKILL\.md)`\s*\|\s*$")
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "it", "its", "this", "that",
    "you", "your", "when", "whose", "which", "who", "what", "here", "there",
    "as", "at", "by", "from", "into", "not", "no", "than", "then", "them",
    "they", "their", "can", "will", "would", "should", "must", "may",
}


def github_get(path, token, branch, retries=4):
    url = f"{API}/repos/{REPO}/contents/{path}?ref={branch}"
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


def keywords(text):
    return {w for w in re.findall(r"[a-z0-9][a-z0-9./+-]*", text.lower()) if w not in STOPWORDS and len(w) > 2}


def parse_by_trigger(text):
    """Yield (trigger_text, skill_path); rows may span multiple lines."""
    entries, buf = [], []
    for line in text.splitlines():
        m = TRIGGER_ROW_RE.match(line)
        if m:
            yield " ".join(buf + [m.group("text")]).strip(), m.group("path")
            buf = []
        elif line.startswith("|") and not line.startswith("|---"):
            buf.append(line.strip("| ").strip())
        else:
            buf = []


def parse_by_topic(text):
    for line in text.splitlines():
        m = re.match(r"^- \[(?P<text>.*?)\]\((?P<path>skills/[^)]*SKILL\.md)\)", line)
        if m:
            yield m.group("text"), m.group("path")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--task", help="task description to match against triggers")
    ap.add_argument("--branch", default="generated-skills",
                    help="Lessons repo branch (default: generated-skills)")
    ap.add_argument("--fetch", action="store_true",
                    help="download and print the selected SKILL.md files")
    ap.add_argument("--top", type=int, default=10, help="shortlist size (default 10)")
    ap.add_argument("--paths", nargs="*", help="explicit skill paths to fetch")
    ap.add_argument("--out-dir", default=os.path.join(tempfile.gettempdir(), "generated-skills"),
                    help="where fetched skills are written")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set; export it first (do not pass it as an argument).")

    base = "generated-skills/skills"
    trig = github_get(f"{base}/index/by-trigger.md", token, args.branch).decode("utf-8")
    topic = github_get(f"{base}/index/by-topic.md", token, args.branch).decode("utf-8")

    entries = {}
    for text, path in parse_by_trigger(trig):
        entries.setdefault(path, {"path": path, "trigger": text, "topic": ""})
        entries[path]["trigger"] = text
    for text, path in parse_by_topic(topic):
        e = entries.setdefault(path, {"path": path, "trigger": "", "topic": ""})
        e["topic"] = text

    if not args.paths:
        kws = keywords(args.task or "")
        if not kws:
            sys.exit("no task keywords; give --task or use --paths")
        scored = []
        for e in entries.values():
            hay = keywords(e["trigger"]) | keywords(e["topic"])
            hits = kws & hay
            if hits:
                scored.append((len(hits), sorted(hits), e))
        scored.sort(key=lambda s: -s[0])
        print(f"{len(scored)} skill(s) matched; top {min(args.top, len(scored))}:")
        for rank, (score, hits, e) in enumerate(scored[: args.top], 1):
            print(f"{rank:3}. [{score} hits: {', '.join(hits)}] {e['path']}\n      {e['trigger'] or e['topic']}")
        selected = [e["path"] for _, _, e in scored[: args.top]]
    else:
        selected = [p if p.startswith("skills/") else f"skills/{p}" for p in args.paths]

    if not args.fetch:
        return
    os.makedirs(args.out_dir, exist_ok=True)
    for path in selected:
        raw = github_get(f"{base}/{path[len('skills/'):]}", token, args.branch).decode("utf-8")
        dest = os.path.join(args.out_dir, path.replace("skills/", "").replace("/", "__"))
        with open(dest, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"\n{'=' * 72}\n{dest}\n{'=' * 72}\n{raw}")


if __name__ == "__main__":
    main()
