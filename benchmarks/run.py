#!/usr/bin/env python3
"""Benchmark neandercode vs normal Agent output token counts via `cursor agent`.

Output token counts are tiktoken `o200k_base` on the returned text (approximate),
same spirit as evals — not provider-reported usage.
"""

import argparse
import hashlib
import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Load .env.local from repo root if it exists
_env_file = Path(__file__).parent.parent / ".env.local"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

SCRIPT_VERSION = "1.0.0"
SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
PROMPTS_PATH = SCRIPT_DIR / "prompts.json"
SKILL_PATH = REPO_DIR / "skills" / "neandercode" / "SKILL.md"
README_PATH = REPO_DIR / "README.md"
RESULTS_DIR = SCRIPT_DIR / "results"

NORMAL_SYSTEM = "You are a helpful assistant."
BENCHMARK_START = "<!-- BENCHMARK-TABLE-START -->"
BENCHMARK_END = "<!-- BENCHMARK-TABLE-END -->"


def load_prompts():
    with open(PROMPTS_PATH) as f:
        data = json.load(f)
    return data["prompts"]


def load_neandercode_system():
    return SKILL_PATH.read_text()


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


_ENC = None


def _encoding():
    """Lazy-load tiktoken so `python benchmarks/run.py --dry-run` works without deps."""
    global _ENC
    if _ENC is None:
        try:
            import tiktoken
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "benchmarks need tiktoken. Install: pip install -r benchmarks/requirements.txt"
            ) from e
        _ENC = tiktoken.get_encoding("o200k_base")
    return _ENC


def _count_tokens(text: str) -> int:
    return len(_encoding().encode(text))


def call_cursor_agent(model: str, system: str, prompt: str) -> dict:
    """Run `cursor agent -p` with combined system + user prompt; count output tokens locally."""
    full_prompt = f"{system}\n\nUser prompt:\n{prompt}"
    cmd = ["cursor", "agent", "-p", "--output-format", "text", "--trust"]
    if model:
        cmd += ["--model", model]
    cmd.append(full_prompt)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or "") + (proc.stdout or "")
        low = err.lower()
        hint = ""
        if (
            "authentication" in low
            or "cursor agent login" in low
            or "CURSOR_API_KEY" in err
        ):
            hint = " Authenticate: `cursor agent login` or set `CURSOR_API_KEY`."
        elif "Cannot find module" in err or "file-service" in err:
            hint = (
                " Try `cursor agent update` or reinstall Cursor; use ARM Cursor on Apple Silicon, x64 on Intel."
            )
        raise RuntimeError(f"cursor agent failed (exit {proc.returncode}):\n{err}{hint}")
    text = proc.stdout.strip()
    out_tok = _count_tokens(text)
    in_tok = _count_tokens(system) + _count_tokens(prompt)
    return {
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "text": text,
        "stop_reason": "end_turn",
    }


def run_benchmarks(model, prompts, neandercode_system, trials):
    results = []
    total = len(prompts)

    for i, prompt_entry in enumerate(prompts, 1):
        pid = prompt_entry["id"]
        prompt_text = prompt_entry["prompt"]
        entry = {
            "id": pid,
            "category": prompt_entry["category"],
            "prompt": prompt_text,
            "normal": [],
            "neandercode": [],
        }

        for mode, system in [("normal", NORMAL_SYSTEM), ("neandercode", neandercode_system)]:
            for t in range(1, trials + 1):
                print(
                    f"  [{i}/{total}] {pid} | {mode} | trial {t}/{trials}",
                    file=sys.stderr,
                )
                result = call_cursor_agent(model, system, prompt_text)
                entry[mode].append(result)
                time.sleep(0.5)

        results.append(entry)

    return results


def compute_stats(results):
    rows = []
    all_savings = []

    for entry in results:
        normal_medians = statistics.median(
            [t["output_tokens"] for t in entry["normal"]]
        )
        neandercode_medians = statistics.median(
            [t["output_tokens"] for t in entry["neandercode"]]
        )
        savings = 1 - (neandercode_medians / normal_medians) if normal_medians > 0 else 0
        all_savings.append(savings)

        rows.append(
            {
                "id": entry["id"],
                "category": entry["category"],
                "prompt": entry["prompt"],
                "normal_median": int(normal_medians),
                "neandercode_median": int(neandercode_medians),
                "savings_pct": round(savings * 100),
            }
        )

    avg_savings = round(statistics.mean(all_savings) * 100)
    min_savings = round(min(all_savings) * 100)
    max_savings = round(max(all_savings) * 100)
    avg_normal = round(statistics.mean([r["normal_median"] for r in rows]))
    avg_neandercode = round(statistics.mean([r["neandercode_median"] for r in rows]))

    return rows, {
        "avg_savings": avg_savings,
        "min_savings": min_savings,
        "max_savings": max_savings,
        "avg_normal": avg_normal,
        "avg_neandercode": avg_neandercode,
    }


