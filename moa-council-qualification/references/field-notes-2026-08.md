# Field Notes — Qualification Run, 2026-08-05

A worked example of the protocol against a live operator-agent council on the Hermes stack.
Recorded because the *sequence of wrong turns* teaches more than the final roster does.

**Everything dated here ages.** The laws in the pack README do not. Model ids, scores, and
rates below were true on 2026-08-05 and should be re-probed, never copied.

---

## What triggered the exercise

An operator agent proposed building a "dynamic MoA router": score task complexity 1–10,
answer directly below 7, and above 7 fan out to several models via the delegation tool,
consolidate to JSON, then synthesize as the master model.

The instinct — spend more only when the task earns it — was right. Every mechanical claim
in the design was wrong, and the design also duplicated two skills the agent already had.
That gap between a good instinct and an unbuildable plan is what qualification exists to
close.

---

## Defects caught, in the order the protocol catches them

### Law 4 — the fan-out primitive was homogeneous

The proposed council routed through a delegation tool assumed to accept a per-child model.
Reading the implementation: it resolves **one** credential bundle and passes the same
provider/model to every child in the batch; the model-facing schema has no per-task model
field. With the delegation config unset, children inherit the parent.

The proposed "board of advisors" would have been **five copies of one small model agreeing
with each other** — at 5× the cost, with the appearance of consensus.

> This is the defect with the worst signal-to-noise: it produces confident, agreeing output.
> Nothing looks wrong.

### Law 1 — the storefront roster was not the API roster

The broker's subscription app listed four frontier models as official bots. Direct probes
against the developer API returned `not_found` for all of them, while a control id from the
API's own listing returned `200` on the same key in the same run.

Two different products, one brand. The council bills against the API, so the app's roster
was decoration. **The control probe is what makes this conclusive** — without it, four
`404`s read as a credential problem.

### Law 2 — the token cap counted reasoning

An initial advisor cap of 600 was set from a hint in the runtime's own source comments.
Measurement on one concise three-point advisory prompt:

| candidate | total completion | reasoning | verdict at 600 cap |
|---|---|---|---|
| general frontier A | 191 | 0 | fine |
| general frontier B | 253 | 67 | fine |
| small-tier "flash" model | 1116 | 835 | **truncated** |
| open reasoning model | 1585 | 1296 | **truncated** |

Two of four advisors would have been cut off mid-advice on every turn, permanently, with no
error surfaced. Note the small-tier "flash" model reasoned *harder* than the large-tier
model it had just replaced — tier naming predicted nothing.

### Law 3 — newer regressed, twice in one session

- Opus-class **4.7 scored above 4.8** on overall benchmark, and 4.8 was slotted only because it was newer.
- A **3.5-generation flash model beat the 3.6-generation** replacement on 7 of 8 axes at statistically identical measured latency (3.0s vs 3.2s), including a +5.6 margin on agentic coding — the axis that matters most for an agent living in tool loops.

Both "upgrades" were downgrades. Neither would have been caught without per-axis comparison.

### Law 5 — unit price and cost-per-task diverged

The two Opus-class candidates were initially described as differing 2× in cost, based on a
published cost-per-successful-task figure. Pulling the broker's own per-token rates: the two
models bill **identically** (same input rate, same output rate). The entire published gap
was the newer model being benchmarked at a higher effort setting and emitting more tokens.

The score advantage still favoured 4.7 — but "half the cost" was wrong, and would have been
repeated to stakeholders as fact.

### Law 6 — one roster could not serve both data classes

The strongest-value candidates were restricted by existing governance to public data only.
That constraint binds before any score, and it forced the correct structure: **two rosters**
— one whose members may see internal context, one wider roster for public work — rather than
one roster and a promise to be careful.

### Bonus — output hygiene disqualifies on non-capability grounds

