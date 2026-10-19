# Preserve attribution history when moving to agent-notary-layer

This repository remains archived. `agent-notary-layer` is the maintained successor
for signed receipt verification. It is not a drop-in replacement for every
attribution field in the commit-provenance scaffold.

Inventory the existing report rows and record their file hashes before migrating.
Keep the source commit SHA, supplied author/session metadata, collection method,
and any known gaps as historical evidence. A missing session record stays missing;
a new signature cannot reconstruct it or establish who actually wrote a line.

Create an external migration manifest containing those references and hashes,
canonicalize it by an agreed rule, then bind its action hash to a normal notary
receipt. Verify the receipt and retain the manifest beside it. Keep old records
readable while a consumer learns to follow the manifest; do not rewrite them into
newly verified observations.

The successor checks schema, signatures, chains and the delegated-hop rules it
implements. Attribution confidence, test correctness, identity proofing and key
custody remain separate concerns. A migration acceptance check should therefore
include a valid manifest, a tampered manifest, an unavailable source session and
a commit that was amended after the old report was written. The last two should
produce explicit evidence gaps rather than a fresh authorship claim.

[AI Product Team's change workflow](https://github.com/3orionkings/ai-product-team/blob/main/workflows/process-change.md)
offers a useful distinction here: preserve historical evidence while reassessing
which present claim it supports. The migration manifest described above is a
proposed integration recipe, not a shipped adapter or revived signing service.
