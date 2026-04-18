# Security

## Snyk High Risk Rating

`neandercode-compress` receives a Snyk High Risk rating due to static analysis heuristics. This document explains what the skill does and does not do.

### What triggers the rating

1. **subprocess usage**: The skill calls the `cursor agent` CLI via `subprocess.run()`. The subprocess call uses a fixed argument list — no shell interpolation occurs. User file content is passed as a single argument to `cursor agent`, not as a shell string.

2. **File read/write**: The skill reads the file the user explicitly points it at, compresses it, and writes the result back to the same path. A `.original.md` backup is saved alongside it. No files outside the user-specified path are read or written.

### What the skill does NOT do

- Does not execute user file content as code
- Does not call vendor HTTP APIs directly from Python (no bundled API keys; inference goes through the user’s Cursor `cursor agent` install)
- Does not access files outside the path the user provides
- Does not use shell=True or string interpolation in subprocess calls

### Auth behavior

Compression uses **`cursor agent`**. Authenticate with **`cursor agent login`** (or **`CURSOR_API_KEY`** for headless/CI — see Cursor documentation). If `cursor agent` fails (including missing native modules), use the Cursor installer that matches your CPU (**Apple Silicon** vs **Intel**), then run **`cursor agent update`** or reinstall from [cursor.com](https://cursor.com).

### File size limit

Files larger than 500KB are rejected before any agent call is made.

### Reporting a vulnerability

If you believe you've found a genuine security issue, please open a GitHub issue with the label `security`.
