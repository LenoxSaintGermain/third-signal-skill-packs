# Studio-Pod: Agentic Filmmaking & Narrative Architecture

This architecture solves the "Context Bloat" problem when generating massive graphic novels, videos, or lore bibles. It prevents models from hallucinating by grounding them in a strictly controlled local markdown state machine, rather than passing 50+ images/assets into the context window.

## The 6-File Markdown Chassis
Keep these at the root of the project (e.g., `/hermes/workspaces/ProjectName/pipeline/`):

1. `01_Quickstart.md` - Session boot sequence & rules for the agent.
2. `02_Script_Hybrid.md` - The interconnected document mapping narrative dialogue directly to the exact generation prompt required.
3. `03_Style_Guide.md` - Visual, lighting, and model configurations (e.g., the DIRTY protocol, "Bloomberg-meets-Apple", gritty ink-wash).
4. `04_Character_Grid.md` - Reference seeds and Omni-reference assets for characters.
5. `05_Production_Brief.md` - Core themes, arcs, plot states, and goals.
6. `06_Tracker.md` - The live state machine table (Shot ID | Status | File Ref | Timestamp).

## The Orchestrator Script
A python script (`scripts/orchestrator.py`) runs locally to:
1. Automatically update `06_Tracker.md` whenever an asset is generated.
2. Generate **Handoff Documents** (`exports/Handoff_Doc_V[X].md`).

## The Handoff Protocol (Context Boundary)
When the context window gets too heavy (after many generations):
1. The script compiles the compressed plot state, locked stylistic variables, and the *last line* of the tracker into a Handoff Doc.
2. The agent wipes its current session memory (spins up a new session/branch).
3. The new session ingests the Handoff Doc to instantly re-anchor context without the token bloat of the previous 50 turns.

**Rule:** Never pull large visual/video files directly into the context window to evaluate layout. The user downloads them; the agent reads the local file metadata/tracker.