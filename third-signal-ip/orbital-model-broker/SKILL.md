---
name: orbital-model-broker
description: Use when LANDSAT, Hermes, Orbital, or a Third Signal persona needs brokered model routing instead of hardcoding a provider or model.
---

# orbital-model-broker

Use this skill when LANDSAT, Hermes, or an Orbital persona needs to route model work through the Phase 1 model broker instead of hardcoding a provider or model.

## Contract

- Treat the broker as an OpenAI-compatible provider.
- Prefer passing broker metadata through `extra_body`.
- If the caller cannot pass `extra_body`, prepend a structured `[BROKER-METADATA]` system block.
- Never place secret values in prompts, config, logs, audit records, or examples. Use env var names only.
- Do not directly write Agent Wiki, Armory canonical rows, Manifest release truth, production Cloud Run config, or Secret Manager values.

## Required Metadata

Every brokered request must declare:

- `task_profile`
- `data_sensitivity`
- `allowed_origins`
- `modality`
- `latency_class`
- `quality_floor`
- `budget_hint`
- `output_contract`

## Budget Gates

- Monthly hard cap: `$300`
- Monthly warning: `$200`
- Per-job cap: `$25`
- Per-task cap: `$5`

If a request exceeds the cap, block the route and emit a Swarm trace event. If a request crosses the warning threshold, continue only when policy allows and record the warning.

## Sensitivity And Geography

Apply the data sensitivity x geography matrix from `config/landsat/model-broker.example.yaml`.

China-hosted providers, including DeepSeek, Qwen, Kimi, and equivalent routes, are blocked above `public` sensitivity. This is a compliance and suspension-risk control, not a model-quality judgment.

## Poe

Poe is a first-class provider. Prefer `POE_API_KEY` and Poe OpenAI-compatible routing when the task benefits from provider breadth, quota flexibility, or multimodal access. Verify live model names before relying on a new Poe model in implementation code.

## Donna / YouTube Video Lane

Video generation for Donna or YouTube is gated behind storyboard approval.

Required before route:

- `storyboard_id`
- `storyboard_approval_id`
- `operator_approver`

The broker may generate assets after approval, but must not publish, schedule, or expose public content automatically.

## Audit Replay

Record enough metadata to replay the routing decision:

- selected provider/model
- candidate and blocked models
- budget cap and estimate
- routing reason
- approval gate state
- fallback attempts
- Swarm trace ID
- config version

## Fallback Preamble

Use this only when `extra_body` is unavailable:

```text
[BROKER-METADATA]
task_profile: <profile>
data_sensitivity: <public|internal|operator-only|restricted|secret-ref-only>
allowed_origins: <origins>
modality: <text|image|video|audio|multimodal>
latency_class: <interactive|batch|overnight>
quality_floor: <floor>
budget_hint: <number>
output_contract: <contract-id>
[/BROKER-METADATA]
```
