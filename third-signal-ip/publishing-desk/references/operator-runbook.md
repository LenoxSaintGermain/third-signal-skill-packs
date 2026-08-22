# Publishing Desk operator runbook

## State ownership

| State | Meaning | Next actor |
| --- | --- | --- |
| `inbox` | Source is registered but unread | Desk agent |
| `preflight-running` | Recovery package is being materialized | Desk agent |
| `needs-recovery` | Required originals or evidence are missing | Recovery operator/agent |
| `operator-review` | Source package is ready for a creative decision | Operator |
| `source-approved` | Operator authorized production from this package | Signal Stage agent |
| `production-running` | Runtime pack and private preview are being built | Signal Stage agent |
| `uat-review` | Private preview awaits operator acceptance | Operator |
| `release-approved` | Operator authorized the publishing integration | Publisher |
| `published` | A verified release receipt was recorded | None |
| `on-hold` | Operator paused the item | Operator |
| `rejected` | Item is preserved as non-production evidence | None |

## Command sequence

Set the reusable command prefix from the Signal Publishing repository:

```bash
DESK="skills/publishing-desk/scripts/run.sh --root publishing-desk"
```

`run.sh` selects a verified interpreter and refuses silent/broken Python shims. Every successful state-changing command must emit the resulting desk JSON; an empty response is a failed verification even when the shell reports exit `0`.

Intake a conversation:

```bash
$DESK intake \
  --id witches-time-economy \
  --title "Subverting the Witch Trope" \
  --property witches-time-economy \
  --conversation 6a6eb04a-9ae8-83ea-b24f-3ca202f71c80 \
  --priority 90 --by lenox
```

Recover and route:

```bash
$DESK begin-preflight --id witches-time-economy --by publishing-desk-agent
$DESK complete-preflight --id witches-time-economy \
  --package publishing-desk/packages/witches-time-economy/source-package/v1 \
  --blocker "Original character sheet binary needs export" \
  --by publishing-desk-agent
```

Operator source approval:

```bash
$DESK approve-source --id witches-time-economy \
  --evidence "Approved source-package review record" --by lenox
```

Production and UAT:

```bash
$DESK begin-production --id witches-time-economy --by signal-stage-agent
$DESK submit-uat --id witches-time-economy \
  --preview https://private-preview.example/story \
  --report /absolute/path/to/UAT.md \
  --ingestion-spec /absolute/path/to/ingestion.json \
  --library-pack /absolute/path/to/library-pack \
  --by signal-stage-agent
```

Operator release approval and receipt recording:

```bash
$DESK approve-release --id witches-time-economy \
  --evidence "Desktop/mobile UAT accepted" --by lenox
$DESK record-publish --id witches-time-economy \
  --receipt /absolute/path/to/publish-receipt.json --by publisher
```

## Recovery loop

After resolving every blocker, run `begin-preflight` again from `needs-recovery`. Create a new versioned source-package directory; never overwrite the prior recovery record.

## Operating constraints

- Keep credentials and signed download URLs out of desk JSON and Git.
- Use absolute paths for external artifacts and repository-relative paths for tracked artifacts.
- Store binary media in the content-addressed vault or approved Drive hierarchy, not in Git.
- Do not hand-edit events or approvals.
