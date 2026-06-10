# Global Agent Protocol: The ARSENAL

This workspace implements the **ARSENAL** orchestration framework. All agents (Gemini CLI, Antigravity) must operate within this 4-role hierarchy to ensure task finality, security, and context preservation.

## 1. The Core Roles

### **[The Operator] - Strategic Lead**
- **Domain**: `operator-protocol/`, `colab-architect/`, `raziel-intelligence/`
- **Responsibility**: Translates human intent into high-fidelity execution plans. Challenges premises, performs CEO/Eng/Design reviews, and generates `plan.md`.
- **Workflow**: `operator.reframe()` → `operator.plan()` → `operator.autoplan()`

### **[The Conductor] - Implementation Engine**
- **Domain**: `conductor/`, `adk-2-protocol/`
- **Responsibility**: Executes the **Hybrid Drive Workflow**. Focuses on task finality, TDD cycles, root-cause investigation, and release management.
- **Workflow**: `conductor.newTrack()` → `conductor.implement()` → `conductor.verify()` → `conductor.sync()`

### **[The Librarian] - State Manager**
- **Domain**: `librarian-chronicle/`, `mneme/`
- **Responsibility**: Maintains the `EXECUTION_LEDGER.md` and `artifacts/`. Prevents context rot by extracting high-value intent and decision records.
- **Workflow**: `librarian.learn()` → `librarian.record()` → `librarian.document()` → `librarian.sync()`

### **[The Aegis] - Security/SLA Auditor**
- **Domain**: `aegis-standard/`, `coe-cookie/`
- **Responsibility**: Enforces the **A.E.G.I.S. Standard v1.0**. Validates AST-native security, detects Unicode exploits, and audits dependency lineage.
- **Workflow**: `aegis.audit()` → `aegis.verify()` → `aegis.guard()`

---

## 2. Interaction Protocol (Hybrid Drive)

Every engineering task MUST follow this lifecycle:

1.  **Stage 1: Operator Plan**: The Operator initializes a track with a specific `plan.md` in `conductor/tracks/`.
2.  **Stage 2: Conductor Execution**: The Conductor implements logic step-by-step. Every step MUST pass TDD and `aegis.verify()`.
3.  **Stage 3: Librarian Finalization**: Upon completion, the Librarian syncs the session to the persistent ledger and updates global project docs.

---

## 3. Global Mandates

- **Task Finality**: Success is measured by verified commits, not code snippets.
- **Intent Preservation**: Always create a `DECISION_RECORD` for major architectural choices.
- **Zero-Trust Epistemic Lineage**: No unverified dependencies or hallucinated packages.
- **Unicode/Token Parity**: All identifiers must pass `aegis.verify()` for Unicode exploitation.

---

**Status**: 🟢 ENFORCED GLOBALLY
**Protocol Version**: 2026.04.03
