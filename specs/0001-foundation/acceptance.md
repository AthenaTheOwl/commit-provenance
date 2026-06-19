# Spec 0001 — Foundation acceptance

## What "v0 done" means

Spec 0001 is closed when:

1. The three PRs in `tasks.md` are merged.
2. `uv pip install -e .[dev]` succeeds.
3. `git provenance --help` prints the CLI surface (installable as
   the `git-provenance` subcommand).
4. The pre-commit hook is installed on this repo and produces a
   `.provenance/*.json` entry on every commit.
5. The Ed25519 sign / verify round-trip passes against fixtures.
6. The conformance script runs in CI and exits non-zero if any
   commit in the configured range lacks or fails its provenance
   record.

## Commands to run

```bash
uv pip install -e .[dev]
git provenance --help

uv run pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py

# Generate a signing keypair (local, not for production)
git provenance keygen --out ~/.config/commit-provenance/keys/dogfood

# Install the hook on this repo
git provenance install-hook

# Verify the configured range
python -m commit_provenance.verify.conformance --range origin/main..HEAD

python eval/signature_round_trip.py
python eval/schema_conformance.py
```

## Gates

| Gate | Source | Blocks merge when |
|---|---|---|
| pytest | `tests/` | any test fails |
| voice_lint | `scripts/voice_lint.py` | banned term anywhere |
| schemas | `scripts/validate_schemas.py` | any provenance or session record fails |
| signature_round_trip | `eval/signature_round_trip.py` | sign-then-verify fails |
| schema_conformance | `eval/schema_conformance.py` | any commit in range lacks a record or fails verify |

## What v0 explicitly does NOT include

- Hosted KMS / HSM signing.
- Statistical AI-detection without session metadata.
- Multi-org public-key federation.
- Per-line attribution as a posted-comment surface.
