---
name: director
description: Scene planning and story direction tool
---

# Scene Planning Tool

This skill documents the Director stage of the storytelling pipeline.

## Invoking the Director Stage

The Director stage is invoked via the `run_pipeline.py` script (which also runs the Actor stage):

**Step 1** — Write premise to `/tmp/oc-premise.txt`

**Step 2** — Run bash:
```
python3 /root/storytelling-agent/workspace/skills/director/run_pipeline.py \
  /tmp/oc-premise.txt /tmp/oc-pipeline.json 2>&1
```

You will see:
```
[Director] === Stage 1: Scene Planning ===
[Director] Calling Director LLM (OpenAI)...
[Director] Scene plan received (N chars)
[Director] Cast: <character name(s)>
```

**Step 3** — Read `/tmp/oc-pipeline.json` to get the Director's output.

The JSON contains:
- `scene_plan` — full Director output (scene type, cast, blueprint)
- `cast` — array of cast members, each with:
  - `character_name` — the character's name
  - `acting_instructions` — Director's bullet-point notes for the Actor
  - `actor_performance` — the Actor's raw performance as this character
