# Bitwarden Secrets Manager (BWS) & Hermes Integration

When configuring Hermes or the Mac Mini Sovereign Bridge to use Bitwarden Secrets Manager instead of plaintext `.env` files:

## 1. Installing `bws` CLI on macOS
Do not use `brew install bws` (formula does not exist) or `npm install -g @bitwarden/sm-cli` (404 errors). 
**Correct Installation:**
```bash
curl -sL https://bws.bitwarden.com/install | sh
export PATH="$PATH:$HOME/.local/bin"
```

## 2. Configuring Hermes
Do **not** attempt to set the token via `hermes config set bws.access_token <token>` (throws `ValueError: Invalid environment variable name`).

**Correct Configuration Flow:**
1. Manually append the token to the profile's `.env` file:
   `echo 'export BWS_ACCESS_TOKEN="<token>"' >> ~/.hermes/profiles/<profile>/.env`
2. Enable the provider in the Hermes config:
   `hermes config set secrets_manager.provider bws`
   `hermes config set secrets_manager.enabled true`