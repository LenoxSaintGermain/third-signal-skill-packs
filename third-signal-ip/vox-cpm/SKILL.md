---
name: vox-cpm
description: "Local, zero-shot voice cloning and TTS engine running natively on Apple M4 Silicon. Replaces ElevenLabs."
version: 1.0.0
author: Donna
platforms: [macos]
metadata:
  hermes:
    tags: [voice, tts, audio, cloning, offline, studio-pod]
    category: media
    related_skills: [third-signal-video-assembly]
---

# Vox CPM (Local Voice Synthesis & Cloning)

This skill provides local Text-to-Speech (TTS) and zero-shot voice cloning capabilities using the Mac Mini's unified M4 memory. It completely replaces ElevenLabs for the **Studio-Pod** pipeline, providing high-fidelity, commercial-grade narration with zero network latency and $0 API cost.

## Workflow Execution

To generate audio, use the local `vox-cpm` CLI installed on LANDSAT.

### Basic Text-to-Speech
Generates standard high-quality TTS using built-in voices.
```bash
vox-cpm generate --voice "narrator-deep" --text "Welcome to the Third Signal ecosystem." --output "/Volumes/Third Signal Lab HD/hermes/workspaces/Studio-Pod/pipeline/assets/audio/shot_01.wav"
```

### Zero-Shot Voice Cloning
Clones a target voice using a 5-10 second clean reference audio sample.
```bash
vox-cpm clone --reference "/Volumes/Third Signal Lab HD/hermes/workspaces/Studio-Pod/pipeline/assets/audio/lenox_sample.wav" --text "This is an exact voice clone." --output "/Volumes/Third Signal Lab HD/hermes/workspaces/Studio-Pod/pipeline/assets/audio/cloned_narration.wav"
```

## Studio-Pod Integration Checklist
When executing the Studio-Pod pipeline:
1. Parse the narrative dialogue blocks from `02_Script_Hybrid.md`.
2. Generate the corresponding `.wav` files using the `vox-cpm` terminal commands above.
3. Output all audio files to `/Volumes/Third Signal Lab HD/hermes/workspaces/Studio-Pod/pipeline/assets/audio/`.
4. Update `06_Tracker.md` to associate the newly minted audio assets with their Shot IDs.
5. Hand off to the `third-signal-video-assembly` skill to loudnorm and merge the audio with the Veo 3.1 video renders.
