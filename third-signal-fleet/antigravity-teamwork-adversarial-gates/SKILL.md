---
name: antigravity-teamwork-adversarial-gates
description: Use when orchestrating Google Antigravity Teamwork preview with Gemini 3.7 Flash and adversarial acceptance, exploration, critique, and audit gates.
metadata:
  requires_tools: [file, terminal]
  fallback_for_tools: [file, terminal]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# Antigravity Teamwork Adversarial Gates

## Level 0 — Overview

Use `/teamwork-preview` as a four-stage verification loop, not as unreviewed parallel generation. Gemini 3.7 Flash workers first agree on `01_ACCEPTANCE_CRITERIA.md`, explore independently, stress-test edge cases as Challenger/Critic pairs, and finish with a Success Auditor approval.

No stage may declare success from another worker's self-report alone.

## Level 1 — Runbook

1. Scoping: write testable acceptance criteria in `01_ACCEPTANCE_CRITERIA.md`, including non-goals and evidence requirements.
2. Exploration: run independent parallel investigations with isolated notes; preserve contradictions.
3. Adversarial gate: have a Challenger attack each criterion and a Critic reproduce, reject, or bound the claim. Record edge cases and failed probes.
4. Success Auditor: inspect the criteria, evidence, challenge record, and artifact; approve only when every criterion has evidence or mark the run blocked.

Use one immutable run ID across stage artifacts. Keep worker prompts bounded and label hypotheses, observations, and conclusions separately.

## Level 2 — Reference

A stage record should contain `run_id`, `stage`, `owner`, `status`, `inputs`, `evidence`, `open_risks`, and `next_gate`. Parallel workers must not overwrite one another's notes. The Auditor's approval is a signed decision record, not a generated summary; it must link to concrete files, tests, screenshots, or command output.

## Common Mistakes

- Starting exploration before acceptance criteria exist.
- Calling parallel agreement verification.
- Letting the Challenger change the criteria it is testing.
- Treating an unanswered edge case as passed.
- Using a single model response as the Success Auditor.

## Verification

Check that all four stages exist in order, every criterion maps to evidence, adversarial findings are dispositioned, and the Auditor explicitly approves or blocks the run.
