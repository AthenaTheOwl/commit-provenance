"""Artifact checks for the v0.1 readiness report."""

from __future__ import annotations

from pathlib import Path

REQUIRED_STATUS_SECTIONS = (
    "Current state",
    "Known limits",
    "Next feature queue",
)

REQUIRED_ARTIFACTS = (
    "README.md",
    "STATUS.md",
    "PRODUCT_BRIEF.md",
    "SYSTEM_MAP.md",
    "specs/0001-foundation/requirements.md",
    "specs/0001-foundation/design.md",
    "specs/0001-foundation/tasks.md",
    "specs/0001-foundation/acceptance.md",
    "specs/0002-design/requirements.md",
    "specs/0002-design/design.md",
    "specs/0002-design/tasks.md",
    "specs/0002-design/acceptance.md",
    "pyproject.toml",
    "commit_provenance/cli.py",
    "commit_provenance/model.py",
    "commit_provenance/scoring.py",
    "reports/commit-provenance-v0.1.jsonl",
)


def parse_status_sections(status_text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in status_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current and line.startswith("- "):
            sections[current].append(line[2:].strip())
    return sections


def collect_artifact_presence(repo_path: Path) -> dict[str, bool]:
    return {
        artifact: (repo_path / artifact).exists()
        for artifact in REQUIRED_ARTIFACTS
    }


def missing_status_sections(status_sections: dict[str, list[str]]) -> list[str]:
    return [
        section for section in REQUIRED_STATUS_SECTIONS
        if section not in status_sections
    ]


def count_surfaces(repo_path: Path) -> dict[str, int]:
    return {
        "docs": len(list((repo_path / "docs").glob("*.md"))) if (repo_path / "docs").exists() else 0,
        "spec_files": len(list((repo_path / "specs").rglob("*.md"))) if (repo_path / "specs").exists() else 0,
        "tests": len(list((repo_path / "tests").glob("test_*.py"))) if (repo_path / "tests").exists() else 0,
        "jsonl_reports": len(list((repo_path / "reports").glob("*.jsonl"))) if (repo_path / "reports").exists() else 0,
    }


def score_report(artifact_presence: dict[str, bool], missing_sections: list[str]) -> dict[str, int]:
    present = sum(1 for exists in artifact_presence.values() if exists)
    total = len(artifact_presence)
    return {
        "required_artifacts_present": present,
        "required_artifacts_total": total,
        "missing_status_sections": len(missing_sections),
    }
