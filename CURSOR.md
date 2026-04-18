# CLAUDE.md — neandercode

## README is a product artifact

README = product front door. Non-technical people read it to decide if neandercode worth install. Treat like UI copy.

**Rules for any README change:**

- Readable by non-AI-agent users. If you write "SessionStart hook injects system context," invisible to most — translate it.
- Keep Before/After examples first. That the pitch.
- Install table always complete + accurate. One broken install command costs real user.
- What You Get table must sync with actual code. Feature ships or removed → update table.
- Preserve voice. Neandercode speak in README on purpose. "Brain still big." "Cost go down forever." "One rock. That it." — intentional brand. Don't normalize.
- Benchmark numbers from real runs in `benchmarks/` and `evals/`. Never invent or round. Re-run if doubt.
- Adding new agent to install table → add detail block in `<details>` section below.
- Readability check before any README commit: would non-programmer understand + install within 60 seconds?

---

## Project overview

Neandercode makes AI coding agents respond in compressed neandercode-style prose — cuts ~65-75% output tokens, full technical accuracy. Ships as Codex plugin, Gemini CLI extension, agent rule files for Cursor, Windsurf, Cline, Copilot, 40+ others via `npx skills`.

---

## File structure and what owns what

### Single source of truth files — edit only these

| File | What it controls |
|------|-----------------|
| `skills/neandercode/SKILL.md` | Neandercode behavior: intensity levels, rules, wenyan mode, auto-clarity, persistence. Only file to edit for behavior changes. |
| `rules/neandercode-activate.md` | Always-on auto-activation rule body. CI injects into Cursor, Windsurf, Cline, Copilot rule files. Edit here, not agent-specific copies. |
| `skills/neandercode-commit/SKILL.md` | Neandercode commit message behavior. Fully independent skill. |
| `skills/neandercode-review/SKILL.md` | Neandercode code review behavior. Fully independent skill. |
| `skills/neandercode-help/SKILL.md` | Quick-reference card. One-shot display, not a persistent mode. |
| `neandercode-compress/SKILL.md` | Compress sub-skill behavior. |

### Auto-generated / auto-synced — do not edit directly

Overwritten by CI on push to main when sources change. Edits here lost.

| File | Synced from |
|------|-------------|
| `neandercode/SKILL.md` | `skills/neandercode/SKILL.md` |
| `plugins/neandercode/skills/neandercode/SKILL.md` | `skills/neandercode/SKILL.md` |
| `.cursor/skills/neandercode/SKILL.md` | `skills/neandercode/SKILL.md` |
| `.windsurf/skills/neandercode/SKILL.md` | `skills/neandercode/SKILL.md` |
| `neandercode.skill` | ZIP of `skills/neandercode/` directory |
| `.clinerules/neandercode.md` | `rules/neandercode-activate.md` |
| `.github/copilot-instructions.md` | `rules/neandercode-activate.md` |
| `.cursor/rules/neandercode.mdc` | `rules/neandercode-activate.md` + Cursor frontmatter |
| `.windsurf/rules/neandercode.md` | `rules/neandercode-activate.md` + Windsurf frontmatter |

---

## CI sync workflow

`.github/workflows/sync-skill.yml` triggers on main push when `skills/neandercode/SKILL.md` or `rules/neandercode-activate.md` changes.

What it does:
1. Copies `skills/neandercode/SKILL.md` to all agent-specific SKILL.md locations
2. Rebuilds `neandercode.skill` as a ZIP of `skills/neandercode/`
3. Rebuilds all agent rule files from `rules/neandercode-activate.md`, prepending agent-specific frontmatter (Cursor needs `alwaysApply: true`, Windsurf needs `trigger: always_on`)
4. Commits and pushes with `[skip ci]` to avoid loops

CI bot commits as `github-actions[bot]`. After PR merge, wait for workflow before declaring release complete.

---

## Skill system

Skills = Markdown files with YAML frontmatter consumed by `npx skills` for other agents.

### Intensity levels