def format_prompt_label(prompt_id):
    labels = {
        "react-rerender": "Explain React re-render bug",
        "auth-middleware-fix": "Fix auth middleware token expiry",
        "postgres-pool": "Set up PostgreSQL connection pool",
        "git-rebase-merge": "Explain git rebase vs merge",
        "async-refactor": "Refactor callback to async/await",
        "microservices-monolith": "Architecture: microservices vs monolith",
        "pr-security-review": "Review PR for security issues",
        "docker-multi-stage": "Docker multi-stage build",
        "race-condition-debug": "Debug PostgreSQL race condition",
        "error-boundary": "Implement React error boundary",
    }
    return labels.get(prompt_id, prompt_id)


def format_table(rows, summary):
    lines = [
        "| Task | Normal (tokens) | Neandercode (tokens) | Saved |",
        "|------|---------------:|----------------:|------:|",
    ]
    for r in rows:
        label = format_prompt_label(r["id"])
        lines.append(
            f"| {label} | {r['normal_median']} | {r['neandercode_median']} | {r['savings_pct']}% |"
        )
    lines.append(
        f"| **Average** | **{summary['avg_normal']}** | **{summary['avg_neandercode']}** | **{summary['avg_savings']}%** |"
    )
    lines.append("")
    lines.append(
        f"*Range: {summary['min_savings']}%–{summary['max_savings']}% savings across prompts.*"
    )
    lines.append("")
    lines.append(
        "*Token counts: tiktoken `o200k_base` on model output text (approximate). Requires `cursor` CLI.*"
    )
    return "\n".join(lines)


def save_results(results, rows, summary, model, trials, skill_hash):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output = {
        "metadata": {
            "script_version": SCRIPT_VERSION,
            "model": model,
            "date": datetime.now(timezone.utc).isoformat(),
            "trials": trials,
            "skill_md_sha256": skill_hash,
            "token_counter": "tiktoken o200k_base on output text",
            "backend": "cursor agent CLI",
        },
        "summary": summary,
        "rows": rows,
        "raw": results,
    }
    path = RESULTS_DIR / f"benchmark_{ts}.json"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    return path


def update_readme(table_md):
    content = README_PATH.read_text()
    start_idx = content.find(BENCHMARK_START)
    end_idx = content.find(BENCHMARK_END)
    if start_idx == -1 or end_idx == -1:
        print(
            "ERROR: Benchmark markers not found in README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    before = content[: start_idx + len(BENCHMARK_START)]
    after = content[end_idx:]
    new_content = before + "\n" + table_md + "\n" + after
    README_PATH.write_text(new_content)
    print("README.md updated.", file=sys.stderr)


def dry_run(prompts, model, trials):
    print(f"Model:  {model}")
    print(f"Trials: {trials}")
    print(f"Prompts: {len(prompts)}")
    print(f"Total cursor agent runs: {len(prompts) * 2 * trials}")
    print()
    for p in prompts:
        print(f"  [{p['id']}] ({p['category']})")
        preview = p["prompt"][:80]
        if len(p["prompt"]) > 80:
            preview += "..."
        print(f"    {preview}")
    print()
    print("Dry run complete. No cursor agent invocations.")


def main():
    parser = argparse.ArgumentParser(description="Benchmark neandercode vs normal Agent")
    parser.add_argument("--trials", type=int, default=3, help="Trials per prompt per mode (default: 3)")
    parser.add_argument("--dry-run", action="store_true", help="Print config, no cursor agent calls")
    parser.add_argument("--update-readme", action="store_true", help="Update README.md benchmark table")
    parser.add_argument("--model", default="gpt-5", help="Model to use")
    args = parser.parse_args()

    prompts = load_prompts()

    if args.dry_run:
        dry_run(prompts, args.model, args.trials)
        return

    neandercode_system = load_neandercode_system()
    skill_hash = sha256_file(SKILL_PATH)

    print(f"Running benchmarks: {len(prompts)} prompts x 2 modes x {args.trials} trials", file=sys.stderr)
    print(f"Model: {args.model}", file=sys.stderr)
    print(file=sys.stderr)

    results = run_benchmarks(args.model, prompts, neandercode_system, args.trials)
    rows, summary = compute_stats(results)
    table_md = format_table(rows, summary)

    json_path = save_results(results, rows, summary, args.model, args.trials, skill_hash)
    print(f"\nResults saved to {json_path}", file=sys.stderr)

    if args.update_readme:
        update_readme(table_md)

    print(table_md)


if __name__ == "__main__":
    main()
