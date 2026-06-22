# CommitProvenance

Commit-time author attribution for AI-mixed codebases. Cryptographically
signed, machine-verifiable provenance records for every commit in a
repo, with per-line attribution composed later by the blame walker:
human-authored, AI-suggested-and-edited, AI-authored-and-reviewed,
generated-and-merged-without-review.

## What this is

EU AI Act Article 12 explicitly requires logging for high-risk AI use
including code generation. DoD CMMC 2.0 and FedRAMP are starting to
ask similar questions. Codex / Cursor / Devin volume has made "who
actually wrote this" unanswerable by `git blame`. The 2026-W22 voice
review surfaced encoding bugs that would have been caught earlier if
AI-author attribution were structured at commit time.

CommitProvenance is a git hook plus a GitHub App. For any PR with
AI-session metadata available, the hook emits a signed
`provenance.json` alongside the commit. A conformance check verifies
signatures on push and rejects unsigned AI-mixed commits.

The schema (`provenance.schema.json`) plus the signing infrastructure
plus the integration with Codex / Cursor / Devin session metadata is
the product surface.

Buyers: regulated-industry eng teams (defense, finance, medical
devices); open-source maintainers facing AI-PR floods; firms needing
to meet contractual "no AI-generated code" clauses.

## Status

v0.1 data-report slice. The repo has a product brief, system map,
design ledger, runnable Python CLI, tests, and one checked-in report
artifact. The signing and hook flow remains specified but not complete.

## How to run

Current report command:

```bash
python -m uv run git-provenance report --out reports/commit-provenance-v0.1.jsonl
python -m uv run git-provenance version
```

Future signed emit flow:

```bash
git provenance emit --session ~/.claude/sessions/2026-06-19.json \
  --staged --out .provenance/commit-abc1234.json

git provenance verify HEAD~5..HEAD
```

## Layout

```
commit-provenance/
  README.md
  LICENSE
  AGENTS.md
  .gitignore
  pyproject.toml
  STATUS.md
  PRODUCT_BRIEF.md
  SYSTEM_MAP.md
  commit_provenance/
    __init__.py
    cli.py
    model.py
    report.py
    scoring.py
  reports/
    commit-provenance-v0.1.jsonl
  specs/
    0001-foundation/
      requirements.md          # R-CP-NNN
      design.md
      tasks.md
      acceptance.md
    0002-design/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
  tests/
    test_cli.py
    test_report.py
```

Downstream additions:

```
  commit_provenance/
    schema/loader.py
    emit/cli.py                  # `git provenance emit`
    emit/session_loaders/
      codex.py
      cursor.py
      devin.py
      claude_code.py
    sign/ed25519.py
    verify/cli.py                # `git provenance verify`
    verify/conformance.py        # gate logic
    blame/walker.py              # composes per-line attribution from per-commit records
  schemas/
    provenance.schema.json
    session.schema.json
  hooks/
    pre-commit                   # installs as a git hook
    post-commit
    pre-push
  github-app/
    action.yml                   # GitHub Action wrapper
  tests/
    fixtures/sessions/codex.json
    fixtures/sessions/cursor.json
  eval/
    signature_round_trip.py
    schema_conformance.py
```

## License

MIT. See [LICENSE](LICENSE).
