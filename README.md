# Storytelling Agent — OpenClaw Multi-Agent System

A multi-agent storytelling system built on [OpenClaw](https://openclaw.ai) that generates immersive, episodic stories via Telegram.

## Architecture

```
User (Telegram)
  │
  ▼
OpenClaw Gateway
  │
  ▼
Narrator (main agent — OpenClaw session, Claude Sonnet 4.6)
  │
  │  1. Reads context files: MEMORY.md + USER.md
  │  2. Builds 2-section premise (Story Memory / User Prompt)
  │  3. Writes premise to /tmp/oc-premise.txt
  │  4. Runs pipeline via bash ─────────────────────────────────────┐
  │                                                                  │
  │     ┌────────────────────────────────────────────────────────────┘
  │     ▼
  │   run_pipeline.py
  │     │
  │     ├─ Stage 1: Director (API call → Claude Sonnet 4.6)
  │     │    → Reads USER.md for preferences
  │     │    → Returns: scene type, cast, acting instructions, blueprint
  │     │
  │     ├─ Stage 2: Actor × N (API call → Claude Sonnet 4.6, once per cast member)
  │     │    → Reads USER.md for preferences
  │     │    → Returns: inner voice, actions, dialogue per character
  │     │
  │     └─ Output: /tmp/oc-pipeline.json (scene_plan + cast performances)
  │
  │  5. Checks context: if >30k tokens or >2 episodes in context → compact first
  │  6. Synthesizes pipeline output into literary prose
  │  7. Delivers episode to user
  │  8. Updates MEMORY.md
  │
  ▼
Narrated Episode → Telegram
```

### Agent Roles

| Agent | How it runs | Model | Role |
|-------|-------------|-------|------|
| **Narrator** | OpenClaw session (main agent) | Claude Sonnet 4.6 via OpenClaw | Orchestrates the story, writes final prose, manages memory and context compaction |
| **Director** | Python function (`director.py`) called via `run_pipeline.py` | Claude Sonnet 4.6 via Anthropic API | Plans scenes — cast, beats, emotional arc, hooks |
| **Actor** | Python function (`actor.py`) called via `run_pipeline.py` | Claude Sonnet 4.6 via Anthropic API | Performs in-character — inner voice, dialogue, actions |

**Note:** Director and Actor are **not** OpenClaw sub-agents. They are Anthropic API calls (`helpers.call_llm()`) invoked from a Python pipeline script. The Narrator runs the pipeline via bash, reads the JSON output, and synthesizes it into final prose.

### Persistent Files (survive restarts)

| File | Purpose |
|------|---------|
| `workspace/MEMORY.md` | Story state — episode count, character roster, plot threads, episode summaries (~5k token cap) |
| `workspace/USER.md` | User preferences — tone, pacing, content boundaries (~1k token cap) |

### Context Management — Compaction

The Narrator compacts conversation context **before** generating an episode if either condition is met:

1. **Input tokens exceed 30k** — context window is filling up
2. **More than 2 episodes in conversation context** — e.g., before Episode 3, episodes 1+2 are still in context

When triggered, the Narrator runs:
```bash
python3 /root/storytelling-agent/workspace/tools/compact.py --keep-last 6
```

This auto-generates a summary from `MEMORY.md` + `USER.md` and trims the session JSONL (~85% token reduction), keeping only the last 6 conversation turns.

After each episode, the Narrator updates `MEMORY.md` with the episode summary. MEMORY.md is the single source of story continuity — conversation history is disposable.

---

## Setup

### Prerequisites
- **Node.js** v22+
- **Telegram Bot Token** via [@BotFather](https://t.me/BotFather)
- **Telegram User ID** via [@userinfobot](https://t.me/userinfobot)
- **OpenAI API Key** (configured in `openclaw.json`)

### Install & Configure
```bash
npm install -g openclaw
git clone <repository-url>
cd storytelling-agent

# Run onboarding — select Telegram, provide bot token and user ID
openclaw onboard
```

Copy the project config:
```bash
cp openclaw.json ~/.openclaw/openclaw.json
```

### Run
```bash
openclaw gateway start
```

Monitor logs:
```bash
tail -f ~/.openclaw/logs/gateway.log
```

---

## Usage

- **Start a story**: Send any prompt — *"A detective story set in a flooded London."*
- **Continue**: *"next"* or *"what happens next?"*
- **Rewrite**: *"no, make it darker"* or *"rewrite the last part"*
- **New story**: *"new story"* or send an unrelated prompt

The Narrator starts immediately — no clarifying questions.

---

## Reset (Fresh Start)

```bash
# Reset story memory
cat <<'EOF' > workspace/MEMORY.md
# Story Memory

## Active Story
- **Status**: Idle
- **Episode Count**: 0

## Character Roster
(none yet)

## Episode Log
(none yet)

## Open Threads
(none yet)
EOF

# Restart gateway
openclaw gateway stop
openclaw gateway start
```

---

## Project Structure

```
storytelling-agent/
├── openclaw.json                          # Gateway config (model, channels, tools)
├── workspace/
│   ├── SOUL.md                            # Narrator instructions + orchestration protocol
│   ├── AGENTS.md                          # Safety rules, memory policies, context reset docs
│   ├── MEMORY.md                          # Persistent story state (survives restarts)
│   ├── USER.md                            # User preferences (read by all agents)
│   ├── tools/
│   │   └── compact.py                     # Context compaction script (~85% token reduction)
│   └── skills/
│       ├── director/
│       │   ├── run_pipeline.py            # Pipeline entry point (bash → Director → Actor → JSON)
│       │   ├── director.py                # Director: scene planning (Anthropic API call)
│       │   ├── actor.py                   # Actor: character performance (Anthropic API call)
│       │   ├── helpers.py                 # call_llm() — Anthropic API wrapper
│       │   └── store/episodes/            # Director's episode archive (timestamped files)
│       └── actor/
│           └── SKILL.md                   # Actor skill documentation
```
