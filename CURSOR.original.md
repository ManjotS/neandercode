# CLAUDE.md — neandercode

## README is a product artifact

The README is not documentation. It is the product's front door — the thing non-technical people read to decide if neandercode is worth installing. Treat it with the same care you would treat UI copy.

**Rules for any README change:**

- Every sentence must be readable by someone who has never used an AI coding agent. If you write "SessionStart hook injects system context," that is invisible to most users — translate it.
- Keep the Before/After examples as the first thing users see. They are the entire pitch.
- The install table must always be complete and accurate. One broken install command costs a real user.
- The feature matrix (What You Get table) must stay in sync with what the code actually does. If a feature ships or is removed, update the table.
- Preserve the voice. Neandercode speak in README on purpose. "Brain still big." "Cost go down forever." "One rock. That it." — this is intentional brand. Don't normalize it.
- Benchmark numbers come from real runs in `benchmarks/` and `evals/`. Never invent or round numbers. Re-run if in doubt.
- When adding a new agent to the install table, always add the corresponding detail block in the `<details>` section below it.
- Readability check before any README commit: would a non-programmer understand what this does and how to install it within 60 seconds of reading?

---

## Project overview

Neandercode makes AI coding agents respond in compressed, neandercode-style prose — cutting ~65-75% of output tokens while keeping full technical accuracy. It ships as a a Codex plugin, a Gemini CLI extension, and as agent rule files for Cursor, Windsurf, Cline, Copilot, and 40+ others via `npx skills`.

---

## File structure and what owns what

### Single source of truth files — edit only these

| File | What it controls |
|------|-----------------|
| `skills/neandercode/SKILL.md` | Neandercode behavior: intensity levels, rules, wenyan mode, auto-clarity, persistence. This is the only file to edit for neandercode behavior changes. |
| `rules/neandercode-activate.md` | The body of the always-on auto-activation rule. Injected into Cursor, Windsurf, Cline, and Copilot rule files by CI. Edit here, not in the agent-specific copies. |
| `skills/neandercode-commit/SKILL.md` | Neandercode commit message behavior. Fully independent skill. |
| `skills/neandercode-review/SKILL.md` | Neandercode code review behavior. Fully independent skill. |
| `neandercode-compress/SKILL.md` | Compress sub-skill behavior. |

### Auto-generated / auto-synced — do not edit directly

These files are overwritten by CI on every push to main that touches the sources above. Edits here will be lost.

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

`.github/workflows/sync-skill.yml` triggers on push to main when `skills/neandercode/SKILL.md` or `rules/neandercode-activate.md` changes.

What it does:
1. Copies `skills/neandercode/SKILL.md` to all agent-specific SKILL.md locations
2. Rebuilds `neandercode.skill` as a ZIP of `skills/neandercode/`
3. Rebuilds all agent rule files from `rules/neandercode-activate.md`, prepending the agent-specific frontmatter (Cursor needs `alwaysApply: true`, Windsurf needs `trigger: always_on`)
4. Commits and pushes with `[skip ci]` to avoid loops

The CI bot commits as `github-actions[bot]`. After a PR merges, wait for this workflow before declaring the release complete.

---

## Skill system

Skills are Markdown files with YAML frontmatter consumed by `npx skills` for other agents.

### Intensity levels

Defined in `skills/neandercode/SKILL.md`. Six levels: `lite`, `full` (default), `ultra`, `wenyan-lite`, `wenyan-full`, `wenyan-ultra`. Level persists until changed or session ends.

### Auto-clarity rule

Neandercode drops to normal prose automatically for: security warnings, irreversible action confirmations, multi-step sequences where fragment ambiguity risks misread, and when the user is confused or repeats a question. Resumes after the clear part. This is defined in the skill and must be preserved in any SKILL.md edit.

### neandercode-compress

Sub-skill in `neandercode-compress/SKILL.md`. Takes a file path, compresses natural-language prose to neandercode style, writes the compressed version to the original path, and saves a human-readable backup at `<filename>.original.md`. Validation step checks that headings, code blocks, URLs, file paths, and commands are preserved exactly. Retries up to 2 times on validation failure with targeted patches only (no full recompression). Requires Python 3.10+.

### neandercode-commit / neandercode-review

Independent skills in `skills/neandercode-commit/SKILL.md` and `skills/neandercode-review/SKILL.md`. Both have their own `description` and `name` frontmatter fields so they load independently. neandercode-commit generates Conventional Commits format with ≤50 char subject. neandercode-review outputs one-line comments in `L<line>: <severity> <problem>. <fix>.` format.

---

## Agent distribution

How neandercode reaches each agent type:

| Agent | Mechanism | Auto-activates? |
|-------|-----------|----------------|
| Codex | Plugin in `plugins/neandercode/` with `hooks.json` | Yes — SessionStart hook |
| Gemini CLI | Extension with `GEMINI.md` context file | Yes — context file loads every session |
| Cursor | `.cursor/rules/neandercode.mdc` with `alwaysApply: true` | Yes — always-on rule |
| Windsurf | `.windsurf/rules/neandercode.md` with `trigger: always_on` | Yes — always-on rule |
| Cline | `.clinerules/neandercode.md` (auto-discovered) | Yes — Cline injects all .clinerules files |
| Copilot | `.github/copilot-instructions.md` + `AGENTS.md` | Yes — repo-wide instructions |
| Others | `npx skills add ManjotS/neandercode` | No — user must say `/neandercode` each session |

For agents without hook systems, the minimal always-on snippet lives in README under "Want it always on?" — keep it current with `rules/neandercode-activate.md`.

---

## Evals

`evals/` has a three-arm harness:
- `__baseline__` — no system prompt
- `__terse__` — `Answer concisely.`
- `<skill>` — `Answer concisely.\n\n{SKILL.md}`

The honest delta for any skill is **skill vs terse**, not skill vs baseline. Baseline comparison conflates the skill with generic terseness — that is cheating. The harness is designed to prevent this.

`llm_run.py` calls `cursor agent -p ...` per (prompt, arm), saves output to `evals/snapshots/results.json`. Requires **`cursor agent login`** or **`CURSOR_API_KEY`**. `measure.py` reads the snapshot offline with tiktoken (OpenAI BPE — tokenizer approximation, ratios are meaningful, absolute numbers are approximate).

To add a skill: drop `skills/<name>/SKILL.md`. The harness auto-discovers it. To add a prompt: append a line to `evals/prompts/en.txt`.

Snapshots are committed to git. CI reads them without API calls. Only regenerate the snapshot when SKILL.md files or prompts change.

---

## Benchmarks

`benchmarks/` runs prompts through **`cursor agent -p`**, then scores output with **tiktoken** (`o200k_base`). Results are committed as JSON in `benchmarks/results/`. The benchmark table in README is generated from these results — update it when regenerating.

To reproduce: install `benchmarks/requirements.txt`, ensure `cursor` is on PATH, then `uv run python benchmarks/run.py`. If the agent fails, run **`cursor agent update`**.

---

## Key rules for agents working here

- Edit `skills/neandercode/SKILL.md` for behavior changes. Never edit synced copies.
- Edit `rules/neandercode-activate.md` for auto-activation rule changes. Never edit agent-specific rule copies.
- The README is the most important file in the repo for user-facing impact. Optimize it for non-technical readers. Preserve the neandercode voice.
- Benchmark and eval numbers must be real. Never fabricate or estimate them.
- The CI workflow commits back to main after merge. Account for this when checking branch state.
- Hook files must silent-fail on all filesystem errors. Never let a hook crash block session start.
