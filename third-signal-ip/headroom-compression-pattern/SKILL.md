---
name: headroom-compression-pattern
description: Log and error output compression using headroom to reduce context token usage.
---

# Log and Error Output Compression (headroom Pattern)

When local agents run tests or compile code, verbose trace logs can consume thousands of context tokens. Adopt the headroom pattern to intercept and compress massive text blocks before forwarding.

## Tool Schema (MCP Custom Design)

Use or implement the following tool pattern:

```json
{
  "name": "compress_terminal_output",
  "description": "Compress verbose build traces, error logs, or stdout files, preserving semantic error keys while reducing token count by up to 90%.",
  "input_schema": {
    "type": "object",
    "properties": {
      "raw_text": { "type": "string", "description": "The verbose console logs or files to compress." }
    },
    "required": ["raw_text"]
  }
}
```

## References
- [chopratejas/headroom on GitHub](https://github.com/chopratejas/headroom)