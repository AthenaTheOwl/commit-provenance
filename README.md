# commit-provenance

Status: archived 2026-07-01. Successor is agent-notary-layer, which already has the signed-receipt machinery this repo needed.

`git blame` tells you which human last touched a line. It cannot tell you that
the line was suggested by Codex, edited by a person, and merged without review.
For a codebase where some of the authors are models, that distinction is the
whole question, and the tool that would answer it does not exist in git.

## What it does

EU AI Act Article 12 requires logging for high-risk AI use, code generation
included. CMMC 2.0 and FedRAMP are starting to ask the same thing. Meanwhile the
volume coming out of Codex, Cursor, and Devin has made "who actually wrote this"
a question `git blame` answers wrong, because it was never asked to answer it.

commit-provenance writes the missing record. It is a git hook plus a GitHub App.
For any commit with AI-session metadata available, the hook emits a signed
`provenance.json` next to the commit, and a conformance check verifies the
signatures on push and rejects unsigned AI-mixed commits. Per-line attribution
gets composed later by a blame walker over those per-commit records, across four
states: human-authored, AI-suggested-and-edited, AI-authored-and-reviewed,
generated-and-merged-without-review.

The schema, the signing, and the session adapters are the product surface. The
records are self-reported by the local tools, so this is honest metadata, not
inference from code content. It does not guess that a line is AI-written; it
keeps the receipt the tools hand it, and signs it so the receipt cannot be
forged after the fact.

## Status

v0.1 is the data-report slice: a product brief, system map, design ledger, a
runnable Python CLI, tests, and one checked-in report artifact. The signed
emit-and-verify flow is specified in `specs/0001-foundation` but not yet built.

## Try it

One command, no setup, no keys. It reads the committed readiness report and
prints which artifacts the repo has against the ones it needs:

```bash
python -m uv run git-provenance show
```

```
commit-provenance - repo readiness, report v0.1 (commit-provenance @ 55bad7e, branch main)
generated 2026-06-22T23:16:11Z - 17/17 required artifacts present (100%), 0 status section(s) missing

artifact                                                status
--------------------------------------------------------------
PRODUCT_BRIEF.md                                       present
README.md                                              present
STATUS.md                                              present
SYSTEM_MAP.md                                          present
commit_provenance/cli.py                               present
commit_provenance/model.py                             present
commit_provenance/scoring.py                           present
pyproject.toml                                         present
reports/commit-provenance-v0.1.jsonl                   present
specs/0001-foundation/acceptance.md                    present
specs/0001-foundation/design.md                        present
specs/0001-foundation/requirements.md                  present
specs/0001-foundation/tasks.md                         present
specs/0002-design/acceptance.md                        present
specs/0002-design/design.md                            present
specs/0002-design/requirements.md                      present
specs/0002-design/tasks.md                             present

repository surfaces:
  docs           1
  spec_files     8
  tests          2
  jsonl_reports  1

biggest gap: none - all 17 required artifacts present. readiness 100%. next surface is the signed emit/verify flow (specs/0001).
```

The readiness report is the tool pointed at itself: it checks whether the repo
has the pieces v0.1 promised, and tells you the next surface to build.

## Live demo

A read-only browser over the same committed report
(`reports/commit-provenance-v0.1.jsonl`): required artifacts present versus
missing, the readiness score, and the repository surfaces counted. Same data as
the CLI, interactive.

```bash
python -m uv run --with streamlit streamlit run streamlit_app.py
```

Streamlit Community Cloud: New app -> repo `AthenaTheOwl/commit-provenance`,
branch `main`, main file `streamlit_app.py`.

<!-- live-url: https://… -->

## How to run

Current report command:

```bash
python -m uv run git-provenance report --out reports/commit-provenance-v0.1.jsonl
python -m uv run git-provenance version
```

The signed emit-and-verify flow, once built:

```bash
git provenance emit --session ~/.claude/sessions/2026-06-19.json \
  --staged --out .provenance/commit-abc1234.json

git provenance verify HEAD~5..HEAD
```

## How it connects

commit-provenance keeps the receipt at the commit; the neighbors enforce and
extend it:

- [proof-gate-runner](https://github.com/AthenaTheOwl/proof-gate-runner) — the
  drop-in GitHub Action that runs the conformance gate on AI-PRs, the layer that
  would reject an unsigned AI-mixed commit on push.
- [agent-notary-layer](https://github.com/AthenaTheOwl/agent-notary-layer) — the
  receiver-attested receipt schema for cross-org agent actions; same signing
  instinct applied to actions instead of commits.
- [mcp-security-lab](https://github.com/AthenaTheOwl/mcp-security-lab) — the
  default-deny tool policies for the agents whose edits this repo attributes.

## Layout

```
commit_provenance/     cli, model, report, scoring
reports/               the one v0.1 readiness report this ships
specs/0001-foundation/ the signed emit/verify flow, specified
specs/0002-design/     the design pass
docs/  tests/          first-pr walkthrough, cli + report tests
```

Downstream, the emit/verify/sign/blame modules, the `provenance.schema.json`,
the git hooks, and the GitHub Action wrapper land alongside.

## License

MIT. See [LICENSE](LICENSE).
