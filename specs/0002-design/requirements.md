# Spec 0002 requirements

## Status

Proposed. This spec records the v0.1 data-report slice and the next
implementation queue. It does not supersede spec 0001.

## Requirements

- R-CP-020: The repo has root `PRODUCT_BRIEF.md` and `SYSTEM_MAP.md` files.
- R-CP-021: `STATUS.md` uses the exact headings `Current state`, `Known limits`, and `Next feature queue`.
- R-CP-022: The Python package is importable from root `commit_provenance/`.
- R-CP-023: The CLI writes a checked-in JSONL report artifact under `reports/`.
- R-CP-024: Dev dependencies live under `[dependency-groups]`, and `[tool.uv] package = true` is set.
- R-CP-025: Signed provenance remains future work until schemas, adapters, keys, and hooks exist.
