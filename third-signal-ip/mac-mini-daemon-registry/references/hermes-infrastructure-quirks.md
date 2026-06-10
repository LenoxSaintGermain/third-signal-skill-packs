# Hermes Infrastructure Quirks & Setup Patterns

When migrating, rebuilding, or extending the Sovereign Bridge infrastructure, use these exact patterns to avoid known setup pitfalls.

## Bitwarden Secrets Manager (BWS)
Hermes can dynamically fetch API keys from BWS instead of using plaintext `.env` files.
- **Installation Pitfall:** Do NOT attempt to install via `brew install bws` (formula does not exist/conflicts) or `npm install -g @bitwarden/bws` (registry error).
- **Correct Installation:** `curl -sL https://bws.bitwarden.com/install | sh`
- **Hermes Configuration:**
  ```bash
  hermes config set secrets_manager.provider bws
  hermes config set secrets_manager.enabled true
  ```
- **Token Injection:** Do NOT use `hermes config set bws.access_token` (this throws an invalid environment variable name error due to Hermes config mapping). You must manually append `export BWS_ACCESS_TOKEN="<your_machine_token>"` to the profile's `.env` file (e.g., `~/.hermes/profiles/donna/.env`).

## Hermes OAuth Proxy
The `hermes proxy` daemon allows local tools (like Cursor or other agents) to route OpenAI-compatible requests through flat-rate consumer web subscriptions (like X Premium / Grok) without paying per-token API costs.
- **Authentication Pitfall:** The proxy requires a live OAuth web session cookie, not a standard developer API key. Running `hermes auth add xai` captures a standard API key, which causes the proxy to crash with "Not logged into xAI Grok OAuth".
- **Correct Authentication:** You MUST explicitly specify the OAuth provider and type to trigger the browser flow:
  ```bash
  hermes auth add xai-oauth --type oauth
  ```
- **Daemon Execution:** Once authenticated, the proxy must explicitly target the provider: `/path/to/hermes proxy start --provider xai`