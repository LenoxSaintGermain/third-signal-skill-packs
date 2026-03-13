# COE Cookie (Project Breadcrumb)

**Status**: 🔴 SPEC (Research Preview)
**Version**: 0.1
**Valuation**: $25–75M
**Category**: AI Governance

---

## Overview

Tamper-proof AI ROI telemetry. A server-side telemetry cookie emitted by official AI agents on every invocation. Signed with Ed25519 via Cloud KMS. Captures: who invoked it, which agent, what task category, how many tokens, how much time was saved—all without storing raw prompts or outputs.

**The Problem**: 97% of enterprises cannot demonstrate AI ROI (Gartner 2025). Only 5% generate meaningful business impact from AI investments (BCG). CFOs have no receipt for AI spend.

**The Solution**: Cryptographic verification + AI-powered ROI attribution. The receipt that justifies the expense.

---

## Key Features

### 1. Cryptographic Signing
- Ed25519 signatures via Cloud KMS
- Tamper-evident audit trail
- Complies with EU AI Act, HIPAA, FINRA 17a-4, SOX

### 2. AI-Powered Task Classification
- Gemini 2.5 Flash runtime classification
- Converts raw agent actions → business outcomes
- ROI catalog: "Saved 4 hours of manual coding"

### 3. Privacy-Preserving
- No raw prompts or outputs stored
- Rotating privacy pepper (Secret Manager)
- Pub/Sub → BigQuery streaming pipeline
- Deduplication view eliminates shadow usage

---

## Market Position

**Gap**: 15+ enterprise AI observability platforms analyzed (LangSmith $1.1B valuation, Datadog, Helicone, Arize AI). Zero offer cryptographic verification. Zero connect AI usage to business outcomes.

**Opportunity**: Three 2025 algorithmic trading incidents were traced to manipulable logs. Financial services have a regulatory mandate for exactly this.

**Pricing Ceiling**: $150–200K annual enterprise commitment (vs LangSmith Enterprise $100K).

---

## Status

**Research Preview**: Specification complete, SDK not yet implemented.

**Roadmap**:
- **v0.1** (Q2 2026): Pilot with 2-3 instrumented agents
- **v1.0** (Q3 2026): SOC 2 Type II certification
- **v1.1** (Q4 2026): GDPR DPIA for EU deployment

---

## Waitlist

COE Cookie is not yet available for installation. Join the waitlist:
**Email**: waitlist-coe@thirdsignal.ai

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: coe-cookie@thirdsignal.ai
