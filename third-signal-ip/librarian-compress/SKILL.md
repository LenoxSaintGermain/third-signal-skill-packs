---
name: librarian-compress
description: Automatically compresses EXECUTION_LEDGER.md using hierarchical compression tiers to maintain token efficiency while preserving architectural context.
---

# LIBRARIAN Compress Protocol

**Purpose:**
Prevent ledger bloat and token inefficiency by intelligently compressing the EXECUTION_LEDGER.md through hierarchical compression strategies. Maintains the "Current Truth" while archiving historical details.

**When to Use:**
- Automatically invoked by `librarian-sync` when Tier 1 threshold is met
- Manually invoked when ledger exceeds 1000 lines
- Before major version releases to create architectural snapshots

---

## Compression Tiers

### Tier 1: Inline Batch Compression (Auto-triggered at 1000+ lines)
**Threshold**: Ledger ≥ 1000 lines OR ≥ 10 consecutive entries in same domain

**Process**:
1. Identify batch of entries to compress (last 10-20 entries OR entries older than 30 days)
2. Extract key patterns and decisions from the batch
3. Create a "Period Summary" (5-10 lines) capturing:
   - What was built
   - Why key architectural decisions were made
   - What interfaces/dependencies were established
4. Archive raw entries to `docs/ledgers/archive/BATCH_[start-date]_[end-date].md`
5. Replace batch in main ledger with the summary
6. Update `COMPRESSION_METADATA.json`

**Example Compression**:
```markdown
BEFORE (180 lines):
### 🗓️ [2026-01-29 14:30] Task: US-10.1
[detailed implementation...]
### 🗓️ [2026-01-30 09:15] Task: US-10.2
[detailed implementation...]
[...8 more entries...]

AFTER (12 lines):
### 📦 Period Summary: Jan 29 - Feb 5, 2026
**Domain**: Authentication & Authorization
**Entries Compressed**: 10 (See: docs/ledgers/archive/BATCH_2026-01-29_2026-02-05.md)

**Key Achievements**:
- Implemented Firebase Auth with Firestore-based RBAC (not custom claims due to quota limits)
- Established `useAuthStore` as canonical auth interface
- Created `PermissionGuard` component for UI-level access control

**Critical Constraints**:
- Must validate permissions client-side (Firebase Rules too slow for real-time UI)
- Session tokens expire after 1 hour; implement auto-refresh in `lib/auth.ts`
```

---

### Tier 2: Domain Sharding (Triggered at 2000+ lines)
**Threshold**: Ledger ≥ 2000 lines

**Process**:
1. Analyze all ledger entries and classify by domain:
   - `auth` - Authentication, authorization, user management
   - `ui` - Frontend components, UI/UX changes
   - `audio` - Audio engine, voice processing, TTS/STT
   - `server` - Backend APIs, cloud functions, infrastructure
   - `integration` - Third-party integrations, external APIs
   - `deployment` - CI/CD, builds, releases

2. Create domain-specific ledgers:
   - `docs/ledgers/auth_ledger.md`
   - `docs/ledgers/ui_ledger.md`
   - `docs/ledgers/audio_ledger.md`
   - etc.

3. Create `EXECUTION_LEDGER_INDEX.md` as the new main entry point:
   ```markdown
   # Execution Ledger Index

   This project uses domain-sharded ledgers for token efficiency.

   ## Domain Ledgers
   - [Authentication](docs/ledgers/auth_ledger.md) - 245 lines
   - [UI/Frontend](docs/ledgers/ui_ledger.md) - 312 lines
   - [Audio Engine](docs/ledgers/audio_ledger.md) - 189 lines
   - [Server/API](docs/ledgers/server_ledger.md) - 428 lines
   - [Integrations](docs/ledgers/integration_ledger.md) - 156 lines

   ## Quick Navigation
   - Working on auth? Read `auth_ledger.md`
   - UI changes? Read `ui_ledger.md`
   - Full context needed? Read all domain ledgers

   Last sharding: 2026-03-12
   ```

4. Move original `EXECUTION_LEDGER.md` to `docs/ledgers/archive/LEDGER_PRE_SHARD_[date].md`
5. Update `COMPRESSION_METADATA.json` with sharding event

**Benefits**:
- Agents working on UI only load ~300 lines instead of 2000+
- Token reduction: 66-85% for domain-specific work
- Preserves full context when needed (read all shards)

---

### Tier 3: Semantic Compression (Triggered at 5000+ lines)
**Threshold**: Total ledger content ≥ 5000 lines (across all shards if using Tier 2)

**Process**:
1. Read all ledger content (main ledger OR all domain shards)
2. Extract architectural principles, patterns, and "Current Truth":
   - Core architectural decisions and their rationale
   - Established patterns (e.g., "Always use Zod for API validation")
   - Known constraints and gotchas
   - Critical dependencies and interfaces
   - Anti-patterns to avoid

3. Create `docs/ledgers/chronicle/CURRENT_TRUTH_[date].md`:
   ```markdown
   # Architectural Current Truth
   *Generated: 2026-03-12 from 5,247 ledger lines*

   ## Core Principles

   ### Authentication Architecture
   **Decision**: Firestore-based RBAC, not Firebase custom claims
   **Rationale**: Custom claims hit quota limits; Firestore scales better
   **Interface**: `useAuthStore()` in `lib/stores/authStore.ts`
   **Constraints**: Client-side permission checks required (Firebase Rules too slow)

   ### UI Component Patterns
   **Decision**: Compound components over prop proliferation
   **Example**: `<Radio.Group><Radio.Item /></Radio.Group>` not `<Radio options={[]} />`
   **Rationale**: Better composition, easier to extend

   [... more principles ...]

   ## Critical Gotchas
   - Firebase quota: 50k custom claim updates/day
   - React Native Audio: Must request permissions before playback
   - TypeScript: Avoid `any`, use `unknown` for truly dynamic types

   ## Deprecated Approaches
   - ❌ Mock localStorage (breaks real browser behavior)
   - ❌ Direct Firebase SDK in components (use stores)
   - ❌ Prop drilling for auth state (use context)
   ```

