# Creation-capture contract

This contract is the durable boundary between a generation turn and the Signal Publishing source vault. It applies whenever a creative binary is generated or received and a project destination has been authorized.

## Required action before the turn ends

Run `scripts/capture_at_creation.py` against the original binary returned by the generation tool. The command copies bytes without decoding, resizing, recompression, or renaming, and writes a receipt next to the captured source:

```bash
python3 skills/signal-stage-library/scripts/capture_at_creation.py \
  --source <runtime-output-path> \
  --destination-dir <source-package>/source \
  --asset-dna-id <ASSET_DNA_ID> \
  --conversation-id <conversation-id> \
  --turn-id <turn-id> \
  --tool <generation-tool> \
  --capture-context creation-time \
  --prompt-file <exact-prompt-file-if-exposed> \
  --model <model-if-exposed> \
  --seed <seed-if-exposed>
```

The prompt, model, seed, file ID, generation IDs, and parent IDs are optional because runtimes do not always expose them. Omit unavailable fields; the receipt records `not recorded or exposed` rather than inventing values.

## Success invariant

A generation handoff is not complete until all of these exist and verify:

- the captured path exists;
- the original filename is preserved;
- byte count, MIME type, dimensions, and SHA-256 are recorded;
- the captured checksum matches the source checksum;
- a receipt names the conversation, turn, tool, Asset DNA, approval state, and canon state;
- a rejected or superseded asset has a receipt too.

If capture fails, keep the generation result in a recovery state and do not advance to source approval, Signal Stage production, runtime packaging, publication, or deployment. A later manual export is a recovery fallback and must be labeled `manual-export-recovery`, not `creation-time`.

## State boundary

The utility only creates a local source binary and receipt. It does not approve, canonize, publish, deploy, or edit a Publishing Desk record. Those gates remain separate and require their existing operator actions.
