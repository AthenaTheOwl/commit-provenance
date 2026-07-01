"""Command-line interface for CommitProvenance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from commit_provenance import __version__
from commit_provenance.model import build_report, write_report

DEFAULT_REPORT = "reports/commit-provenance-v0.1.jsonl"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_report(path: Path) -> dict | None:
    if not path.is_file():
        return None
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError:
        raise SystemExit(f"report at {path} is not valid JSONL")


def _run_show(report_path: str | None) -> int:
    """Print a readable, ranked readiness view from the committed report (no args needed)."""
    root = _repo_root()
    path = Path(report_path) if report_path else root / DEFAULT_REPORT
    report = _load_report(path)
    if report is None:
        raise SystemExit(
            f"no report found at {path} - run `git-provenance report --out {DEFAULT_REPORT}` first"
        )

    repo = report.get("repository", {})
    artifacts: dict[str, bool] = report.get("artifacts", {})
    score = report.get("score", {})
    counts = report.get("counts", {})
    present = score.get("required_artifacts_present", sum(1 for v in artifacts.values() if v))
    total = score.get("required_artifacts_total", len(artifacts) or 1)
    pct = (present / total * 100) if total else 0.0

    print(
        f"commit-provenance - repo readiness, report v{report.get('report_version', '?')} "
        f"({repo.get('name', '?')} @ {repo.get('head', '?')}, branch {repo.get('branch', '?')})"
    )
    print(
        f"generated {report.get('generated_at', '?')} - "
        f"{present}/{total} required artifacts present ({pct:.0f}%), "
        f"{len(report.get('missing_status_sections', []))} status section(s) missing\n"
    )

    # ranked: missing artifacts surface first, then present - within each group, sorted by name.
    ranked = sorted(artifacts.items(), key=lambda kv: (kv[1], kv[0]))
    header = f"{'artifact':<52} {'status':>9}"
    print(header)
    print("-" * len(header))
    for name, ok in ranked:
        print(f"{name[:52]:<52} {'present' if ok else 'MISSING':>9}")

    print("\nrepository surfaces:")
    for key in ("docs", "spec_files", "tests", "jsonl_reports"):
        print(f"  {key:<14} {counts.get(key, 0)}")

    missing = [name for name, ok in artifacts.items() if not ok]
    if missing:
        print(
            f"\nbiggest gap: {len(missing)} required artifact(s) absent - "
            f"first to fix: {sorted(missing)[0]}. readiness {pct:.0f}%."
        )
    else:
        print(
            f"\nbiggest gap: none - all {total} required artifacts present. "
            f"readiness {pct:.0f}%. next surface is the signed emit/verify flow (specs/0001)."
        )
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="git-provenance")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("version", help="print the package version")

    show_parser = subcommands.add_parser(
        "show", help="print a readable, ranked readiness view from the committed report"
    )
    show_parser.add_argument(
        "--report",
        default=None,
        help=f"path to a report jsonl (default: {DEFAULT_REPORT})",
    )

    report_parser = subcommands.add_parser("report", help="write a v0.1 readiness report")
    report_parser.add_argument("--repo", default=".", help="repository path to inspect")
    report_parser.add_argument("--out", help="write JSONL report to this path")
    report_parser.add_argument(
        "--generated-at",
        help="override report timestamp, useful for deterministic artifacts",
    )

    validate_parser = subcommands.add_parser("validate", help="validate the bundled v0.1 report")
    validate_parser.add_argument("--path", default="reports/commit-provenance-v0.1.jsonl")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(f"commit-provenance {__version__}")
        return 0

    if args.command == "show":
        return _run_show(args.report)

    if args.command == "report":
        report = build_report(Path(args.repo), generated_at=args.generated_at)
        if args.out:
            write_report(report, args.out)
        else:
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    if args.command == "validate":
        report_path = Path(args.path)
        # is_file() rather than exists() so a directory path reports as missing
        # instead of blowing up on read_text with IsADirectoryError.
        if not report_path.is_file():
            raise SystemExit(f"missing report: {report_path}")
        lines = [line for line in report_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            raise SystemExit(f"empty report: {report_path}")
        for i, line in enumerate(lines, start=1):
            try:
                json.loads(line)
            except json.JSONDecodeError:
                raise SystemExit(f"invalid report {report_path}: line {i} is not valid JSON")
        print(f"OK {report_path} ({len(lines)} row(s))")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
