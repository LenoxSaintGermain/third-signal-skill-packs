---
name: broker-feedback
description: Use when recording or reviewing quality, cost, latency, safety, or operator feedback about LANDSAT or Orbital model broker routes.
---

# broker-feedback

Use this skill when recording quality, cost, latency, safety, or operator feedback about a LANDSAT model broker route.

## Boundary

- Feedback records inform future routing decisions.
- Feedback does not directly rewrite canonical model registry rows.
- Feedback must not include secrets, full prompts with sensitive data, or private user content unless explicitly allowed by the data policy.
- Use metadata and summaries by default.

## Feedback Fields

Capture:

- `route_id`
- `request_id`
- `requester_agent`
- `persona`
- `task_profile`
- `data_sensitivity`
- `selected_provider`
- `selected_model`
- `output_contract`
- `quality_score`
- `latency_ms`
- `cost_actual_usd`
- `budget_cap_usd`
- `operator_rating`
- `failure_mode`
- `fallback_used`
- `routing_policy_version`
- `swarm_trace_id`
- `created_at`

## Budget Review

Flag feedback when:

- monthly spend crosses `$200`
- monthly spend would exceed `$300`
- a job exceeds `$25`
- a task exceeds `$5`

## Donna / YouTube Video Feedback

For Donna/YouTube video routes, include:

- `storyboard_id`
- `storyboard_approval_id`
- `operator_approver`
- public-surface review status

Do not publish, schedule, or distribute generated video from feedback handling.

## Routing Improvement Proposal

When feedback implies a registry or routing policy change, write a proposal for Librarian review containing:

- observed issue
- route evidence
- recommended policy change
- risk assessment
- rollback path
