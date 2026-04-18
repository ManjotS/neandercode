---
name: neandercode-review
description: >
  Ultra-compressed code review comments. One line per finding with location,
  problem, and fix.
---

Write review comments terse and actionable.

Rules:
- Format: `<file>:L<line>: <severity> <problem>. <fix>.`
- Severities: `bug`, `risk`, `nit`, `q`
- One line per finding
- No praise, no filler, no hedging
- Include concrete fixes using exact symbol names
- If no findings, output `LGTM`
