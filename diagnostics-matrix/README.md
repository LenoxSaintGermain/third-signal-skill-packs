# Diagnostics Matrix (The Mechanic)

**Status**: 🟡 POC (Functional Prototype)
**Version**: 0.8
**Valuation**: $15–35M
**Category**: Developer Experience & Observability

---

## Overview

A cinematic, interactive CLI REPL for querying the architectural graph of a codebase. "The Mechanic" serves as a live factory repair manual for complex software systems, providing high-fidelity "traceroutes" of dependencies and logic flows.

**The Problem**: In large codebases, understanding the ripple effect of a change is difficult. Documentation is often stale, and standard IDE dependency views are either too flat or too overwhelming.

**The Solution**: An AST-powered scanner that generates a structured semantic map (ORBITAL_TECH_INDEX), coupled with an ASCII-art rendering engine that visualizes dependencies in a high-fidelity terminal interface.

---

## The ASCII Engine

The Diagnostics Matrix utilizes a custom ANSI output parser and an ASCII tree tracing engine to provide a "Gundam Core" style navigation experience.

**Key Features**:
- **AST Scanning**: Deep crawling of `components/`, `lib/`, and `server/` using `ts-morph`.
- **High-Fidelity ANSI**: Recursive traceroutes rendered with cinematic terminal visuals.
- **Dependency Graphing**: Automated computation of module types, exports, imports, and "imported by" relationships.

---

## Skillpack Signatures

| Skill | Signature | Description |
|-------|-----------|-------------|
| **mechanic.scan()** | `path: string` | Triggers a full AST scan of the target directory to build the Tech Index. |
| **mechanic.trace()** | `symbol: string` | Executes a recursive "traceroute" for a specific symbol across the codebase. |
| **mechanic.visualize()** | `module: string` | Renders a high-fidelity ASCII dependency tree for the specified module. |
| **mechanic.stats()** | `none` | Returns high-level metrics (files scanned, components mapped, warnings). |

---

## Implementation Details

### The Technical Manual (build_tech_manual.ts)
The core logic resides in a hardened TypeScript script that:
1. Initializes a `ts-morph` project.
2. Crawls the source tree.
3. Maps exports and imports to determine module "gravity."
4. Persists the state to `ORBITAL_TECH_INDEX.json`.

### The CoworkTerminal
A React-based terminal component that integrates `xterm.js` and a custom ANSI parser to handle the complex ASCII visualizations produced by the trace engine.

---

## Market Position

**Gap**: DataDog and New Relic provide runtime observability, but lack deep *structural* observability. The Diagnostics Matrix bridges the gap between static analysis and live developer mental models.

**The Unlock**: Developers spend 70% of their time reading code. Reducing the cognitive load of navigation directly accelerates ship velocity.

---

## Status

- **AST Scanner**: ✅ PRODUCTION (within Orbital)
- **ASCII Engine**: 🟡 POC (Under development)
- **3D Visualization (Psycho-Frame)**: 🔴 SPEC (Planned)

---

## Waitlist

Join the early access for the standalone Diagnostics Matrix CLI.
**Email**: mechanic@thirdsignal.ai

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: mechanic@thirdsignal.ai
