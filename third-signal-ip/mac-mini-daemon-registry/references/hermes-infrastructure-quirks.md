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

## Bitwarden Secrets Manager (BWS) CLI Bulk Upload & Profile Sync
When transitioning multiple local `.env` keys to Bitwarden Secrets Manager (BWS) on the Mac Mini, use the BWS CLI to populate the vault in one shot.
- **Bulk Creation Command:**
  ```bash
  bws secret create <KEY> <VALUE> <PROJECT_ID>
  ```
  *Note:* BWS does not allow empty or blank secret values; skip any empty local `.env` lines (e.g. `ANTHROPIC_API_KEY=""`) during bulk uploads.
- **Multi-Profile Sync Pitfall:** Enabling BWS (`secrets.bitwarden.enabled: true` in `config.yaml`) causes Hermes to run `bws secret list` at startup. If `BWS_ACCESS_TOKEN` is only set in the `donna` profile `.env` and missing from other profiles (like `librarian` or `omi-dev`), those profiles will crash on startup with a missing credential error.
- **The Sync Solution:** Ensure `BWS_ACCESS_TOKEN` is propagated from the local `donna` profile's `.env` to the master `~/.hermes/.env` and all active profile `.env` files.

## OpenAI Codex Transport Hardcoded Rule & Local Proxy Bypass
On Hermes, if a custom or standard provider's `base_url` contains `"api.openai.com"`, the routing framework automatically forces the `codex_responses` transport (which uses the beta Responses API).
- **The Pitfall:** Standard public OpenAI developer keys do not support this transport, throwing: `400: Encrypted content is not supported with this model (param: include)`.
- **The Bypass:** Set up a lightweight, threaded local Python reverse proxy on port `9230` to forward requests to `api.openai.com`. Because the local URL `http://127.0.0.1:9230/v1` does not contain `api.openai.com`, Hermes falls back to standard, clean `chat_completions` transport!
- **The Proxy Rewrite Pattern:** The proxy must parse incoming POST requests to `/v1/chat/completions`, and if `"max_tokens"` or `"max_completion_tokens"` is larger than `16384` (OpenAI's output completion ceiling for models like `gpt-4o`), it must dynamically rewrite the parameter to `16384` to prevent `400: max_tokens is too large` errors.
- **Streaming Note:** Ensure `streaming: false` is set in the profile's `config.yaml` when using a simple non-async proxy to prevent HTTP socket hangs during SSE streaming.