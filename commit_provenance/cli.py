"""Command-line interface for CommitProvenance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from commit_provenance import __version__
from commit_provenance.model import build_report, write_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="git-provenance")
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("version", help="print the package version")

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

    if args.command == "report":
        report = build_report(Path(args.repo), generated_at=args.generated_at)
        if args.out:
            write_report(report, args.out)
        else:
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    if args.command == "validate":
        report_path = Path(args.path)
        if not report_path.exists():
            raise SystemExit(f"missing report: {report_path}")
        lines = [line for line in report_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            raise SystemExit(f"empty report: {report_path}")
        for line in lines:
            json.loads(line)
        print(f"OK {report_path} ({len(lines)} row(s))")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
