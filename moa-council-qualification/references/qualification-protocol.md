# The Qualification Protocol

A runbook for proving a multi-model roster before it ships. Seven steps, in order. Each
step exists because skipping it produces a specific, silent defect — named below.

The ordering is not cosmetic. Governance filters the candidate set, availability filters it
again, and only then does ranking mean anything. Ranking first and filtering later is how
teams end up with a roster they cannot legally or technically run.

---

## Step 0 — Fix the constraint set before looking at any score

Write down, before opening a leaderboard:

- Which data classes this council may see (restricted / internal / public)
- Which vendors, hosting jurisdictions, or endpoints your governance restricts, and to which data classes
- The budget envelope per escalation, and who is billed

**Why this is first**: capability ranking is meaningless over a candidate set you are not
permitted to use. If policy restricts a class of models to public data only, that is a
**gate**, not a tiebreaker — no benchmark margin overrides it.

**Catches**: a roster that is technically excellent and quietly non-compliant. This defect
survives every functional test, because nothing in the output reveals where the data went.

**Output**: an allowed-candidate set per data class. Most stacks need at least two rosters —
one that may see internal context, one for public work that can use a wider field.

---

## Step 1 — Probe the real catalog

Query the API's own model listing, then **call the models you intend to use**. Do not trust
the listing alone, and do not trust the vendor's chat app.

```bash
# 1. what the API claims to serve
curl -s https://<api-host>/v1/models -H "Authorization: Bearer $KEY" \
  | python3 -c "import json,sys; print(sorted(m['id'] for m in json.load(sys.stdin)['data']))"

# 2. what it actually answers — probe each intended id
curl -s -o /tmp/r.json -w '%{http_code}\n' https://<api-host>/v1/chat/completions \
  -H "Authorization: Bearer $KEY" -H 'Content-Type: application/json' \
  -d '{"model":"<id>","messages":[{"role":"user","content":"Reply with exactly: OK"}],"max_tokens":2000}'
```

**Why this matters**: a vendor's consumer subscription app and its developer API are
different products with different rosters and different billing. The flagship model
featured on the storefront can return `not_found` on the endpoint your key bills against.
Always probe a known-good id in the same run as a control — if the control 200s and the
candidate 404s, the gap is the roster, not your credentials.

**Catches**: a config naming models that cannot be called. Fails at the worst moment —
first real escalation — and looks like an auth or network fault, not a roster error.

---

## Step 2 — Rank per seat, not per roster

Split candidates by the seat they are being considered for, and rank each seat on the axes
that seat actually exercises. See the role table in the pack README.

For the **advisor** set, optimise the *set*, not each member: three strong models from one
family are worth less than three merely-good models from three lineages, because MoA's
entire value is decorrelated error.

For the **aggregator**, remember it does two jobs — synthesis *and* driving the tool loop.
An aggregator with excellent language scores and weak agentic scores will write beautifully
and execute badly.

**Catches**: the weak-synthesizer inversion, and the correlated-council illusion — paying
N× for one perspective.

---

## Step 3 — Measure token behaviour before setting any cap

For every candidate, run one representative prompt at a generous cap and record the split
between reasoning and visible tokens.

> ⚠️ **Calibrate under representative context, not a bare prompt.** This is the single
> easiest way to get Step 3 wrong, and it has burned this protocol's own authors. Advisors
> given ~40 input tokens of prompt wrote 190–460 tokens; the same advisors, on a real turn
> carrying ~92k–138k tokens of live conversation, wrote past a 1500 cap and truncated
> mid-sentence. **Models write longer when given more to respond to.** A cap calibrated on
> a toy prompt is not a cap, it is a delayed truncation bug. Measure on a prompt carrying
> realistic context, or measure from a real turn's trace and correct afterwards.

```bash
# inspect usage, not just the text
... | python3 -c "
import json,sys
d=json.load(sys.stdin); u=d['usage']; det=u.get('completion_tokens_details') or {}
print('finish', d['choices'][0].get('finish_reason'),
      '| completion', u.get('completion_tokens'),
      '| reasoning', det.get('reasoning_tokens'),
      '| visible chars', len(d['choices'][0]['message']['content']))"
```

