# Spec 0001 — Foundation tasks

Ordered task list for the first 2-3 PRs after the scaffold.

## PR 1 — package skeleton plus schemas plus claude-code adapter

- [ ] Add `pyproject.toml` declaring `commit-provenance` and the
      `git-provenance` CLI entry.
- [ ] Add `src/commit_provenance/__init__.py` with `__version__`.
- [ ] Add `src/commit_provenance/cli.py` with `version` command.
- [ ] Add `schemas/provenance.schema.json` per R-CP-002.
- [ ] Add `schemas/session.schema.json` per R-CP-003.
- [ ] Add `src/commit_provenance/schema/loader.py`.
- [ ] Add `src/commit_provenance/emit/session_loaders/claude_code.py`.
- [ ] Add stub adapters `codex.py`, `cursor.py`, `devin.py` that
      raise `NotImplementedError`.
- [ ] Add `tests/fixtures/sessions/claude_code.json`.
- [ ] Add `tests/test_session_loader.py`.
- [ ] Add `decisions/DEC-CP-001-signing-choice.md`,
      `decisions/DEC-CP-002-attribution-taxonomy.md`.

## PR 2 — sign / verify plus emit CLI

- [ ] Add `src/commit_provenance/sign/ed25519.py`.
- [ ] Add `src/commit_provenance/emit/cli.py`.
- [ ] Add `src/commit_provenance/verify/cli.py`.
- [ ] Add `src/commit_provenance/verify/conformance.py`.
- [ ] Add `tests/test_sign_roundtrip.py`.
- [ ] Add `tests/test_emit_cli.py` running emit against the fixture
      session and asserting a valid `.provenance/*.json` file.
- [ ] Add `tests/test_verify_cli.py`.
- [ ] Add `eval/signature_round_trip.py`,
      `eval/schema_conformance.py`.
- [ ] Add `scripts/voice_lint.py`,
      `scripts/validate_schemas.py`.

## PR 3 — hooks plus GitHub Action plus dogfood

- [ ] Add `hooks/pre-commit` and `hooks/pre-push`.
- [ ] Add `git provenance install-hook` CLI command.
- [ ] Add `github-app/action.yml`.
- [ ] Add `src/commit_provenance/blame/walker.py`.
- [ ] Dogfood: install the hook in this repo, regenerate
      `.provenance/` for the last 10 commits, check in
      `.provenance/INDEX.md`.
- [ ] Add `docs/dev/installation.md`.
- [ ] Add `docs/regulatory/eu-ai-act-article-12.md` mapping the
      schema fields to Article 12 logging requirements.
