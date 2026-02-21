# Skill: Session Reset

Clears the current conversation context (session history) without affecting workspace files.
Use this after every 2 episodes to keep the context window lean.

## Usage

Run via bash:

```bash
bash /root/storytelling-agent/workspace/skills/session-reset/reset-session.sh
```

This archives the current session JSONL and removes the session entry so the next agent turn starts completely fresh. Workspace files (MEMORY.md, USER.md, last-episode.md) are NOT touched — they provide continuity across resets.

## When to Use

- After delivering an even-numbered episode (2, 4, 6, …)
- The agent calls this AFTER saving last-episode.md and updating MEMORY.md
- The next user message will start a fresh session; the agent bootstraps from files
