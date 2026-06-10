# Hermes Desktop on LANDSAT

Use this note when the operator asks about the Hermes Desktop companion on the Mac Mini and the local CLI/docs appear out of sync.

## Durable lesson

On LANDSAT, do not assume the presence of the `hermes desktop` CLI command just because the docs mention it.

The safe sequence is:

1. Verify the installed CLI version.
2. Verify whether `hermes desktop` actually exists in that build.
3. If the command is missing, check for the installed macOS app bundle directly.
4. Prefer launching the app bundle if it is already present rather than reinstalling blindly.

## LANDSAT-specific findings

- Current observed CLI build: `Hermes Agent v0.15.1`
- In that build, `hermes desktop` was not exposed in `hermes --help`
- The desktop companion was already installed as:
  - `/Applications/Hermes Agent.app`
- The app had a valid notarized macOS signature and launched successfully
- Desktop local state lived under:
  - `/Users/lenoxparis/Library/Application Support/hermes-desktop`
- Shared Hermes state remained under:
  - `/Users/lenoxparis/.hermes`

## Practical operator guidance

If the docs say "run `hermes desktop`" but the local CLI rejects that command:

- Launch `/Applications/Hermes Agent.app` directly
- Treat the mismatch as a docs/CLI-version gap, not immediate proof that desktop is missing
- Only reach for the DMG installer after checking whether the app already exists in `/Applications`

## Verification checklist

- CLI reality check:
  - `hermes --help`
  - `hermes --version`
- Direct app presence:
  - `test -d '/Applications/Hermes Agent.app' && echo present`
- App metadata:
  - `defaults read '/Applications/Hermes Agent.app/Contents/Info' CFBundleIdentifier`
  - `defaults read '/Applications/Hermes Agent.app/Contents/Info' CFBundleShortVersionString`
- Gatekeeper / notarization:
  - `spctl -a -vv '/Applications/Hermes Agent.app'`
  - `codesign -dv --verbose=4 '/Applications/Hermes Agent.app'`
- Desktop support dir:
  - `find '/Users/lenoxparis/Library/Application Support/hermes-desktop' -maxdepth 2 -mindepth 1`

## Why this matters

This avoids wasting time reinstalling Hermes Desktop when the actual issue is only a mismatch between newer docs and an older local CLI build.
