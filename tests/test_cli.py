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
