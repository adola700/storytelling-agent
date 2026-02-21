# Tools

## Pipeline Tool (Director + Actor Stages)

Both the Director and Actor stages are invoked via a single bash command:

### run_pipeline.py
Runs Director (scene planning) then Actor (character performance, once per cast member) in sequence.

**Bash command:**
```
python3 /root/storytelling-agent/workspace/skills/director/run_pipeline.py \
  /tmp/oc-premise.txt /tmp/oc-pipeline.json 2>&1
```

**Input file (write this first):**
- `/tmp/oc-premise.txt` — the story prompt / current direction

**Output file (read after bash completes):**
- `/tmp/oc-pipeline.json` — JSON with:
  - `scene_plan` — full Director output
  - `cast` — array of cast members, each with `character_name`, `acting_instructions`, `actor_performance`

**Debug output** (visible in bash tool result): `[Director]` and `[Actor]` log lines confirming all LLM calls fired.

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
3. `bash` `run_pipeline.py` → Director + Actor stages (one LLM call per cast member)
4. `read` `/tmp/oc-pipeline.json` → get scene_plan + actor_performance
5. **Write the episode yourself** — synthesize Director's blueprint + Actor's performance into literary prose
6. `write` / `edit` MEMORY.md → save state
7. Deliver episode to user (story prose only, no preamble)
