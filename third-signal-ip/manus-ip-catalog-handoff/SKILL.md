---
name: manus-ip-catalog-handoff
description: Package Manus-generated IP media for the Third Signal catalog, or ingest downloaded packages when verified catalog filesystem access is available. Use after image, voice, video or episode production.
---

# Manus IP catalog handoff

Generation is not catalog delivery. Separate generated, downloaded, cataloged, QA-reviewed, canon-approved and publicly released states.

## Cloud producer mode

When running in Manus cloud, do not assume that a local Mac or Google Drive folder is mounted. Produce a downloadable versioned ZIP and `CATALOG_HANDOFF.json`. A Markdown attachment is guidance, not proof of installed skill or local access.

Include the existing property slug and catalog folder supplied by the operator, dispatch/chapter ID, task URL/ID, source references and hashes, model/settings, actual observed cost (or `not_observed`), filenames, roles, versions, supersession relationships, approval evidence and unresolved defects. Never invent approval or cloud-sync success.

Package folders: `final/`, `source_clips/`, `voice_tracks/`, `sfx/`, `refs/`, `project/`, `qa/`, `superseded/`. Preserve original source bytes. Include clean and captioned exports, SRT, timeline/EDL, rebuild instructions, prompts and a SHA-256 file list. Keep failed takes with their rejection reasons; identify the preferred candidate explicitly.

Use relative paths in the handoff. Record a proposed catalog destination without claiming a write. End with downloadable outputs and the next local ingestion action.

## Local catalog operator mode

Read the installed Signal IP Publishing workflow. Resolve the existing property from the catalog, not the provider's task title. Verify the authoritative DriveFS root using its `com.google.drivefs.item-id` attribute; similarly named ordinary folders are not authoritative.

File complete motion packages under the existing property's `03_VIDEO_AUDIO/<dispatch-or-chapter>/<run-and-version>/`. Keep project files, shot takes and voices together so the edit remains reconstructable. Stage source approval documents in `00_INBOX`; original art remains in `02_VISUALS`. Mirror the package into the established `03_SIGNAL_PUBLISHING` staging area. Do not create canon or public release merely because generation succeeded.

Copy, never move or overwrite differing bytes. Repeated imports must skip identical hashes and stop on conflicting destinations. Check ZIP paths before extraction. Verify source checksums, copied-byte hashes and media metadata. Register media in the content-addressed vault with property, role, source task and version; mark failed/replaced takes `superseded` and current unapproved candidates `available-local`.

Save an ingestion receipt naming exact destinations, hashes, verification results, known defects and the state of cloud synchronization. Local DriveFS readback alone does not prove cloud synchronization. Refresh the inventory and leave a Studio ship log. Do not claim installed Manus skill status without observing it in Manus.
