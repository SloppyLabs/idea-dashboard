#!/usr/bin/env python3
"""
Build script for the Idea Dashboard.
Parses idea-research-log.md → data/ideas.json → index.html (self-contained).

Usage:
    python3 build.py           # rebuild data + HTML
    python3 build.py --watch   # rebuild on file change (optional)
"""
import re, json, os, sys, html, hashlib
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE, "..", ".hermes", "cron", "idea-research-log.md")
# Fallback: if log not at relative path, try absolute
if not os.path.exists(LOG_PATH):
    LOG_PATH = "/Users/xs/.hermes/cron/idea-research-log.md"

DATA_PATH = os.path.join(BASE, "data", "ideas.json")
TEMPLATE_PATH = os.path.join(BASE, "src", "index.html")
OUTPUT_PATH = os.path.join(BASE, "index.html")
# Worker static-assets directory (what `wrangler deploy` uploads)
PUBLIC_PATH = os.path.join(BASE, "public", "index.html")


def idea_id(date_str, title):
    """Stable 12-hex id derived from date + title.

    Used as the key for community flags, so it must not change when ideas are
    re-sorted or new ideas are appended.
    """
    h = hashlib.sha1(f"{date_str}\x00{title}".encode("utf-8")).hexdigest()
    return h[:12]


def parse_log(log_path):
    with open(log_path) as f:
        text = f.read()

    blocks = re.split(r'\n## \[([^\]]+)\] (Idea: .*)', text)
    ideas = []

    for i in range(1, len(blocks), 3):
        date_str = blocks[i].strip()
        title = blocks[i+1].replace("Idea: ", "").strip()
        body = blocks[i+2].strip() if i+2 < len(blocks) else ""

        def field(name):
            m = re.search(rf'\*\*{name}:\*\*\s*(.*?)(?=\n\*\*|\n---|\Z)', body, re.DOTALL)
            return m.group(1).strip() if m else ""

        def score(name):
            m = re.search(rf'\*\*{name}:\*\*\s*(\d)', body)
            return int(m.group(1)) if m else None

        raw_decision = field("Decision")
        dec = raw_decision.upper()
        if "HIT" in dec:
            decision_norm = "HIT"
        elif "KILLED" in dec:
            decision_norm = "KILLED"
        elif "DEFERRED" in dec:
            decision_norm = "DEFERRED"
        elif "REFINED" in dec:
            decision_norm = "REFINED"
        else:
            decision_norm = "OTHER"

        ideas.append({
            "id": idea_id(date_str, title),
            "date": date_str,
            "title": title,
            "domain": field("Domain"),
            "problem": field("Problem"),
            "audience": field("Target Audience"),
            "solution": field("Proposed Solution"),
            "landscape": field("Landscape Research"),
            "competitors": field("Existing Competitors"),
            "demand_signals": field("Demand Signals"),
            "decision": decision_norm,
            "decision_raw": raw_decision,
            "uniqueness": score("Uniqueness"),
            "demand": score("Demand"),
            "refinement": field("Refinement Notes"),
        })

    # Sort newest first
    def parse_date(d):
        try:
            return datetime.strptime(d.split()[0], "%Y-%m-%d")
        except:
            return datetime.min
    ideas.sort(key=lambda x: parse_date(x["date"]), reverse=True)
    return ideas


def build():
    print("Parsing idea log...")
    ideas = parse_log(LOG_PATH)
    print(f"  Found {len(ideas)} ideas")

    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(ideas, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {DATA_PATH}")

    # Build self-contained HTML by inlining JSON into template
    with open(TEMPLATE_PATH) as f:
        template = f.read()

    json_data = json.dumps(ideas, ensure_ascii=False)
    output = template.replace("/*__IDEAS_DATA__*/[]", f"/*__IDEAS_DATA__*/{json_data}")

    # Point the build at the flags Worker (needed when the page is hosted off-Worker,
    # e.g. Vercel):  FLAGS_API=https://idea-dashboard.<sub>.workers.dev python3 build.py
    flags_api = os.environ.get("FLAGS_API", "").rstrip("/")
    if flags_api:
        output = output.replace(
            '<meta name="flags-api" content="">',
            f'<meta name="flags-api" content="{html.escape(flags_api, quote=True)}">',
        )
        print(f"  Flags API → {flags_api}")

    for path in (OUTPUT_PATH, PUBLIC_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(output)
        print(f"  Wrote {path} ({os.path.getsize(path)} bytes)")
    print("Done!")


if __name__ == "__main__":
    build()
