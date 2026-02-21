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
Narrator (main agent — OpenClaw session, gpt-5.2)
  │
  │  1. Reads context files: MEMORY.md + USER.md + last-episode.md
  │  2. Builds 3-section premise (Story Memory / Previous Episode / User Prompt)
  │  3. Writes premise to /tmp/oc-premise.txt
  │  4. Runs pipeline via bash ─────────────────────────────────────┐
  │                                                                  │
  │     ┌────────────────────────────────────────────────────────────┘
  │     ▼
  │   run_pipeline.py
  │     │
  │     ├─ Stage 1: Director (direct OpenAI API call → gpt-5-mini)
  │     │    → Reads USER.md for preferences
  │     │    → Returns: scene type, cast, acting instructions, blueprint
  │     │
  │     ├─ Stage 2: Actor × N (direct OpenAI API call → gpt-5-mini, once per cast member)
  │     │    → Reads USER.md for preferences
  │     │    → Returns: inner voice, actions, dialogue per character
  │     │
  │     └─ Output: /tmp/oc-pipeline.json (scene_plan + cast performances)
  │
  │  5. Synthesizes pipeline output into literary prose
  │  6. Delivers episode to user
  │  7. Saves episode to last-episode.md, updates MEMORY.md
  │  8. Every 2 episodes → /restart (clears conversation context)
  │
  ▼
Narrated Episode → Telegram
```

### Agent Roles

| Agent | How it runs | Model | Role |
|-------|-------------|-------|------|
| **Narrator** | OpenClaw session (main agent) | gpt-5.2 via OpenClaw | Orchestrates the story, writes final prose, manages memory and context resets |
| **Director** | Python function (`director.py`) called via `run_pipeline.py` | gpt-5-mini via OpenAI API | Plans scenes — cast, beats, emotional arc, hooks |
| **Actor** | Python function (`actor.py`) called via `run_pipeline.py` | gpt-5-mini via OpenAI API | Performs in-character — inner voice, dialogue, actions |

**Note:** Director and Actor are **not** OpenClaw sub-agents. They are direct OpenAI API calls (`helpers.call_llm()`) invoked from a Python pipeline script. The Narrator runs the pipeline via bash, reads the JSON output, and synthesizes it into final prose.

### Persistent Files (survive restarts)

| File | Purpose |
|------|---------|
| `workspace/MEMORY.md` | Story state — episode count, character roster, plot threads, episode summaries (~5k token cap) |
| `workspace/USER.md` | User preferences — tone, pacing, content boundaries (~1k token cap) |
| `workspace/last-episode.md` | Full text of the most recent episode (overwritten each episode) |

### Context Reset Protocol

The Narrator triggers `/restart` every 2 episodes to clear conversation context and save tokens:

1. After each episode: save full text to `last-episode.md`, update `MEMORY.md`
2. On episodes 2, 4, 6... → `/restart` clears the OpenClaw session
3. On restart: Narrator reads `MEMORY.md` + `USER.md` + `last-episode.md` and continues seamlessly
4. No conversation history is needed — all state lives in files

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

# Reset last episode
echo "(No episode yet)" > workspace/last-episode.md

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
│   ├── last-episode.md                    # Latest episode full text (survives restarts)
│   └── skills/
│       ├── director/
│       │   ├── run_pipeline.py            # Pipeline entry point (bash → Director → Actor → JSON)
│       │   ├── director.py                # Director: scene planning (OpenAI API call)
│       │   ├── actor.py                   # Actor: character performance (OpenAI API call)
│       │   ├── helpers.py                 # call_llm() — direct OpenAI API wrapper
│       │   └── store/episodes/            # Director's episode archive (timestamped files)
│       └── actor/
│           └── SKILL.md                   # Actor skill documentation
```
