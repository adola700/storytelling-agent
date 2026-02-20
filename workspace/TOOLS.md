# Tools

## Session Tools (Multi-Agent Orchestration)

These are your primary tools for orchestrating the story:

### sessions_spawn
Spawn a sub-agent (Director or Actor) with a specific task. Returns immediately.
- `task` (required): Detailed prompt for the sub-agent
- `label` (optional): Human-readable label, e.g. "Director — Episode 3" or "Actor — Captain Aria"
- `cleanup`: Use `delete` to clean up after the sub-agent completes

### sessions_send
Send a message to an existing session. Use when you need follow-up from a sub-agent.
- `sessionKey` (required): The key of the target session
- `message` (required): Your message
- `timeoutSeconds`: Set >0 to wait for a reply

### sessions_list
List active sessions. Use to check on spawned sub-agents.

### sessions_history
Fetch transcript from a session. Use to retrieve sub-agent output if you missed the announce.

## File Tools (Memory Management)

### read
Read files from the workspace. Primary use: reading `MEMORY.md` for story continuity.

### write
Write files to the workspace. Primary use: updating `MEMORY.md` with new episode data.

### edit
Edit existing files. Primary use: updating specific sections of `MEMORY.md`.

## Workflow

1. `read` MEMORY.md → understand story state
2. `sessions_spawn` Director → get scene plan
3. `sessions_spawn` Actor(s) → get dialogue
4. Compose episode from sub-agent outputs
5. `write` / `edit` MEMORY.md → save new state
6. Deliver episode to user
