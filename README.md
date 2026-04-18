<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/rock_1faa8.png" width="120" />
</p>

<h1 align="center">neandercode</h1>

<p align="center">
  <strong>why use many token when few do trick</strong>
</p>

<p align="center">
  <a href="https://github.com/ManjotS/neandercode/stargazers"><img src="https://img.shields.io/github/stars/ManjotS/neandercode?style=flat&color=yellow" alt="Stars"></a>
  <a href="https://github.com/ManjotS/neandercode/commits/main"><img src="https://img.shields.io/github/last-commit/ManjotS/neandercode?style=flat" alt="Last Commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ManjotS/neandercode?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="#before--after">Before/After</a> •
  <a href="#install">Install</a> •
  <a href="#intensity-levels">Levels</a> •
  <a href="#neandercode-skills">Skills</a> •
  <a href="#benchmarks">Benchmarks</a> •
  <a href="#evals">Evals</a>
</p>

---

A [Cursor](https://cursor.com) rule/skills/commands set that makes the agent talk like neandercode — cutting **~75% of output tokens** while keeping full technical accuracy. Now with [文言文 mode](#文言文-wenyan-mode), [terse commits](#neandercode-commit), [one-line code reviews](#neandercode-review), and a [compression tool](#neandercode-compress) that cuts **~46% of input tokens** every session.

Based on the viral observation that neandercode-speak dramatically reduces LLM token usage without losing technical substance. So we made it a one-line install.

## Before / After

<table>
<tr>
<td width="50%">

### 🗣️ Normal Agent (69 tokens)

> "The reason your React component is re-rendering is likely because you're creating a new object reference on each render cycle. When you pass an inline object as a prop, React's shallow comparison sees it as a different object every time, which triggers a re-render. I'd recommend using useMemo to memoize the object."

</td>
<td width="50%">

### 🪨 Neandercode Agent (19 tokens)

> "New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."

</td>
</tr>
<tr>
<td>

### 🗣️ Normal Agent

> "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix."

</td>
<td>

### 🪨 Neandercode Agent

> "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

</td>
</tr>
</table>

**Same fix. 75% less word. Brain still big.**

**Pick your level of grunt:**

<table>
<tr>
<td width="25%">

#### 🪶 Lite

> "Your component re-renders because you create a new object reference each render. Inline object props fail shallow comparison every time. Wrap it in `useMemo`."

</td>
<td width="25%">

#### 🪨 Full

> "New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`."

</td>
<td width="25%">

#### 🔥 Ultra

> "Inline obj prop → new ref → re-render. `useMemo`."

</td>
<td width="25%">

#### 📜 文言文

> "物出新參照，致重繪。useMemo Wrap之。"

</td>
</tr>
</table>

**Same answer. You pick how many word.**

```
┌─────────────────────────────────────┐
│  TOKENS SAVED          ████████ 75% │
│  TECHNICAL ACCURACY    ████████ 100%│
│  SPEED INCREASE        ████████ ~3x │
│  VIBES                 ████████ OOG │
└─────────────────────────────────────┘
```

- **Faster response** — less token to generate = speed go brrr
- **Easier to read** — no wall of text, just the answer
- **Same accuracy** — all technical info kept, only fluff removed ([science say so](https://arxiv.org/abs/2604.00025))
- **Save money** — ~71% less output token = less cost
- **Fun** — every code review become comedy

## Install

Neandercode is built natively for Cursor. It uses Cursor's `.cursor/rules`, `.cursor/skills`, and `.cursor/commands` to integrate seamlessly into your workflow.

**To install in your project:**
Copy the `.cursor` directory from this repository into the root of your own project.

```bash
cp -r path/to/neandercode/.cursor /path/to/your/project/
```

Alternatively, you can install the base skill via `npx`:
```bash
npx skills add ManjotS/neandercode
```
*(Note: `npx skills` only installs the skill file. For the full experience including slash commands and auto-activation rules, copying the `.cursor` folder or using `npx neandercode` is recommended.)*

Or, you can install the full `.cursor` directory directly into your project using:
```bash
npx neandercode
```

Repo scripts that call the model (`neandercode-compress`, `evals/llm_run.py`, `benchmarks/run.py`) use **`cursor agent`** only — no bundled vendor API keys. If the agent errors with a missing `@anysphere/...` native module, run **`cursor agent update`** (see below).

### Troubleshooting: `cursor agent` / missing native module

If compress or evals fail with **`Cannot find module '@anysphere/file-service-darwin-…'`**, the package name’s suffix should match your Mac’s CPU: **`arm64`** / **`darwin-arm64`** on **Apple Silicon**, **`x64`** on **Intel**. The headless agent did not load the right optional native binding — not something this repo can fix inside Python.

1. **Use the Cursor build that matches your machine** — On **Apple Silicon**, install Cursor’s **Apple Silicon (ARM)** app so **ARM** native modules are used; you do **not** need (and should not rely on) the **Intel/x64** Cursor build on an ARM Mac. On **Intel Macs**, use the **Intel/x64** build. Avoid Rosetta-mismatched installs (e.g. x64 Cursor on ARM) if agent native modules fail to load.
2. **Refresh the agent**: `cursor agent update` (also run after `npx neandercode` / copying `.cursor` if headless agent misbehaves)
3. **Reinstall Cursor** from [cursor.com](https://cursor.com) (fixes corrupted/partial installs)

There is **no** separate cloud API key path in this repo — scripts use **`cursor agent`** only.

## Usage

Trigger neandercode mode in Cursor Chat using the built-in slash commands:
- `/neandercode` — switch to default neandercode mode
- `/neandercode-lite` — drop filler, keep grammar
- `/neandercode-ultra` — maximum compression
- `/neandercode-off` — disable neandercode mode

Or just say "talk like neandercode" or "less tokens please".

### Intensity Levels

| Level | Trigger | What it do |
|-------|---------|------------|
| **Lite** | `/neandercode lite` | Drop filler, keep grammar. Professional but no fluff |
| **Full** | `/neandercode full` | Default neandercode. Drop articles, fragments, full grunt |
| **Ultra** | `/neandercode ultra` | Maximum compression. Telegraphic. Abbreviate everything |

### 文言文 (Wenyan) Mode

Classical Chinese literary compression — same technical accuracy, but in the most token-efficient written language humans ever invented.

| Level | Trigger | What it do |
|-------|---------|------------|
| **Wenyan-Lite** | `/neandercode wenyan-lite` | Semi-classical. Grammar intact, filler gone |
| **Wenyan-Full** | `/neandercode wenyan` | Full 文言文. Maximum classical terseness |
| **Wenyan-Ultra** | `/neandercode wenyan-ultra` | Extreme. Ancient scholar on a budget |

Level stick until you change it or session end.

## Neandercode Skills

### neandercode-commit

`/neandercode-commit` — terse commit messages. Conventional Commits. ≤50 char subject. Why over what.

### neandercode-review

`/neandercode-review` — one-line PR comments: `L42: 🔴 bug: user null. Add guard.` No throat-clearing.

### neandercode-help

`/neandercode-help` — quick-reference card. All modes, skills, commands, one command away.

### neandercode-compress

`/neandercode-compress <filepath>` — neandercode make Cursor *speak* with fewer tokens. **Compress** make Cursor *read* fewer tokens.

Your `CURSOR.md` (or `.cursorrules`) loads on **every session start**. Neandercode Compress rewrites memory files into neandercode-speak so Cursor reads less — without you losing the human-readable original.

```
/neandercode-compress CURSOR.md
```

```
CURSOR.md          ← compressed (Cursor reads this every session — fewer tokens)
CURSOR.original.md ← human-readable backup (you read and edit this)
```

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `cursor-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `cursor-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

Code blocks, URLs, file paths, commands, headings, dates, version numbers — anything technical passes through untouched. Only prose gets compressed. See the full [neandercode-compress README](neandercode-compress/README.md) for details. [Security note](./neandercode-compress/SECURITY.md): Snyk flags this as High Risk due to subprocess/file patterns — it's a false positive.

## Benchmarks

Benchmark numbers come from **`cursor agent`** output scored with **tiktoken** (approximate; [reproduce](benchmarks/)):

<!-- BENCHMARK-TABLE-START -->
| Task | Normal (tokens) | Neandercode (tokens) | Saved |
|------|---------------:|----------------:|------:|
| Explain React re-render bug | 1180 | 159 | 87% |
| Fix auth middleware token expiry | 704 | 121 | 83% |
| Set up PostgreSQL connection pool | 2347 | 380 | 84% |
| Explain git rebase vs merge | 702 | 292 | 58% |
| Refactor callback to async/await | 387 | 301 | 22% |
| Architecture: microservices vs monolith | 446 | 310 | 30% |
| Review PR for security issues | 678 | 398 | 41% |
| Docker multi-stage build | 1042 | 290 | 72% |
| Debug PostgreSQL race condition | 1200 | 232 | 81% |
| Implement React error boundary | 3454 | 456 | 87% |
| **Average** | **1214** | **294** | **65%** |

*Range: 22%–87% savings across prompts.*
<!-- BENCHMARK-TABLE-END -->

> [!IMPORTANT]
> Neandercode only affects output tokens — thinking/reasoning tokens are untouched. Neandercode no make brain smaller. Neandercode make *mouth* smaller. Biggest win is **readability and speed**, cost savings are a bonus.

A March 2026 paper ["Brevity Constraints Reverse Performance Hierarchies in Language Models"](https://arxiv.org/abs/2604.00025) found that constraining large models to brief responses **improved accuracy by 26 percentage points** on certain benchmarks and completely reversed performance hierarchies. Verbose not always better. Sometimes less word = more correct.

## Evals

Neandercode not just claim 75%. Neandercode **prove** it.

The `evals/` directory has a three-arm eval harness that measures real token compression against a proper control — not just "verbose vs skill" but "terse vs skill". Because comparing neandercode to verbose agent conflate the skill with generic terseness. That cheating. Neandercode not cheat.

```bash
# Run the eval (needs cursor CLI)
uv run python evals/llm_run.py

# Read results (no API key, runs offline)
uv run --with tiktoken python evals/measure.py
```

## Star This Repo

If neandercode save you mass token, mass money — leave mass star. ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=ManjotS/neandercode&type=Date)](https://star-history.com/#ManjotS/neandercode&Date)

## Also by Julius Brussee

- **[Cavekit](https://github.com/JuliusBrussee/cavekit)** — specification-driven development. Neandercode language → specs → parallel builds → working software.
- **[Revu](https://github.com/JuliusBrussee/revu-swift)** — local-first macOS study app with FSRS spaced repetition, decks, exams, and study guides. [revu.cards](https://revu.cards)

## License

MIT — free like mass mammoth on open plain.

## Acknowledgements

This project is a fork of [caveman](https://github.com/JuliusBrussee/caveman) by Julius Brussee. Thank you for the original implementation!