4. Archive full chronological history to `docs/ledgers/chronicle/FULL_CHRONICLE_[date].md`
5. Replace main ledger(s) with reference to CURRENT_TRUTH + recent entries (last 30 days)
6. Update `COMPRESSION_METADATA.json`

**Benefits**:
- Token reduction: 80-90% for routine work
- New agents onboard faster (read Current Truth, not 5000 lines)
- Historical record preserved for deep dives
- "Documentary" of the project's evolution

---

## Compression Protocol Steps

### 1. Measure Ledger Metrics
```markdown
Calculate:
- Total lines (across all ledgers if sharded)
- Entry count
- Estimated tokens (lines × 0.31)
- Oldest entry date
- Domain distribution (if entries are tagged)
```

### 2. Determine Compression Tier Needed
```markdown
If ledger ≥ 5000 lines:
  → Recommend Tier 3 (requires user approval - major change)
Else if ledger ≥ 2000 lines:
  → Recommend Tier 2 (requires user approval - structural change)
Else if ledger ≥ 1000 lines:
  → Execute Tier 1 automatically
Else:
  → No compression needed
```

### 3. Execute Compression
Based on tier determined, execute the appropriate compression process.

**Critical Rules**:
- ✅ Never delete original data (always archive)
- ✅ Preserve entry integrity (don't split atomic entries)
- ✅ Maintain chronological order (timestamps guide everything)
- ✅ Update COMPRESSION_METADATA.json (track all compressions)
- ✅ Preserve status markers (✅/⚠️/❌) in archives

### 4. Verify Compression
```markdown
After compression:
- Confirm archive files created
- Verify chronological order maintained
- Calculate token reduction percentage
- Test that new structure is readable
- Update metadata file
```

### 5. Report Results
```markdown
Example confirmation:
"✅ Tier 1 Compression Complete
- Before: 1,247 lines (~3,900 tokens)
- After: 847 lines (~2,650 tokens)
- Reduction: 32% (1,250 tokens saved)
- Archived: 10 entries → docs/ledgers/archive/BATCH_2026-02-15_2026-03-01.md
- Metadata: COMPRESSION_METADATA.json updated"
```

---

## Special Considerations

### Domain Classification Logic
When analyzing entries for Tier 2 sharding, classify by:
1. **File paths mentioned** (e.g., `lib/auth.ts` → auth domain)
2. **Keywords in entry** (e.g., "authentication", "login" → auth)
3. **Agent role** (e.g., "UI Agent" → ui domain)
4. **Explicit tags** (if entry has `[domain:auth]` marker)

If entry spans multiple domains, duplicate into both domain ledgers with cross-reference:
```markdown
### 🗓️ [2026-03-12 15:00] Task: US-15.3 [Cross-domain: auth + ui]
**Primary Domain**: Authentication
**Also affects**: UI (see ui_ledger.md for UI-specific details)
[...entry content...]
```

### Handling Edge Cases
- **Very long single entries** (100+ lines): Don't compress; these are detailed architectural docs
- **Empty batches**: If a period has no entries, don't create empty summaries
- **Rapid iteration**: If same file modified 10 times in a day, summarize as "Iterative refinement of X"
- **Breaking changes**: Always preserve entries documenting breaking changes (never compress these)

### Token Estimation Formula
```
Estimated tokens = (Total lines × 0.31) + (Code block lines × 0.15)
```
This accounts for markdown overhead and code blocks being more token-dense.

---

## Integration with librarian-sync

When `librarian-sync` detects Tier 1 threshold:
```markdown
### In librarian-sync Protocol Step 3 (Compression Check):

If ledger ≥ 1000 lines:
  - Invoke: Skill(skill="librarian-compress")
  - Wait for completion
  - Include compression results in confirmation
```

For Tier 2+:
```markdown
If ledger ≥ 2000 lines:
  - Add warning: "⚠️ Ledger has {lines} lines. Consider running `librarian-compress` with tier2"
  - Do NOT auto-execute (requires user approval)
```

---

## Manual Invocation

Users can manually trigger compression:

**Syntax**:
- Auto-detect tier: Just invoke the skill without arguments
- Specific tier: Pass tier as argument (e.g., `args: "tier2"`)

**Examples**:
```
User: "compress the ledger"
→ Skill invokes with auto-detect, runs appropriate tier

User: "shard the ledger into domains"
→ Skill invokes with tier2 explicitly
```

---

## Success Criteria

After running this skill, verify:
- ✅ Ledger size reduced OR sharded appropriately
- ✅ No data loss (all original entries in archives)
- ✅ Chronological integrity maintained
- ✅ COMPRESSION_METADATA.json updated
- ✅ Token reduction measured and reported
- ✅ Future `librarian-sync` works with new structure

---

## Notes

**Philosophy**: Compression is an implementation detail. Agents reading the ledger should get the "Current Truth" without needing to know compression happened.

**Safety**: Original data is never deleted. If compression fails or creates issues, archives can always be restored.

**Scalability**: Designed for projects lasting months/years with thousands of entries. The three-tier system ensures ledgers stay efficient even at enterprise scale.
