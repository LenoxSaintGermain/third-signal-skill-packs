# Seedance 2.5 and MiniMax H3 prompting

Verified 2026-10-14; provider limits are not automatically Manus limits.

## Seedance 2.5

ByteDance describes up to 30 seconds and reference-driven audio/video generation. Assign exact roles to provided references, name subjects consistently, use ordered physical actions and camera paths, and state audio separately. Keep spatial goals concrete: who moves, toward which target, what contact occurs and how the state changes. Avoid a pile of adjectives or contradictory simultaneous moves.

Template: reference roles → environment and opening composition → timestamped action beats → camera path → continuity constraints → sound → ending state. For action, fix screen direction, hand/weapon custody and the consequence of contact. Do not claim a motion reference, character record or end-frame control unless the interface actually accepts it.

Sources: https://seed.bytedance.com/en/seedance2_5 and https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5

## MiniMax H3

H3 is a distinct model; do not silently substitute Hailuo. MiniMax describes up to 15 seconds, 2K and native stereo. Official prompt-writing guidance separates integrated_multimodal_description, overall_soundscape and non_diegetic_music. Keyframe mode requires explicit frame alignment. Full-reference guidance adds subject_definitions, summary, retention_analysis and detailed_description. Maintain consistent Subject/Picture/Video/Audio labels and state what to retain or change from each supplied reference.

Use this structure as a briefing aid in Manus. Do not pretend Manus exposes native H3 JSON or every underlying mode. The official h3-prompt-writing skill is portable; other MiniMax Hub production skills require their own tooling. For longer trailers assemble coherent shots instead of claiming a single H3 generation exceeds its documented duration.

Sources: https://www.minimax.io/blog/minimax-h3 ; https://github.com/MiniMax-AI/MiniMax-H3 ; https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt ; https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt

## Acceptance

Score identity, action readability, physical interaction, spatial continuity, requested effect, audio and export integrity against actual playback. A model reputation or preview thumbnail is not quality evidence. Report settings, input differences and observed costs when comparing providers.
