# thread-sorter

Daily housekeeping for the Claude Code Desktop sidebar: files ungrouped threads into a **small, stable set of named groups** (cap 12) so the sidebar never sprawls.

Part of the Third Signal personal harness. It borrows the **Great Sage mode** lifecycle idea used for the skill library: a lifecycle *with a way back*.

## Rules (see `SKILL.md`)
- Reuse an existing group before creating one; new groups need evidence (>=3 threads fit nothing) and room under the cap.
- Hard cap of 12 groups; at the cap, file into the nearest group or `Inbox / Triage`.
- Demote, don't delete: sparse, idle groups are folded into a neighbour and logged with a `recall_when` note so they can be restored.
- Never touch pinned, running, archived or already-grouped threads; never archive or retitle sessions.

## Harness wiring
| Piece | Location |
|---|---|
| Skill (source of truth) | `~/.agents/skills/thread-sorter/` |
| Claude Code access | symlink `~/.claude/skills/thread-sorter` -> the above |
| Private state (not published) | `~/.agents/state/thread-sorter/{taxonomy,demoted}.md` |
| Schedule | Claude Desktop scheduled task `morning-thread-sorter`, daily ~06:30 local |

`taxonomy.example.md` and `demoted.example.md` show the state-file formats. Real taxonomies name private projects, so they stay out of this repo.

## Requirements
Needs a sidebar-grouping API (Claude Code Desktop `ccd_sidebar` / `ccd_session_mgmt` tools). Agents without it produce a move plan only.
