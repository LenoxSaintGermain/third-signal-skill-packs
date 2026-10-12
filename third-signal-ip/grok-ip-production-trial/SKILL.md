---
name: grok-ip-production-trial
description: Run a bounded cross-agent trial of WIND through finished comics and verified reader deployment, with a capability preflight, private source handoff and scored evidence. Use to test Grok or another agent against the Third Signal production workflow.
---

# Grok IP Production Trial

This is an execution test, not proof that Grok supports native skill installation or any particular connector. Read these files as instructions if the host does not implement `$skill-name` invocation.

Read [TRIAL.md](TRIAL.md), then [the runnable prompt](PROMPT.md). Use the adjacent `wind`, `signal-recipe-engine`, `ip-continuation-desk`, `ip-to-production`, `signal-ip-publishing` skills. Add `ip-to-signal-stage` and `signal-stage-library` only for the harness route. `publishing-desk` is optional queue management, not the generator or deployer.

First prove available capabilities: reading the supplied files, inspecting actual images, generating reference-conditioned art, exporting original files, executing code/hashing, browsing the result, and accessing the selected hosting destination. Record each as available, unavailable or unverified with evidence. Never claim the public skill pack grants local filesystem access, Codex tools, authenticated providers or publication authority.

Continue the user's authorized stages. Missing deployment access still permits a complete portable artifact; label that packaged, not published. A runtime restricted to text may complete planning only; that is not an end-to-end pass. Keep a failed capability visible rather than swapping in invented links or placeholder art.
