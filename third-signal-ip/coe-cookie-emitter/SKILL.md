---
description: Deploy, utilize, and maintain the COE (Cookie Object Emitter) telemetry architecture across projects using GCP Secret Manager and Cloud KMS for cryptographically secure payload signing.
---

# COE Cookie Emitter Integration

This skill outlines the necessary steps and best practices for interacting with the COE (Cookie Object Emitter) framework. Orbital OS uses this framework to securely sign and emit telemetry session cookies, leveraging GCP's Key Management Service (KMS) for asymmetric signatures and Secret Manager for privacy-preserving hash peppers.

## Core Capabilities

The COE Emitter provides:
1.  **Deterministic Hashing:** Creates stable `user_hash` values for telemetry by hashing the `user_id` with a high-entropy "pepper" stored in GCP Secret Manager (`coe-user-hash-pepper`).
2.  **Asymmetric Signing:** Signs payloads using a dedicated GCP KMS keyring (`coe-telemetry-keys`) to ensure cookie integrity and non-repudiation.
3.  **Mock Fallback:** A safety mechanism that falls back to a development mock key if the GCP infrastructure or IAM permissions are unavailable, ensuring the frontend does not crash during local development or network partitions.
4.  **Automatic Provisioning:** Infrastructure scripts that automatically create the KMS keyring and Secret Manager secrets if they do not exist.

## File Locations & Resources
- **Core Logic:** `server/lib/coeEmitter.ts` (or equivalent location depending on the codebase structure).
- **Provisioning Script:** `scripts/provision_coe_crypto.sh` (Provisions KMS and Secrets).
- **IAM Hardening:** `scripts/harden_coe_permissions.sh` (Assigns IAM roles to the service account).
- **Verification Script:** `scripts/verify_coe_crypto.ts` (Crucible test for GCP infrastructure resolution).

## How to Provision the Emitter in a New Environment

If deploying the COE Cookie Emitter into a new GCP project or completely rebuilding the environment, you **must** use the automated provisioning scripts:

1.  **Run Provisioning:**
    Execute `scripts/provision_coe_crypto.sh`. This script handles the idempotency of checking if `coe-telemetry-keys` and `coe-user-hash-pepper` exist, and creates them if they don't.
    
2.  **Harden Service Account IAM:**
    Execute `scripts/harden_coe_permissions.sh`. This ensures the active `firebase-adminsdk-fbsvc` service account is bound to `roles/secretmanager.secretAccessor` and `roles/cloudkms.signerVerifier`.

3.  **Verify the Integration:**
    Run `npx ts-node scripts/verify_coe_crypto.ts`. You should expect to see the Pepper successfully retrieved, the hash generated, and the payload successfully signed via KMS. 

## Architectural Rules & Restrictions

- **Never bypass IAM for the KMS Signer:** The application service account *must* be granted `cloudkms.signerVerifier`. Do not export symmetric keys. The application should only have the ability to explicitly sign payloads, never extract the private materials.
- **Client Resolution:** The COE Emitter relies entirely on Google's default credential resolution logic via `@google-cloud/kms` and `@google-cloud/secret-manager`. This is governed by the `getGoogleCloudClientOptions()` utility which maps the standard `GOOGLE_APPLICATION_CREDENTIALS` environment variable first, before trying service account fallback files.
- **Mock Mode is NOT for Production:** The COE framework contains a `_activateMockMode()` logic path. This is exclusively designed for local development resilience. You must ensure the `verify_coe_crypto.ts` script never falls back to mock mode in the deployment pipeline.

## Error Handling best Practices

If a `PERMISSION_DENIED` error is thrown by the GCP API (typically code 403), do not assume the keys are missing. It almost always indicates that the targeted service account lacks the explicit read/sign IAM roles, or the `GOOGLE_APPLICATION_CREDENTIALS` context is pointing to the wrong account block. Use the hardening script to auto-remediate role assignments.
