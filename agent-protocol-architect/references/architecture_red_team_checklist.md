# Agent Architecture Red-Team Checklist

Use this checklist to stress-test proposed AI agent architectures. The goal is to identify custom integration sprawl, missing guardrails, and monolithic anti-patterns before development begins.

## 1. The Integration Sprawl Audit (MCP Focus)

*   [ ] **Are we building custom API wrappers?**
    *   *Red Flag:* The architecture diagram shows direct REST/GraphQL calls from the agent to common SaaS tools (Slack, Notion, Postgres, GitHub).
    *   *Correction:* Mandate the use of existing MCP servers for these connections.
*   [ ] **Is the agent tightly coupled to specific tools?**
    *   *Red Flag:* Changing a backend database or CRM requires rewriting the agent's core logic or prompt.
    *   *Correction:* Abstract the connection through an MCP gateway to ensure tool-agnostic agent design.
*   [ ] **How are tool definitions maintained?**
    *   *Red Flag:* The engineering team is responsible for manually updating OpenAPI specs or tool schemas when external APIs change.
    *   *Correction:* Rely on MCP servers maintained by the tool providers to ensure automatic discovery of the latest definitions.

## 2. The Monolith vs. Swarm Audit (A2A Focus)

*   [ ] **Is the agent trying to do too much? (The "God Agent" Anti-Pattern)**
    *   *Red Flag:* A single agent is tasked with research, coding, code review, and deployment.
    *   *Correction:* Break the monolith into specialized agents. Use A2A for horizontal collaboration and handoffs.
*   [ ] **How do agents discover each other?**
    *   *Red Flag:* Agent endpoints and capabilities are hardcoded into other agents' configurations.
    *   *Correction:* Implement A2A Agent Cards (`/.well-known/agent-card.json`) for dynamic discovery.
*   [ ] **How is long-running coordination handled?**
    *   *Red Flag:* Agents use synchronous HTTP calls and polling loops to wait for other agents to finish tasks.
    *   *Correction:* Utilize A2A's task lifecycle and push notifications for asynchronous coordination.

## 3. The Commerce & Security Audit (UCP + AP2 Focus)

*   [ ] **Are we building custom checkout flows?**
    *   *Red Flag:* The agent has separate integration logic for Supplier A, Supplier B, and Supplier C.
    *   *Correction:* Implement UCP to standardize the shopping lifecycle into modular capabilities, regardless of the supplier.
*   [ ] **Who authorizes the agent's spending?**
    *   *Red Flag:* The agent can execute transactions without explicit, auditable approval limits.
    *   *Correction:* Implement AP2. Define an `IntentMandate` with spending limits and merchant restrictions.
*   [ ] **Is there a non-repudiatable audit trail?**
    *   *Red Flag:* We cannot cryptographically prove that a specific manager authorized a specific agent transaction.
    *   *Correction:* Ensure the AP2 flow generates a signed `PaymentMandate` and a final `PaymentReceipt`.

## 4. The Frontend Bottleneck Audit (A2UI + AG-UI Focus)

*   [ ] **Is the "Rendering Wall" blocking deployment?**
    *   *Red Flag:* The agent's reasoning is complete, but deployment is delayed because the frontend team needs to build custom React components for the output.
    *   *Correction:* Implement A2UI to allow the agent to dynamically compose layouts from safe component primitives.
*   [ ] **How is streaming handled?**
    *   *Red Flag:* The frontend has complex, brittle boilerplate code to parse raw framework events (e.g., LangChain or ADK specific streams).
    *   *Correction:* Implement AG-UI as middleware to translate raw events into a standardized SSE stream (`TOOL_CALL_START`, `TEXT_MESSAGE_CONTENT`).
*   [ ] **Are UI structure and data coupled?**
    *   *Red Flag:* The agent must resend the entire UI component tree just to update a single data value (e.g., a price change).
    *   *Correction:* Ensure A2UI implementation separates the component tree (`surfaceUpdate`) from the data payload (`dataModelUpdate`).
