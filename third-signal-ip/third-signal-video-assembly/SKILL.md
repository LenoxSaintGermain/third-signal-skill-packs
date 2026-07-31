---
name: third-signal-video-assembly
description: "Programmatic video editing pipeline bridging Studio-Pod trackers to FFmpeg and Remotion. Automates assembly, EDLs, and cinematic overlays."
version: 1.0.0
author: Donna
platforms: [macos]
metadata:
  hermes:
    tags: [video, editing, ffmpeg, remotion, ecc, studio-pod]
    category: media
    related_skills: [vox-cpm, headroom-compression-pattern]
---

# Third Signal Video Assembly (The ECC Protocol)

This skill operationalizes the programmatic video assembly pipeline (assimilated from the `affaan-m/ECC` framework) into the sovereign Third Signal **Studio-Pod** architecture. 

Rather than editing manually in Premiere or CapCut, this skill empowers agents to execute programmatic cuts, compositing, and rendering of raw footage or AI-generated B-roll (Veo 3.1) directly via local CLI tools.

## The 4-Layer Assembly Pipeline

### Layer 1: The Edit Decision List (EDL)
Before rendering, the agent generates an EDL based on the `02_Script_Hybrid.md` and the current `06_Tracker.md` state.
- Formats timestamps and cut points (e.g., `00:00:15.000` to `00:00:22.500`).
- Maps visual assets (Veo 3.1 outputs) to their respective audio tracks (`vox CPM` local voiceovers).

### Layer 2: FFmpeg Scaffolding (Raw Cuts & Concat)
Use `ffmpeg` for lightning-fast, headless video trimming and concatenation.
**Command Pattern - Trim:**
```bash
ffmpeg -i input.mp4 -ss 00:00:15 -to 00:00:22.5 -c:v libx264 -c:a aac -strict experimental output_cut.mp4
```
**Command Pattern - Concat (from text list):**
```bash
# file_list.txt must contain: file 'shot1.mp4' \n file 'shot2.mp4'
ffmpeg -f concat -safe 0 -i file_list.txt -c copy final_assembly.mp4
```

### Layer 3: Remotion (React-Based Cinematic Overlays)
For motion graphics, chapter cards, progress bars, and lower-thirds, we use **Remotion** (React for video).
- Spin up a generic Remotion template in the Studio-Pod workspace: `npx create-video@latest studio-overlays`
- Agents write programmatic React components for cinematic text overlays matching the Third Signal Design System (Electric Blue / Copper).
- Render headlessly: `npx remotion render HelloWorld out/video.mp4`

### Layer 4: Final Audio Polish & Loudnorm
Instead of external services like Descript or ElevenLabs, we use local FFmpeg filters to normalize audio levels and merge the `vox CPM` voiceovers with ambient tracks.
**Command Pattern - Loudnorm & Mix:**
```bash
ffmpeg -i video.mp4 -i ambient.wav -filter_complex "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[norm];[1:a]volume=0.2[bg];[norm][bg]amix=inputs=2:duration=first" -c:v copy final_mix.mp4
```

## Integration with Studio-Pod

1. When the `06_Tracker.md` reaches 100% completion for a scene or video...
2. The agent executes a Python script to parse the tracker and generate the FFmpeg `concat` file.
3. The agent triggers FFmpeg to merge the clips.
4. The agent triggers Remotion to bake the title cards and UI overlays on top of the merged output.
5. The final asset is deposited in `/Volumes/Third Signal Lab HD/hermes/workspaces/Studio-Pod/pipeline/exports/`.
