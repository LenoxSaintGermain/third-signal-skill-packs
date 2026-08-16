# MCP for Gemini Connected Apps

**Status**: 🟢 PRODUCTION
**Version**: 1.0.0
**Category**: Agent Integration

---

## Overview

You write an MCP server. `curl` proves it works: initialize returns, tools list, tools call,
auth rejects correctly. You paste the URL into Gemini's **custom connected app** dialog and
get four words back:

> *The MCP server could not be reached.*

**The server is fine. `curl` is the wrong instrument.**

**The Problem**: Gemini's connector is a **browser client**, not a server-to-server caller.
Four of the five bugs that block it are invisible to `curl` by construction — CORS preflight,
`HEAD`, keep-alive body desync, and OAuth grant type are all things `curl` either doesn't
exercise or tolerates silently. Every one of them surfaces as the same generic "could not be
reached," with no distinction between *unreachable*, *unauthenticated*, and *protocol
mismatch*.

**The Solution**: stop debugging reachability and start debugging **browser semantics**. The
checklist below is the complete set of five failures, in the order they surface, each of
which fully masks the next.

> Companion to [`inference-spend-forensics`](../inference-spend-forensics). That pack is about
> cost with no feedback signal; this one is about *integration* with no feedback signal — one
> opaque error standing in for five distinct root causes.

---

## The Five Laws

| # | Law | The instinct it corrects |
|---|-----|--------------------------|
| **1** | **`curl` success proves nothing about a browser client** — it skips preflight, sends no `Origin`, and reuses connections differently | "It works from the terminal, so the server is fine." The connector runs in a browser. Test what the browser does. |
| **2** | **404 on the MCP endpoint reads as "no server"** — a GET-less server must answer `405` with `Allow: POST` | "GET isn't part of my protocol, so 404 is honest." To a client probing reachability, 404 *is* the answer "nothing here." |
| **3** | **An early return on keep-alive must drain the request body** — unread bytes corrupt the *next* request on that socket | "I rejected it, so I'm done." The leftover body desyncs the connection; a valid follow-up call arrives mangled and fails for reasons unrelated to itself. |
| **4** | **`client_credentials` is not what an interactive connector speaks** — a redirect URI in the setup dialog means Authorization Code + PKCE | "It's machine-to-machine, so machine-to-machine auth fits." The dialog showing a redirect URI is the tell. Advertise the wrong grant and you are rejected as unsupported, not misconfigured. |
| **5** | **The two discovery documents are different documents** — RFC 9728 and RFC 8414 are not interchangeable | "Discovery is discovery; serve the same JSON at both." A spec-strict client cannot resolve *where* to authenticate from an authorization-server payload served at the protected-resource URL. |

---

## The discriminating test

Before touching server code, ask:

> **Does this client run in a browser?** If yes, `curl` is not a proxy for it and never was.
> Preflight, `Origin`, `HEAD`, and redirect flows are all in play.
>
> **Does the error distinguish between unreachable, unauthorized, and unsupported?** If it
> says only "could not be reached," treat that string as *no information* and instrument the
> server instead of theorising.

The single highest-value move in this entire pack: **log every request the server receives.**
Method, path, status. Five minutes of that beats an hour of hypotheses, because it converts
one opaque client-side string into the exact sequence of probes the client actually made.

---

## The checklist

| # | do this | because |
|---|---|---|
| 1 | Implement `do_OPTIONS` → `204` + `Access-Control-Allow-Origin/Headers/Methods` | preflight failure is silent and total |
| 2 | Implement `do_HEAD` (delegate to GET, suppress body) | default handlers return `501`, which reads as broken |
| 3 | Put `Access-Control-Allow-Origin` on **every** response path, errors included | a CORS-less 401 is unreadable to the browser, so auth can never start |
| 4 | Return `405` + `Allow: POST` on GET of the MCP endpoint | `404` means "no server here" |
| 5 | Drain the request body before any early-return error on HTTP/1.1 | otherwise the *next* request on that socket is corrupted |
| 6 | Support Authorization Code + PKCE (`S256` and `plain`) at `/authorize` and `/token` | interactive connectors require 3-legged OAuth |
| 7 | Serve `/.well-known/oauth-protected-resource` as **`resource` + `authorization_servers`** only | RFC 9728 — it points *at* the AS, it is not the AS |
| 8 | Serve `/.well-known/oauth-authorization-server` with `authorization_endpoint`, `token_endpoint`, grants, PKCE methods | RFC 8414 — this is the AS metadata |
| 9 | Keep `client_credentials` alongside the code grant | scripts and `curl` still need a non-interactive path |

**On `/authorize` without a login system.** A single-operator bridge has no users to
authenticate, so auto-approving any request whose `client_id` matches is defensible — but be
explicit that you are doing it, and know what it means: whoever holds the client ID is
presumed to be the operator. That is the same trust boundary the tunnel URL already rests on.
Do not carry this pattern into anything multi-tenant.

---

## Security, stated plainly

This class of integration ends with **a public HTTPS endpoint that can act on your machine**.
That is the actual deliverable, and it deserves to be named:

- **Expose named operations, never a generic command runner.** A tool taking a shell string —
  or a prompt forwarded to an agent that has shell — is remote code execution wearing a
  friendlier name. The allowlist *is* the security model.
- **A quick tunnel has no auth of its own.** Until the OAuth flow works, the shared secret is
  the only control, and the hostname is guessable by anyone who has seen a screenshot.
- **Gate mutating tools behind explicit confirmation.** An autonomous caller should be able to
  *propose* a state change and not to *make* one in the same turn.
- **Write a receipt for every invocation.** A remote control with no audit trail is a remote
  control you cannot reason about after the fact.

---

## Anti-Patterns

- **Debugging reachability when the client said "unreachable."** That string covers CORS, auth, protocol version, and genuine network failure. It is a category, not a diagnosis.
- **Adding an endpoint per hypothesis.** Two of the five bugs here were found by guessing and would have been found in one pass by logging.
- **Serving one discovery document at both well-known URLs.** They have different required fields and different jobs.
- **Assuming a spec you have not re-read.** MCP's transport and auth story has moved repeatedly; an implementation written from memory will be subtly wrong in exactly the places a strict client checks.
- **Leaving the tunnel up while auth is broken.** A machine-controlling endpoint on the open internet with a half-finished auth path is the worst moment to walk away from the terminal.

---

## Provenance

Derived from a live integration of a stdlib-only Python MCP server (`hermes_bridge.py`) with
Gemini's custom connected app, 2026-08-16. Five distinct bugs, each fully masking the next,
all presenting as the same four-word error. Verified end to end with `curl` at every step —
including a simulated browser OAuth redirect and PKCE exchange — before confirming in the
live client.

Two of the five were found by guessing, and the guessing was the slow part. The 404→405 fix
was real and necessary and did not resolve the symptom, which is precisely the trap: a true
fix that changes nothing observable reads as a dead end and tempts you to revert it. Only
logging the actual request sequence turned the remaining three from hypotheses into facts.
