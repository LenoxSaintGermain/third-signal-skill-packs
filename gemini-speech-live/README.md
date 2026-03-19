# Gemini Speech & Live API (The Director's Framework)

**Status**: 🟡 POC (Functional Prototype)
**Version**: 2026.03
**Valuation**: $35–85M
**Category**: Conversational AI & Audio Engineering

---

## Overview

A high-fidelity multimodal orchestration framework for Gemini 2.5 and 3.1 architectures. This skillpack provides the "Director’s Framework" for studio-quality speech synthesis and the "WebSocket Protocol" for zero-latency live conversational agents.

**The Problem**: Traditional speech AI suffers from "lossy" STT-to-Text-to-TTS conversion, leading to robotic pacing and high latency. Most agents lack "barge-in" support and multimodal awareness (seeing while talking).

**The Solution**: Native audio execution using Gemini 2.5/3.1, eliminating intermediate text layers. It utilizes **Natural Language Direction** instead of SSML and stateful WebSockets for real-time bidirectional streaming.

---

## 1. Capability Mapping

| Capability | Best Model | Primary Use Case |
| :--- | :--- | :--- |
| **High-Fidelity TTS** | `gemini-2.5-pro-preview-tts` | Audiobooks, Podcasts, Professional Narrations. |
| **Real-time Voice** | `gemini-2.5-flash-live-preview` | Low-latency Agents, In-car assistants, Gaming NPCs. |
| **Live Multimodality** | `gemini-2.5-flash-native-audio` | Visual Agents (e.g., "See my screen and talk to me"). |
| **Audio Intelligence** | `gemini-3.1-flash` | Transcription, Sentiment, and Batch Analysis. |

---

## 2. Text-to-Speech: The "Director’s Notes" Framework

Gemini replaces rigid SSML tags with **Natural Language Direction**. To achieve professional output, send a **Contextual Brief** alongside the transcript.

**Example Strategy**:
- **Audio Profile**: Define the archetype (e.g., "Detective Thorne, mid-40s, gravelly").
- **Scene Context**: Describe the environment (e.g., "Rainy alleyway at 2 AM").
- **Director's Notes**: Specify style, pacing, and emotional shifts (e.g., "Gritty, hushed, start fast then slow down").

---

## 3. Live API: Low-Latency Orchestration

The Live API uses a **stateful WebSocket (WSS)** for bidirectional streaming of audio/video in and audio/text out.

**Core Features**:
- **Barge-in Support**: Intelligent interruption detection.
- **Multimodal Input**: Streaming JPEG frames at 1 FPS alongside audio.
- **Real-time Tool Use**: Calling functions (e.g., `check_inventory()`) mid-conversation.
- **Stateful Logic**: 16-bit PCM, 16kHz raw audio streaming for minimal overhead.

---

## 4. Audio Intelligence & RAG

Extracting semantic value from raw audio files without separate transcription steps.
- **Multimodal Sentiment**: Detecting frustration vs. satisfaction via acoustic cues (pitch/speed).
- **Speaker Diarization**: Identifying multiple speakers in a single track.
- **Batch Analysis**: Timestamped transcripts and action item extraction from long-form recordings.

---

## 5. Strategic Guardrails

- **🚨 Legacy Trap**: Avoid Gemini 1.5 for speech; the Native Audio engine in 2.5/3.1 is 4x more efficient.
- **🚨 Sample Rate**: Always use **16kHz** for input to avoid resampling artifacts and latency.
- **🚨 Speaker Limits**: Direct TTS handles up to 2 speakers; use the Live API for larger casts and dynamic turn-taking.

---

## Status

- **Director's Framework (TTS)**: ✅ PRODUCTION
- **Live WebSocket Bridge**: 🟡 POC (Under development)
- **Audio Intelligence (RAG)**: ✅ PRODUCTION

---

## License

Specification: CC BY-SA 4.0

---

**Maintained by**: Third Signal
**Contact**: audio@thirdsignal.ai
