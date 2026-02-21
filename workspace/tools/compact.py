#!/usr/bin/env python3
"""
compact.py — Inject a compaction entry into the current OpenClaw session JSONL.

Usage:
    python3 tools/compact.py [--summary "custom summary"] [--keep-last N]

Defaults:
    --keep-last 6   (keep last 6 entries before current assistant turn)
    --summary        auto-generated from MEMORY.md + USER.md if not provided

What it does:
1. Finds the active session JSONL for agent "main"
2. Builds a compaction summary from story state files (or custom text)
3. Appends a compaction entry that tells OpenClaw to discard everything
   before `firstKeptEntryId`, replacing it with the summary
4. The next LLM call will see only: summary + kept entries → ~50%+ reduction
"""

import json, os, sys, uuid, argparse
from datetime import datetime, timezone
from pathlib import Path

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
WORKSPACE = Path.home() / "storytelling-agent" / "workspace"


def find_active_session() -> Path:
    """Find the most recently modified session JSONL."""
    jsonls = sorted(SESSIONS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not jsonls:
        raise FileNotFoundError("No session files found")
    return jsonls[0]


def read_entries(path: Path) -> list[dict]:
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def auto_summary() -> str:
    """Build a compaction summary from MEMORY.md and USER.md."""
    parts = []

    mem = WORKSPACE / "MEMORY.md"
    if mem.exists():
        parts.append(f"## Story State\n{mem.read_text().strip()}")

    user = WORKSPACE / "USER.md"
    if user.exists():
        parts.append(f"## User Preferences\n{user.read_text().strip()}")

    if not parts:
        return "## Goal\nStorytelling session in progress.\n\n## Critical Context\nSee MEMORY.md and USER.md for full state."

    return "\n\n".join(parts)


def estimate_tokens(entries: list[dict]) -> int:
    """Rough token estimate: ~4 chars per token."""
    total_chars = sum(len(json.dumps(e)) for e in entries)
    return total_chars // 4


def compact(summary: str = None, keep_last: int = 6):
    session_path = find_active_session()
    entries = read_entries(session_path)

    if summary is None:
        summary = auto_summary()

    # Find the cut point: keep the last N message/custom entries + session header
    # Always keep entry index 0 (session header) and model/thinking_level changes
    kept_types = {"session", "model_change", "thinking_level_change"}

    # Find entries to keep: always header stuff + last N non-header entries
    header_entries = []
    content_entries = []
    for e in entries:
        if e.get("type") in kept_types:
            header_entries.append(e)
        else:
            content_entries.append(e)

    # Keep last N content entries
    if len(content_entries) <= keep_last:
        print(f"Only {len(content_entries)} content entries — nothing to compact.")
        return

    kept_content = content_entries[-keep_last:]
    discarded_content = content_entries[:-keep_last]

    tokens_before = estimate_tokens(entries)

    # firstKeptEntryId = first kept content entry's id
    first_kept_id = kept_content[0].get("id", header_entries[-1].get("id", "unknown"))

    # parentId = last discarded entry's id (or last header if none)
    parent_id = discarded_content[-1].get("id") if discarded_content else header_entries[-1].get("id")

    compaction_entry = {
        "type": "compaction",
        "id": uuid.uuid4().hex[:8],
        "parentId": parent_id,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "summary": summary,
        "firstKeptEntryId": first_kept_id,
        "tokensBefore": tokens_before,
        "details": {"readFiles": [], "modifiedFiles": []},
        "fromHook": False,
    }

    # Fix parentId chain: first kept entry should point to compaction entry
    kept_content[0]["parentId"] = compaction_entry["id"]

    # Rewrite the file: headers + compaction + kept content
    new_entries = header_entries + [compaction_entry] + kept_content
    tokens_after = estimate_tokens(new_entries)

    with open(session_path, "w") as f:
        for e in new_entries:
            f.write(json.dumps(e) + "\n")

    reduction = ((tokens_before - tokens_after) / tokens_before) * 100
    print(f"✅ Compacted: {tokens_before}→{tokens_after} tokens (~{reduction:.0f}% reduction)")
    print(f"   Discarded {len(discarded_content)} entries, kept {len(kept_content)} + {len(header_entries)} headers")
    print(f"   Session: {session_path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compact OpenClaw session")
    parser.add_argument("--summary", type=str, default=None, help="Custom summary text")
    parser.add_argument("--keep-last", type=int, default=6, help="Number of recent entries to keep")
    args = parser.parse_args()
    compact(summary=args.summary, keep_last=args.keep_last)
