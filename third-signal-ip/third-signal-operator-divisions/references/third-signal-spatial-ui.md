# Third Signal Spatial UI / Investor Hub Design Standard

When building high-fidelity presentation layers for Third Signal (like the Investor Hub or Showcase), the standard is "Bloomberg-meets-Apple Vision OS." Do not use generic flat dashboards, rigid pill buttons, or simple box layouts. The goal is to convey deep-tech arrogance, high operating leverage, and sovereign infrastructural stability.

## 1. Aesthetic Constraints
- **Colors:** Deep Dark (`#0D0E11`), Copper (`#C87D3E`), Cyan (`#00D4FF`).
- **Typography:** 
  - UI & Body: `Inter`
  - Headlines & Editorial/Briefs: `EB Garamond` (gives it the WSJ/Prospectus weight)
  - Tech Specs & Telemetry: `JetBrains Mono` (gives it the terminal/cockpit precision)
- **Glassmorphism & Depth:** Heavy use of `backdrop-blur-[40px]`, double-border gradients (`from-nexus-copper/30 to-transparent`), and inset shadows to simulate physical glass depth.
- **Naming Conventions:** Use stark, utilitarian, minimalist titles. "Venture Index" instead of "Portfolio." "Specifications" instead of "Details." "Sovereign System Blueprint" instead of "Tech Stack."

## 2. Structural Layout Patterns (The Dual Hero Deck)
When presenting complex assets (like an OS, SaaS, or IP):
- **Avoid single massive videos** pushing content down.
- **Use the Dual-Hero Split Deck:** On large screens, split the top into two 16:9 cinematic glass windows.
  - *Left Screen (Primary):* The cinematic walkthrough video (NotebookLM / YouTube embed).
  - *Right Screen (Secondary):* The interactive live app sandbox (iframe).
  - If a video is pending, use a deterministic holographic radar placeholder with a "Pipeline Pending // Awaiting Uplink" terminal prompt.

## 3. The Interactive Brief vs. Dossier Tab System
Do not dump all information on one screen. Follow the "Signal Spark" narrative flow:
- **Briefing Tab (Marketing Layer):** Clean, asymmetric grid of cream-accented cards for "Market Signal", "Monetization Path", and "Replication Thesis". Accompanied by a stark, terminal-styled "Allocation Ask" card showing development cost and SAFE equity target.
- **Specifications Tab (Engineering Layer):** 
  - *Venture Canvas:* A 2x2 grid representing a Business Model Canvas (Customer Segments, Channels, Cost Structure, Revenue Streams) with custom monospace bullet glyphs (`›`).
  - *System Blueprint:* A grid of micro-tagged technical specification capsules (e.g., `⟨ React 19 ⟩`, `⟨ Ollama Local Node ⟩`) instead of boring text lists.
  - *Telemetry:* Live-looking radar charts showing maturity, complexity, scale, security, and innovation.

## 4. The Sovereign Prospectus Footer
Never use floating status bars that break container boundaries or obscure content.
- Use a static, elegant, and highly structured metadata footer at the absolute bottom of the scrollable panel.
- Example: `UPLINK: ACTIVE • PROJECT ID: {ASSET_ID} • DEPLOYED REVISION: V4.0 | THIRD SIGNAL VENTURE STUDIO • SEC REG D ACCREDITED PROSPECTUS`

## 5. Agent-Readable Markdown Exports
Any "Export Spec" button must not just dump plain text. It must generate a *self-contained cognitive seed* for autonomous agents.
- **Structure:** Strict YAML Frontmatter -> Investability Brief -> BMC Task Lists (`- [ ]`, `- [x]`) -> Tech Blueprint Array.
- **Agentic Recompilation Instructions:** Always embed a `[SYSTEM DIRECTIVE // INTERPRET_PROSPECTUS]` at the end of the markdown export instructing a high-reasoning LLM (like Claude 3.5 Sonnet) on how to recompile the file into a 10-page PRD and pitch deck outline.