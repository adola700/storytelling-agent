#!/usr/bin/env bash
# reset-session.sh — Clears the current OpenClaw session context
# by renaming the active JSONL file so the next agent turn starts fresh.
# Usage: bash reset-session.sh <session-id>
#
# The agent's workspace files (MEMORY.md, USER.md, last-episode.md) are untouched.
# Only the conversation history is wiped.

set -euo pipefail

SESSION_DIR="/root/.openclaw/agents/main/sessions"
SESSIONS_JSON="$SESSION_DIR/sessions.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%S.000Z")

# Find the session ID from sessions.json for the given session key
# The main Telegram DM session key is "agent:main:main"
SESSION_KEY="${1:-agent:main:main}"

# Get the session UUID from sessions.json
SESSION_UUID=$(python3 -c "
import json, sys
with open('$SESSIONS_JSON') as f:
    data = json.load(f)
key = '$SESSION_KEY'
if key in data:
    print(data[key].get('sessionId', ''))
else:
    # Try matching by sessionId directly (for --session-id style)
    for k, v in data.items():
        if v.get('sessionId') == key or k.endswith(':$SESSION_KEY'):
            print(v.get('sessionId', ''))
            sys.exit(0)
    # If nothing found, try the key as a direct JSONL filename
    print(key)
")

if [ -z "$SESSION_UUID" ]; then
    echo "ERROR: Could not find session for key: $SESSION_KEY"
    exit 1
fi

JSONL_FILE="$SESSION_DIR/${SESSION_UUID}.jsonl"
LOCK_FILE="$SESSION_DIR/${SESSION_UUID}.jsonl.lock"
RESET_FILE="$SESSION_DIR/${SESSION_UUID}.jsonl.reset.${TIMESTAMP}"

if [ ! -f "$JSONL_FILE" ]; then
    echo "ERROR: Session file not found: $JSONL_FILE"
    exit 1
fi

# Rename the JSONL to .reset (same as /restart does)
mv "$JSONL_FILE" "$RESET_FILE"

# Remove lock file if present
rm -f "$LOCK_FILE"

# Update sessions.json — remove the old session entry so a fresh one is created
python3 -c "
import json
with open('$SESSIONS_JSON') as f:
    data = json.load(f)
# Remove entries matching this session UUID
to_remove = [k for k, v in data.items() if v.get('sessionId') == '$SESSION_UUID']
for k in to_remove:
    del data[k]
with open('$SESSIONS_JSON', 'w') as f:
    json.dump(data, f, indent=2)
print('Removed session entries:', to_remove)
"

echo "OK: Session reset. File archived as: $(basename "$RESET_FILE")"
echo "Next agent turn will start a fresh session."
