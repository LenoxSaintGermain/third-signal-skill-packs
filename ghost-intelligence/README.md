# Ghost Intelligence

**Status**: 🟡 POC (Proof of Concept)
**Version**: 2.0
**Valuation**: $10–25M
**Category**: Reasoning Interface

---

## Overview

Contextual ambient reasoning engine. An ambient safety net that operates at the edge of attention. Ghost doesn't wait to be asked—it watches where you are and speaks.

**The Problem**: AI assistants are reactive. You have to know what to ask. If you don't know to ask, you don't get the answer.

**The Solution**: Proactive AI that surfaces what's relevant before you know to ask. Ghost V2 adds self-healing metadata—catches model hallucinations as a background integrity process.

---

## Key Features

### 1. Attention Zone Detection
- mousemove → getBoundingClientRect → binary search O(log n)
- 350ms dwell timer
- AbortController per zone change

### 2. Streaming Claude API Response
- claude-sonnet API
- 200 token max per response
- Typewriter delivery (2 chars/18ms)

### 3. Self-Healing Metadata (Ghost V2)
- Hallucination detection loops
- Background integrity process
- Catches model errors before user sees them

---

## Architecture

```
User Attention (mousemove)
↓
Attention Zone Detection (350ms dwell)
↓
Context Extraction (getBoundingClientRect)
↓
Claude Sonnet API (200 token max)
↓
Self-Healing Metadata Loop (V2)
↓
Typewriter Delivery (2 chars/18ms)
```

---

## Market Position

**Gap**: AI assistants are reactive. NotebookLM has 5M+ users but requires explicit queries. Ghost is the shift from "ask about the document" to "the document reads you back."

**Opportunity**: Natural integration into Gemini NotebookLM as active reading layer. Ghost V2 hallucination detection has standalone value as safety infrastructure for any platform deploying RAG at scale.

**Strategic Case**: NotebookLM is the interaction model it's missing. Ghost V2's self-healing metadata is a capability no competing product has shipped.

---

## Status

**Proof of Concept**: ✅ (functional prototype)
**Documentation**: Partial (attention zones + API integration documented)
**Known Gaps**: Standalone deep-dive spec for Ghost V2 self-healing iterative loops is missing.

---

## Early Access

Ghost Intelligence is in POC status. Early access available for research partners:
**Email**: ghost-early-access@thirdsignal.ai

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: ghost@thirdsignal.ai
