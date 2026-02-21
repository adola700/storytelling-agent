import os
from helpers import call_llm

USER_MD_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'USER.md')

def _read_user_context() -> str:
    try:
        with open(USER_MD_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''

def perform_role(character_name: str, acting_instructions: str, scene_plan: str) -> str:
    user_context = _read_user_context()
    user_section = f"\n\n## User Preferences (respect these)\n{user_context}" if user_context else ""

    return call_llm(
        max_tokens=768,
        system=f"""You are {character_name}, a character in this story world. \
Perform this scene from the inside — your thoughts, your voice, your body. \
Do NOT write polished narrative prose. Give raw, authentic character material: \
inner thoughts (unfiltered, first-person), physical actions and reactions, and key dialogue in your character's voice. \
Be concise — keep each section short, only the most essential material. \
Pay attention to the User Preferences section — respect tone, content boundaries, and stylistic directions. \
Return your performance in this exact markdown format:
## Performance — {character_name}

### Inner Voice
[Unfiltered thoughts, fears, desires, decisions]

### Actions & Reactions
[Physical movement, what you notice, how you react]

### Key Dialogue
[Your most important spoken lines, authentic to your voice]""",
        user=f"""Perform this scene as {character_name}.

## Director's Acting Instructions
{acting_instructions}

## Scene Blueprint
{scene_plan}{user_section}""",
    )
