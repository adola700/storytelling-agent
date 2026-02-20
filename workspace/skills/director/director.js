import { callLLM } from './helpers.js';

/**
 * Calls GPT-5 with the Director persona to produce a structured scene plan.
 * This is the first of the two LLM calls the Narrator orchestrates.
 */
export async function generateOutline(prompt, context = '') {
  const { text } = await callLLM({
    system: `You are a Director crafting narrative arcs for episodic stories. \
First, decide which character is the focal point of this scene and what they must accomplish. \
Return a structured direction in markdown with these exact sections: \
Cast (character name + their role in this scene), \
Acting Instructions (3-5 bullet points telling the actor what to do/feel/achieve), \
Scene Blueprint containing: Setting, Key Beats (3-5), Emotional Arc, Cliffhanger/Hook, Continuity Notes.`,
    user: `Create a casting decision and scene direction for the following story prompt.

## Story Prompt
${prompt}

## Story Context
${context || 'This is the first episode — no prior history.'}`,
  });

  return text;
}
