# GrokBot adapter

## Good fits

- signed-in, read-only X and cultural scanning;
- persistent browser research;
- campaign hypothesis generation;
- objection and language clustering;
- long-running public-surface audits;
- review-package assembly from already-cleared inputs;
- cross-platform performance synthesis;
- browser-heavy UAT where no more reliable API exists.

GrokBot is not the preferred authority for canon decisions, rights authorization, permanent memory, task state, approvals, or receipt verification.

## Shared-computer trust boundary

Assume Bots on the same Grok Agent Computer can access the same browser session and shared workspace. Separate Bot names organize work; they do not isolate credentials.

- Prefer a dedicated Third Signal operating account.
- Keep sensitive personal accounts off the shared computer.
- Grant Drive or other connectors only the actions the workflow needs.
- Disable delete/trash and permission-changing actions by default.
- Keep approved publish destinations narrow and explicit.

## Installation checklist

For each Bot or routine record:

- persistent Third Signal `role_id`;
- adapter id and runtime node id;
- bounded mission and capability list;
- prohibited mutations;
- source manifests and canonical paths;
- output contract and destination;
- schedule or trigger;
- approval policy;
- fallback adapter;
- receipt destination;
- current installation state and provider-native routine id.

Do not mark a routine installed until the provider UI exposes it and a shadow run produces a verified receipt. Store provider-issued identity and configuration hashes outside the mutable desired-state registry.

## Browser procedure

1. Confirm the intended account is visibly signed in.
2. Run read-only or shadow work first.
3. Record source queries, timestamps, and limitations.
4. Stop on CAPTCHA, account challenge, or unexpected permission prompt.
5. For external mutations, bind approval to exact content, account, destination, asset hashes, and expiration.
6. Confirm immediately before clicking the final submit/publish/send/deploy control.
7. Record the destination permalink or provider receipt and independently verify it.

Do not treat an internal-browser failure as permission to bypass controls. Route the task to another approved browser adapter when possible.

## Scheduling

Provider schedules are projections of the canonical HQ schedule. Store the provider-native routine id in adapter metadata, not as the schedule identity.

Scheduled work may autonomously observe, draft, test, and prepare review packets. It must pause for actions that require operator confirmation. A scheduled job should emit `noop` when no eligible work exists and `blocked` when authorization, access, or evidence is missing.

## Current Third Signal role posture

Use Grok primarily for:

- Signal Scout;
- Campaign Experiment Analyst;
- Community Analyst;
- persistent-browser research;
- public-surface audit and proposal generation.

Direct social posting is a production capability of the governed publishing lane. Grok may support intelligence and experiments, but it is not required as a shuttle between approved assets and social channels.
