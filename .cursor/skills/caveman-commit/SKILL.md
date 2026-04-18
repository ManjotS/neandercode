---
name: caveman-commit
description: >
  Ultra-compressed commit message generator. Conventional Commits format.
  Subject <=50 chars when possible. Body only when non-obvious why is needed.
---

Write commit messages terse and exact.

Rules:
- Format: `<type>(<scope>): <imperative summary>` (`<scope>` optional)
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`
- Subject max 50 chars when possible (hard cap 72), no trailing period
- Body only for non-obvious `why`, breaking changes, migrations, security fixes
- Prefer intent over diff narration
- Never include AI attribution
