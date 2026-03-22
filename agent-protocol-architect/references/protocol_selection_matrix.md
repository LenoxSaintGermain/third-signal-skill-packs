# AI Agent Protocol Selection Matrix

This matrix provides a structured framework for selecting the appropriate AI agent protocols based on the specific requirements of the system. It is designed to eliminate custom integration code and ensure scalable, standardized architectures.

## Core Protocol Mapping

| Protocol | Full Name | Primary Function | When to Use (The "Why") | Key Architectural Pattern |
| :--- | :--- | :--- | :--- | :--- |
| **MCP** | Model Context Protocol | Vertical Integration (Agent to Tools/Data) | When the agent needs to interact with external APIs, databases, or SaaS platforms. Use to avoid writing custom API wrappers. | Standardized tool discovery via MCP servers. JSON-RPC over stdio/SSE/HTTP. |
| **A2A** | Agent-to-Agent Protocol | Horizontal Collaboration (Agent to Agent) | When multiple specialized agents need to coordinate, especially across organizational boundaries or different frameworks. | Agent Cards at `/.well-known/agent-card.json`. Task lifecycle management with push notifications. |
| **UCP** | Universal Commerce Protocol | Standardized Commerce | When the agent needs to execute transactions, place orders, or interact with multiple suppliers/vendors. | Strongly typed request/response schemas. Transport agnostic (works over REST, MCP, A2A). |
| **AP2** | Agent Payments Protocol | Authorization & Audit Trails | When financial transactions require explicit guardrails, spending limits, or managerial approval. | Cryptographic proof of intent. Chain: `IntentMandate` -> `PaymentMandate` -> `PaymentReceipt`. |
| **A2UI** | Agent-to-User Interface Protocol | Declarative UI Rendering | When the agent needs to present dynamic, rich interfaces (dashboards, forms) without requiring custom frontend code for each new view. | 18 safe component primitives. Separates UI structure from underlying data payload. |
| **AG-UI** | Agent-User Interaction Protocol | Event Streaming | When connecting an agent to a frontend that requires real-time streaming of text, tool calls, and pauses for human input. | Standardized SSE event types (e.g., `TOOL_CALL_START`, `TEXT_MESSAGE_CONTENT`). |

## Strategic Selection Guidelines

### 1. The "Start Here" Rule
**Always begin with MCP.** Most agents require data access before they require collaboration. Establish the vertical integration layer first.

### 2. The Multi-Agent Threshold
**Introduce A2A only when necessary.** Do not over-engineer a single-agent system. Introduce A2A when:
*   The workflow requires distinct, specialized expertise (e.g., a researcher agent handing off to a writer agent).
*   Agents must cross organizational boundaries (e.g., a client agent negotiating with a vendor agent).
*   Asynchronous coordination is required (tasks taking minutes/hours).

### 3. The Commerce Stack (UCP + AP2)
**Treat UCP and AP2 as a coupled pair for enterprise use cases.**
*   UCP handles *what* is ordered and *who* it is ordered from.
*   AP2 handles *who authorized* the purchase and provides the non-repudiatable audit trail.
*   *Red Flag:* An architecture proposing UCP without AP2 in a corporate environment lacks necessary financial guardrails.

### 4. The Frontend Decoupling (A2UI + AG-UI)
**Use UI protocols to break the "Rendering Wall."**
*   If the engineering team is writing custom React/Vue components for every new agent output, they are wasting leverage.
*   Implement A2UI to allow the agent to compose layouts dynamically.
*   Implement AG-UI to standardize the event stream, preventing frontend breakage when the underlying agent framework changes.

## Maturity Assessment (As of 2026)

*   **MCP:** Production-ready. High maturity. 5,000+ public servers. The default standard for tool integration.
*   **A2A:** Early adoption. Growing ecosystem (~200 compatible agents). Best for forward-looking architectures but requires careful monitoring.
*   **UCP/AP2/A2UI/AG-UI:** Emerging standards. Highly valuable for specific use cases (commerce, dynamic UI) but may require reliance on specific toolkits like Google's Agent Development Kit (ADK).
