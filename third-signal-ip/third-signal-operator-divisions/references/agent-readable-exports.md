# Agent-Readable Exports Pattern

When generating documentation or exports (like Markdown specifications, data room assets, or system proposals) for the Third Signal ecosystem, the document must be a **self-contained cognitive seed** for autonomous agents.

## Implementation: The System Directive Block

At the end of the exported file (e.g., `.md` or `.json`), append a dedicated `[SYSTEM DIRECTIVE]` block. This acts as an embedded prompt so that when the file is dropped into a high-reasoning LLM (like Claude 3.5 Sonnet or Gemini 3.5 Flash), the model immediately knows what to do without requiring human context.

### Example Markdown Footer:

```markdown
---

## RECOMPILATION INSTRUCTIONS FOR AGENTIC SWARMS
To recompile this venture's data or generate secondary marketing artifacts, feed this markdown file to a high-reasoning LLM with the following system directive:

\`\`\`text
[SYSTEM DIRECTIVE // INTERPRET_PROSPECTUS]
You are an autonomous Venture Architect. Read this spec file carefully. Analyze the target customer segments, key activities, and technical stack. 
Your goal is to recompile a highly detailed, 10-page Product Requirements Document (PRD) and a 12-slide Pitch Deck Outline for this asset, fully capturing its technical specs, monetization pathways, and the core Third Signal venture studio thesis.
\`\`\`
```

## Why This Matters
*   **Zero-Context Handoff**: It enables a "Signal-to-System" loop. An agent generated the spec; another agent can consume it and expand it seamlessly.
*   **Operating Leverage**: Reduces the operator's cognitive load. The user doesn't need to write a prompt every time they upload a file.