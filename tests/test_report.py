from pathlib import Path

import commit_provenance.model as model
from commit_provenance.report import build_report
from commit_provenance.scoring import REQUIRED_ARTIFACTS


def test_build_report_reads_required_status_sections(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "specs").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "STATUS.md").write_text(
        "\n".join(
            [
                "# Status",
                "",
                "## Current state",
                "- Running",
                "",
                "## Known limits",
                "- Limited",
                "",
                "## Next feature queue",
                "- Next",
            ]
        ),
        encoding="utf-8",
    )

    report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")

    assert report["generated_at"] == "2026-06-22T12:00:00Z"
    assert report["missing_status_sections"] == []
    assert report["status_sections"]["Current state"] == ["Running"]


def test_build_report_marks_missing_artifacts(tmp_path: Path) -> None:
    report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")

    assert report["artifacts"]["README.md"] is False
    assert "Current state" in report["missing_status_sections"]
    # empty tmp repo: no required artifacts present, total is the full set.
    assert report["score"]["required_artifacts_present"] == 0
    assert report["score"]["required_artifacts_total"] == len(REQUIRED_ARTIFACTS)


def test_score_counts_present_required_artifacts(tmp_path: Path) -> None:
    # Create a known subset of REQUIRED_ARTIFACTS on disk.
    present = ("README.md", "STATUS.md", "pyproject.toml")
    for rel in present:
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x", encoding="utf-8")

    report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")

    assert report["score"]["required_artifacts_present"] == len(present)
    assert report["score"]["required_artifacts_total"] == len(REQUIRED_ARTIFACTS)


def test_counts_report_file_surfaces(tmp_path: Path) -> None:
    (tmp_path / "specs").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "specs" / "requirements.md").write_text("r", encoding="utf-8")
    (tmp_path / "specs" / "design.md").write_text("d", encoding="utf-8")
    (tmp_path / "tests" / "test_x.py").write_text("t", encoding="utf-8")

    report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")

    assert report["counts"]["spec_files"] == 2
    assert report["counts"]["tests"] == 1


def test_repository_dirty_flag_tracks_git_status(tmp_path: Path, monkeypatch) -> None:
    def fake_git(repo: Path, *args: str) -> str | None:
        if args[:1] == ("status",):
            return " M some/file.py"
        return "stub"

    monkeypatch.setattr(model, "_git", fake_git)
    dirty_report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")
    assert dirty_report["repository"]["dirty"] is True

    def fake_git_clean(repo: Path, *args: str) -> str | None:
        if args[:1] == ("status",):
            return ""
        return "stub"

    monkeypatch.setattr(model, "_git", fake_git_clean)
    clean_report = build_report(tmp_path, generated_at="2026-06-22T12:00:00Z")
    assert clean_report["repository"]["dirty"] is False
