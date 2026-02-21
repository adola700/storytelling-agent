---
name: actor
description: Character performance tool — embodies a cast character and performs a raw scene
---

# Character Performance Tool

This skill documents the Actor stage of the storytelling pipeline.

## Invoking the Actor Stage

The Actor stage runs automatically as Stage 2 inside `run_pipeline.py` — it always follows the Director stage.

You will see in the bash output:
```
[Actor] === Stage 2: Character Performance ===
[Actor] Performing as: <character name>
[Actor] Calling Actor LLM (OpenAI)...
[Actor] Performance received (N chars)
```

The Actor's raw performance is included in `/tmp/oc-pipeline.json` under the `actor_performance` key.

The performance contains:
- **Inner Voice** — the character's unfiltered thoughts, fears, and decisions (first-person)
- **Actions & Reactions** — physical movement, what the character notices, how they react
- **Key Dialogue** — the character's most important spoken lines in their authentic voice

The Narrator (you) synthesizes this raw performance into final literary prose.
