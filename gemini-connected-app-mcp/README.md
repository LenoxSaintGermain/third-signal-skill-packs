# Gemini Connected App MCP

**Status**: 🟢 PRODUCTION
**Version**: 1.0.0
**Category**: Agent Integration

---

## Overview

You write an MCP server. You test it with `curl` and every path returns exactly what the
spec says it should. You point Gemini's "custom connected app" at it and get four words:

> **The MCP server could not be reached.**

The server is running. The tunnel is up. `curl` proves it. The client says it isn't there.

**The Problem**: six distinct failures, each one masked by the last, and every one of them
invisible to `curl`. A working `curl` session is not evidence that a browser-hosted client
can talk to your server — it is evidence that a *server-to-server* client could.

**The Solution**: build for the client's actual execution context. Gemini's connector runs
**in a browser**, which means CORS preflight, three-legged OAuth with a real redirect, and
spec-exact discovery documents. None of that applies to `curl`, so none of it shows up in
the test that made you confident.

> This is the same failure mode as [`inference-spend-forensics`](../inference-spend-forensics)
> Law 1, transposed: there, the bill named the model and people theorised anyway. Here, the
> client names its context and people test with the wrong one.

---

## The Six Laws

| # | Law | The instinct it corrects |
|---|-----|--------------------------|
| **1** | **`curl` is not the client** — test in the execution context the real client uses | "It works with curl, so the server is fine." curl has no CORS, no preflight, no redirect handling. It cannot fail the way a browser fails. |
| **2** | **A browser client needs CORS or it never reaches you** — implement `OPTIONS`, `HEAD`, and `Access-Control-Allow-Origin` on **every** response path | "CORS is a frontend concern." A missing `do_OPTIONS` returns 501 to the preflight, and the browser reports your healthy server as unreachable. |
| **3** | **404 means "no server", 405 means "wrong method"** — `GET` on the MCP endpoint must return 405 with `Allow: POST` | "GET isn't supported, so 404 is honest." To a client probing for reachability, 404 is proof of absence. 405 is proof of presence. |
| **4** | **Drain the request body before an early return** — on HTTP/1.1 keep-alive, unread bytes corrupt the *next* request on that socket | "It's a 401, the body doesn't matter." The unread body stays buffered; the following request arrives mangled and fails as something unrelated, sending you after the wrong bug. |
| **5** | **A redirect URI in the setup dialog means three-legged OAuth** — implement Authorization Code + PKCE, not just `client_credentials` | "It's machine-to-machine, so client credentials." The dialog showing a redirect URI is the tell. Advertising only `client_credentials` gets flatly rejected as unsupported. |
| **6** | **The two discovery documents are different documents** — RFC 9728 and RFC 8414 are not interchangeable | "Discovery is discovery, serve the same JSON at both." `oauth-protected-resource` declares `resource` + `authorization_servers`. `oauth-authorization-server` carries `authorization_endpoint`/`token_endpoint`. Serve AS fields at the RP URL and a spec-strict client cannot resolve where to authenticate. |

---

## The discriminating test

Before blaming the server, ask:

> **Where does this client execute?** In a browser, on a vendor's servers, or on my machine?
> Each answer implies a different protocol surface. Test from *that* place.
>
> **Did my last "fix" change the symptom, or just my confidence?** If the error message is
> byte-identical after a change, you fixed something real but not the thing in front of you.

An unchanged error after a change means keep the fix and keep looking. It does not mean the
fix was wrong.

---

## The diagnostic sequence

Run in order. Each step eliminates a whole class.

| # | step | what it settles |
|---|------|-----------------|
| **1** | **Read the server's own request log** | Whether the client reached you at all. No entries means DNS, tunnel, or vendor-side blocking — nothing server-side will help. |
| **2** | **`curl -X OPTIONS`** | CORS preflight. A 501 here is Law 2 and explains "could not be reached" on its own. |
| **3** | **`curl` GET the MCP endpoint** | Law 3. Anything but 405 misleads a reachability probe. |
| **4** | **Issue two requests on one connection** | Law 4. If the second is mangled, you have a keep-alive body-drain bug, not a protocol bug. |
| **5** | **Fetch both `.well-known` documents and diff them** | Law 6. If they are identical, one of them is wrong by construction. |
| **6** | **Walk the OAuth flow by hand with `curl`** — `/authorize` → code → `/token` → authenticated call | Law 5. Proves the grant type the client actually requires. |

