---
name: ADK 2.0 Migration
description: Upgrades legacy ADK 1.x agents and their storage layers to ADK 2.0 Alpha Graph/Coordinator standards while enforcing strict strict storage separation.
---

# ADK 2.0 Migration Guide

This skill is designed to guide agents and human operators when migrating legacy Orbital ADK 1.x architectures to ADK 2.0 Alpha.

## Core Tenets

1. **Strict Storage Separation (The Golden Rule):**
   ADK 2.0 storage systems (Sessions, Memory) are fundamentally incompatible with ADK 1.x.
   - **DO NOT** reuse existing `sessions` or `orbital_swarm_memory` schemas.
   - **ALWAYS** instantiate `FirestoreSessionService` with new, specific collection paradigms (e.g. `adk2_sessions`).

2. **Graph-based Workflows over Tool Chains:**
   ADK 1.x relied on implicit tool-calling models. ADK 2.0 emphasizes deterministic Node flows.
   - Refactor single massive prompts into multiple nodes using `google.adk.agents.LlmAgent`.
   - String them together via `google.adk.Workflow`, `SequentialAgent`, or structural graphs.

3. **Subagent Specialization:**
   Instead of giving one model 20 MCP tools, use `task`-mode subagents.
   - Create a specialized `LlmAgent` that holds restricted tools to isolate logical tasks.
   - Route tasks securely instead of attempting all-in-one prompts.

## Migration Steps

1. Install `google-adk --pre` from pip.
2. Abstract the legacy `Agent` call into `LlmAgent`.
3. Wrap `InMemorySessionService` or `FirestoreSessionService` with ADK 2-specific collections.
4. Test isolated workflows end-to-end to ensure `BaseAgent` compatibility prior to wide deployment.

> **Note:** The ADK 2.0 alpha is highly volatile. Pydantic validations for classes like `SequentialAgent` change rapidly. Always structure code defensively with `try/except` initialization wrappers.
