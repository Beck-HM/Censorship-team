---
name: progress-tracker
description: Real-time progress sync to markdown. Maintains PROGRESS.md (narrative log) and SESSION_DATA.md (structured data: decisions, lists, entities), plus git version control with task-level auto-commit and safe rollback.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

When loaded, the current agent takes on the role of progress tracker. After every file change or task completion, it:

1. Appends a narrative entry to `PROGRESS.md`
2. Extracts structured data (decisions, lists, entities, pending tasks) from the conversation and syncs them to `SESSION_DATA.md`
3. Auto-commits to git at task level

This gives the user both a human-readable timeline and a machine-queryable data snapshot.

## When to Use

- User says "keep track of what we're doing"
- Before/after running the code-architect pipeline
- During long sessions with multiple tasks
- User asks "what have we done so far?" or "what did we decide about X?"

---

## Process

When this skill is loaded, the agent maintains an internal `tracking_enabled` flag. All tracking operations are conditional on this flag.

### Step 1: Gate — Enable or Skip

This is the entry point of the skill. Do the following **immediately** upon loading:

1. Check if `SESSION_DATA.md` exists in project root — if so, read the last recorded `tracking_enabled` state.
2. Use the `question` tool:

> **header**: "Enable Progress Tracking?"
> **question**: "Do you want to enable progress tracking? This will:\n  - Maintain PROGRESS.md (narrative log)\n  - Maintain SESSION_DATA.md (decisions, named items, pending tasks)\n  - Auto-commit file changes to git at task level"
> **options**: ["Yes, enable tracking", "No, keep it disabled"]

- **"Yes, enable tracking"** → set `tracking_enabled = true`. Then proceed to **Step 2: Initialize** (which also handles git setup).
- **"No, keep it disabled"** → set `tracking_enabled = false`. Skip all of Steps 2-5. Inform the user: "Tracking is disabled. You can say 'resume tracking' or 'enable tracking' at any time to turn it on."

> If the user says "resume tracking" or "enable tracking" at any point later, go to **Step 7: Re-enable** instead.

### Step 2: Initialize

Only execute this if `tracking_enabled = true`.

1. **Check PROGRESS.md**: exists → read to understand current state; not exists → create with header.
2. **Check SESSION_DATA.md**: exists → read to understand past decisions and pending items; not exists → create with header.
3. **Check git repo**: no `.git` → ask: "Project is not a git repository. Shall I initialize one?" Options: "Yes, init with .gitignore" / "No, skip git".
   - If yes: `git init` + write a `.gitignore` (ignore `node_modules/`, `.opencode/state/`, `*.log`).

Use the `question` tool: "Progress tracker initialized. Log has [N] entries, data has [M] recorded decisions. Shall I start a new session?" Options: "Start new session" / "Continue current".

---

### Step 3: Track Every Action

Only execute this if `tracking_enabled = true`.

After each action that changes files (edit, write, bash that produces meaningful output):

**a) Append to PROGRESS.md:**

```
| 1 | 2026-06-02 14:50 | <brief description> | ✅ Done |
```

**b) Extract and sync to SESSION_DATA.md:**

Scan the current conversation turn for any of these patterns and update SESSION_DATA.md sections:

| Conversation content | SESSION_DATA.md section |
|---------------------|------------------------|
| User says "pick option B" / "go with approach X" / "do it this way" | `## Decision Log` + row |
| User or agent lists files, agents, skills, etc. | `## Named Items` — merge into existing lists |
| User mentions something to do later | `## Pending Tasks` + unchecked box |
| Agent reports a decision it made | `## Decision Log` + row |
| User says "note this" / "remember" / "write it down" | Force-extract the following content |

Use the `question` tool: "Logged: [description]. Data synced." — only if user seems to want confirmation; otherwise silently log and proceed.

Record a git commit: `git add -A` + `git commit -m "task: <description>"`.

---

### Step 4: Record Blockers

Only execute this if `tracking_enabled = true`.

If an action fails or is blocked:

**a) Append to PROGRESS.md:**

```
| 2 | 2026-06-02 15:00 | <attempted action> | ❌ Blocked — <reason> |
```

**b) Append to SESSION_DATA.md `## Pending Tasks`:**

```
- [ ] <blocked action> — blocked by: <reason>
```

Ask: "This is blocked. What should I do?" Options: "Skip and move on" / "Try alternative approach" / "Wait and come back".

---

### Step 5: Session End

Only execute this if `tracking_enabled = true`.

When the session ends (user signals done or conversation wraps up):

