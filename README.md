# ACT271-TI: Vibe Coding with Claude Code

> 2-day hands-on training for Texas Instruments — Kuala Lumpur

## Quick Start

```bash
# Clone and enter the repo
git clone https://github.com/datatweets/ti-vibe-coding.git
cd ti-vibe-coding

# Launch Claude Code
claude
```

## Course Structure

| Day | Modules | Focus |
|-----|---------|-------|
| Day 1 AM | M1–M4 | Foundations: vibe coding, prompting, CLI deep dive |
| Day 1 PM | M5–M8 | Coding: automation, Lab 1 scaffold, refactor, QA |
| Day 2 AM | M9–M12 | DevOps & Agents: CI/CD, subagents, Lab 2 assistant loop |
| Day 2 PM | M13–M16 | Advanced: parallel tasks, production patterns, Lab 3 sprint |

## Labs

| Lab | Module | What You Build |
|-----|--------|----------------|
| Lab 1 | M6 | Scaffold `my-sensor-toolkit` from scratch — validators, cleaners, analyzers, tests |
| Lab 2 | M12 | Complete assistant loop — observe → plan → implement → test → review → ship |
| Lab 3 | M15 | 60-min feature sprint — Track A: REST API / Track B: report pipeline |

## Repo Layout

```
ti-vibe-coding/
├── CLAUDE.md                 # Project context for Claude Code
├── README.md                 # This file
├── .claude/
│   ├── settings.json         # Pre-configured permissions
│   ├── commands/             # Custom slash commands (Module 4)
│   └── agents/               # Subagent definitions (Module 10)
├── src/
│   └── data/                 # Sample sensor datasets (CSV)
│       ├── sensor_readings_1000.csv
│       ├── sensor_readings_dirty.csv
│       └── README.md
├── labs/
│   ├── lab1_scaffold/        # Lab 1: create my-sensor-toolkit here
│   ├── lab2_assistant/       # Lab 2: mini assistant loop
│   └── lab3_sprint/          # Lab 3: full feature sprint
├── .github/
│   └── workflows/            # CI/CD templates (Module 9)
└── .gitignore
```

## Sample Data

`src/data/` contains synthetic sensor datasets:

- **sensor_readings_1000.csv** — 1,000 clean readings from 5 sensors (for learning)
- **sensor_readings_dirty.csv** — 200 readings with nulls, outliers, duplicates, bad IDs (for testing validation)

### Data Schema

| Column | Type | Valid Range | Description |
|--------|------|-------------|-------------|
| timestamp | ISO 8601 | — | Reading timestamp |
| sensor_id | string | TI-XXXX | Sensor identifier |
| temperature | float | -40 to 150 °C | Ambient temperature |
| pressure | float | 0 to 1000 hPa | Atmospheric pressure |
| humidity | float | 0 to 100 % | Relative humidity |

## Prerequisites

- Python 3.10+
- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Git
- VS Code (recommended)

## Trainer

Mehdi Allahyari — Abundent Academy | HRDF Certified Training Provider
