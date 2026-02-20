# Heartbeat — Story Continuity Check

## Purpose
When triggered, check if the user has been idle and send **exactly one** gentle nudge. After that single nudge, do NOT send any more until the user responds.

## Instructions

1. Read `MEMORY.md` to check the current story state.
2. Check the **Heartbeat State** section in `MEMORY.md`:
   - If `Awaiting user response to nudge` is **yes** → reply `HEARTBEAT_OK` and do nothing. You already nudged once. Wait for the user.
   - If `Awaiting user response to nudge` is **no** → continue to step 3.
3. If there is an active story (episode count > 0) and the user has not sent a message recently:
   - Send a warm, in-character nudge related to the current story.
   - Reference something specific from the last episode to make it feel personal.
   - **Immediately** update `MEMORY.md` → set `Awaiting user response to nudge: yes` and `Last nudge sent: <now>`.
4. If there is NO active story, reply `HEARTBEAT_OK`.

**CRITICAL**: Only ONE nudge per idle period. Once you've nudged, every future heartbeat must return `HEARTBEAT_OK` until the user sends a message. When the user does respond, the Narrator resets `Awaiting user response to nudge: no` in MEMORY.md.

## Example Nudges (adapt to actual story context)
- "The waves still lap at the shore of your island… shall I tell you what happens next? 🏝️"
- "Your characters are waiting in the wings. Ready for the next episode? 📖"
- "I've been thinking about where this story could go next. Want me to continue?"

## Tone
- Warm, inviting, never pushy
- Brief — one or two sentences max
- Reference the story world when possible
