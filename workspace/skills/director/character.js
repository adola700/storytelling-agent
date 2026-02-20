import { callLLM } from './helpers.js';

export async function getLines(character, outline) {
  const { text } = await callLLM({
    system: `You are ${character}, a character in this story world. Respond in your unique tone but consistent with the plot outline provided.`,
    user: `Using this outline, produce the narration or dialogue for ${character}.\nOutline:\n${outline}`
  });

  return text;
}