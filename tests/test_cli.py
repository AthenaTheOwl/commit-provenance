import json
from pathlib import Path

from commit_provenance.cli import main


def test_version_command_prints_version(capsys) -> None:
    exit_code = main(["version"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "commit-provenance 0.1.0"


def test_report_command_writes_json(tmp_path: Path) -> None:
    out_path = tmp_path / "report.json"
    exit_code = main(
        [
            "report",
            "--repo",
            str(Path.cwd()),
            "--out",
            str(out_path),
            "--generated-at",
            "2026-06-22T12:00:00Z",
        ]
    )

    assert exit_code == 0
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["report_version"] == "0.1"
    assert data["generated_at"] == "2026-06-22T12:00:00Z"


def test_validate_command_checks_bundled_report(capsys) -> None:
    exit_code = main(["validate"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "commit-provenance-v0.1.jsonl" in captured.out


def test_show_command_prints_ranked_readiness(capsys) -> None:
    exit_code = main(["show"])

    captured = capsys.readouterr()
    out = captured.out
    assert exit_code == 0
    # headline with readiness percentage
    assert "repo readiness" in out
    assert "required artifacts present" in out
    # ranked table header + a known artifact row
    assert "artifact" in out and "status" in out
    assert "pyproject.toml" in out
    # surfaces block and a headline finding
    assert "repository surfaces:" in out
    assert "biggest gap:" in out


def test_show_command_prints_exact_readiness_percentage(tmp_path, capsys) -> None:
    # 2 of 4 required artifacts present -> the headline must read 50%.
    report = {
        "report_version": "0.1",
        "generated_at": "2026-06-22T12:00:00Z",
        "repository": {"name": "demo", "head": "abc123", "branch": "main"},
        "artifacts": {"a": True, "b": True, "c": False, "d": False},
        "score": {"required_artifacts_present": 2, "required_artifacts_total": 4},
        "counts": {"docs": 0, "spec_files": 0, "tests": 0, "jsonl_reports": 0},
        "missing_status_sections": [],
    }
    report_path = tmp_path / "report.jsonl"
    report_path.write_text(json.dumps(report) + "\n", encoding="utf-8")

    exit_code = main(["show", "--report", str(report_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "2/4 required artifacts present (50%)" in captured.out


def test_show_command_handles_missing_report(tmp_path, capsys) -> None:
    missing = tmp_path / "nope.jsonl"
    try:
        main(["show", "--report", str(missing)])
    except SystemExit as exc:
        assert "no report found" in str(exc.code)
    else:  # pragma: no cover - show must error on missing data
        raise AssertionError("expected SystemExit for missing report")
