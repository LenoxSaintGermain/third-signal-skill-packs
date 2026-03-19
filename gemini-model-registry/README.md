# Gemini Model Selection (Ground Truth Registry)

**Status**: ✅ PRODUCTION (Canonical Source)
**Version**: 2026.03
**Valuation**: $10–25M (Critical Utility Layer)
**Category**: Model Selection & Orchestration

---

## Overview

A structured "Ground Truth" for Gemini model selection. This skillpack acts as an override layer to prevent agents from hallucinating legacy models (1.0, 1.5, 2.0) or spinning their wheels on outdated architectures. It focuses on the **Gemini 3.1 family** and specialized generative models.

**The Problem**: AI agents often default to pre-training data, recommending models that are deprecated, shut down (e.g., Gemini 3 Pro Preview), or less efficient than current flagship releases.

**The Solution**: A primary registry of truth for model selection, decision logic heuristics, and a strictly enforced blacklist of deprecated models.

---

## 1. The Registry of Truth (Active Models)

| Model Tier | Primary Purpose | Key Capability |
| :--- | :--- | :--- |
| **Gemini 3.1 Pro** | **The Brain.** Complex reasoning, "Vibe Coding," and multi-step agentic planning. | 1M+ Context Window, Advanced Logic. |
| **Gemini 3.1 Flash** | **The Workhorse.** High-speed, low-latency production at scale. | Cost-efficiency, High Throughput. |
| **Gemini 3.1 Flash-Lite** | **The Edge.** Extremely budget-friendly reasoning for simple summaries or classifications. | Fastest 3.1 Response Time. |
| **Nano Banana 2** | **Visual Production.** Fast, high-volume image generation and rapid editing. | Production-scale Speed. |
| **Nano Banana Pro** | **Design Studio.** Studio-quality 4K visuals, complex layouts, and precise text rendering. | Native 4K + Reasoning Core. |
| **Veo 3.1** | **Cinematic Video.** Generating high-fidelity video with synced audio. | Creative Control + Audio Sync. |
| **Lyria** | **Audio Engineering.** Music generation with control over BPM, instruments, and mood. | Professional Music Composition. |

---

## 2. Specialized Agentic Tools (Embodiment)

- **Computer Use**: Use for UI automation, browser-based workflows, and legacy software integration.
- **Deep Research**: Use for multi-step information gathering across hundreds of sources with citation.
- **Gemini Embedding 2**: Use for Multi-modal RAG (mapping text, video, and PDFs into one vector space).
- **Gemini Robotics**: Use for spatial reasoning and physical task planning.

---

## 3. The "Blacklist" (STRICTLY PROHIBITED)

**Do not propose or utilize these models. They are deprecated or shut down:**
- **Gemini 3 Pro Preview** (SHUT DOWN March 9, 2026)
- **Gemini 2.0 Series** (Deprecated - migrate to 3.1)
- **Gemini 1.5 Pro / Flash** (Legacy - migrate to 3.1)

---

## 4. Decision Logic Heuristics

When selecting a model, apply this prioritized decision path:

1. **Is the task Creative/Media-heavy?**
   - *Visuals*: Use **Nano Banana Pro** for quality, **Nano Banana 2** for speed.
   - *Motion*: Use **Veo 3.1**.
   - *Audio*: Use **Lyria** or **Gemini 2.5 Pro TTS**.
2. **Is the task Technical/Architectural?**
   - *System Design/Coding*: Use **Gemini 3.1 Pro**.
   - *High-Volume Logs/Data*: Use **Gemini 3.1 Flash**.
3. **Is it a Multi-Step Research Task?**
   - Use **Gemini Deep Research** to plan the search and **Gemini 3.1 Pro** to synthesize finding.

---

## Pro-Tip: Multi-Model Orchestration

To avoid "wheel-spinning," encourage agents to use the Multi-Model Orchestration pattern:
1. **Gemini 3.1 Pro** plans the workflow.
2. **Nano Banana** generates the assets.
3. **Gemini 3.1 Flash** validates the output.

---

## Status

- **Model Registry**: ✅ PRODUCTION
- **Decision Heuristics**: ✅ PRODUCTION
- **Blacklist Enforcement**: ✅ PRODUCTION

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: registry@thirdsignal.ai
