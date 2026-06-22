# Spec 0002 acceptance

## Required checks

- `python -m uv run pytest`
- `python -m uv run git-provenance report --out reports/commit-provenance-v0.1.jsonl`

## File checks

- `PRODUCT_BRIEF.md` exists at repo root.
- `SYSTEM_MAP.md` exists at repo root.
- `specs/0002-design/requirements.md` exists.
- `specs/0002-design/design.md` exists.
- `specs/0002-design/tasks.md` exists.
- `specs/0002-design/acceptance.md` exists.
- `commit_provenance/cli.py` exists.
- `commit_provenance/model.py` exists.
- `commit_provenance/scoring.py` exists.
- At least one `reports/*.jsonl` artifact exists.