Set the cap from the **worst** measured candidate, with explicit headroom, and record the
measurements as a comment beside the value.

**Why this matters**: caps named for output routinely include reasoning tokens. A reasoning
model can consume the entire budget thinking and emit a fragment. Two further traps:

- **"Flash"/"mini"/"lite" naming does not imply low reasoning spend.** Measure it; small-tier models sometimes reason *harder* than the large-tier model they replaced.
- **Some models leak raw chain-of-thought into visible content** instead of reporting `reasoning_tokens`. An aggregator then receives transcribed thinking rather than advice. Disqualify these for advisor seats — the defect is in output hygiene, not intelligence.

**Catches**: silent mid-advice truncation. Nothing errors; the advisor simply contributes
less than you think, forever.

---

## Step 4 — Prove resolution end-to-end

Resolve every seat through the *runtime's own* credential chain, not by calling the vendor
directly. A model that answers `curl` can still fail in-agent if the provider slug,
credential source, or API mode is misconfigured.

Assert on: endpoint, auth mode, credential **source**, and key presence. Never print key
values — assert `SET`/`MISSING` and length.

**Why this matters**: this is where multi-provider rosters break. A roster spanning a
broker and a first-party key exercises two different credential paths, and only one of them
is the one you tested by hand.

**Catches**: an aggregator that silently falls back to a default provider, or a slot that
resolves against the wrong profile — the classic symptom is a config edit that "does
nothing" because the process loaded a different config file than the one you edited.

---

## Step 5 — Price the turn, not the token

Convert measured token counts and published rates into **cost per escalation**, then into
runway against current balance.

```
turn_cost = Σ_advisors (ctx_tokens × in_rate + measured_out × out_rate) + aggregator_cost
```

**`ctx_tokens` must come from a real trace, never an estimate.** Every advisor receives the
full conversation, so context — not output — sets the bill. A production measurement:
327,429 input tokens against 2,518 output tokens across three advisors, a **130:1 ratio**.
An estimate that assumed a few thousand tokens of context under-predicted the true cost by
more than an order of magnitude.

Consequences worth internalising:

- **Output caps are not a cost control.** At 130:1, doubling every advisor's output cap moves the bill by under 1%.
- **The real levers are advisor count, input rate, and cache hits.** Dropping one advisor from three cuts ~33%. The seat with the highest *input* rate dominates — in that measurement one advisor was 60% of spend on input alone.
- **Long-lived sessions get expensive quietly.** Council cost scales with accumulated conversation length, so the same question costs more in week six than week one.
- **A first turn is a cold cache.** Judge steady-state cost from a second turn inside the cache window, not the first.

Report which single seat dominates spend. There is usually one, and it is usually the seat
someone added for prestige.

**Why this matters**: unit price and cost-per-finished-task diverge sharply. Two models
billing at an identical rate can differ 2× per task because one is benchmarked at a higher
effort setting and emits far more tokens. A published cost-per-task figure bundles rate,
verbosity, effort, and success rate — useful for comparison, useless for forecasting *your*
bill.

**Catches**: budget surprise, and prestige seats nobody can justify once their share of the
bill is visible.

---

## Step 6 — Encode the decision where it is enforced

Write the reasoning into the config beside the value it explains — measured numbers, the
date, and why the rejected candidate was rejected. Then update the agent's own operating
instructions so it knows the roster's constraints at runtime.

**Why this matters**: a roster is a set of decisions with expiry dates. Six weeks later,
"why is this cap 1500?" has no answer unless the measurement is recorded next to it, and
the most likely edit — rounding it down to a tidier number — reintroduces the truncation
bug the number was chosen to prevent.

**Catches**: silent regression by well-meaning cleanup.

---

## Re-qualification triggers

Re-run the protocol when any of these occur:

- The vendor announces a model you intend to use → **Step 1** (announcement ≠ API availability)
- You change an effort or reasoning setting → **Step 3** (caps are effort-dependent)
- You add a provider or rotate a credential → **Step 4**
- Published rates change → **Step 5**
- Governance changes → **Step 0**, and the whole protocol after it

Treat a roster as qualified **as of a date**. Record that date.
