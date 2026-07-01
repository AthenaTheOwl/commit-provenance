# CommitProvenance status

## Current state
- Archived 2026-07-01. The signed-receipt machinery this repo was building toward already exists in agent-notary-layer, so work continues there instead of here.
- v0.1 is a data-report slice with a runnable `git-provenance report` command.
- The repo has a product brief, system map, design ledger, tests, and a checked-in report artifact.
- Spec 0001 still defines the future signed emit, verify, hook, and GitHub Action workflow.

## Known limits
- v0.1 does not emit signed `.provenance/*.json` records for commits.
- v0.1 does not install git hooks or verify Ed25519 signatures.
- The report CLI summarizes repository readiness; it is not the final conformance gate.

## Next feature queue
- Add `schemas/provenance.schema.json` and `schemas/session.schema.json`.
- Add the Claude Code session adapter and fixture-backed schema tests.
- Add Ed25519 signing, `keygen`, emit, and verify commands.
- Add the pre-commit, post-commit, and pre-push hooks with recursion-safe amend behavior.

- Resolve factory defect: implementation produced no file changes relative to base; refusing to mark a no-op as done
- Resolve factory defect: claude_code review requested patch; inspect defect log
- Resolve factory defect: missing PRODUCT_BRIEF.md,SYSTEM_MAP.md
- Resolve factory defect: missing reports/*.jsonl
- Resolve factory defect: PRODUCT_BRIEF.md is required for active repos
- Resolve factory defect: SYSTEM_MAP.md is required for active repos
- Resolve factory defect: expected file 'PRODUCT_BRIEF.md' is missing
- Resolve factory defect: expected file 'SYSTEM_MAP.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/requirements.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/design.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/tasks.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/acceptance.md' is missing
- Resolve factory defect: expected file 'commit_provenance/cli.py' is missing
- Resolve factory defect: expected glob 'reports/*.jsonl' matched no files
- Resolve factory defect: module 'cli' declares source 'commit_provenance/cli.py', but it is missing
- Resolve factory defect: module 'model' declares source 'commit_provenance/model.py', but it is missing
- Resolve factory defect: module 'report' declares source 'commit_provenance/scoring.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
