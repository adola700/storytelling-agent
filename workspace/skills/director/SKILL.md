---
name: director
description: Scene planning and story direction tool
---

# Scene Planning Tool

This skill documents the Director stage of the storytelling pipeline.

## Invoking the Director Stage

The Director stage is invoked via the `run-pipeline.js` bash script (which also runs the Actor stage):

**Step 1** — Write premise to `/tmp/oc-premise.txt`

**Step 2** — Write context to `/tmp/oc-context.txt`

**Step 3** — Run bash:
```
node /root/storytelling-agent/workspace/skills/director/run-pipeline.js \
  /tmp/oc-premise.txt /tmp/oc-context.txt /tmp/oc-pipeline.json 2>&1
```

You will see:
```
[Director] === Stage 1: Scene Planning ===
[Director] Calling Director LLM (OpenAI)...
[Director] Scene plan received (N chars)
[Director] Cast: <character name>
```

**Step 4** — Read `/tmp/oc-pipeline.json` to get the Director's output.

The JSON contains:
- `character_name` — the cast character for this scene
- `acting_instructions` — Director's bullet-point notes for the Actor
- `scene_plan` — full Scene Blueprint (Setting, Key Beats, Emotional Arc, Hook, Continuity Notes)
- `actor_performance` — the Actor's raw performance (see Actor stage)
