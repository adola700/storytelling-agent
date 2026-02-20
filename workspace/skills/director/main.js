import { runEpisode } from './narrator.js';

const args = process.argv.slice(2);
const prompt = args.join(' ');

if (!prompt) {
  console.error('Usage: node main.js "<story prompt>"');
  process.exit(1);
}

runEpisode(prompt, { episodeNumber: 1 })
  .then(result => {
    console.log('\n=== Episode Output ===\n');
    console.log(result);
  })
  .catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
