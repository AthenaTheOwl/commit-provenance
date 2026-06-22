from pathlib import Path

from commit_provenance.report import build_report


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
