# AGENTS.md — commit-provenance

Operating contract for AI agents (Claude, Codex, Cursor) working in
this repo. Same conventions as the rest of the AthenaTheOwl
portfolio.

## What this repo is

A git-hook plus GitHub-App pair that emits and verifies signed
provenance records for AI-mixed commits. The schema and the signing
flow are the product; the per-vendor session-format adapters are
the integration layer.

This is the repo where AI agents are required to populate their own
provenance record. An AI that ships a commit without a corresponding
provenance entry fails the local pre-commit gate.

## Roles you may see in tasks

| Role | What they do |
|---|---|
| `schema-curator` | Owns `schemas/provenance.schema.json`; versions changes |
| `session-adapter` | Writes a per-vendor adapter (codex, cursor, devin, claude-code) that reads vendor session metadata and emits a normalized session record |
| `signer` | Owns the signing flow; key-management policy lives in `decisions/` |
| `verifier` | Walks commit ranges, verifies signatures, asserts schema conformance |
| `blame-walker` | Composes per-line attribution from the chain of per-commit records |

## Voice constraints

- Plain assertions. No marketing words. Banned set lives in
  `scripts/voice_lint.py::BANNED_FAIL`; spec 0001 adds the gate and
  spec 0002 may expand the term list.
- No antithetical reversals as a structural device.
- Security claims are conditional. The v0 signing scheme is
  Ed25519 with a local keypair; production deployment needs key
  management this repo does not provide.

## Gates (start in spec 0001 and continue in spec 0002)

```bash
uv run pytest
python scripts/voice_lint.py
python scripts/validate_schemas.py
python eval/signature_round_trip.py
python eval/schema_conformance.py
```

A PR that touches code without producing a corresponding provenance
record fails `eval/schema_conformance.py`. (Yes, this repo dogfoods
the gate on itself.)

## Out of scope

- Hosted key-management. Operator runs their own KMS / HSM.
- Detecting AI-generated code when no session metadata is supplied.
  This is an honest-self-report system, not a detector.
- Per-line statistical attribution. v0 records attribution at the
  commit level; per-line composition is derived from the commit chain
  by the blame-walker.
- Enforcement at the GitHub branch-protection level. The GitHub App
  posts a status; org admins decide whether to block merge on it.
