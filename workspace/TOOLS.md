# Tools

## Pipeline Tool (Director + Actor Stages)

Both the Director and Actor stages are invoked via a single bash command:

### run-pipeline.js
Runs Director (scene planning) then Actor (character performance) in sequence.

**Bash command:**
```
node /root/storytelling-agent/workspace/skills/director/run-pipeline.js \
  /tmp/oc-premise.txt /tmp/oc-context.txt /tmp/oc-pipeline.json 2>&1
```

**Input files (write these first):**
- `/tmp/oc-premise.txt` — the story prompt / current direction
- `/tmp/oc-context.txt` — story history from MEMORY.md

**Output file (read after bash completes):**
- `/tmp/oc-pipeline.json` — JSON with: `character_name`, `scene_plan`, `acting_instructions`, `actor_performance`

**Debug output** (visible in bash tool result): `[Director]` and `[Actor]` log lines confirming both LLM calls fired.

## File Tools (Memory Management)

### read
Read files from the workspace. Primary use: reading `MEMORY.md` for story continuity.

### write
Write files to the workspace. Primary use: updating `MEMORY.md` with new episode data.

### edit
Edit existing files. Primary use: updating specific sections of `MEMORY.md`.

## Workflow

See `SOUL.md` for the full orchestration protocol. In brief:
1. `read` MEMORY.md → understand story state
2. `write` `/tmp/oc-premise.txt` and `/tmp/oc-context.txt`
3. `bash` `run-pipeline.js` → Director + Actor stages (both LLM calls in one script)
4. `read` `/tmp/oc-pipeline.json` → get scene_plan + actor_performance
5. **Write the episode yourself** — synthesize Director's blueprint + Actor's performance into literary prose
6. `write` / `edit` MEMORY.md → save state
7. Deliver episode to user (story prose only, no preamble)