Defined in `skills/neandercode/SKILL.md`. Six levels: `lite`, `full` (default), `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`. Persists until changed or session ends.

### Auto-clarity rule

Neandercode drops to normal prose for: security warnings, irreversible action confirmations, multi-step sequences where fragment ambiguity risks misread, user confused or repeating question. Resumes after. Defined in skill — preserve in any SKILL.md edit.

### neandercode-compress

Sub-skill in `neandercode-compress/SKILL.md`. Takes file path, compresses prose to neandercode style, writes to original path, saves backup at `<filename>.original.md`. Validates headings, code blocks, URLs, file paths, commands preserved. Retries up to 2 times on failure with targeted patches only. Requires Python 3.10+.

### neandercode-commit / neandercode-review

Independent skills in `skills/neandercode-commit/SKILL.md` and `skills/neandercode-review/SKILL.md`. Both have own `description` and `name` frontmatter so they load independently. neandercode-commit: Conventional Commits, ≤50 char subject. neandercode-review: one-line comments in `L<line>: <severity> <problem>. <fix>.` format.

---

## Agent distribution

How neandercode reaches each agent type:

| Agent | Mechanism | Auto-activates? |
|-------|-----------|----------------|
| Codex | Plugin in `plugins/neandercode/` plus repo `.codex/hooks.json` and `.codex/config.toml` | Yes on macOS/Linux — SessionStart hook |
| Gemini CLI | Extension with `GEMINI.md` context file | Yes — context file loads every session |
| Cursor | `.cursor/rules/neandercode.mdc` with `alwaysApply: true` | Yes — always-on rule |
| Windsurf | `.windsurf/rules/neandercode.md` with `trigger: always_on` | Yes — always-on rule |
| Cline | `.clinerules/neandercode.md` (auto-discovered) | Yes — Cline injects all .clinerules files |
| Copilot | `.github/copilot-instructions.md` + `AGENTS.md` | Yes — repo-wide instructions |
| Others | `npx skills add ManjotS/neandercode` | No — user must say `/neandercode` each session |

For agents without hook systems, minimal always-on snippet lives in README under "Want it always on?" — keep current with `rules/neandercode-activate.md`.

---

## Evals

`evals/` has three-arm harness:
- `__baseline__` — no system prompt
- `__terse__` — `Answer concisely.`
- `<skill>` — `Answer concisely.\n\n{SKILL.md}`

Honest delta = **skill vs terse**, not skill vs baseline. Baseline comparison conflates skill with generic terseness — that cheating. Harness designed to prevent this.

`llm_run.py` calls `cursor agent -p ...` per (prompt, arm), saves to `evals/snapshots/results.json`. `measure.py` reads snapshot offline with tiktoken (OpenAI BPE — tokenizer approximation, ratios meaningful, absolute numbers approximate).

Add skill: drop `skills/<name>/SKILL.md`. Harness auto-discovers. Add prompt: append line to `evals/prompts/en.txt`.

Snapshots committed to git. CI reads without API calls. Only regenerate when SKILL.md or prompts change.

---

## Benchmarks

`benchmarks/` runs prompts through **`cursor agent -p`**, then scores output length with **tiktoken** (`o200k_base`) — same approximation idea as `evals/`. Results committed as JSON in `benchmarks/results/`. Benchmark table in README generated from results — update when regenerating.

To reproduce: install deps (`pip install -r benchmarks/requirements.txt` or `uv pip install -r benchmarks/requirements.txt`), ensure `cursor` is on PATH, then `uv run python benchmarks/run.py`. If the agent fails to start, run **`cursor agent update`**.

---

## Key rules for agents working here

- Edit `skills/neandercode/SKILL.md` for behavior changes. Never edit synced copies.
- Edit `rules/neandercode-activate.md` for auto-activation rule changes. Never edit agent-specific rule copies.
- README most important file for user-facing impact. Optimize for non-technical readers. Preserve neandercode voice.
- Benchmark and eval numbers must be real. Never fabricate or estimate.
- CI workflow commits back to main after merge. Account for when checking branch state.
