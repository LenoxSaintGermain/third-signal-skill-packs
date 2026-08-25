# LaunchAgent contract

The installed host schedule is:

- Label: `com.thirdsignal.mcp-memory-guard`
- Trigger: `RunAtLoad` plus `StartInterval=300`
- Program: `~/.hermes/skills/mcp-memory-guard/scripts/mcp_memory_guard.sh --once`
- Logs: `~/.hermes/runtime/mcp-memory-guard/launchd.out.log` and `.err.log`
- No secrets or network calls

Use `launchctl print gui/$(id -u)/com.thirdsignal.mcp-memory-guard` to inspect
the live job. Use `launchctl bootout gui/$(id -u)/com.thirdsignal.mcp-memory-guard`
followed by `launchctl bootstrap gui/$(id -u) ...plist` to reload it.
