import os
from helpers import call_llm

USER_MD_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'USER.md')

def _read_user_context() -> str:
    try:
        with open(USER_MD_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''

def generate_outline(prompt: str) -> str:
    user_context = _read_user_context()
    user_section = f"\n\n## User Profile & Preferences\n{user_context}" if user_context else ""

    return call_llm(
        max_tokens=1024,
        system="""You are a Director crafting narrative arcs for episodic stories. \
Analyse the scene and decide whether it calls for a solo performance or an ensemble cast:
- Cast ONE character for solo/intimate/introspective scenes (a single character's inner journey).
- Cast MULTIPLE characters for ensemble scenes (conflict, dialogue, group dynamics, two or more characters interacting).

Pay close attention to the User Profile & Preferences section — respect the user's stated genre preferences, \
tone, content boundaries, and any specific directions they have given.

Return a structured direction in this EXACT markdown format:

## Scene Type
[Solo | Ensemble] — reason in one sentence

## Cast
### Character: <Name>
**Role:** one sentence describing their role in this scene
**Acting Instructions:**
- bullet: what the character must do, feel, or achieve
- bullet
- bullet
- bullet

### Character: <Name2>
**Role:** ...
**Acting Instructions:**
- bullet
- bullet
- bullet
- bullet

(Repeat ### Character blocks for every cast member. Solo scenes have exactly one block.)

## Scene Blueprint
**Setting:** where and when
**Key Beats:** 3-5 plot beats that must happen
**Emotional Arc:** how the emotional tone shifts from start to finish
**Cliffhanger/Hook:** the unresolved tension or question left at the end
**Continuity Notes:** details future episodes should remember""",
        user=f"""Create a casting decision and scene direction for the following story prompt.

## Story Prompt
{prompt}{user_section}""",
    )
