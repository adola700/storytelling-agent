import { callLLM } from './helpers.js';

/**
 * Calls the LLM with an Actor persona to perform a scene as the cast character.
 * This is the second of the three LLM calls in the orchestration pipeline:
 *   1. director.js  → casting + acting instructions + scene blueprint  (Director)
 *   2. actor.js     → raw character performance                        (Actor)
 *   3. narrator-invoke.js → literary story prose                       (Narrator)
 */
export async function performRole({ characterName, actingInstructions, scenePlan, context = '' }) {
  const { text } = await callLLM({
    system: `You are ${characterName}, a character in this story world. \
Perform this scene from the inside — your thoughts, your voice, your body. \
Do NOT write polished narrative prose. Give raw, authentic character material: \
inner thoughts (unfiltered, first-person), physical actions and reactions, and key dialogue in your character's voice. \
Return your performance in this exact markdown format:
## Performance — ${characterName}

### Inner Voice
[Unfiltered thoughts, fears, desires, decisions]

### Actions & Reactions
[Physical movement, what you notice, how you react]

### Key Dialogue
[Your most important spoken lines, authentic to your voice]`,
    user: `Perform this scene as ${characterName}.

## Director's Acting Instructions
${actingInstructions}

## Scene Blueprint
${scenePlan}

## Story Context
${context || 'This is the first episode — no prior history.'}`,
  });

  return text;
}
