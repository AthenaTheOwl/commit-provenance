# Spec 0001 — Foundation design

## Shape

A Python CLI installed as the `git-provenance` git subcommand. Three
layers: per-vendor session adapters, the emit / sign pipeline, and
the verify pipeline. A pre-commit hook calls emit. A GitHub Action
calls verify.

## Components

### Schema layer (`src/commit_provenance/schema/`)

- `loader.py` — loads and validates `provenance.schema.json` and
  `session.schema.json` once at startup; caches the validators.

### Session adapters (`src/commit_provenance/emit/session_loaders/`)

Each adapter is a pure function:

```python
def load(session_path: Path) -> SessionRecord: ...
```

Initial adapters:

- `claude_code.py` — reads a Claude Code session JSON.
- `codex.py` — reads an OpenAI Codex session metadata file.
- `cursor.py` — reads Cursor's chat-session export format.
- `devin.py` — reads Devin's run-transcript export.

In v0 only `claude_code` is required to be implemented; the others
are stubs that raise `NotImplementedError`.

### Emit CLI (`src/commit_provenance/emit/cli.py`)

`git provenance emit` flow:

1. `git diff --cached --name-only` to know which files are staged.
2. For each `--session` argument, run the matching adapter.
3. Build the `attribution[]` heuristic from session evidence
   (e.g. `accepted_diffs_count` against total hunks staged).
4. Build the provenance record (commit_sha is filled by the
   pre-commit hook after the commit object is created in a second
   pass; the emit step writes a placeholder and the post-commit
   hook patches the sha).
5. Canonicalize via RFC 8785 JCS, sign with Ed25519.
6. Write `.provenance/<short_sha>.json` and `git add` it.

### Sign / verify (`src/commit_provenance/sign/`,
`src/commit_provenance/verify/`)

- `sign/ed25519.py` — wraps the `cryptography` package. Key files
  live at `~/.config/commit-provenance/keys/<keyname>.{pub,key}` by
  default; path is overridable via `--keyfile`.
- `verify/cli.py` — `git provenance verify <range>`.
- `verify/conformance.py` — the script run in CI; reads the configured
  range from `pyproject.toml` `[tool.commit_provenance]`.

### Blame walker (`src/commit_provenance/blame/walker.py`)

For each line in a file at HEAD, walks `git blame` plus the per-commit
provenance records to compose a per-line attribution chain. Output
is a JSON map `{ file_path: { line: [ provenance_record_refs ] } }`.

In v0 the walker is a CLI command, not yet a GitHub App surface.

### Hooks (`hooks/`)

- `pre-commit` — bash wrapper that invokes `git provenance emit
  --staged --session-from-env` (reads `$COMMIT_PROVENANCE_SESSIONS`).
- `pre-push` — invokes `git provenance verify ORIG_HEAD..HEAD` and
  exits non-zero on failure.

### GitHub Action (`github-app/action.yml`)

A composite action that:

1. checks out the PR head,
2. runs `git provenance verify origin/main...HEAD`,
3. posts a status check `provenance/verified` or
   `provenance/missing`.

## Data model

```
ProvenanceRecord
  record_version: "1"
  commit_sha
  author_email
  created_at
  attribution: [ { kind, share, session_ref } ]
  session_refs: [ session_id ]
  signing: { algorithm: "ed25519", public_key_fingerprint, signature_b64 }

SessionRecord
  session_id, vendor, started_at, finished_at
  model_identifier
  prompts_count, accepted_diffs_count
  vendor_payload_hash
```

## Out of scope for spec 0001

- Hosted KMS / HSM signing.
- Per-line attribution as a GitHub-comment surface.
- Statistical detection of AI-generated code without session metadata.
- Multi-org public key federation.
