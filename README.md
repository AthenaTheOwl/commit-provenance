# CommitProvenance

Trustable author attribution for AI-mixed codebases. Cryptographically
signed, machine-verifiable provenance records for every line of code
in a repo: human-authored, AI-suggested-and-edited,
AI-authored-and-reviewed, generated-and-merged-without-review.

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
the first-mover advantage on becoming the EU AI Act compliance
artifact for code-gen.

Buyers: regulated-industry eng teams (defense, finance, medical
devices); open-source maintainers facing AI-PR floods; firms needing
to meet contractual "no AI-generated code" clauses.

## Status

v0 scaffold. No implementation. The repo holds the README, the
license, the agents contract, the foundation spec, and the literal
first PR plan. The first runnable PR after this scaffold lands the
provenance schema and a minimal `git-provenance` CLI that emits a
provenance record for a staged change.

## How to run

Placeholder. After implementation:

```bash
git provenance emit --session ~/.codex/sessions/2026-06-19.json \
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
  specs/
    0001-foundation/
      requirements.md          # R-CP-NNN
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
```

Downstream additions:

```
  src/commit_provenance/
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
