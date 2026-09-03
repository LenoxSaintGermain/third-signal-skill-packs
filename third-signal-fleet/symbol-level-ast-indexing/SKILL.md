---
name: symbol-level-ast-indexing
description: Use when agents need token-efficient repository navigation, AST symbol trees, method signatures, or unified multi-tool code intelligence plugins.
metadata:
  requires_tools: [file, terminal]
  fallback_for_tools: [file, terminal]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# Symbol-Level AST Indexing

## Level 0 — Overview

Use symbol-level indexing to give agents a structural map before they read source. Parse supported languages into symbol trees, signatures, spans, references, and diagnostics; expose focused lookups through one plugin rather than forcing whole-file retrieval. This follows the github-codemunch-mcp/token-savior pattern while preserving source-of-truth links.

Indexes accelerate navigation; they do not replace reading implementation or running tests.

## Level 1 — Runbook

1. Discover repository roots, language parsers, generated paths, and ignore rules.
2. Parse files into deterministic symbol records: module, class, function, method, constant, export, signature, span, and parent.
3. Store parser version, file hash, language, and index timestamp for invalidation.
4. Add references and call edges where the parser can prove them; label inferred edges.
5. Expose tools such as `tree`, `symbol`, `signature`, `references`, and `read_span` behind one permission boundary.
6. On lookup, return concise structure plus exact file path and line span; fetch source only on request.
7. Re-index changed files, delete removed symbols, and verify index/source consistency in CI.

## Level 2 — Reference

A symbol record should include `id`, `kind`, `name`, `qualified_name`, `file`, `start_line`, `end_line`, `signature`, `parent_id`, `language`, `file_sha256`, and `parser_version`. Keep adapters language-specific and the plugin contract language-neutral. Never execute indexed code or treat comments as declarations without a parser-backed kind.

## Common Mistakes

- Returning stale symbols after a file changes.
- Collapsing overloaded methods by name alone.
- Losing generated/source-map provenance.
- Claiming inferred references are compiler-proven.
- Exposing a broad filesystem reader through the indexing plugin.

## Verification

Run fixture repositories for each supported language, compare spans to source, test incremental updates and deletions, verify overloaded signatures, and confirm tool responses remain bounded and provenance-linked.
