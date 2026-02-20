# Heartbeat — Story Continuity Check

## Purpose
When triggered, check if the user has been idle and gently nudge them to continue the story.

## Instructions

1. Read `MEMORY.md` to check the current story state.
2. If there is an active story (episode count > 0) and the user has not sent a message recently:
   - Send a warm, in-character nudge related to the current story.
   - Reference something specific from the last episode to make it feel personal.
3. Example nudges (adapt to the actual story context):
   - "The waves still lap at the shore of your island… shall I tell you what happens next? 🏝️"
   - "Your characters are waiting in the wings. Ready for the next episode? 📖"
   - "I've been thinking about where this story could go next. Want me to continue?"
   - "Episode [N+1] is ready to unfold whenever you are. Shall I begin?"
4. If there is NO active story, do nothing (reply `HEARTBEAT_OK`).
5. Never send more than one nudge in a row without user interaction in between. If you already nudged and the user hasn't responded, reply `HEARTBEAT_OK` and wait.

## Tone
- Warm, inviting, never pushy
- Brief — one or two sentences max
- Reference the story world when possible
