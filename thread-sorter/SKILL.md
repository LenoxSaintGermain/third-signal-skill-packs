---
name: thread-sorter
description: Sort ungrouped Claude Code sidebar threads into a small, stable set of named groups. Use for the daily morning cleanup, or when asked to organize/group/tidy threads or sessions. Applies Great Sage mode lifecycle rules (reuse before create, hard cap, reversible demotion, never delete).
---

# Thread sorter (Great Sage mode)

Keeps the sidebar to a **stable 8-12 groups** no matter how many threads pile up.
Agent-neutral: the rules below apply to any agent. Executing them needs a sidebar-grouping API. In Claude Code Desktop that is `mcp__ccd_session_mgmt__list_sessions` + `mcp__ccd_sidebar__{list_groups,move_sessions,create_group,rename_group,delete_group}` (load via ToolSearch if deferred). An agent without such tools must not improvise: produce the proposed moves as a plan and stop.

State (private, not part of the skill): `~/.agents/state/thread-sorter/taxonomy.md` (canonical groups) and `demoted.md` (recall log). Read both first. If missing, seed `taxonomy.md` from the current groups using `taxonomy.example.md` as the format.

## Great Sage rules
1. **Reuse before create.** Match each ungrouped thread to an existing group using `taxonomy.md` (theme, cwd hints, keywords). Judge by title + cwd + branch; if still unclear, `search_session_transcripts` on a distinctive title word. Never read/export full transcripts.
2. **Hard cap: 12 groups.** Target 8-12. At the cap, never create; file into the nearest group or `Inbox / Triage`.
3. **Create only on evidence.** New group only if >=3 threads fit nothing existing AND count < cap. Name = durable theme (project/system), not a one-off task. 2-6 words.
4. **Demote, don't delete (the way back).** Only under pressure (>=10 groups): if a group has <=1 thread and is >30 days idle, or overlaps another group, fold its threads into the nearest group **with real theme overlap** (if none overlaps, leave it alone rather than force a bad fit), delete the empty group, and append to `demoted.md`: date, old name, merged-into, `recall_when` (what would justify bringing it back), thread titles. To recall: recreate group from that entry and move threads back.
5. **Never touch**: pinned threads, running threads, threads already in a group (user filed them), archived threads. Never archive/delete/retitle sessions. Only ungrouped, unpinned, idle threads move.
6. **Names are sticky.** Rename a group only to fix a clearly wrong name; log it in `taxonomy.md`.
7. **Inbox / Triage** holds genuinely unclassifiable threads (max ~5); revisit next run.
8. Cap moves per run at 40. Batch `move_sessions` per destination group.

## Run procedure
1. Read `taxonomy.md`, `demoted.md`; `list_groups`, `list_sessions` (limit 200, group=null filter by checking `group`).
2. Reconcile: add any user-created groups missing from `taxonomy.md` (copy name, infer theme from members); note groups that vanished.
3. Classify and move ungrouped threads (rules 1-3, 5).
4. Run demotion check (rule 4); enforce cap.
5. Update `taxonomy.md` counts/last-run date.
6. Output a short report: moved N (by group), groups created/demoted, group count, items needing the user's decision. Keep under 15 lines.
