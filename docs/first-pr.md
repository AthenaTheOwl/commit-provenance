# First PR after the scaffold

Branch: `feat/0001-schemas-and-claude-code-adapter`

## Scope

Land the package skeleton, the two JSON schemas, the schema loader,
and the first session adapter (claude-code). No signing or emit yet.

### Files added

- `pyproject.toml` — declares `commit-provenance`, CLI entry
  `git-provenance = "commit_provenance.cli:main"`, `[tool.uv]
  package = true`, and dev deps under `[dependency-groups]`.
- `src/commit_provenance/__init__.py` — `__version__ = "0.0.1"`.
- `src/commit_provenance/cli.py` — Click app with `version` command.
- `schemas/provenance.schema.json` — per R-CP-002.
- `schemas/session.schema.json` — per R-CP-003.
- `src/commit_provenance/schema/__init__.py`
- `src/commit_provenance/schema/loader.py` — caches validators.
- `src/commit_provenance/emit/__init__.py`
- `src/commit_provenance/emit/session_loaders/__init__.py`
- `src/commit_provenance/emit/session_loaders/claude_code.py`.
- `src/commit_provenance/emit/session_loaders/codex.py` (raises
  `NotImplementedError`).
- `src/commit_provenance/emit/session_loaders/cursor.py` (raises
  `NotImplementedError`).
- `src/commit_provenance/emit/session_loaders/devin.py` (raises
  `NotImplementedError`).
- `tests/fixtures/sessions/claude_code.json` — a real (sanitized)
  Claude Code session file.
- `tests/test_schema_loader.py` — asserts both schemas pass
  `Draft202012Validator.check_schema`.
- `tests/test_session_loader.py` — asserts the claude-code adapter
  produces a record that validates against `session.schema.json`.
- `decisions/DEC-CP-001-signing-choice.md` — Ed25519 with local
  keypair in v0; KMS / HSM is the production swap path.
- `decisions/DEC-CP-002-attribution-taxonomy.md` — the four kinds
  in R-CP-002 and why.

### Files NOT touched

- `src/commit_provenance/sign/` — empty until PR 2.
- `src/commit_provenance/verify/` — empty until PR 2.
- `src/commit_provenance/emit/cli.py` — empty until PR 2.
- `src/commit_provenance/blame/` — empty until PR 3.
- `hooks/`, `github-app/` — empty until PR 3.
- `eval/` — empty until PR 2.

## Verification

```bash
python -m uv sync
python -m uv run git-provenance version
# expect: commit-provenance 0.0.1

python -m uv run pytest
# expect: 2 tests pass

python -c "
from commit_provenance.emit.session_loaders.claude_code import load
r = load('tests/fixtures/sessions/claude_code.json')
print(r.session_id, r.vendor, r.model_identifier, r.accepted_diffs_count)
"
```

## Out of scope for this PR

- Ed25519 sign / verify.
- Emit CLI (no `.provenance/*.json` files written yet).
- Pre-commit hook.
- GitHub Action.
- Per-line blame walker.
