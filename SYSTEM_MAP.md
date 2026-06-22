# System map

## Surfaces

- `git-provenance report` reads repo files and writes a JSONL readiness report.
- Future `git provenance emit` will read staged changes and session metadata.
- Future `git provenance verify` will validate signed provenance records over a commit range.
- Future hooks will run emit and verify during local git workflows.

## Data flow

1. A developer stages code.
2. The emit flow reads staged paths and optional session metadata.
3. Session adapters normalize vendor-specific session files.
4. The signing flow canonicalizes the provenance record and signs it.
5. The hook stages the provenance file with the commit.
6. The verify flow walks commits and checks records, signatures, and schemas.
7. The blame walker composes per-line attribution from commit-level records.

## v0.1 data-report flow

1. `git-provenance report` inspects required docs, specs, status sections, source files, tests, and report artifacts.
2. The command writes compact JSONL to `--out`, or pretty JSON to stdout.
3. Tests assert the report shape and CLI write path.

## Trust boundary

CommitProvenance records honest self-report metadata supplied by local
tools. It does not infer AI generation from code content. The v0 signing
scheme is Ed25519 with local keys. Production deployment requires key
management outside this repo.
