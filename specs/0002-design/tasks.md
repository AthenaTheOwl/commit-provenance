# Spec 0002 tasks

## Done

- Create root product and system-map docs.
- Create the `specs/0002-design/` ledger files.
- Move the importable package surface to root `commit_provenance/`.
- Emit a checked-in JSONL readiness report.
- Keep uv development dependencies under `[dependency-groups]`.

## Next

- Add `schemas/provenance.schema.json` and `schemas/session.schema.json`.
- Add the Claude Code session adapter and fixture-backed schema tests.
- Add Ed25519 signing, `keygen`, emit, and verify commands.
- Add pre-commit, post-commit, and pre-push hooks with recursion-safe amend behavior.
