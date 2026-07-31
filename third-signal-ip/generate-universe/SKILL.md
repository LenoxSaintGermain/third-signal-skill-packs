---
name: generate-universe
description: Triggers a multi-agent worldbuilding workflow to automatically generate a comprehensive Worldtree branch (including characters, locations, and events) from a single "seed" input (a prompt, artifact, or image). Use this skill when the user asks to "generate a universe", "build a world from this seed", "create a full world tree branch", or "draft a new repo from this artifact".
license: Complete terms in LICENSE.txt
---

# Generate Universe Workflow

This skill orchestrates a multi-step, multi-agent process to automatically sketch out and populate a new Worldproject or Worldtree Branch based on a seed provided by the user.

## Triggering the Workflow

When the user invokes this skill (e.g., `/generate-universe "seed material"`), immediately execute the following procedural steps without asking for further permission. 

### Phase 1: Seed Extraction & Analysis
1. **Analyze the Seed:** Carefully read the prompt text, examine the provided artifact, or process the seed context.
2. **Deconstruct the Universe:** Break the core concept down into narrative pillars:
   - **Primary Actors (Characters):** Identify 3-5 key figures, protagonists, and antagonists.
   - **Key Locations (Places):** Identify 2-3 anchor locations where the narrative takes place.
   - **Core Chronology (Events):** Identify 2-3 inciting incidents or deep lore historical anchors.

### Phase 2: Architecture & Dispatch (The DIRTY Protocol)
1. **Formulate the Operation Plan:** Create an internal checklist of the distinct `create-character`, `create-location`, and `create-event` operations needed to populate this universe.
2. **Mint the Repository/Branch:** Use the Worldtree Engine to create a localized `projectId` or master `Branch` specific to this seed so that the new nodes do not bleed into other IPs.
3. **Execute the Node Creation:** Act autonomously as the DIRTY agent (or standard coding agent) to rapidly instantiate the designed nodes. 
   - Ensure the JSON metadata of each node is rich and detailed.
   - Ensure characters and events are logically connected (e.g., cross-referencing IDs in their metadata maps).

### Phase 3: Finalization & Cinematic Debrief
1. **Verify Integrity:** Ensure all generated nodes successfully appear in the active branch/project list natively.
2. **Trigger the UI:** If capable, emit the `open-worldtree-panel` event or instruct the user to open the Lore Tab to view the newly compiled Journey Map.
3. **Report to Operator:** Output a highly cinematic "Mission Debrief" (in the ALFRED/Orbit OS voice) detailing the shape of the newly spawned universe. Conclude by suggesting three potential dramatic "next steps" or timeline forks the user could explore.
