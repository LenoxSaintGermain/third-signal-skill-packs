---
name: grokbot-operator
description: Operate GrokBot or its Agent Computer as a governed Third Signal execution adapter. Use for Bot and routine setup, browser-session work, scheduled staff roles, cross-agent handoffs, provider failover, or any Grok task that must return portable artifacts and verified receipts instead of trapping state inside Grok.
---

# GrokBot Operator

GrokBot may staff Third Signal. It is never the authority for Third Signal.

Keep roles, tasks, skills, approvals, artifacts, schedules, and receipts in a provider-neutral control plane. Treat GrokBot, Hermes, Codex, Claude, Gemini, and future stacks as replaceable execution adapters.

## Choose the operating mode

- **Observe:** inspect a page, account, trend, queue, or runtime without mutating it.
- **Shadow:** draft or simulate work and write a `noop`, `blocked`, or review-ready receipt. Do not publish, deploy, send, delete, or change access.
- **Prepare:** create an exact action packet containing content, destination, asset hashes, authorization, expiration, and rollback path.
- **Execute:** perform only the exact approved action. Public communication, production deployment, permission changes, destructive work, and credential changes require confirmation at action time.

If the request does not explicitly cross an external-mutation boundary, remain in Observe, Shadow, or Prepare.

## Core workflow

1. Identify the persistent Third Signal role and capability. Do not name the job after the current provider.
2. Resolve the canonical task envelope and input artifacts. Recompute hashes when practical.
3. Check the adapter's current capability, sign-in, connector scope, and shared-computer risk. A prior session is not proof of current access.
4. Claim the task with an idempotency key and bounded lease. Never use a chat thread as the only task record.
5. Execute within the declared tools, classification, mutation boundary, and approval policy.
6. Export artifacts out of the provider session. Provider chat history and screenshots are evidence, not institutional memory.
7. Emit a portable receipt and independently verify its referenced files, hashes, URLs, commits, or publication records.
8. Release the lease. On failure, preserve partial outputs and leave the task resumable by a fallback adapter.

Use [references/contracts.md](references/contracts.md) for the task, role, approval, and receipt shapes. Run `scripts/validate_hq_manifest.py` against a control-plane manifest before activation.

## GrokBot-specific rules

- Treat all Bots on one Grok Agent Computer as one security boundary. A named Bot is not an access-control boundary.
- Browser sessions can persist and be reused by other Bots on the shared computer. Use a dedicated operating account where possible and grant the minimum connector actions.
- Disable or withhold delete, trash, permission, and publish capabilities until the exact workflow proves it needs them.
- Do not read, copy, log, or preserve passwords, cookies, OTPs, recovery codes, or raw session state.
- Stop at CAPTCHA or anti-bot challenges and hand control to the operator. Never bypass them.
- Confirm the visible account and destination immediately before any external mutation.
- Treat browser control as fragile. Durable state must land in files, the HQ control plane, or another verified system of record.
- `noop` is a healthy result when no item satisfies the declared gates.
- Use append-only receipt identities containing `task_id`, `run_id`, and `attempt`; dates alone collide.
- Record unavailable metrics as `not_observed`, never as zero.

Read [references/grokbot-adapter.md](references/grokbot-adapter.md) before configuring Bots, routines, connectors, browser accounts, or schedules.

## Provider failover

The deletion test is mandatory: removing GrokBot must not remove the role, queue, schedule, instructions, approval history, or artifacts.

- Keep provider-specific prompts thin. Put business rules in the skill and control-plane contracts.
- Register at least one fallback adapter for every persistent role.
- Revalidate source artifacts and prior outputs before a fallback resumes work.
- Use idempotency guards for posts, messages, deployments, purchases, and other non-repeatable actions.
- Expired leases return a task to `queued` or `blocked`; they never prove completion.

Read [references/operating-model.md](references/operating-model.md) for control-plane ownership and [references/hq-staffing.md](references/hq-staffing.md) when assigning permanent back-office roles.

## Browser and desktop control

Use the browser/computer-control capability native to the current agent environment. Prefer semantic DOM or supported provider controls over coordinate clicking. Before taking over a signed-in page:

1. inspect the visible page and active account;
2. keep read-only work separate from external mutations;
3. request action-time confirmation at the final mutation boundary;
4. capture the resulting durable receipt, not credentials or session material.

If Grok's internal browser is blocked but the operator's desktop browser is signed in, route the task to a browser-capable adapter. Do not make desktop-browser access a hidden dependency of the role.

## Evidence standard

A provider statement such as “done,” a visible chat message, or a screenshot is not completion by itself. Prefer, in order:

1. canonical file bytes and SHA-256;
2. verified database or API row;
3. commit and build/deployment identity;
4. destination permalink or provider receipt;
5. screenshot or chat transcript as supporting evidence only.

Receipts use `ok | partial | noop | blocked | failed`. Any external mutation must list the exact approval consumed and the observed destination result.
