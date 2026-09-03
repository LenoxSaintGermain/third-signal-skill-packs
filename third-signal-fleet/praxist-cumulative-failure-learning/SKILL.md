---
name: praxist-cumulative-failure-learning
description: Use when autonomous experiments or debugging loops repeat hypotheses and need shared evidence lineage from prior failed runs.
metadata:
  requires_tools: [file, terminal]
  fallback_for_tools: [file, terminal]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# PRAXIST Cumulative Failure Learning

## Level 0 — Overview

Use PRAXIST to make failed experiments reusable evidence instead of disposable logs. Every run appends a structured record to `experiments.jsonl`; future workers query prior failures before proposing a hypothesis and must explain why a new run is not redundant.

A failure is evidence about conditions, not proof that an entire idea is impossible.

## Level 1 — Runbook

1. Give the experiment a stable `experiment_id`, hypothesis fingerprint, parent run, environment, and owner.
2. Query `experiments.jsonl` for matching or near-matching hypotheses, parameters, and failure signatures.
3. Classify prior results: reproduced failure, contradicted, inconclusive, or superseded.
4. Reject redundant retries, or document the changed variable that justifies one.
5. Run with explicit inputs and capture commands, outputs, metrics, and artifacts.
6. Append one immutable JSON object; never rewrite history.
7. Link the next hypothesis to the evidence it consumes.

```json
{"experiment_id":"exp-0042","hypothesis":"cache reduces latency","fingerprint":"cache|latency","status":"failed","changed_variables":["ttl"],"evidence":["runs/exp-0042/result.json"]}
```

## Level 2 — Reference

Required fields: `experiment_id`, `created_at`, `hypothesis`, `fingerprint`, `status`, `environment`, `inputs`, `result`, `failure_signature`, `evidence`, and `parent_experiment_id`. Use canonical JSON for fingerprints and stable categorical failure signatures. Keep sensitive values out of the shared log; store a redacted reference instead.

## Common Mistakes

- Searching only exact prose and missing equivalent hypotheses.
- Retrying a failed run without a changed variable.
- Mutating JSONL records in place.
- Recording a conclusion without command output or artifact evidence.
- Treating inconclusive as failed or failed as universally impossible.

## Verification

Validate every line as JSON, require evidence for failed runs, check lineage links, and run a duplicate-hypothesis query before launching autonomous work.
