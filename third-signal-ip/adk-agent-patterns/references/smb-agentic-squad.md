# Case Study: SMB Agentic Squad Harness Pattern
**Originating Context:** Verizon Velocity standups vs. SMB development needs.

## 1. The Enterprise Pain Points (The "Why")
Large enterprise software development is characterized by high-friction, slow, and manual loops:
- **Contract Rigidity:** Simple Boolean features are proposed but immediately run into scalability limits (e.g., lines having multiple features, add-ons, or hierarchical settings). To avoid slowing down MVP1, teams defer data structure refactoring to MVP2, creating instant technical debt and requiring endless alignment meetings.
- **Manual LLM Evaluation:** Team members are forced to download static files locally, open them in local browsers, audit-map predictions, and type out manual justifications to train/validate models, risking data loss on tab refreshes.
- **Vague Intent Translation:** Large meetings are spent translating fuzzy human inputs into legacy deterministic system codes.

For SMBs, this level of meeting and manual validation overhead is fatal. An automated, codebase-native multi-agent squad is needed to bypass this entirely.

---

## 2. The 4-Agent Closed-Loop Architecture
The Agentic Squad decomposes the software development cycle into 4 specialized, synchronized agents acting in a closed loop:

```
┌────────────────────────────────────────────────────────────────┐
│                   AGENTIC SQUAD CLOSED-LOOP                    │
│                                                                │
│   ┌───────────────┐                  ┌───────────────────┐     │
│   │  Spec-Agent   │─────────────────▶│     Dev-Agent     │     │
│   │  (Architect)  │                  │    (Refactor)     │     │
│   └───────────────┘                  └───────────────────┘     │
│           ▲                                    │               │
│           │                                    ▼               │
│   ┌───────────────┐                  ┌───────────────────┐     │
│   │Feedback-Agent │◀─────────────────│     QA-Agent      │     │
│   │  (Evaluator)  │                  │   (Validation)    │     │
│   └───────────────┘                  └───────────────────┘     │
└────────────────────────────────────────────────────────────────┘
```

### 1. Product Architect Agent (Spec-Agent)
- **Role:** Software & System Architect.
- **Goal:** Analyzes existing codebase structure, JSON schemas, and API definitions. Models edge cases (e.g., design generic feature arrays instead of restricting Booleans) before writing any code.
- **Output:** Precise, scalable Technical Specifications.

### 2. Codebase Refactoring Agent (Dev-Agent)
- **Role:** Lead Software Engineer.
- **Goal:** Deep-dives into the codebase, traces data flow, and implements precise, typed refactoring changes.
- **Output:** Clean code drafts or patched files.

### 3. Integration & Contract Testing Agent (QA-Agent)
- **Role:** Quality Assurance & Dependency Guard.
- **Goal:** Writes deterministic integration tests, contract mocks, and runs static analysis to ensure no breaking changes to upstream/downstream services.
- **Output:** Integration test reports and contract verification logs.

### 4. Auto-Evaluating Agent (Feedback-Agent)
- **Role:** LLM Output Evaluator & Human Loop Minimizer.
- **Goal:** Ingests actual logs or model outputs, evaluates performance, clusters compilation or prediction errors, and drafts automated patch proposals back to the Dev-Agent.
- **Output:** Corrective patch recommendations, eliminating manual review overhead.

---

## 3. Mandatory Artifact Logging Protocol
To maintain strict auditability, every phase of the squad must write its structured output to a tickets/ directory (e.g., `docs/artifacts/tickets/`) before committing code:
1. `US-X.Y_technical_spec.md` (Spec-Agent)
2. `US-X.Y_implementation_plan.md` (Dev-Agent)
3. `US-X.Y_qa_report.md` (QA-Agent)
4. `US-X.Y_feedback_evaluation.md` (Feedback-Agent)
