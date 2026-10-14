---
name: manus-integration
description: Operate Manus 2.0 through verified Studio, Video and Alchemy, API v2, and Hermes routes with explicit source, cost, skill and completion evidence.
version: 2.0.0
author: Third Signal Lab
platforms: [macos, linux]
---

# Manus Integration

Prepare a bounded specification and select the route that actually exposes the needed capability. Manus 2.0 product features do not imply API, bridge or local-wrapper parity. Inspect the current account and tool surface; never infer model IDs, free entitlement or local filesystem access from a product announcement.

## Route

| Route | Use | Verify first |
| --- | --- | --- |
| Studio desktop | Local-file intake, Video Editor, timeline work | Actual app/window, signed-in account, folder and cloud/local scope |
| Video / Alchemy | Reference-driven creation and editing, account promotions | Exact offer, model, quality, duration, output count and cost |
| Developer API v2 | Durable task creation, messages, skill selection and output recovery | Current schema, credentials through secure configuration, confirmation events |
| Hermes bridge | Operator-approved dispatch and retrieval | Actual tool contract; never self-approve a proposal |

For motion read [video production](references/manus-2-video.md) and [model prompting](references/seedance-minimax-prompting.md). For API work read [task lifecycle](references/task-lifecycle.md). Default to private output when audience is unspecified.

## Before execution

Record task/run ID or submission fingerprint, exact account/project, selected asset IDs and hashes, latest cast references, source-use authority, model label, aspect ratio, duration, quality, expected outputs, offer evidence, paid-credit ceiling and release scope. Keep earlier accepted assets immutable. Assign every image/video reference a specific identity, environment, composition or motion role.

A one-free-video promotion is not unlimited credits. Verify eligibility at submission, including retries and edits. When scope is free-only, paid ceiling is zero: no top-up, upgrade or automatic paid fallback. Do not spend the offer on a throwaway test. Preserve task IDs immediately and reconcile ambiguous submissions before trying again.

## Skills and local adapters

API v2 supports skill selection through actual IDs resolved with skill.list, then enable_skills/force_skills as documented. OAuth clients may be restricted to App-owned skills. A Markdown attachment is useful instruction material, not proof a skill was installed or invoked. Do not send private credentials or unrelated source libraries inside a skill pack.

Some installations have a manus_client.py wrapper. Inspect its --help and code capabilities; the historically observed create/status/send wrapper does not implement full file upload, event confirmation, skill discovery or video timeline control. Discover its path locally instead of assuming another operator's home or host. Desktop automation and cloud API execution are different routes.

## Complete and recover

Inspect task messages, background jobs and actual artifacts. Generated, downloaded, QA-accepted, canon-approved and publicly released are distinct states. Download originals and preserve prompts, exposed model/settings, costs or not_observed, source hashes, MP4 metadata and editable project reference where available. Hash local output bytes and review playback; provider chat claiming success is insufficient.

For video verify identity, hands/weapon geometry, spatial continuity, action cause/effect, intended mechanic, audio, titles and duration. For sites verify live routes and images. Archive a receipt, remaining defects and next action. Public sharing, deployment and canon promotion require their own recorded user scope.

Official references were checked 2026-10-14; inspect current schemas and live account limits before each execution.
