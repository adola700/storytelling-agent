# 📖 Storytelling Agent — OpenClaw Multi-Agent System

A multi-agent storytelling system built on [OpenClaw](https://openclaw.ai) that collaboratively generates episodic stories via Telegram. One OpenClaw endpoint = one story.

## Architecture

```
User (Telegram)
    │
    ▼
┌─────────────────────────────────────┐
│  OpenClaw Gateway                   │
│                                     │
│  🎙️ Narrator (main agent)           │
│    ├── spawns 🎬 Director            │
│    │     └── returns scene plan      │
│    ├── spawns 🎭 Actor(s)            │
│    │     └── returns dialogue        │
│    ├── reads/writes MEMORY.md        │
│    └── delivers narrated episode     │
│                                     │
│  ⏰ Heartbeat (3 min, once only)     │
│    └── nudges idle user (once)       │
└─────────────────────────────────────┘
```

### Agent Roles

| Agent | Type | Role |
|-------|------|------|
| **Narrator** | Main session | Orchestrates the story, narrates episodes, manages memory |
| **Director** | Spawned sub-agent | Plans scenes — setting, beats, emotional arc, hooks |
| **Actor** | Spawned sub-agent | Generates in-character dialogue and actions |

## Prerequisites

- **Node.js** v22+ (required for OpenClaw 2026)
- **OpenClaw** installed globally: `npm install -g openclaw`
- **Telegram Bot** created via [@BotFather](https://t.me/BotFather) — save the bot token
- **Telegram User ID** — get it from [@userinfobot](https://t.me/userinfobot)
- **OpenAI API Key** (GPT-5.1) — already configured in `openclaw.json`

## Quick Start

### 1. Clone & Enter

```bash
git clone <your-repo-url>
cd storytelling-agent
```

### 2. Install OpenClaw

```bash
npm install -g openclaw
```

### 3. Run Onboarding

```bash
openclaw onboard
```

During onboarding:
- Select **Telegram** as your channel
- Enter your **Telegram Bot Token** (from @BotFather)
- Enter your **Telegram User ID** (from @userinfobot)
- When asked about workspace, point to the `./workspace` directory in this repo

### 4. Copy Configuration

Copy the provided `openclaw.json` to your OpenClaw config directory:

```bash
cp openclaw.json ~/.openclaw/openclaw.json
```

> **Note**: If you already have an `openclaw.json`, merge the settings manually. The key settings are the `cron` job for heartbeat and the `agents.defaults` for sub-agent support.

### 5. Start the Gateway

```bash
openclaw gateway start
```

To see live logs:
```bash
tail -f ~/.openclaw/logs/gateway.log
```

### 6. Chat on Telegram
...
### 7. Test in Terminal (Optional)
```bash
openclaw agent --message "Start a story..." --agent main
```

Open your Telegram bot and send a story prompt:

> *"Give me a story of a lonely island with peacocks as the only animal on it and someone trapped."*

The Narrator will orchestrate Director + Actor agents behind the scenes and deliver a beautifully narrated episode.

## Usage

### Start a Story
Send any story premise. The Narrator will create Episode 1.

### Continue
Say "continue", "next", or ask what happens next. A new episode is created.

### Refine / Rewrite
Say "rewrite", "change", or give feedback on the current episode. The Narrator rewrites it.

### Guide the Story
Say things like *"I want more mystery"* or *"make the protagonist braver"*. The Narrator records this in memory and follows it in future episodes.

### Idle Nudge
If you're inactive for 3+ minutes during an active story, the Narrator sends **one** gentle nudge asking if you'd like to continue. It won't nag — only one nudge until you respond.

## Project Structure

```
storytelling-agent/
├── openclaw.json              # Gateway config (model, cron, sub-agents)
├── README.md                  # This file
└── workspace/
    ├── SOUL.md                # Narrator personality & orchestration logic
    ├── IDENTITY.md            # Narrator identity (name, emoji, vibe)
    ├── AGENTS.md              # Safety rules & tool permissions
    ├── TOOLS.md               # Available tools reference
    ├── HEARTBEAT.md           # 3-min idle check (single nudge only)
    ├── USER.md                # User profile (populated over time)
    ├── MEMORY.md              # Story state, episodes, preferences
    ├── memory/                # Daily interaction logs (auto-generated)
    └── skills/
        ├── director/
        │   └── SKILL.md       # Scene planning sub-agent
        └── actor/
            └── SKILL.md       # Character dialogue sub-agent
```

## Configuration

Key settings in `openclaw.json`:

| Setting | Value | Purpose |
|---------|-------|---------|
| `agent.model` | `openai/gpt-5.1` | LLM model |
| `agent.thinking` | `null` | No extended thinking |
| `cron[0].schedule` | `*/3 * * * *` | 3-min heartbeat |
| `agents.defaults.subagents.allowAgents` | `["*"]` | Allow spawning any sub-agent |

## License

MIT
