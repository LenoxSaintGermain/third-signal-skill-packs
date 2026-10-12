# Workflow portability audit — 2026-10-11

Surface: Studio. Scope: enable a bounded Grok trial from WIND through comic and reader release.

Added missing current WIND execution entrypoint, recipe engine, continuation desk, standalone production and Signal Stage route. Preserved the earlier wind-worldbuilding doctrine and linked it to production. Updated Signal Stage capture contract/helper and tests. Added a portable archive skill instead of publishing machine-specific private vault scripts. Added trial prompt, private-input checklist, capability preflight and evidence scorecard.

The existing publishing-desk queue tools remain optional, with their explicit source/UAT/release gates intact. They do not generate art or deploy a reader. The ZIP does not include them or the owner's account-specific examples. Existing untracked google-flow work was preserved untouched; its motion adapter is a follow-on, not a dependency of the comic pilot. Private social queues, canon catalogs, account sessions and private vault scripts were deliberately excluded. The actual Signal Stage runtime and provider adapters must be supplied separately when selected.

Validation: 4 existing capture/ingestion tests passed, including overwrite refusal, missing-original provenance, independent states and selected-asset approval. Relative documentation links and bundle hashes checked. Generic skill validator could not run because its interpreter lacks PyYAML; frontmatter checked structurally instead. Grok execution itself has not been tested.

Linear synchronization unavailable: connector rejected the request for a missing link_id. Ready-to-sync acceptance: reusable workflow exists, no private source assets or credentials included, one prompt defines a bounded observable deployment trial. Deployment/build/live URL: not applicable to this documentation release. Git source revision is supplied by the repository commit.
