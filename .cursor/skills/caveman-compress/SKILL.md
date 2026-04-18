---
name: caveman-compress
description: >
  Compress natural-language memory files into caveman format while preserving
  code, URLs, structure, and technical identifiers.
---

Process:
1. Require one absolute file path from user.
2. Run `python3 -m scripts <absolute_filepath>` inside `caveman-compress`.
3. Report whether file was compressed, skipped, or restored on validation failure.

Boundaries:
- Compress only natural-language files.
- Never alter code blocks, inline code, URLs, paths, commands, or headings.
- Keep backup as `<filename>.original.md`.
