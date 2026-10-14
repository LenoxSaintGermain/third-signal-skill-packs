# Signal Publishing pipeline profile

This profile is the routing layer shared by the publishing skills. Read it after [SKILL.md](../SKILL.md) whenever work moves from lore or editorial intent toward a graphic-novel artifact, story pack, runtime package, or publication record.

## Automatic entry rule

Before creating or extending creative content, select a recipe. Do not wait for the user to name the recipe.

If the task includes any of these signals, invoke the engine:

- extend lore, develop a new IP, build a chapter, create a spread, create panels, make a story pack, write a visual brief, or generate a production handoff;
- graphic novel, comic, manga, panel, page, spread, splash, gutter, lettering, storyboard, or reader harness;
- witchcraft, magic, power, ritual, curse, technology, faction doctrine, or another system that needs rules and consequences;
- continuity, canon, approved art, asset provenance, runtime direction, or publication sync.

## Routing matrix

| Work surface | Primary recipe | Secondary recipe(s) | Required decision |
|---|---|---|---|
| New lore or IP extension | Situation-Forced Design | Constraint-Bearing System when rules are central | What situation makes the new lore unavoidable? |
| Graphic-novel chapter or panel spread | Sequential Reveal | Situation-Forced Design; Constraint-Bearing System when the system is dramatized | What changes across the page turn and what does each panel reveal? |
| Witches IP → chapter-one panel spreads | Sequential Reveal | Situation-Forced Design; Constraint-Bearing System only if witchcraft rules are being introduced/tested | What does the reader learn by watching the witchcraft operate under a cost or constraint? |
| WIND visual-development spread | Situation-Forced Design | Sequential Reveal for a sequence; Constraint-Bearing System for powers/institutions | What is the hero moment and what canon can be extracted from it? |
| Story pack / art-production plan | Sequential Reveal | Evidence Ledger | What is the panel/page geometry, text policy, and reveal order? |
| Signal Stage ingestion/runtime direction | Evidence Ledger | Sequential Reveal | What approved evidence can be directed without altering the source pixels? |
| Archive, sync, Drive, or release handoff | Evidence Ledger | Signal Adaptation when translating across surfaces | What is confirmed, approved, available, superseded, or still missing? |

The matrix is a default, not a substitute for diagnosis. If the task's actual job differs, record why another recipe won.

## Required recipe handoff

Every creative handoff should carry this compact block, even when it is embedded in a larger manifest:

```yaml
recipe:
  primary: sequential-reveal
  secondary:
    - situation-forced-design
    - constraint-bearing-system
  narrative_job: "What the audience should understand or feel afterward"
  controlled_mutation: "The one structural choice making this version distinct"
  source_boundary: "Canon, research, or approved asset boundary"
  output_contract: "Pages, panels, spread brief, story pack, runtime spec, or release record"
  validation: "The observable tests that must pass"
  canon_changes: "confirmed | proposed | inferred | reserved | none"
  unresolved: []
```

## Witches chapter-one profile

This is a production profile, not canon. It applies when the witches IP is being extended into the MVP graphic-novel harness.

1. Read the witches source dossier, prior chapter material, visual rules, and any approved assets. If no durable dossier exists, create a source-bound proposal and mark the lore as proposed.
2. Select **Sequential Reveal** as the primary recipe. The output is a page/spread sequence, not a lore encyclopedia.
3. Use **Situation-Forced Design** to make the witch, coven, ritual, institution, or threat reveal itself through an event.
4. Add **Constraint-Bearing System** only for rules that the chapter must teach through use, cost, access, failure, or consequence.
5. Build the chapter spine before panel copy: page promise → panel jobs → gutter inference → page-turn pressure → changed state.
6. Record every new lore decision beside the panel or spread that demonstrates it. Separate confirmed canon from proposed extensions.
7. Hand off only after panel geometry, lettering/text ownership, character continuity, system continuity, and the next chapter question are explicit.

The profile must not invent witches canon merely because a panel needs a detail. A missing detail becomes a proposal or a reserved question.