**Read the log before touching code.** In the run this pack came from, one whole debugging
round was spent on a server that had never started — the launch shell lacked the env var
that the server refuses to boot without. The client error was identical either way.

---

## Environment parity: the same law, one layer down

Once it works, it has to keep working unattended, and that is where the same mistake repeats.

A service that runs fine in your shell can fail under `launchd`, `systemd`, or cron, because
those run with a minimal `PATH`. Observed here: `/usr/bin/env python3` resolved to
`/opt/homebrew/bin/python3` (3.14) interactively and to `/usr/bin/python3` (macOS system
Python) under `launchd` — which is too old for `dict | None` annotations. The service
crash-looped with a `TypeError` that never appeared during manual testing.

**Pin the interpreter, and verify its version at startup.** Law 1 again: the environment that
runs your code is not the environment you tested in.

---

## Reusable checklist

- [ ] `do_OPTIONS` returning 204 with `Access-Control-Allow-Origin`, `-Methods`, `-Headers`
- [ ] `do_HEAD` delegating to GET with the body suppressed
- [ ] `Access-Control-Allow-Origin` on **every** response, including error paths
- [ ] Request body drained before any early-return error on a keep-alive connection
- [ ] `GET` on the MCP endpoint returns **405** with `Allow: POST`
- [ ] `/authorize` + `/token` supporting Authorization Code with PKCE (S256 and plain)
- [ ] `client_credentials` retained for scripts and tests
- [ ] `/.well-known/oauth-protected-resource` — RFC 9728 shape only
- [ ] `/.well-known/oauth-authorization-server` — RFC 8414 shape only
- [ ] `WWW-Authenticate` on 401 pointing at the protected-resource document
- [ ] Absolute interpreter path in the service wrapper, version-checked at boot
- [ ] Secrets in a `chmod 600` env file, **never** in a `launchd` plist (world-readable)
- [ ] Named tunnel, not a quick tunnel, before anything is made persistent

---

## Anti-Patterns

- **Auto-restarting a quick tunnel.** It returns with a new hostname, so the client silently loses the endpoint on every reboot. This is worse than not restarting at all, because it fails quietly. Get the stable hostname *first*, then add persistence.
- **Putting the bearer token in the plist.** LaunchAgent plists are world-readable by default. A token that grants access to your machine's tooling does not belong in one.
- **Exposing a generic command tool.** The value of an MCP bridge is a fixed allowlist of named operations. One `run_command(cmd)` tool converts an autonomous agent's stray prompt into arbitrary code execution on your machine.
- **Trusting the connection because the vendor UI says "synced".** Sync means the tool list was fetched. It does not mean a tool call succeeds, or that auth holds under expiry.
- **Chasing the next hypothesis before reading the log.** Every guess costs a round trip and adds a change you now have to reason about.

---

## Provenance

Derived from a live integration of a stdlib-only Python MCP server with Gemini Spark's
custom connected apps, 2026-08-16, ending in a working named-tunnel deployment managed by
`launchd`. Every law corresponds to a failure that actually blocked the connection and was
fixed before the next became visible.

Two things worth recording honestly, because they cost the most time:

- **Two fixes were correct and changed nothing observable.** The 404 → 405 change and the
  keep-alive drain were both real bugs, and the client's error message was identical after
  each. It is tempting to revert a fix that "didn't work"; both were load-bearing once CORS
  landed. An unchanged symptom is not a failed fix.
- **A full round was spent debugging a server that was never running.** The launch shell did
  not carry the required env var, the process refused to start by design, and the client
  reported the same "could not be reached" it reports for a protocol mismatch. Reading the
  log first would have caught it immediately — which is why it is step 1 above and not step 6.
