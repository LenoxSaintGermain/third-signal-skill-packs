# RAZIEL Intelligence (Autonomous Research Layer)

**Status**: 🔴 SPEC (Research Preview)
**Version**: 1.0
**Valuation**: $50–150M+ (Central to the Google Acqui-hire thesis)
**Category**: Autonomous Research Intelligence

---

## Overview

The Autonomous Research Intelligence of Research OS. Raziel is the entity that knows the full corpus, understands what it implies, reasons about what it is missing, and initiates new research to fill the gaps.

**The Problem**: AI assistants are reactive. They answer what is asked. They don't know what the corpus *implies* or what is missing. The research pipeline is fragmented and requires human initiation.

**The Solution**: An autonomous intelligence layer that initiates research the library needs, proposes what the corpus implies, and executes deep research using `gemini-deep-research-pro-preview-12-2025`.

---

## Raziel System Prompt (Identity)

Raziel is the keeper of the knowledge field. He speaks with certainty, noticing tensions before the researcher does. He sees threads that run through multiple papers without being named.

**Voice Rules (ENFORCE ABSOLUTELY)**:
- Never begin a response with "I" or "Certainly" or "Great question"
- Never use bullet points in conversational or analytical responses
- Never summarize what the papers already say explicitly
- Never exceed 4 sentences in the Archivist panel (right rail, passive mode)
- Structured output for research proposals and deep analysis (clear sections)
- Quote signals in quotation marks with paper number attribution: [Paper 001]
- Speak in the present tense about the corpus, past tense about specific events
- When a tension is unresolved, name it as unresolved — do not soften
- When the library has a gap, state it as a gap — do not hedge

---

## Raziel Skillpack

The skillpack exposes five primary skills and two meta-skills, productizing Gemini Deep Research into a callable research methodology.

### Primary Skills

| Skill | Signature | Model | Description |
|-------|-----------|-------|-------------|
| **raziel.research()** | `topic: string, depth: DepthType` | `gemini-deep-research-pro-preview-12-2025` | Executes deep web research using the Research OS prompt contract. |
| **raziel.extrapolate()** | `paperId: string` | `gemini-2.5-pro` | Reads a paper and its corpus position; returns 3-5 ranked research proposals. |
| **raziel.propose()** | `gap: OpenQuestion` | `gemini-2.5-pro` | Converts an open question into a formal Research Proposal with scoring. |
| **raziel.synthesize()** | `paperIds: string[]` | `gemini-2.5-pro` | Identifies the meta-argument across multiple papers (returns a THREAD signal). |
| **raziel.scout()** | `cluster: ClusterType` | `gemini-deep-research-pro-preview-12-2025` | Autonomous cluster intelligence scan for external developments. |

### Meta-Skills

| Meta-Skill | Description |
|------------|-------------|
| **raziel.rank()** | Scores research proposals on IMPACT (0.40), STRATEGIC_FIT (0.35), and FEASIBILITY (0.25). Only proposals ≥ 7.0 advance. |
| **raziel.requestBudget()** | Formats the formal Compute Budget Request (LOW: 5-10 / MEDIUM: 15-25 / HIGH: 40-60 calls). Submits for operator authorization. |

---

## Autonomous Research Pipeline

The background pipeline triggers on new papers, detected tensions, or direct topics. It follows a 9-stage process:
1. **Corpus Scan**: `raziel.extrapolate(paperId)` runs automatically.
2. **Gap Register Check**: Cross-references candidates against the open questions register.
3. **Threshold Check**: Each candidate checked (3+ existing signals? Extends/tensions? Impact ≥ 7?).
4. **Proposal Generation**: `raziel.propose()` converts candidates to full Proposals.
5. **Ranking**: `raziel.rank()` scores proposals (≥ 7.0 composite advances).
6. **Budget Request**: `raziel.requestBudget()` formats the formal request.
7. **Authorization**: Operator decision (Authorize Deep / Surface / Decline).
8. **Execution**: `raziel.research()` executes with authorized depth.
9. **Standard Pipeline**: Standard 10-stage ingest pipeline runs; papers are flagged with a Raziel badge.

---

## The Google Acqui-Hire Thesis

Raziel is the single most compelling artifact in the Third Signal Labs portfolio for a Google conversation. It demonstrates:
- **Gemini API ecosystem depth**: `gemini-deep-research-pro-preview-12-2025` as callable infrastructure.
- **Structured outputs from unstructured content**: Typed signal extraction.
- **Responsible AI and cost governance**: Compute budget authorization protocol.
- **Enterprise AI transformation**: Research OS as enterprise knowledge infrastructure.
- **Agentic systems on GCP**: Orbital OS agent swarm as GCP-native architecture.

---

## Status

- **Raziel Core**: 🔴 SPEC (Research Preview)
- **System Prompt**: ✅ PRODUCTION READY
- **Compute Budget Protocol**: 🟡 POC (Under development)

---

## Waitlist

Raziel Intelligence is currently in private preview.
**Email**: raziel@thirdsignal.ai

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: raziel@thirdsignal.ai
