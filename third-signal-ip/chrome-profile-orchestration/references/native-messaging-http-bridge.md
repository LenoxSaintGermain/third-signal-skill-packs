# Architectural Reference: Chrome Native Messaging to Local HTTP Bridge

This document details the architecture, implementation rules, and debugging pitfalls discovered while building the **Orbital Context** browser-control bridge on LANDSAT. It serves as a guide for implementing secure, low-latency, zero-cost agentic browser control in Manifest V3.

---

## 1. The Sandbox Challenge
In Manifest V3, Chrome Extensions are strictly sandboxed. They are prohibited from:
*   Opening local TCP ports (making direct WebSocket or HTTP servers impossible inside the browser).
*   Loading remote scripts (such as CDN-hosted frameworks like Tailwind) due to strict Content Security Policy (CSP).

---

## 2. The Solution: Asymmetric Native Messaging Bridge
To bridge the local Hermes agent with the browser, we use Chrome's **Native Messaging API** to tunnel commands through a local Node.js process acting as a proxy.

```
 [ Local Hermes Agent ] ──(Local HTTP:4114)──➔ [ Node.js Native Host (.cjs) ]
                                                        │
 [ Chrome Browser State ] ◄──(Native Messaging stdio)───┘
```

1.  **The Host Registration:** The local Node script is registered as a native host via a JSON manifest placed in `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/`.
2.  **The Lifecycle:** Chrome launches this Node process in the background when the extension service worker connects, piping `stdin`/`stdout` directly to the browser.
3.  **The Local HTTP Listener:** The Node script spins up a native `http` server on `127.0.0.1:4114`. 
4.  **The Command Loop:** Hermes sends standard HTTP requests to `localhost:4114`. The Node script translates these into Chrome-compliant JSON structures, pushes them over `stdout`, receives the asynchronous reply over `stdin`, and returns the HTTP response.

---

## 3. Critical Developer Pitfalls & Failures

### Pitfall A: TypeScript inside Chrome Service Workers
*   **The Error:** Silent service worker boot crashes.
*   **The Cause:** Chrome's extension engine cannot natively compile or execute `.ts` files inside background service workers (`manifest.json` pointing directly to `background.ts`).
*   **The Fix:** Write the background service worker in native JavaScript (`background.js`) or compile it strictly via Vite/esbuild prior to loading.

### Pitfall B: CommonJS vs ES Modules (`type: module`)
*   **The Error:** `ReferenceError: require is not defined in ES module scope` on native host boot.
*   **The Cause:** Modern Vite/React repositories set `"type": "module"` in their root `package.json`. If your Node.js native host script uses standard `require('fs')` or `require('http')` and is named `index.js`, Node will force it into ESM scope and crash immediately upon Chrome launch.
*   **The Fix:** Force Node into CommonJS scope by explicitly naming the host script with a `.cjs` extension (e.g., `index.cjs`) and updating the Chrome host manifest `path` property to match.

### Pitfall C: Port Conflicts (`EADDRINUSE`) on Extension Reload
*   **The Error:** `Uncaught Error: listen EADDRINUSE: address already in use 127.0.0.1:4114` in logs, causing subsequent connections to instantly disconnect.
*   **The Cause:** When you click "Reload" on an unpacked extension card in `chrome://extensions/`, Chrome kills the extension background page and launches a new one. However, if the old Node host process does not explicitly terminate itself when `stdin` closes, it becomes an **orphaned background daemon**, holding onto port `4114`. The new instance then crashes on boot.
*   **The Fix:** You MUST monitor `stdin` close events inside the native host script and force a clean exit:
    ```javascript
    process.stdin.on('end', () => {
        process.exit(0);
    });
    ```

### Pitfall D: Content Security Policy (CSP) Style Blocks
*   **The Error:** Broken, unstyled sidebar UI where image favicons are rendered at massive, native sizes.
*   **The Cause:** Chrome completely blocks `<script src="https://cdn.tailwindcss.com"></script>` inside the SidePanel context due to CSP rules.
*   **The Fix:** Avoid external CSS/JS CDNs entirely. Write pure, native, inline CSS inside a `<style>` block in your HTML. Use rigid CSS constraints (e.g., `.tab-icon { max-width: 16px !important; }`) to guarantee high-res favicons scale down correctly.
