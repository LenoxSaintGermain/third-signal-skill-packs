# Operator Protocol (Strategic Lead & Product Architecture)

**Status**: 🟢 PRODUCTION
**Version**: 1.0
**Valuation**: $35–85M
**Category**: Strategic AI Orchestration

---

## Overview

The Operator Protocol is the strategic intelligence layer of the Hybrid Drive workflow. It translates human intent and high-level mission objectives into formal, high-fidelity execution plans. 

**The Problem**: Human-to-AI communication often lacks the strategic rigor required for complex engineering tasks. Requirements are underspecified, edge cases are ignored, and architectural "blind spots" lead to downstream rework.

**The Solution**: A multi-stage planning and review pipeline that challenges premises, explores alternatives, and locks in technical specs before a single line of code is written by the Conductor.

---

## The Strategic Review Pipeline

Every major feature or architectural change MUST pass through the Operator's review stages:

1. **Strategic Reframing (`/office-hours`)**: Challenges the initial problem statement. Explores implementation alternatives and generates a formal Design Document.
2. **Founder's Review (`/ceo-review`)**: Analyzes product-market fit and scope. Focuses on "Expansion" or "Reduction" to find the "10-star product" version of the feature.
3. **Architectural Review (`/eng-review`)**: Locks in data flow, component diagrams, edge cases, and the TDD plan. Eliminates hidden assumptions.
4. **Design/UX Audit (`/design-review`)**: Audits UX dimensions and eliminates "AI Slop." Ensures high-quality design standards and accessibility.
5. **Autoplan Orchestration (`/autoplan`)**: Automates the sequential review process (CEO → Design → Eng), presenting the human lead with only critical "Taste Decisions" for final approval.

---

## Skillpack Signatures

| Skill | Signature | Description |
|-------|-----------|-------------|
| **operator.reframe()** | `intent: string` | Executes `/office-hours` logic to challenge and refine the initial request. |
| **operator.plan()** | `specId: string` | Generates a multi-role review plan (CEO, Eng, Design) for a specific feature. |
| **operator.audit()** | `artifact: string` | Performs a "Senior Designer" or "Eng Manager" audit of a design/spec. |
| **operator.autoplan()** | `goal: string` | Orchestrates the full review pipeline autonomously. |

---

## Core Tenets

- **Challenge the Premise**: Never accept a request at face value. Always explore the "why" and "what if."
- **Spec First, Code Second**: No implementation track starts without a verified `plan.md` from the Operator.
- **Taste Decisions Only**: Automate the mechanical planning; escalate only the creative and strategic decisions to the human lead.

---

## Market Position

**The Unlock**: Most AI tools are "doers." The Operator is a "thinker." It provides the strategic oversight that turns a group of subagents into a cohesive engineering team.

**Strategic Case**: As implementation becomes commoditized by better models, the value shifts to the **Strategic Intent Layer**. The Operator Protocol owns that layer.

---

## Status

- **Strategic Review Pipeline**: ✅ PRODUCTION
- **Design/UX Audit**: ✅ PRODUCTION
- **Autoplan Engine**: 🟡 POC (Under development)

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: operator@thirdsignal.ai
