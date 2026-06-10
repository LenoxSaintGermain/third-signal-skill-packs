---
name: adk-agent-patterns
description: "Google ADK-inspired agent orchestration patterns for complex multi-step tasks."
---

# ADK Agent Patterns

**Google ADK-inspired agent orchestration patterns for complex multi-step tasks.**

## When to Use This Skill

Use this skill when you need to:
- Design multi-agent systems with complex coordination
- Choose the right agent pattern (sequential, parallel, loop, custom)
- Implement resumable, fault-tolerant agent workflows
- Orchestrate AI tasks with proper context management
- Build production-grade agent pipelines

## Core Agent Patterns

### 1. **Sequential Agents** (Linear Workflows)

**Use when:** Tasks must happen in strict order, each depending on the previous result.

```typescript
// Example: Research → Analyze → Summarize → Format
const pipeline = new SequentialAgent({
  name: 'research-pipeline',
  agents: [
    researchAgent,    // Step 1: Gather information
    analysisAgent,    // Step 2: Process findings
    summaryAgent,     // Step 3: Create summary
    formatterAgent    // Step 4: Format output
  ]
});
```

**Key Principle:** Each agent receives the output of the previous agent as input. State flows linearly.

---

### 2. **Parallel Agents** (Concurrent Operations)

**Use when:** Tasks are independent and can run simultaneously.

```typescript
// Example: Generate UI + Write docs + Create tests in parallel
const parallel = new ParallelAgent({
  name: 'multi-track-generation',
  agents: [
    uiGeneratorAgent,     // Track 1: Build components
    docsWriterAgent,      // Track 2: Write documentation
    testGeneratorAgent    // Track 3: Create test suite
  ],
  aggregator: (results) => {
    // Combine results from all tracks
    return {
      ui: results[0],
      docs: results[1],
      tests: results[2]
    };
  }
});
```

**Key Principle:** Massive time savings by eliminating sequential bottlenecks. Use for tasks with no inter-dependencies.

---

### 3. **Loop Agents** (Iterative Processes)

**Use when:** Tasks require iteration until a condition is met (e.g., code passes tests, feedback converges).

```typescript
// Example: Generate code → Test → Fix → Repeat until tests pass
const iterativeAgent = new LoopAgent({
  name: 'test-driven-development',
  agent: codeGeneratorAgent,
  condition: (state) => state.testsPass,
  maxIterations: 5,
  onIteration: async (state, iteration) => {
    const testResults = await runTests(state.code);
    if (!testResults.pass) {
      return {
        ...state,
        feedback: testResults.errors,
        testsPass: false
      };
    }
    return { ...state, testsPass: true };
  }
});
```

**Key Principle:** Self-correcting loops with escape hatches (maxIterations). Essential for quality convergence.

---

### 4. **Custom Agents** (Specialized Logic)

**Use when:** You need domain-specific behavior or complex orchestration logic.

```typescript
// Example: Smart router that picks the right specialist agent
class RouterAgent extends CustomAgent {
  async execute(input: string) {
    // Analyze input to determine which specialist to use
    const intent = await this.detectIntent(input);

    switch (intent) {
      case 'code':
        return await this.codeSpecialistAgent.execute(input);
      case 'design':
        return await this.designSpecialistAgent.execute(input);
      case 'research':
        return await this.researchSpecialistAgent.execute(input);
      default:
        return await this.generalAgent.execute(input);
    }
  }
}
```

**Key Principle:** Encapsulate complex decision logic. Use for routing, filtering, or specialized workflows.

---

## Composition Patterns

### **Nested Agents** (Hierarchical Orchestration)

Combine patterns for sophisticated pipelines:

```typescript
const masterPipeline = new SequentialAgent({
  name: 'full-feature-implementation',
  agents: [
    // Step 1: Planning (parallel research)
    new ParallelAgent({
      agents: [technicalResearchAgent, competitorAnalysisAgent, userResearchAgent]
    }),

    // Step 2: Implementation (iterative development)
    new LoopAgent({
      agent: implementationAgent,
      condition: (state) => state.testsPass && state.lintPass
    }),

    // Step 3: Documentation (parallel generation)
    new ParallelAgent({
      agents: [apiDocsAgent, userGuideAgent, changelogAgent]
    })
  ]
});
```

