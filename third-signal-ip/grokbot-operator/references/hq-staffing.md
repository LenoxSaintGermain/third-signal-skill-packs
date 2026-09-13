# Initial Agentic HQ staff

Start with proposal-first roles whose work is reversible and independently verifiable.

| Role | Mission | Preferred first adapter | Public mutation posture |
|---|---|---|---|
| Public Surface Steward | Audit site health and prepare code/content change proposals | GrokBot or Hermes | Approval required |
| Librarian & Documentation Editor | Turn verified artifacts into sourced documentation and article proposals | Hermes or GrokBot | Approval required |
| Demo Catalog Curator | Reconcile repos, manifests, screenshots, URLs, and proof status | Hermes or Codex | Approval required |
| Signal Scout | Cultural and market intelligence | GrokBot | Read-only |
| Campaign Experiment Analyst | Form hypotheses and synthesize performance | GrokBot | Draft-only |
| Community Analyst | Cluster questions and draft responses | GrokBot | Approval required to send |
| Release Captain | Verify builds, previews, rollback paths, and deployment receipts | Codex or Hermes | Separate deploy approval |
| Operations Auditor | Find missing receipts, stale skills, stalled tasks, and runtime drift | Hermes | Read-only |

Do not initially assign autonomous authority for:

- canon or rights approval;
- public messaging or publication;
- production deployment;
- financial commitments;
- credential or permission changes;
- destructive actions.

## Public Surface Steward lanes

Code/configuration:

```text
audit -> change proposal -> branch/PR -> preview -> automated QA
      -> operator approval -> deploy adapter -> verified deployment receipt
```

Editorial/documentation:

```text
source artifact -> sourced draft -> claim ledger -> public-safe review
                -> staged release -> operator approval -> permalink receipt
```

The first UAT should run Site Steward, Librarian, Catalog Curator, and Operations Auditor in shadow mode using both GrokBot and Hermes on representative tasks. Compare artifacts and receipt compliance before making either adapter active.