**a) Finalize PROGRESS.md:** Add session summary block.

**b) Finalize SESSION_DATA.md:** Update `## Pending Tasks` (mark completed items), add timestamp to all sections.

**c) Git**: `git add -A` + `git commit -m "session: <date> end"`.

**d)** Use `question` tool: "Session complete. Both files committed. Anything to add?" Options: "Looks good" / "Let me add notes".

---

### Step 6: Version Control & Rollback

This step is **always available** regardless of `tracking_enabled`.

#### 6a. .gitignore

Created during git init (see Step 2):

```
node_modules/
.opencode/state/
*.log
.DS_Store
Thumbs.db
```

#### 6b. Rollback (User-Triggered)

When user says "rollback" / "revert" / "undo":

1. Run `git log --oneline -20` to get the last 20 commits.
2. Present as a numbered list:

```
Recent commits in F:\Censorship team:
  1) a1b2c3d task: add brainstorming skill
  2) e4f5g6h task: update code-architect permissions
  3) ...
```

Use the `question` tool: "Which commit would you like to roll back to?" — option for each commit number.

3. Execute `git revert <hash>..HEAD` (safe, preserves history). If user wants to revert to a single commit, use `git revert <hash>`.
4. If `tracking_enabled = true`, also append to PROGRESS.md:

```
| N | <time> | Rolled back to <hash>: <message> | ✅ Done |
```

5. If `tracking_enabled = true`, also append to SESSION_DATA.md `## Rollback History`:

```
| # | Rolled Back To | Reason | Timestamp |
|---|----------------|--------|-----------|
| 1 | <hash> | <user's reason> | <time> |
```

---

### Step 7: Disable / Stop Tracking

When user says "stop tracking" / "disable" / "turn off tracking":

1. If `tracking_enabled = true`:
   - Do a final commit: `git add -A` + `git commit -m "tracking: session data final"`
2. Set `tracking_enabled = false`.
3. Inform user: "Tracking disabled. I will no longer update PROGRESS.md, SESSION_DATA.md, or auto-commit. You can say 'enable tracking' to turn it back on at any time."

### Step 8: Re-enable

When user says "resume tracking" / "enable" / "turn on tracking":

1. If `tracking_enabled` is already `true`, inform: "Tracking is already enabled."
2. If `tracking_enabled` is `false`, go back to **Step 1: Gate** and re-ask the enable question.

---

## PROGRESS.md Format

Project root (`F:\Censorship team\PROGRESS.md`):

```markdown
# Progress Log

**Project**: Censorship team
**Started**: <date>

## Session Log

| # | Time | Task | Status |
|---|------|------|--------|
| 1 | <time> | <description> | ✅ Done |
| 2 | <time> | <description> | ⬜ In progress |
| 3 | <time> | <description> | ❌ Blocked |

## Session Summary — <date>
- **Tasks completed**: N
- **Blockers**: -
- **Next steps**: -
```

## SESSION_DATA.md Format

Project root (`F:\Censorship team\SESSION_DATA.md`):

```markdown
# Session Data

Last updated: <timestamp>

## Decision Log

| # | Decision | Detail | Source | Timestamp |
|---|----------|--------|--------|-----------|
| 1 | <title> | <detail> | <agent or user> | <time> |

## Named Items

### Agents
- code-architect, installer, scout-alpha, ...

### Skills
- brainstorming, debugging, writing-plans, ...

### Files / Paths
- PROGRESS.md, .gitignore, ...

## Pending Tasks

- [ ] <task description> — noted: <timestamp>
- [x] <completed task> — done: <timestamp>

## Rollback History

| # | Rolled Back To | Reason | Timestamp |
|---|----------------|--------|-----------|
| 1 | <hash> | <user's reason> | <time> |
```

## Constraints

- `tracking_enabled = false` means Steps 3, 4, 5 are entirely skipped. Do not write to PROGRESS.md or SESSION_DATA.md, do not auto-commit.
- Only Step 1 (gate), Step 7 (disable), and Step 8 (re-enable) can change `tracking_enabled`.
- Do NOT override existing entries in either file — always append.
- PROGRESS.md descriptions: under 100 chars.
- SESSION_DATA.md: deduplicate named items (union merge), don't duplicate existing decisions.
- Status emoji: ✅ Done, ⬜ In progress, ❌ Blocked, 🔄 Retrying.
- Rollback always uses `git revert` (safe), never `git reset --hard`.
- Keep PROGRESS.md and SESSION_DATA.md in sync — if one is updated, the other should be too if relevant.
