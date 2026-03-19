# ADK 2.0 Protocol (Agent Development Kit)

**Status**: 🔴 SPEC (Alpha / Research Preview)
**Version**: 2.0.0-alpha
**Valuation**: $45–110M (The Enterprise Agent Standard)
**Category**: Agent Frameworks & Orchestration

---

## Overview

The Google Agent Development Kit (ADK) 2.0 is a significant evolution in autonomous agent architecture, moving from simple chat patterns to **Graph-Based Workflows**. It provides the infrastructure for building deterministic, collaborative, and highly predictable agentic systems.

**The Problem**: ADK 1.0 and traditional agent frameworks often lack control over task routing, leading to unpredictable loops and high token waste. "Hallucinated" execution paths are common in complex multi-step tasks.

**The Solution**: ADK 2.0 introduces fine-grained control via graph-based state machines, native multi-agent collaboration protocols (A2A), and deep integration with the Gemini 3.1 Live API for multimodal streaming.

---

## Core Innovations

### 1. Graph-Based Workflows
Moves beyond sequential execution to deterministic DAGs (Directed Acyclic Graphs).
- **Control**: Fine-grained routing and execution logic.
- **Predictability**: Pre-defined paths for complex tasks (loops, parallel branches).
- **Code-Based Logic**: Dynamic workflows defined in Python/TypeScript for maximum flexibility.

### 2. Collaborative Multi-Agent Systems (A2A)
Standardizes the **Agent-to-Agent (A2A)** protocol for complex architectures.
- **Coordinator Model**: A master agent that manages specialized subagents.
- **Delegation**: Structured handoffs between specialized agents (e.g., Researcher -> Coder -> Validator).
- **Federated Memory**: Shared context across the agent swarm.

### 3. Gemini 3.1 Live Integration
Deep support for the **Gemini Live API Toolkit**:
- **Streaming**: Real-time bidirectional audio/video/text.
- **Low Latency**: Native handling of event-driven agent responses.
- **Multimodal Grounding**: Integrated Google Search and Vertex AI Search for real-time verification.

---

## Skillpack Signatures

| Skill | Signature | Description |
|-------|-----------|-------------|
| **adk.createGraph()** | `nodes: Node[], edges: Edge[]` | Initializes a deterministic agent workflow graph. |
| **adk.coordinate()** | `agents: Agent[], goal: string` | Sets up a multi-agent swarm with a coordinator. |
| **adk.liveStream()** | `input: Stream, config: LiveConfig` | Connects an agent to the Gemini 3.1 Live WSS protocol. |
| **adk.ground()** | `query: string, source: 'GOOGLE_SEARCH' \| 'VERTEX'` | Forces grounding of agent claims against external data. |

---

## Architectural Components

- **Agent Runtime**: Multi-interface support (Web, CLI, API Server).
- **Deployment**: Native support for Cloud Run, GKE, and Agent Engine.
- **Context Management**: Built-in caching, compression, and session persistence.
- **Protocols**: Standardization of callbacks, events, and A2A handoffs.

---

## ⚠️ Critical Compatibility Note (Migration)

ADK 2.0 is a breaking change from 1.0. 
- **Storage Isolation**: **DO NOT** share persistent storage (sessions, memory) between 1.0 and 2.0 to prevent corruption.
- **Requirement**: Python 3.11+ is mandatory.
- **Install**: Requires `--pre` flag (Alpha status).

---

## Market Position

**Gap**: LangChain and CrewAI are popular but often difficult to deploy at enterprise scale with deterministic guarantees. ADK 2.0 is the "Production-Grade" answer from Google.

**The Unlock**: Deterministic agents. You stop "hoping" the agent follows the plan and start "defining" the plan as a graph.

---

## Status

- **Graph Workflows**: 🔴 SPEC (Alpha)
- **A2A Protocol**: 🔴 SPEC (Research)
- **Gemini Live Toolkit**: 🟡 POC (Under development)

---

## Waitlist

ADK 2.0 is currently in private Alpha.
**Email**: adk2@thirdsignal.ai

---

## License

Specification: Proprietary (Google ADK Docs)
Implementation: Apache 2.0

---

**Maintained by**: Third Signal (Community Spec)
**Contact**: adk@thirdsignal.ai
