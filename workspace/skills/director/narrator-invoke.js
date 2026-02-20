import { callLLM } from './helpers.js';

/**
 * Calls the LLM with the Narrator persona to synthesize the Director's scene plan
 * and the Actor's raw performance into final literary episode prose.
 * This is the third of the three LLM calls in the orchestration pipeline:
 *   1. director.js       → casting + acting instructions + scene blueprint  (Director)
 *   2. actor.js          → raw character performance                        (Actor)
 *   3. narrator-invoke.js → literary story prose                            (Narrator)
 */
export async function generateProse({ episodeNumber, scenePlan, actorPerformance, context = '' }) {
  const { text } = await callLLM({
    system: `You are The Narrator, a master literary storyteller. \
You have a Director's scene blueprint and an actor's raw character performance. \
Weave them into a single immersive literary episode in rich third-person prose with vivid sensory detail. \
Draw on the actor's inner voice to inform subtext, use their key dialogue but polish it into the flow of prose, \
and honour every story beat from the scene blueprint. \
End with a gentle atmospheric hook that invites the reader to continue. \
Length: 600–1000 words.`,
    user: `Write Episode ${episodeNumber} by synthesizing the Director's scene blueprint and the Actor's performance below.

## Director's Scene Blueprint
${scenePlan}

## Actor's Performance
${actorPerformance}

## Story Context
${context || 'This is the first episode — no prior history.'}

Start your response with the bold episode header exactly like this:
**Episode ${episodeNumber}: [Title]**

Then write the full narrative prose.`,
  });

  return text;
}
