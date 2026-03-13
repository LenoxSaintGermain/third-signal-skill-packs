# MNEME (Multimodal Neuro-Emotional Memory Engine)

**Status**: 🔴 SPEC (Research Preview)
**Version**: 0.4
**Valuation**: $30–100M+
**Category**: Memory & Continuity

---

## Overview

Cross-model, cross-session, user-owned memory protocol. The OAuth of AI memory. Solves the memory silo problem: ChatGPT's memory doesn't talk to Claude's doesn't talk to Gemini's.

**The Problem**: Every major AI platform has a memory problem. Memory is silo'd per model, per session. You can't take your Claude conversation history to Gemini.

**The Solution**: Federated Memory Protocol. Memory as a portable, user-owned, cross-model primitive.

---

## Current Implementation (Titan Memory)

**Status**: PRODUCTION (partial)

Orbital implements Titan Memory: long-term facts stored in Firestore with per-operator memory profiles and emotional context tags.

**What Works**:
- Firestore long-term store
- Per-operator memory profiles
- Emotional context tags
- Cross-session persistence (within Orbital)

**What's Missing** (The Federated Layer):
- Federated identity layer (spec not built)
- Multi-model memory handoff (spec not built)
- OAuth-style authorization flow
- Cross-platform memory portability

---

## The Federated Memory Protocol (Spec)

**Vision**: Memory as an interoperable protocol, not a platform feature.

**Architecture** (Research Preview):
```
User Identity (OAuth-like)
↓
Memory Provider (Firestore, Supabase, self-hosted)
↓
Memory Consumer (GPT, Claude, Gemini, custom agents)
↓
Handoff Protocol (standardized schema)
```

**Schema** (Draft):
```json
{
  "userId": "user-123",
  "memoryId": "mem-abc",
  "facts": [
    { "content": "User prefers TypeScript over JavaScript", "confidence": 0.95, "timestamp": "2026-03-12" }
  ],
  "emotionalContext": {
    "frustration": 0.2,
    "excitement": 0.8
  },
  "provenance": {
    "source": "claude-sonnet-4",
    "session": "sess-xyz"
  }
}
```

---

## Market Position

**Gap**: ChatGPT's memory is silo'd. Claude's is silo'd. Gemini's is silo'd. MNEME is the bridge.

**Opportunity**: If Google adopts MNEME as memory layer for Gemini, they own the standard. If it goes open, the creator controls the spec. ElevenLabs Series D ($180M) validated emotional AI—MNEME is the infrastructure that market is missing.

**Strategic Case**: First-mover in AI memory interoperability is a category-defining position.

---

## Status

**Titan Memory**: ✅ PRODUCTION (within Orbital)
**Federated Protocol**: 🔴 SPEC (research only)

**Critical Gap**: No dedicated Federated Memory Protocol spec exists outside high-level ARCHITECTURE overview.

**Signal Note**: The Federated Memory spec is the $100M document that hasn't been written yet. Priority 1 before any acquisition conversation.

---

## Waitlist

MNEME Federated Protocol is not yet available. Join the waitlist:
**Email**: waitlist-mneme@thirdsignal.ai

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: mneme@thirdsignal.ai
