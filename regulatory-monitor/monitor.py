#!/usr/bin/env python3
"""
DC-LEARN Regulatory Monitor
Fetches watched source pages, diffs against stored snapshots,
updates CHANGELOG.md and produces run_report.json for GitHub Actions.
"""

import json
import os
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

MONITOR_DIR = Path(__file__).parent
SNAPSHOT_DIR = MONITOR_DIR / "snapshots"
SOURCES_FILE = MONITOR_DIR / "sources.json"
CHANGELOG_FILE = MONITOR_DIR / "CHANGELOG.md"
REGISTER_FILE = MONITOR_DIR / "REGISTER.md"
REPORT_FILE = MONITOR_DIR / "run_report.json"

HEADERS = {
    "User-Agent": "DC-LEARN-Regulatory-Monitor/1.0 (lmurphy@legacybe.ie)"
}

TIMEOUT = 30  # seconds


def load_sources():
    with open(SOURCES_FILE) as f:
        return json.load(f)


def fetch_page(url):
    """Fetch page and extract text content."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        # Normalise whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text
    except Exception as e:
        return f"FETCH_ERROR: {e}"


def load_snapshot(filename):
    """Load previous snapshot, return empty string if none."""
    path = SNAPSHOT_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def save_snapshot(filename, content):
    """Save current page content as snapshot."""
    path = SNAPSHOT_DIR / filename
    path.write_text(content, encoding="utf-8")


def content_hash(text):
    """SHA-256 of normalised text."""
    normalised = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalised.encode()).hexdigest()


def detect_changes(old_text, new_text):
    """Compare two text snapshots and return summary of differences."""
    if not old_text:
        return "Initial snapshot — no previous version to compare."

    old_lines = set(old_text.strip().splitlines())
    new_lines = set(new_text.strip().splitlines())

    added = new_lines - old_lines
    removed = old_lines - new_lines

    if not added and not removed:
        return None  # No meaningful change

    summary_parts = []
    if added:
        # Find the most relevant new lines (skip very short ones)
        significant = [l for l in added if len(l) > 30][:10]
        if significant:
            summary_parts.append(
                f"{len(added)} new lines detected. Examples:\n"
                + "\n".join(f"  + {l[:120]}" for l in significant[:5])
            )
    if removed:
        significant = [l for l in removed if len(l) > 30][:10]
        if significant:
            summary_parts.append(
                f"{len(removed)} lines removed. Examples:\n"
                + "\n".join(f"  - {l[:120]}" for l in significant[:5])
            )

    return "\n".join(summary_parts) if summary_parts else None


def classify_priority(source_id, change_summary):
    """Classify change as P1/P2/P3 based on content signals."""
    if not change_summary or "FETCH_ERROR" in change_summary:
        return "P3"

    # P1 signals: canonical value keywords
    p1_keywords = [
        "emission factor", "carbon tax", "clearing price", "CRM",
        "PUE", "1.3", "80%", "renewable", "F-Gas", "phase-down",
        "GWP", "threshold", "50 MW", "licence"
    ]

    lower = change_summary.lower()
    for kw in p1_keywords:
        if kw.lower() in lower:
            return "P1"

    # P2 signals: regulatory action keywords
    p2_keywords = [
        "decision", "consultation", "amendment", "regulation",
        "directive", "delegated act", "guidance", "connection",
        "capacity", "auction", "pathway"
    ]

    for kw in p2_keywords:
        if kw.lower() in lower:
            return "P2"

    return "P3"


def update_changelog(entry):
    """Append entry to CHANGELOG.md."""
    existing = ""
    if CHANGELOG_FILE.exists():
        existing = CHANGELOG_FILE.read_text(encoding="utf-8")

    new_entry = f"""
## {entry['date']} | {entry['source_name']} | {entry['priority']}

**What changed:** {entry['summary']}
**Source URL:** {entry['url']}
**Modules to check:** {', '.join(entry['modules_affected'])}
**Priority:** {entry['priority']}
**Action taken:** _pending_

---
"""
    CHANGELOG_FILE.write_text(existing + new_entry, encoding="utf-8")


def update_register(source_id, date_str):
    """Update last-verified date in REGISTER.md."""
    if not REGISTER_FILE.exists():
        return

    content = REGISTER_FILE.read_text(encoding="utf-8")
    # Pattern: | source_id | ... | YYYY-MM-DD |
    # Simple approach: update any date that follows the source_id
    pattern = rf"(\| {re.escape(source_id)}\b.*?\| )\d{{4}}-\d{{2}}-\d{{2}}( \|)"
    replacement = rf"\g<1>{date_str}\2"
    updated = re.sub(pattern, replacement, content)

    if updated != content:
        REGISTER_FILE.write_text(updated, encoding="utf-8")


def main():
    print("DC-LEARN Regulatory Monitor — Starting check")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print()

    config = load_sources()
    SNAPSHOT_DIR.mkdir(exist_ok=True)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    report = {
        "run_date": now.isoformat(),
        "sources_checked": 0,
        "sources_changed": 0,
        "fetch_errors": 0,
        "changes": []
    }

    for source in config["sources"]:
        source_id = source["id"]
        source_name = source["name"]
        url = source["url"]
        snapshot_file = source["snapshot_file"]

        print(f"Checking {source_name}...")
        report["sources_checked"] += 1

        # Fetch current page
        current_text = fetch_page(url)

        if current_text.startswith("FETCH_ERROR"):
            print(f"  ⚠ Fetch failed: {current_text}")
            report["fetch_errors"] += 1
            continue

        # Load previous snapshot
        previous_text = load_snapshot(snapshot_file)

        # Compare
        if content_hash(previous_text) == content_hash(current_text):
            print(f"  ✓ No changes")
            update_register(source_id, date_str)
            continue

        # Detect what changed
        change_summary = detect_changes(previous_text, current_text)

        if change_summary is None:
            print(f"  ✓ Whitespace-only changes, no content diff")
            save_snapshot(snapshot_file, current_text)
            update_register(source_id, date_str)
            continue

        # Real change detected
        all_modules = source["primary_modules"] + source["secondary_modules"]
        priority = classify_priority(source_id, change_summary)

        print(f"  🔔 CHANGE DETECTED — {priority}")
        print(f"     Modules affected: {', '.join(all_modules)}")

        report["sources_changed"] += 1

        change_entry = {
            "date": date_str,
            "source_id": source_id,
            "source_name": source_name,
            "url": url,
            "priority": priority,
            "summary": change_summary[:500],
            "modules_affected": all_modules
        }
        report["changes"].append(change_entry)

        # Update files
        save_snapshot(snapshot_file, current_text)
        update_changelog(change_entry)
        update_register(source_id, date_str)

    # Write run report (used by GitHub Actions to create issue)
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print()
    print("=" * 50)
    print(f"Sources checked:  {report['sources_checked']}")
    print(f"Changes detected: {report['sources_changed']}")
    print(f"Fetch errors:     {report['fetch_errors']}")
    if report["changes"]:
        print()
        print("CHANGES:")
        for c in report["changes"]:
            print(f"  [{c['priority']}] {c['source_name']} → modules {', '.join(c['modules_affected'])}")
    print("=" * 50)


if __name__ == "__main__":
    main()
