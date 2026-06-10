# Third Signal Command Cockpit Architecture

This reference outlines the unified local dashboard deployed on LANDSAT to visualize and execute the Third Signal Executive Board's directives.

## Core Components

1. **The Knowledge & UI Layer (`open-notebook`)**:
   - Deployed locally via Docker Compose.
   - Volumes mapped to the synced Google Drive folders (`raw_sources` and `Executive_Board`).
   - Acts as the visual UI to read Board Directives, search historical IP, and use multi-speaker podcast generation on the raw text.

2. **The Generative Media Layer (`vertex-ai-creative-studio` MCPs)**:
   - Extracted from Google's open-source `vertex-ai-creative-studio` repo.
   - Exposes Google's flagship generative media models (Veo 3.1 for video, Lyria for music, Chirp HD for speech, Gemini Flash for images) to the local machine via the Model Context Protocol (MCP).

3. **The Orchestrator (Hermes)**:
   - Wires the two layers together.
   - When the CMO (Nova) writes a script, Hermes invokes the Vertex MCP servers to generate the audio/video assets and pipes them into Open Notebook or the filesystem for the Operator's review.

## Operator Workflow
Instead of managing terminal scripts, the Operator views `localhost:8502` to see the synthesized strategies from Atlas and Nova, then triggers Hermes to build the physical assets.