import { generateOutline } from './director.js';
import { performRole } from './actor.js';
import { generateProse } from './narrator-invoke.js';
import { saveFile } from './helpers.js';

/**
 * Orchestrates a full episode across three LLM calls:
 *   Step 1 — Director:  generateOutline  → casting + acting instructions + scene blueprint
 *   Step 2 — Actor:     performRole      → raw character performance (inner voice, actions, dialogue)
 *   Step 3 — Narrator:  generateProse    → literary episode prose synthesized from both
 */
export async function runEpisode(prompt, { episodeNumber = 1, context = '' } = {}) {
  // 1. Save raw prompt
  const promptsDir = './store/prompts';
  saveFile(promptsDir, `${Date.now()}.txt`, prompt);

  // 2. Director call → casting decision + acting instructions + scene blueprint
  console.log('[Director] Casting character and generating scene blueprint…');
  const direction = await generateOutline(prompt, context);

  // Parse character name and acting instructions from the Director's output
  const characterNameMatch = direction.match(/\*\*Actor:\*\*\s*(.+)/);
  const characterName = characterNameMatch ? characterNameMatch[1].trim() : 'The Protagonist';

  const actingInstructionsMatch = direction.match(/### Acting Instructions\n([\s\S]*?)(?=###|$)/);
  const actingInstructions = actingInstructionsMatch ? actingInstructionsMatch[1].trim() : direction;

  const sceneBlueprintMatch = direction.match(/### Scene Blueprint[\s\S]*$/);
  const scenePlan = sceneBlueprintMatch ? sceneBlueprintMatch[0].trim() : direction;

  console.log(`[Actor] Performing as "${characterName}"…`);
  const performance = await performRole({ characterName, actingInstructions, scenePlan, context });

  // 3. Narrator call → literary episode prose
  console.log('[Narrator] Synthesizing direction and performance into literary prose…');
  const prose = await generateProse({ episodeNumber, scenePlan, actorPerformance: performance, context });

  // 4. Save episode
  const episodesDir = './store/episodes';
  saveFile(episodesDir, `${Date.now()}.txt`, prose);

  return prose;
}