One high-scoring candidate returned its raw chain-of-thought inside the visible content
field (`"Thinking... > We are asked:"`) with `reasoning_tokens: null`. An aggregator would
have received ~2.6k characters of transcribed thinking instead of advice. Disqualified for
advisor duty despite competitive benchmarks — a formatting contract failure, not an
intelligence one.

---

## Process traps worth naming

**The wrong config file.** The first pass edited the *global* config while the agent ran
from a *profile* config — 7KB vs 18KB, same filename. Every conclusion drawn from it about
"what is configured" was void. Verify which file the running process actually loads.

**The environment-fallback lie.** A resolution probe failed with "unknown provider" purely
because a home-directory environment variable was unset, so the library silently loaded the
default profile and reported a truthful answer *about the wrong profile*. The warning was
printed and easy to scroll past. Read the warnings on a failing probe before believing the
failure.

**Secrets that are not in the file you grepped.** An early conclusion — "this broker has no
credentials configured" — was flatly wrong. The key was injected at boot from a secrets
manager into a cache, never written to the env file. **A grep over `.env` proves nothing
about what the process has at runtime.** Enumerate the resolved environment, not the file.

That error is the most instructive one here: it was stated confidently, it was checkable,
and it was wrong. The operator pushed back, and the correction surfaced the two existing
skills that made half the original plan redundant. **Qualification is adversarial or it is
theatre.**

---

## Postmortem — what the first live turn broke

The roster above was qualified, validated, and **still shipped with two defects**. Both were
found only by running a real turn and reading its trace. They are recorded here because
they are the strongest argument in this pack: static qualification is necessary and not
sufficient.

**1. The cap was calibrated on a toy prompt.** Advisor caps were set from bench runs on a
bare ~40-token prompt, where the worst advisor wrote 459 tokens. A 1500 cap looked like 3×
headroom. On the first real turn — ~92k–138k input tokens of live conversation per advisor
— one advisor ran straight through 1500 and truncated mid-sentence, in the middle of the
very section the prompt had asked for. The aggregator noticed and flagged it in its own
synthesis, which is the only reason it was visible at all. **Law 2 now says: calibrate
under representative context.**

**2. The cost estimate was ~25× low.** Predicted $0.03–0.05 per turn; actual **$1.18**. The
estimate assumed a few thousand tokens of context per advisor. The trace showed **327,429
input tokens against 2,518 output** — a 130:1 ratio. Every advisor receives the entire
conversation, and this session had been accumulating for weeks. That error produced a
runway forecast wrong by an order of magnitude: ~25 escalations per monthly allowance, not
~630. **Law 7 exists because of this.**

**3. The verifier reported a false PASS.** The purpose-built check printed
`PASS no advisor hit the None-token cap` — it could not read the cap (a missing YAML
dependency in the interpreter it ran under), so the comparison was skipped, and skipping
rendered as passing. The truncation in defect 1 was sitting in the same output, unreported.

That third one is the most damning, because the tool existed *specifically* to catch
defect 1. **A check that cannot run must fail loudly, never silently pass.** The verifier
now prints `UNCHECKED` with the reason and returns non-zero when it cannot read what it is
asserting against. Every assertion tool in this protocol should be audited for the same
failure mode: ask what it prints when its own inputs are missing.

## Final structure

| seat | selection basis |
|---|---|
| advisors (internal-safe roster) | three distinct non-first-party lineages via the broker |
| aggregator (internal-safe) | first-party key, chosen for best instruction-following and language scores on the board |
| advisors (public roster) | widest available field, including governance-restricted lineages |
| aggregator (public) | highest overall + best language of the models the API actually serves |

The division of labour that fell out: **the broker supplies only lineages the first-party
key cannot** — never pay a broker for a model you already hold a direct key for.

The agent's own default model was deliberately left on a *fast* small-tier model rather than
promoted. The quality gradient belongs in the escalation path, not the front door: if the
base model and the aggregator are the same, escalating adds advisors but no better
synthesizer, and the council stops being an upgrade.