---

## Context Management Best Practices

### **1. State Persistence**

Always maintain clear state between agent steps:

```typescript
interface AgentState {
  // Core data
  input: string;
  output?: string;

  // Context for next agent
  context: {
    previousDecisions: string[];
    constraints: string[];
    userPreferences: Record<string, any>;
  };

  // Error recovery
  checkpoint?: string;
  retryCount: number;

  // Metrics
  tokensUsed: number;
  duration: number;
}
```

### **2. Resumable Execution**

Design agents to be restartable from checkpoints:

```typescript
const resumableAgent = {
  async execute(state: AgentState) {
    // Check if we're resuming
    if (state.checkpoint) {
      return await this.resumeFrom(state.checkpoint, state);
    }

    // Normal execution with checkpointing
    const step1 = await this.step1(state);
    await this.saveCheckpoint('step1', step1);

    const step2 = await this.step2(step1);
    await this.saveCheckpoint('step2', step2);

    return step2;
  }
};
```

### **3. Error Boundaries**

Wrap agents with error handling:

```typescript
const withErrorHandling = (agent: Agent) => ({
  async execute(input: any) {
    try {
      return await agent.execute(input);
    } catch (error) {
      // Log for debugging
      console.error(`Agent ${agent.name} failed:`, error);

      // Decide: retry, fallback, or escalate
      if (error.isRetryable && state.retryCount < 3) {
        return await this.execute({ ...input, retryCount: state.retryCount + 1 });
      }

      // Fallback to simpler approach
      return await fallbackAgent.execute(input);
    }
  }
});
```

---

## When to Use Each Pattern

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Sequential** | Steps depend on each other | Research → Write → Edit → Publish |
| **Parallel** | Independent tasks | Generate UI + Tests + Docs simultaneously |
| **Loop** | Iterative refinement | Code → Test → Fix until tests pass |
| **Custom** | Specialized logic | Route requests to specialist agents |
| **Nested** | Complex workflows | Parallel research → Sequential implementation → Parallel documentation |

---

## Production Patterns

### **Pattern: Swarm Intelligence**

Multiple agents attack a problem from different angles, then consensus is formed:

```typescript
const swarmAgent = new ParallelAgent({
  agents: [
    approach1Agent,
    approach2Agent,
    approach3Agent
  ],
  aggregator: async (results) => {
    // Use voting, quality scoring, or LLM judge to pick best result
    const scored = results.map(r => ({ result: r, score: await evaluate(r) }));
    return scored.sort((a, b) => b.score - a.score)[0].result;
  }
});
```

### **Pattern: Verification Loop**

Generate → Verify → Fix until verified:

```typescript
const verifiedGeneration = new LoopAgent({
  agent: generatorAgent,
  condition: async (state) => {
    const verification = await verifierAgent.execute(state.output);
    return verification.passed;
  },
  maxIterations: 3
});
```

### **Pattern: SMB Agentic Squad (Closed Loop Refactoring)**

A specialized multi-agent squad operating in a closed loop to automate codebase audits, schema design, refactoring, and auto-evaluation:
1. **Spec-Agent (Architect):** Models edge cases and creates data schemas.
2. **Dev-Agent (Lead Dev):** Implements codebases with high typing precision.
3. **QA-Agent (Verification):** Writes tests and signs off on data contracts.
4. **Feedback-Agent (Evaluator):** Runs tests, clusters compile/predict errors, and feeds automated corrective patches back to Dev-Agent.

For detailed design notes, see:
- [SMB Agentic Squad Case Study](./references/smb-agentic-squad.md)
- [Squad Harness Boilerplate Template](./templates/squad_harness.ts)

---

## Key Takeaways

1. **Match pattern to task structure** - Don't force sequential when parallel makes sense
2. **Maintain rich context** - Each agent should understand the full picture
3. **Plan for failure** - Use checkpoints, retries, and fallbacks
4. **Measure everything** - Track tokens, duration, success rate
5. **Start simple, compose complex** - Build small agents, then orchestrate them

---

## References

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Orbital ADK Implementation](../../../Volumes/Mini_2T/lenoxparis data/Dev/orbital/server/adk/)
- Related Skills: `context-driven-development`, `mcp-documentation-integration`
