import fs from 'fs';
import path from 'path';

// ensure directory exists
export function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// save file
export function saveFile(dir, filename, content) {
  ensureDir(dir);
  const filePath = path.join(dir, filename);
  fs.writeFileSync(filePath, content, 'utf8');
  return filePath;
}

// call GPT-5 via OpenAI API (reads OPENAI_API_KEY from env)
export async function callLLM({ system, user, model = 'gpt-5-chat-latest' }) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('OPENAI_API_KEY is not set');

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user },
      ],
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`OpenAI API error ${response.status}: ${err}`);
  }

  const data = await response.json();
  return { text: data.choices[0].message.content };
}

// merge outline + scenes (kept for compatibility)
export function mergeEpisode(outline, scenes) {
  return `--- STORY OUTLINE ---\n${outline}\n\n--- SCENES ---\n${scenes.join('\n\n')}\n`;
}
