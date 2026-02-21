# User Context

This skill reads user preferences from the workspace-level `USER.md` at runtime.
The Director and Actor Python scripts automatically load `../../USER.md` and inject it into their LLM prompts.

Do NOT duplicate user preferences here — update `workspace/USER.md` instead.
