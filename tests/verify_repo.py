#!/usr/bin/env python3
"""Local verification runner for caveman install surfaces."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckFailure(RuntimeError):
    pass


def section(title: str) -> None:
    print(f"\n== {title} ==")


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def run(
    args: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        args,
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise CheckFailure(
            f"Command failed ({result.returncode}): {' '.join(args)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def read_json(path: Path) -> object:
    return json.loads(path.read_text())


def verify_synced_files() -> None:
    section("Synced Files")
    skill_source = ROOT / "skills/caveman/SKILL.md"
    rule_source = ROOT / "rules/caveman-activate.md"

    skill_copies = [
        ROOT / "caveman/SKILL.md",
        ROOT / "plugins/caveman/skills/caveman/SKILL.md",
        ROOT / ".cursor/skills/caveman/SKILL.md",
        ROOT / ".windsurf/skills/caveman/SKILL.md",
    ]
    for copy in skill_copies:
        ensure(copy.read_text() == skill_source.read_text(), f"Skill copy mismatch: {copy}")

    rule_copies = [
        ROOT / ".clinerules/caveman.md",
        ROOT / ".github/copilot-instructions.md",
    ]
    for copy in rule_copies:
        ensure(copy.read_text() == rule_source.read_text(), f"Rule copy mismatch: {copy}")

    with zipfile.ZipFile(ROOT / "caveman.skill") as archive:
        ensure("caveman/SKILL.md" in archive.namelist(), "caveman.skill missing caveman/SKILL.md")
        ensure(
            archive.read("caveman/SKILL.md").decode("utf-8") == skill_source.read_text(),
            "caveman.skill payload mismatch",
        )

    print("Synced copies and caveman.skill zip OK")




def load_compress_modules():
    sys.path.insert(0, str(ROOT / "caveman-compress"))
    import scripts.benchmark  # noqa: F401
    import scripts.cli as cli
    import scripts.compress  # noqa: F401
    import scripts.detect as detect
    import scripts.validate as validate

    return cli, detect, validate


def verify_compress_fixtures() -> None:
    section("Compress Fixtures")
    _, detect, validate = load_compress_modules()

    fixtures = sorted((ROOT / "tests/caveman-compress").glob("*.original.md"))
    ensure(fixtures, "No caveman-compress fixtures found")

    for original in fixtures:
        compressed = original.with_name(original.name.replace(".original.md", ".md"))
        ensure(compressed.exists(), f"Missing compressed fixture for {original.name}")
        result = validate.validate(original, compressed)
        ensure(result.is_valid, f"Fixture validation failed for {compressed.name}: {result.errors}")
        ensure(detect.should_compress(compressed), f"Fixture should be compressible: {compressed.name}")

    print(f"Validated {len(fixtures)} caveman-compress fixture pairs")


def verify_compress_cli() -> None:
    section("Compress CLI")

    skip_result = run(
        ["python3", "-m", "scripts", "../hooks/install.sh"],
        cwd=ROOT / "caveman-compress",
        check=False,
    )
    ensure(skip_result.returncode == 0, "compress CLI skip path should exit 0")
    ensure("Detected: code" in skip_result.stdout, "compress CLI skip path missing detection output")
    ensure(
        "Skipping: file is not natural language" in skip_result.stdout,
        "compress CLI skip path missing skip output",
    )

    missing_result = run(
        ["python3", "-m", "scripts", "../does-not-exist.md"],
        cwd=ROOT / "caveman-compress",
        check=False,
    )
    ensure(missing_result.returncode == 1, "compress CLI missing-file path should exit 1")
    ensure("File not found" in missing_result.stdout, "compress CLI missing-file output mismatch")

    print("Compress CLI skip/error paths OK")



def main() -> int:
    checks = [
        verify_synced_files,
        verify_compress_fixtures,
        verify_compress_cli,
    ]

    try:
        for check in checks:
            check()
    except CheckFailure as exc:
        print(f"\nFAIL: {exc}", file=sys.stderr)
        return 1

    print("\nAll local verification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
