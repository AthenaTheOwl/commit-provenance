"""Repository readiness report for the v0.1 data-report slice."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from commit_provenance.scoring import (
    REQUIRED_STATUS_SECTIONS,
    collect_artifact_presence,
    count_surfaces,
    missing_status_sections,
    parse_status_sections,
    score_report,
)


def _git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _display_path(repo_path: Path) -> str:
    cwd = Path.cwd().resolve()
    if repo_path == cwd:
        return "."
    try:
        return str(repo_path.relative_to(cwd))
    except ValueError:
        return repo_path.name


def build_report(repo: Path | str = ".", generated_at: str | None = None) -> dict[str, Any]:
    repo_path = Path(repo).resolve()
    status_path = repo_path / "STATUS.md"
    status_text = status_path.read_text(encoding="utf-8") if status_path.exists() else ""
    status_sections = parse_status_sections(status_text)

    artifact_presence = collect_artifact_presence(repo_path)
    missing_sections = missing_status_sections(status_sections)
    git_status = _git(repo_path, "status", "--short")
    head_sha = _git(repo_path, "rev-parse", "--short", "HEAD")
    branch = _git(repo_path, "branch", "--show-current")

    return {
        "report_version": "0.1",
        "generated_at": generated_at or _utc_now(),
        "repository": {
            "name": repo_path.name,
            "path": _display_path(repo_path),
            "branch": branch or "unknown",
            "head": head_sha or "unknown",
            "dirty": bool(git_status),
        },
        "artifacts": artifact_presence,
        "status_sections": {
            section: status_sections.get(section, [])
            for section in REQUIRED_STATUS_SECTIONS
        },
        "missing_status_sections": missing_sections,
        "counts": count_surfaces(repo_path),
        "score": score_report(artifact_presence, missing_sections),
    }


def write_report(report: dict[str, Any], out_path: Path | str) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, sort_keys=True) + "\n", encoding="utf-8")
