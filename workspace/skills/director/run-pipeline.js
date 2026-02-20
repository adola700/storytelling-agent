import { generateOutline } from './director.js';
import { performRole } from './actor.js';
import fs from 'fs';

const premiseFile = process.argv[2];
const contextFile = process.argv[3];
const outputFile = process.argv[4] || '/tmp/oc-pipeline.json';

if (!premiseFile) {
  console.error('\n╔══════════════════════════════════════════════════════════════════════════════╗');
  console.error('║                              USAGE ERROR                                     ║');
  console.error('╠══════════════════════════════════════════════════════════════════════════════╣');
  console.error('║ Usage: node run-pipeline.js <premise-file> <context-file> [output-file]     ║');
  console.error('║                                                                              ║');
  console.error('║ Arguments:                                                                   ║');
  console.error('║   premise-file  : Path to file containing the story premise (required)      ║');
  console.error('║   context-file  : Path to file containing context (required)                ║');
  console.error('║   output-file   : Path for JSON output (optional, default: /tmp/oc-*.json)  ║');
  console.error('╚══════════════════════════════════════════════════════════════════════════════╝\n');
  process.exit(1);
}

try {
  console.log('\n╔══════════════════════════════════════════════════════════════════════════════╗');
  console.log('║                        STORYTELLING PIPELINE START                           ║');
  console.log('╚══════════════════════════════════════════════════════════════════════════════╝\n');

  const premise = fs.readFileSync(premiseFile, 'utf8').trim();
  const context = contextFile && fs.existsSync(contextFile)
    ? fs.readFileSync(contextFile, 'utf8').trim()
    : '';

  console.log('📄 INPUT:');
  console.log('─'.repeat(80));
  console.log(`Premise: ${premise.substring(0, 150)}${premise.length > 150 ? '...' : ''}`);
  if (context) {
    console.log(`Context: ${context.substring(0, 150)}${context.length > 150 ? '...' : ''}`);
  }
  console.log('─'.repeat(80));
  console.log('');

  // ── Stage 1: Director ────────────────────────────────────────────────────────
  console.log('\n┌─────────────────────────────────────────────────────────────────────────────┐');
  console.log('│ STAGE 1: DIRECTOR - Scene Planning                                          │');
  console.log('└─────────────────────────────────────────────────────────────────────────────┘');
  console.log('🎬 Calling Director LLM (OpenAI)...\n');

  const direction = await generateOutline(premise, context);

  console.log(`✓ Scene plan received (${direction.length} characters)`);

  // Parse character name — handles multiple Director output formats:
  //   Format A: **Actor:** Elena
  //   Format B: ### **Cast**\n- **Elena Marquéz – role**  (GPT-5 actual output)
  //   Format C: ## Cast\n- **Elena (Chef)**
  const characterNameMatch =
    direction.match(/\*\*Actor:\*\*\s*([^\n]+)/) ||
    direction.match(/Cast[\s\S]{0,150}?-\s*\*\*([^*\n]+)\*\*/);
  let characterName = 'The Protagonist';
  if (characterNameMatch) {
    characterName = characterNameMatch[1]
      .split(/\s+[-–—(]/)[0]  // strip "– role" or "(role)" suffix
      .trim();
  }

  console.log(`🎭 Character Cast: ${characterName}`);
  
  // Parse acting instructions — robust to "### **Acting Instructions**" and "### Acting Instructions"
  const actingInstructionsMatch =
    direction.match(/Acting Instructions[\s\S]{0,10}\n([\s\S]*?)(?=---|\n#{2,3}|$)/);
  const actingInstructions = actingInstructionsMatch ? actingInstructionsMatch[1].trim() : direction;

  console.log('\n📋 SCENE PLAN PREVIEW:');
  console.log('─'.repeat(80));
  const preview = direction.substring(0, 300).replace(/\n/g, '\n   ');
  console.log(`   ${preview}${direction.length > 300 ? '\n   ...' : ''}`);
  console.log('─'.repeat(80));

  // Pass the full Director output as scene_plan so the Narrator gets everything
  const scenePlan = direction;

  // ── Stage 2: Actor ───────────────────────────────────────────────────────────
  console.log('\n┌─────────────────────────────────────────────────────────────────────────────┐');
  console.log('│ STAGE 2: ACTOR - Character Performance                                      │');
  console.log('└─────────────────────────────────────────────────────────────────────────────┘');
  console.log(`🎭 Performing as: ${characterName}`);
  console.log('🎬 Calling Actor LLM (OpenAI)...\n');

  const performance = await performRole({ characterName, actingInstructions, scenePlan, context });

  console.log(`✓ Performance received (${performance.length} characters)`);

  console.log('\n🎪 PERFORMANCE PREVIEW:');
  console.log('─'.repeat(80));
  const perfPreview = performance.substring(0, 300).replace(/\n/g, '\n   ');
  console.log(`   ${perfPreview}${performance.length > 300 ? '\n   ...' : ''}`);
  console.log('─'.repeat(80));

  // ── Write output ─────────────────────────────────────────────────────────────
  const result = {
    character_name: characterName,
    acting_instructions: actingInstructions,
    scene_plan: scenePlan,
    actor_performance: performance,
  };

  fs.writeFileSync(outputFile, JSON.stringify(result, null, 2), 'utf8');

  console.log('\n╔══════════════════════════════════════════════════════════════════════════════╗');
  console.log('║                           PIPELINE COMPLETE ✓                                ║');
  console.log('╠══════════════════════════════════════════════════════════════════════════════╣');
  console.log(`║ Character:        ${characterName.padEnd(60, ' ')} ║`);
  console.log(`║ Scene Plan:       ${direction.length.toString().padEnd(10, ' ')} characters${' '.repeat(49)} ║`);
  console.log(`║ Performance:      ${performance.length.toString().padEnd(10, ' ')} characters${' '.repeat(49)} ║`);
  console.log(`║ Output File:      ${outputFile.padEnd(60, ' ')} ║`);
  console.log('╚══════════════════════════════════════════════════════════════════════════════╝\n');
  
  process.exit(0);
} catch (err) {
  console.error('\n╔══════════════════════════════════════════════════════════════════════════════╗');
  console.error('║                              PIPELINE ERROR ✗                                ║');
  console.error('╠══════════════════════════════════════════════════════════════════════════════╣');
  console.error(`║ ${err.message.substring(0, 76).padEnd(76, ' ')} ║`);
  console.error('╚══════════════════════════════════════════════════════════════════════════════╝\n');
  console.error('Stack trace:', err.stack);
  process.exit(1);
}
