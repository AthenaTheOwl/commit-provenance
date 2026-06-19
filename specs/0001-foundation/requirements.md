# Spec 0001 — Foundation requirements

The first spec for CommitProvenance. Names the provenance schema,
the session schema, the signing flow, the verifier contract, and
the per-vendor session adapter shape.

## Requirements

- **R-CP-001** — The repo MUST expose a `commit-provenance` Python
  package with a `git provenance` CLI installed via the
  `git-provenance` entry point.

- **R-CP-002** — A provenance record MUST conform to
  `schemas/provenance.schema.json` with fields: `record_version`,
  `commit_sha` (filled by hook), `author_email`, `created_at`,
  `attribution[]` (list of `{kind, share, session_ref}` where
  `kind ∈ {human, ai_suggested_human_edited, ai_authored_human_reviewed,
  ai_generated_no_review}`), `session_refs[]`, `signing` (algorithm,
  public_key_fingerprint, signature_b64).

- **R-CP-003** — A session record MUST conform to
  `schemas/session.schema.json` with fields: `session_id`,
  `vendor` (`codex|cursor|devin|claude_code|other`),
  `started_at`, `finished_at`, `model_identifier`, `prompts_count`,
  `accepted_diffs_count`, `vendor_payload_hash`.

- **R-CP-004** — At least one session adapter MUST be implemented in
  v0. Recommended starter: `claude_code`. Each adapter is a pure
  function `session_path -> SessionRecord`.

- **R-CP-005** — The emit CLI MUST:
  - read staged changes from `git diff --cached`,
  - load referenced session records,
  - construct a provenance record,
  - sign it with the configured Ed25519 keypair,
  - write it to `.provenance/<short_sha>.json`,
  - stage the provenance file as part of the same commit.

- **R-CP-006** — The verify CLI MUST accept a commit range, walk
  each commit, read the corresponding `.provenance/*.json`, verify
  the Ed25519 signature against the configured public-key set,
  validate the schema, and exit non-zero on the first failure.

- **R-CP-007** — Signing keys MUST be Ed25519. The signing input is
  the canonical JSON of the provenance record with the `signing`
  field omitted (RFC 8785 JCS).

- **R-CP-008** — The pre-commit hook MUST be installable via
  `git provenance install-hook`. The hook is opt-in per-repo; this
  repo dogfoods it.

- **R-CP-009** — A commit with no AI session metadata MUST still
  produce a provenance record with `attribution = [{kind: human,
  share: 1.0}]`. Absence of AI metadata is never silent.

- **R-CP-010** — The conformance script MUST run in CI and fail the
  build when any commit in a configured range lacks a provenance
  record, or when any provenance record fails signature verification
  or schema validation.

- **R-CP-011** — All tests run against checked-in fixture sessions
  under `tests/fixtures/sessions/`. No live vendor API access at gate
  time.

- **R-CP-012** — The repo MUST include
  `decisions/DEC-CP-001-signing-choice.md` (why Ed25519, what changes
  for KMS / HSM in production) and
  `decisions/DEC-CP-002-attribution-taxonomy.md` (the four kinds
  in R-CP-002 and why).
