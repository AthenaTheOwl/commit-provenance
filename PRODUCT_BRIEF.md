# Product brief

## Problem

Teams that mix human commits with AI-assisted code need a durable record
of what was authored, suggested, reviewed, and merged. Plain `git blame`
does not capture session metadata, model identifiers, accepted diffs, or
review state.

## v0.1 product

CommitProvenance v0.1 is a data-report repo. It defines the product
contract, maps the planned system, and ships a small CLI that reports
which readiness artifacts are present in the repo.

## User

- Regulated engineering teams that need commit-time logging evidence.
- Maintainers who need a consistent record for AI-assisted pull requests.
- Internal platform teams that want a local hook before a central service.

## Output

- A normalized provenance schema for future signed commit records.
- A session schema for vendor metadata adapters.
- A CLI and report artifact that show which v0.1 surfaces are present.
- A design ledger for future implementation work.

## Non-goals

- Hosted key management.
- AI-code detection when no session metadata exists.
- Branch-protection enforcement by default.
