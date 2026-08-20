---
name: custom-domain-operations
description: Diagnose, configure, repair, and verify custom domains across DNS providers and hosted platforms. Use whenever an agent adds or changes a custom hostname, moves DNS to Cloudflare, configures CNAME/A/AAAA/TXT records, connects a hosted site, changelog, API, or MCP endpoint, repairs NXDOMAIN or certificate failures, or verifies DNS propagation and HTTPS. Preserve unrelated DNS records and keep application and tunnel hostnames separate.
---

# Custom Domain Operations

Use this skill for any custom-domain task involving DNS, hosted-platform verification, TLS, a CDN, a reverse proxy, or a tunnel. Make the smallest safe change, then prove the hostname works from the public internet.

## Operating rules

- Treat the hosting platform's custom-domain settings as the source of truth for the destination record. Never guess a target from a similar hostname.
- Determine whether the requested name is an apex (`example.com`) or a subdomain (`app.example.com`). CNAME is common for subdomains; apex records require the DNS provider's ALIAS/ANAME/flattening or documented A/AAAA approach.
- Read before writing: inspect authoritative nameservers, the current record, the hosting-platform status, and the current HTTP/TLS response.
- Preserve unrelated A, AAAA, MX, TXT, CAA, and tunnel records. Do not replace a zone, nameserver delegation, or record set wholesale without explicit approval.
- Keep unrelated applications and tunnels on separate hostnames. A hosted changelog/site hostname must not be routed to an MCP tunnel merely because both use the same domain.
- If the task is diagnosis only, do not mutate DNS. If the user requests a fix and the exact target is known, repair only the missing or incorrect record.

## Standard workflow

### 1. Define the desired mapping

Record the exact hostname, whether it is apex or subdomain, the intended platform, and the platform-provided target. Also note whether the platform requires DNS-only, proxied DNS, TXT verification, or a CAA/TLS change.

### 2. Inspect current DNS and the service

Use read-only checks first:

```bash
dig +short example.com NS
dig +short app.example.com CNAME
dig +short app.example.com A
dig +short app.example.com AAAA
dig +short app.example.com TXT
curl -sSIL --max-time 15 https://app.example.com/
```

Query a public resolver when local caching could mislead:

```bash
dig @1.1.1.1 +short app.example.com CNAME
dig @8.8.8.8 +short app.example.com CNAME
```

Interpret `NXDOMAIN` as a missing name/delegation problem, not as proof that the hosted platform is unhealthy. A resolved name with a 4xx/5xx or TLS error is a different layer.

### 3. Apply the smallest provider-specific change

- Subdomain to an external hosted service: add or correct the platform-provided CNAME.
- Apex to an external hosted service: use the platform's documented ALIAS/ANAME/flattening or exact A/AAAA records; do not invent an IP for a service that publishes a hostname.
- Verification flow: add the exact TXT record and value requested by the platform, leaving existing TXT records intact.
- Nameserver migration: confirm the intended DNS provider is authoritative before editing records. Recreate only the records required for the active zone and protect mail records.

### 4. Verify every layer

Confirm the public record matches the intended target, then check HTTPS:

```bash
dig @1.1.1.1 +short app.example.com CNAME
curl -sSIL --max-time 15 https://app.example.com/
```

If DNS resolves but the service fails, use the hosting platform's custom-domain status and, when the platform supplies a test address, compare it with the custom hostname. Use `curl --resolve` only with a known-good IP to isolate DNS from origin/TLS behavior; do not use it as a substitute for fixing DNS. Allow for TTL and certificate provisioning delays, and report whether the remaining issue is propagation or platform activation.

## Cloudflare guidance

- Confirm the domain is in the correct Cloudflare zone and that the public authoritative nameservers are the Cloudflare nameservers shown for that zone.
- For a subdomain hosted by an external platform, create a CNAME using the exact target from that platform. Use the label (`app`) in the Name field when editing the zone for `example.com`.
- Start with DNS-only (gray cloud) for third-party custom domains unless the platform explicitly supports Cloudflare proxying. Proxying can hide the CNAME, change TLS/origin behavior, and require a valid origin certificate.
- Do not use `cloudflared tunnel route dns` for a hosted site or changelog. That command deliberately routes the hostname to a selected Cloudflare Tunnel; use it only when that hostname is intended to terminate at that tunnel.
- Keep MCP/tunnel hostnames, such as `hermes-bridge.example.com`, separate from hosted-site hostnames, such as `changelog.example.com`.
- Do not change SSL/TLS mode as a first response to missing DNS. For proxied traffic, use the platform's documented origin-certificate setup and prefer Full (strict) when the origin supports it; for DNS-only traffic, the hosted platform normally provisions the public certificate.

## Common failure patterns

- **NXDOMAIN after adding Cloudflare:** the new Cloudflare zone is authoritative, but the old DNS record was never recreated. Add the missing record in the authoritative Cloudflare zone.
- **CNAME points to the wrong product:** copy the target from the hosting platform's custom-domain settings. A tunnel target, preview URL, or old provider target can produce a valid DNS response but the wrong application.
- **Cloudflare 52x or certificate error after orange-clouding:** switch to DNS-only while validating the third-party platform, then follow that platform's proxy/origin requirements before re-enabling proxying.
- **Mail breaks during DNS cleanup:** MX/TXT/SPF/DKIM/DMARC records were removed or replaced. Restore the exact mail records and avoid zone-wide replacement.
- **DNS is correct but platform still says pending:** verify the public record from more than one resolver, then wait for the platform's verification/certificate workflow rather than repeatedly changing DNS.

## Completion report

State the exact hostname, record type, target/value, Cloudflare proxy status if applicable, and verification evidence. Report both DNS and HTTPS results, identify any remaining platform activation or propagation delay, and list unrelated records intentionally left unchanged.
