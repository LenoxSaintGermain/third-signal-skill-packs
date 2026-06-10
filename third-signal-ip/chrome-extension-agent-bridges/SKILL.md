---
name: chrome-extension-agent-bridges
description: Architectural patterns and pitfalls for bridging local AI agents (Hermes) with Google Chrome using Manifest V3 Extensions, Native Messaging, and local HTTP port bridges.
---

# Chrome Extension Agent Bridges

This skill defines the canonical architecture for enabling a local AI agent to programmatically control, read, and manipulate an active Google Chrome browser window securely, bypassing Manifest V3 sandboxing.

## When to Use
Use this skill when designing browser-control integrations, building Manifest V3 extensions, or constructing local Node.js hosts to securely extract browser DOM context or execute keyboard injection (virtual typing) in web apps.

## The Tri-Tier Architecture
To securely bridge a local agent with an active Chrome window, deploy the following three layers:

```
[ Local Agent (Hermes/Cron) ]
            │
            ▼  (HTTP REST API: Localhost Port)
[ Native Messaging Host (Node.js/CJS) ] ──(Exposes Local Port)
            │
            ▼  (Chrome Native Messaging Protocol: stdio with 32-bit length prefixes)
[ Chrome Extension (Manifest V3 Service Worker) ]
            │
            ▼  (Chrome Extension APIs & Injection)
[ Active Browser DOM / Tabs / Webpages ]
```

1. **The Extension Layer (Manifest V3):** Connects to the native host on startup (`chrome.runtime.connectNative`) and executes queries/mutations (e.g., `chrome.tabs.query` or `chrome.scripting.executeScript`).
2. **The Host Layer (Node.js):** Registered globally on macOS. It parses Chrome's proprietary 32-bit length-prefixed stdio protocol and maps incoming calls to local HTTP endpoints (`/tabs`, `/prompt`).
3. **The Local Port Bridge:** The Node script spins up a native, lightweight HTTP server (using `http` native module) on a local port (e.g., `4114`). The local agent uses simple HTTP requests to communicate with Chrome, completely bypassing sandbox limitations.

---

## Critical Pitfalls & Workarounds

### 1. The Manifest V3 Content Security Policy (CSP) Block
*   **The Problem:** Manifest V3 extensions strictly prohibit executing remote scripts. Injecting CDN links like `<script src="https://cdn.tailwindcss.com"></script>` inside extension HTML (like `sidepanel.html`) will fail silently, causing the UI layout to break and assets (like large SVGs) to scale out of control.
*   **The Fix:** Write **100% native, inlined CSS** inside a `<style>` block of the HTML file. Do not rely on external CSS or build-step CSS in unpacked extensions unless fully compiled.

### 2. Orphaned Port Binding (`EADDRINUSE`) on Extension Reload
*   **The Problem:** Clicking "Reload" on a Chrome Extension terminates the service worker and cuts the native connection, but **does not kill the Node.js native host process** unless handled. The old process remains active as an orphan, keeping the local HTTP port locked. The next reload crashes the new native host with `EADDRINUSE`.
*   **The Fix:** The native host *must* listen to `process.stdin` `end` events and immediately self-terminate:
    ```javascript
    process.stdin.on('end', () => {
        process.exit(0);
    });
    ```

### 3. Absolute Node Path in macOS Manifests
*   **The Problem:** Chrome is launched as a macOS GUI application from Finder, meaning it **does not inherit your terminal shell's `$PATH`** (it won't find NVM or Homebrew Node paths). Using `#!/usr/bin/env node` as a shebang will cause Chrome to fail to launch the host silently.
*   **The Fix:** Hardcode the absolute path to Node in the script shebang (e.g., `#!/usr/local/bin/node` or `/opt/homebrew/bin/node`), or use a shell wrapper to source the environment before launching Node.

### 4. ES Modules vs CommonJS Scope Crashes
*   **The Problem:** Vite-configured repositories default to `"type": "module"` in their `package.json`. If you write a standard Node script using legacy CommonJS (`require()`) with a `.js` extension, Node will crash instantly on launch.
*   **The Fix:** Force Node to treat the native host script as CommonJS by renaming the file extension to `.cjs`.

---

## Linked References
- `references/native_messaging_mcp_spec.md` — Complete binary protocol specifications and boilerplate files.
