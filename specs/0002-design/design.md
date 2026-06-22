# Spec 0002 design

## Data-report slice

The v0.1 slice is a repository-readiness report. It does not create
signed commit records. It gives reviewers one executable surface while
the schema and signing flow are still being built.

## CLI

`git-provenance report` reads the repository root, parses `STATUS.md`,
checks required artifact paths, records a few repo counts, and emits one
report object. `--out` writes compact JSONL so report artifacts can be
appended later. Stdout remains pretty JSON for manual inspection.

## Package layout

The package lives at root `commit_provenance/` because the factory
contract checks module source files directly. `cli.py` owns argument
parsing, `model.py` owns report construction and writing, and
`scoring.py` owns required-path checks and status-section parsing.

## Ledger decisions

- D-CP-002-001: v0.1 ships a report CLI before the signing flow.
- D-CP-002-002: Plain `uv sync` must install the project and test tools.
- D-CP-002-003: The three `STATUS.md` H2 headings are a contract.
- D-CP-002-004: The `commit_sha` finding is resolved later by a three-hook design: pre-commit prepares the pending record, post-commit patches the final commit SHA and amends once, and pre-push verifies the range.
