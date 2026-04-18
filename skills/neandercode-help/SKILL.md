---
name: neandercode-help
description: >
  Quick-reference card for all neandercode modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /neandercode-help,
  "neandercode help", "what neandercode commands", "how do I use neandercode".
---

# Neandercode Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in neandercode style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | `/neandercode lite` | Drop filler. Keep sentence structure. |
| **Full** | `/neandercode` | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | `/neandercode ultra` | Extreme compression. Bare fragments. Tables over prose. |
| **Wenyan-Lite** | `/neandercode wenyan-lite` | Classical Chinese style, light compression. |
| **Wenyan-Full** | `/neandercode wenyan` | Full 文言文. Maximum classical terseness. |
| **Wenyan-Ultra** | `/neandercode wenyan-ultra` | Extreme. Ancient scholar on a budget. |

Mode stick until changed or session end.

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **neandercode-commit** | `/neandercode-commit` | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **neandercode-review** | `/neandercode-review` | One-line PR comments: `L42: bug: user null. Add guard.` |
| **neandercode-compress** | `/neandercode:compress <file>` | Compress .md files to neandercode prose. Saves ~46% input tokens. |
| **neandercode-help** | `/neandercode-help` | This card. |

## Deactivate

Say "stop neandercode" or "normal mode". Resume anytime with `/neandercode`.

## Configure Default Mode

Default mode = `full`. Change it:

**Environment variable** (highest priority):
```bash
export NEANDERCODE_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/neandercode/config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start. User can still activate manually with `/neandercode`.

Resolution: env var > config file > `full`.

## More

Full docs: https://github.com/ManjotS/neandercode
