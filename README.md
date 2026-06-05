# Censorship Team

Are you tired of AI writing code you don't understand? Watching files appear with no explanation of why they exist or how they fit together? Wasting time reverse-engineering what a model did, only to find the architecture is worse than before?

Censorship Team fixes this.

**code-architect** routes every request through a clear intent dispatch — no more guessing what the AI is about to do. When you ask for a review, **scout-alpha** and **scout-beta** first map out every file and every convention in your project. **arch-alpha** builds a dependency graph so you can see exactly which modules touch what. **arch-beta** traces data flow and highlights where state management is fragile.

Before any code is written, **test-worker** checks what tests exist and what's missing. When refactoring begins, **refactor-conservative** moves one step at a time, **refactor-aggressive** tackles large cross-cutting changes, and **refactor-pattern** applies proven design patterns — all with tests run after every step.

Every phase produces a readable report. Every change is logged by **progress-tracker** to PROGRESS.md and SESSION_DATA.md, auto-committed to git, and ready to review. Need to explore an idea first? Load **brainstorming**. Found a bug? Load **debugging**. Planning a big feature? Load **writing-plans**.

No hidden changes. No surprises. No black boxes. Just agents with clear jobs, a pipeline you can follow, and reports you can actually read.

---

A structured opencode skills package for code analysis, refactoring, and project workflows. Built around a pipeline of specialised agents and a set of general-purpose skills that load on demand.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Agents](#agents)
- [Pipeline](#pipeline)
- [Quick Mode](#quick-mode)
- [General-Purpose Skills](#general-purpose-skills)
- [Custom Tools](#custom-tools)
- [Full Analysis Mode](#full-analysis-mode)
- [Deep Review Sub-agents](#deep-review-sub-agents)
- [Project Deconstruction](#project-deconstruction)
- [Pipeline State & Resume](#pipeline-state--resume)
- [Usage Scenarios](#usage-scenarios)
- [Design Principles](#design-principles)
- [Translations](#translations)

---

## Requirements

- **opencode** (any version that supports custom agents and skills)
- **Node.js 18+** (`node.exe` must be in PATH)
- **Python 3.10+** (`python.exe` must be in PATH) — only needed if using the custom analysis tools

The 6 Python scripts use stdlib only — no pip install needed.

---

## Installation

### Quick install via npx

```bash
npx censorship-team
```

The CLI detects your opencode config directory and copies all files automatically. After installation, start opencode and configure models:

```
@installer configure skill models
```

### Manual: clone

```bash
git clone <repo-url> Censorship-team
cd Censorship-team

# For a specific project:
cp -r agents skills tools scripts your-project/.opencode/

# Or for global use (all projects):
cp -r * ~/.config/opencode/
```

### Via the installer agent

After copying the files, invoke the installer inside opencode:

```
@installer configure skill models
```

The installer walks you through model assignment for each agent, verifies Python/Node.js availability, and writes the configuration.

---

## Quick Start

### First encounter with a project

```
you: full analysis on this project please
→ code-architect asks: "Do you want to run Full Analysis Mode?"
→ you say yes
→ agent runs scouts → architecture → test check → produces a report
```

### Fixing a bug

```
you: there is a bug, the page list won't load
→ code-architect asks: "Do you want to load the debugging skill?"
→ you say yes
→ debugging skill guides you through reproduce → isolate → fix → verify
```

### Daily development with tracking

```
you: track my progress today
→ code-architect asks: "Do you want to load the progress-tracker?"
→ you say yes
→ agent asks: "Enable tracking?" → you say yes
→ every change from now on is auto-logged + committed
```

### Deep review committee

```
you: deep review this project
→ code-architect runs FA1-FA3 scouts/architecture/tests
→ at FA4: "Run deep review committee?" → you say yes
→ dispatches 8 sub-agents across Architecture / Specialists / Verification teams
→ outputs scored report with evidence chain and future risk prediction
```

### Full pipeline (review + refactor)

```
you: review the code quality of this project
→ code-architect enters Phase 0 → asks language, type, framework, context
→ runs Phases 1-5 with user gates at test plan, review, and refactoring plan
```

---

## How It Works

The package revolves around **code-architect**, the primary agent. Every user message goes through a 5-level intent dispatch before any action is taken:

```
User message
    │
    ▼
┌─ Intent Dispatch ──────────────────────┐
│ Level 1: Casual / chit-chat            │ → short reply, do nothing
│ Level 2: Simple code op (rename, etc.) │ → do it directly
│ Level 3: Specific skill need           │ → ask: "load <skill>?"
│ Level 4: Analysis / refactor           │ → full analysis (+ optional deep review committee), Quick Mode, or Phase 0-5
│ Level 5: Cannot determine              │ → ask: "what do you need?"
└────────────────────────────────────────┘
```

**Key rule**: When in doubt, ask. Never guess the user's intent.

---

## Agents

10 pipeline agents + 8 deep review sub-agents.

### Primary

#### `code-architect`
The only agent that talks to the user directly. Routes every message through a 5-level intent dispatch before taking any action — casual chat, simple edit, skill suggestion, project analysis, or refactoring pipeline. Orchestrates the full pipeline by dispatching sub-agents via the `task` tool and synthesising their results. Never modifies files without explicit user approval.

- **File**: `agents/code-architect.md`
- **Mode**: primary
- **Invoked**: manually by the user only

---

---

### Model configuration

#### `installer`
Sets up the package's model configuration. Guides the user through assigning models to each agent, writes the configuration file, and verifies that Python and Node.js are available. Passive agent — never invoked automatically. The user must explicitly call `@installer`.

- **File**: `agents/installer.md`
- **Color**: `#f59e0b`
- **Mode**: primary
- **Invoked**: manually by the user only

---

### Deep Review Sub-agents

8 sub-agents organized into three teams. Dispatched by code-architect when "Run deep review committee" is selected during FA4 or Phase 4.

**Architecture Team**:
- `deep-architect` — Evaluates why the architecture works: module boundaries, extension points, patterns, design decisions
- `deep-critic` — Evaluates why the architecture could fail: over-engineering, complexity hazards, lifecycle risks, hidden coupling

**Specialists Team**:
- `deep-security` — Scans for eval/runInThisContext/child_process/dynamic imports, outputs Critical/High/Medium/Low
- `deep-performance` — Analyzes O(n²) algorithms, full scans, cache misses, repeated traversal, watch mode efficiency
- `deep-techdebt` — Analyzes coupling degree, boundary pollution, evolution cost (files touched per feature), dead code
- `deep-redteam` — Attack surface analysis: "if I were trying to break this project, where would I attack?"

**Verification Team**:
- `deep-evidence` — Attaches exact file:line evidence to every finding, marks unsupported findings
- `deep-confidence` — Assigns High (code evidence) / Medium (inference) / Low (speculative) to every finding, no default High

---

### project-deconstruction

Offered as an optional supplement after the standard pipeline or Full Analysis Mode. Produces a narrative "how this project runs" appendix plus an ASCII box diagram.

**When**: After Phase 4 (plan stage) or FA4 (analysis report). Triggered by a user-facing question.

**Process**:
1. Read Phase 0 answers to understand the project type
2. Review existing scout, arch, and test reports
3. Read key source files (entry points, wiring, core logic)
4. Write 3-6 narrative paragraphs covering startup, data flow, dependencies, critical paths
5. Generate one ASCII box diagram using Unicode box-drawing characters

**Output example**:
```
HTTP POST /api/orders
    │
    ▼
┌──────────┐
│  Auth    │
│  Guard   │
└────┬─────┘
     │
     ▼
┌──────────┐
│ Order    │
│Controller│
└────┬─────┘
     │
     ▼
┌──────────┐
│ OrderSvc │
└────┬─────┘
     ├────→ PaymentAPI (external)
     │
     ▼
┌──────────┐
│ OrderRepo│
└────┬─────┘
     │
     ▼
  PostgreSQL
```

**Constraints**: read-only, uses existing reports + targeted file reads, no re-analysis, under 60 lines.

---

### How sub-agents are invoked

code-architect dispatches sub-agents via the `task` tool. Each sub-agent works autonomously with its own skill context. The results are collected and synthesised by code-architect.

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (parallel)
  ├── Phase 2: task arch-alpha + task arch-beta (parallel)
  ├── Phase 3: task test-worker
  ├── Phase 5: task refactor-* (sequential, one per step)
  └── Deep Review (FA4 or Phase 4 optional):
      ├── Round 1: deep-architect + deep-critic (parallel)
      ├── Round 2: deep-security + deep-performance + deep-techdebt + deep-redteam (parallel)
      └── Round 3: deep-evidence + deep-confidence (parallel)
```

---

## Pipeline

code-architect runs a standard pipeline for code review and refactoring tasks. Each phase has a specific purpose and most have user gates. Based on project size, a **Quick Mode** variant may be offered during Phase 0 — same structure, fewer sub-agents.

```
Phase 0     Project Assessment ─── Q1-Q3 → Size Scan → Q4 → Mode Recommendation
              • Quick Mode offered if project is small
              • Full pipeline selected for larger or complex projects
   │
Phase 1     Project Exploration ─── scouts explore structure + code
              • Full: scout-alpha + scout-beta in parallel
              • Quick: one scout (selected automatically)
   │
Phase 2     Architecture Analysis ─── arch agents analyse deps + data flow
              • Full: arch-alpha + arch-beta in parallel
              • Quick: one arch (selected automatically)
   │              ┌────────────────────────────┐
Phase 3     Test  │  user gate: review plan     │
            │     │  "Shall I proceed?"         │
            │     └────────────────────────────┘
              • Full: dispatched to test-worker
              • Quick: tests run directly via glob + test command
   │
Phase 3.5   Post-Test Review ─── "Ready for the refactoring plan?"
   │              ┌────────────────────────────┐
Phase 4     Plan  │  user gate: approve plan    │
            │     │  "Shall I execute?"         │
            │     └────────────────────────────┘
              • Full: comprehensive plan
              • Quick: compact plan (3-5 items)
   │
Phase 5     Execute refactoring ─── step by step, test after each
              • Same for both modes
```

The pipeline also supports **resume**: if a session is interrupted, code-architect detects the saved state on next startup and asks whether to resume from where it left off. See [Pipeline State & Resume](#pipeline-state--resume).

### Intent Dispatch (always runs first)

| Level | Matches | Behaviour |
|-------|---------|-----------|
| 1 | Greetings, casual chat | Short reply, no action |
| 2 | "rename X", "change Y", "add comment" | Execute directly |
| 3 | "bug", "explore", "plan", "track" | Ask to load relevant skill |
| 4A | "full analysis", "scan project", "explore project", "deep review", "committee" | Enter Full Analysis Mode |
| 4B | "review", "audit", "refactor", "optimise" | Enter Phase 0 pipeline |
| 5 | Ambiguous | Ask user what they need |

---

## Quick Mode

A lighter variant of the full pipeline for small to medium projects. Triggered by code-architect during Phase 0 after a quick project size scan.

### How it differs

| | Full Pipeline | Quick Mode |
|---|---|---|
| Phase 1 | Two scouts (alpha + beta) | One scout — automatically selected |
| Phase 2 | Two arch agents (alpha + beta) | One arch — automatically selected |
| Phase 3 | Test plan → test-worker → results | Test plan → run tests directly (no dedicated agent) |
| Phase 4 | Comprehensive plan + optional 8-agent deep review | Compact plan (3-5 items) + optional 4-agent quick deep review |
| Reports | Full detail | Summary output |

### When it's offered

code-architect runs `project-summary` during Phase 0 to get file count, line count, and test ratio. Based on all available information, it judges whether the project suits a lighter process. The user always gets a choice:

```
Phase 0 size scan → "This project seems small. Would you like to use Quick Mode?"
                     [Yes, use Quick Mode / No, use full pipeline]
```

### Phase 5 — same as full

Refactoring execution and per-step testing are identical to the full pipeline. Quick Mode only reduces the analysis and planning phases.

---

## General-Purpose Skills

Located in `skills/tools/`. These are loaded on demand — code-architect asks the user first before loading any of them.

### brainstorming

**When**: The user's goal is vague, or there are multiple possible approaches.

**Process**:
1. Clarify the goal (ask one question at a time)
2. Propose 2-3 approaches with pros/cons
3. Dig into details of the selected approach
4. Produce a design summary and ask for approval

### debugging

**When**: Something is broken — errors, crashes, unexpected behaviour.

**Process**:
1. Reproduce the issue
2. Isolate the root cause (binary search through code path)
3. Propose and apply a minimal fix
4. Verify with tests
5. Add regression test

### writing-plans

**When**: A task is large and needs to be broken into concrete steps.

**Process**:
1. Collect context (design summary, project structure)
2. Break down into small, self-contained tasks
3. Order by dependency
4. Present plan for approval

### progress-tracker

**When**: The user wants to track what's been done.

**Process**:
1. Ask: "Enable tracking?" (can be disabled at any time)
2. Maintain PROGRESS.md (narrative log — "what happened when")
3. Maintain SESSION_DATA.md (structured data — decisions, lists, pending tasks)
4. Auto-commit every file change to git at task level
5. Rollback support via `git revert` (user-triggered, shows commit list)

## Custom Tools

6 TypeScript wrappers in `tools/` that call Python scripts in `scripts/`. They are **optional** helpers — the pipeline works without them.

| Tool | Script | Description |
|------|--------|-------------|
| `project-summary` | `scripts/project-summary.py` | File counts per language, total lines, test ratio, entry points |
| `dependency-matrix` | `scripts/dependency-matrix.py` | Import/use graph, circular dependency detection, fan-in/fan-out per module |
| `complexity` | `scripts/complexity.py` | Function length and nesting depth analysis, top-20 worst offenders |
| `test-gap` | `scripts/test-gap.py` | Compares source vs test files to find which modules lack tests |
| `find-orphans` | `scripts/find-orphans.py` | Files that are not imported or referenced anywhere |
| `duplicate-lines` | `scripts/duplicate-lines.py` | Cross-file duplicate or near-duplicate code blocks |

---

## Full Analysis Mode

A read-only shortcut built into code-architect. Use it when you want to understand a project without modifying anything.

**Trigger**: Say "full analysis" / "scan this project" / "get to know the project" to code-architect.

**Flow**:
```
FA0: Ask one question ─── "Any specific focus?" (or "cover everything")
FA1: Scout-alpha + scout-beta (parallel project exploration)
FA2: Arch-alpha + arch-beta (parallel architecture analysis)
FA3: Test coverage check ─── run existing tests, note gaps
FA4: Report production ─── offers options:
     • Deep review committee (+ project-deconstruction optional)
     • Project-deconstruction only
     • Standard report
FA5: Recommend next steps ─── suggest skills based on findings
```

**Key differences from the standard pipeline**:
- No Phase 0 (single question instead of four)
- No user gates at test/plan stages
- No refactoring plan
- No code modification — read-only

**Deep Review Committee**: An optional 8-agent parallel review available at FA4. See [Deep Review Sub-agents](#deep-review-sub-agents) for team composition.

**Expected token cost**: ~50K tokens (FA standard) or ~100K tokens (with deep review committee).

---

## Project Deconstruction

An optional skill that reads existing analysis reports and key source files to produce a narrative breakdown of how a project runs. It does not re-analyse — it synthesises what's already been gathered into a readable "whole picture."

**Triggered by**: code-architect asks "Would you like to add extra analysis before the final report?" at Phase 4 (refactoring plan) or FA4 (analysis report). Select "Show project-deconstruction" from the options, or select "Run deep review committee" and answer "Yes, both" to include project-deconstruction alongside the committee review.

**Output**: 3-6 narrative paragraphs covering startup sequence, data flow, module dependencies, side effects, and critical paths, followed by one ASCII box diagram.

See the [project-deconstruction](#project-deconstruction) skill entry for details.

---

## Pipeline State & Resume

The pipeline automatically saves progress to `.opencode/state/pipeline-state.json` at every major phase boundary. If the session is interrupted (closed terminal, timeout, crash), the next session can resume from where it left off.

### Save points

| When | What's saved |
|------|-------------|
| After Mode Recommendation | Phase 0 answers, size scan data, selected mode |
| After Phase 1 completes | Scout report completed |
| After Phase 2 completes | Architecture report completed |
| After Phase 3 completes | Test results completed |
| After Phase 4 plan approved | Refactoring plan + step count |
| After each Phase 5 step | Current step number |
| After Full Analysis (FA4) | Report completed flag |

### Resume flow

On next startup, code-architect detects the state file automatically and asks:

```
"I found an interrupted pipeline at Phase X. Do you want to resume it?"
[Yes, resume / No, start fresh]
```

If the user resumes:
- Phase 0 answers are restored — no need to re-ask
- Completed phases are skipped
- Phase 5 continues from the last completed step

If the user declines, the state file is deleted and a fresh pipeline begins.

### Edge cases

- **Project path changed**: detected and handled with a user prompt
- **Corrupted state file**: auto-deleted, user informed
- **User wants unrelated work**: resume prompt comes before intent dispatch — declining resumes normal operation

---

## Usage Scenarios

### Scenario 1: New project, first look

```
you: full analysis on this project please
→ code-architect: "Do you want to run Full Analysis Mode?"
→ you: Yes
→ code-architect: "Any specific focus?"
→ you: No, cover everything
→ runs FA1-FA4 automatically
→ outputs a comprehensive report (structure, architecture, tests, risks)
→ code-architect: "Based on the analysis, the test coverage is low.
  Shall I load writing-plans to break down the work?"
→ you: Yes
→ writing-plans helps you plan
```

### Scenario 2: Debug a production issue

```
you: users are getting 500 errors on login
→ code-architect: "It sounds like you need to debug a problem.
  Shall I load the debugging skill?"
→ you: Yes
→ debugging: "Can you provide the exact error message?"
→ you: <pastes error>
→ debugging: traces the code path, identifies the root cause,
  proposes a fix
→ you: approve
→ applies fix, runs tests, asks about regression test
```

### Scenario 3: Refactoring with tracking

```
you: refactor the module structure of this project
→ code-architect: enters Phase 0, asks 4 questions
→ you: answer
→ runs Phases 1-5 with user gates at test/plan/execution
→ at the refactoring plan stage, you see clear steps with risk assessment
→ you approve Phase 5
→ refactoring executes step by step, tests pass after each step
```

### Scenario 4: Daily work with progress tracking

```
you: enable progress tracking please
→ code-architect: "Shall I load progress-tracker?"
→ you: Yes
→ progress-tracker: "Enable tracking? This will log to PROGRESS.md
  and commit to git."
→ you: Yes
→ you make changes throughout the day
→ each change is logged + committed automatically
→ end of day: ask "what did we do today" and get a full log
```

### Scenario 5: Plan a new feature

```
you: I'm not sure how to implement the search feature, any ideas?
→ code-architect: "It sounds like you want to discuss a design.
  Shall I load the brainstorming skill?"
→ you: Yes
→ brainstorming walks through clarifying goals, proposing approaches,
  producing a design summary
→ you approve the design
→ code-architect: "Want to load writing-plans to break this into tasks?"
→ you: Yes
→ writing-plans produces a task plan
```

### Scenario 6: Quick Mode for a small project

```
you: review the code quality of this small utility library
→ code-architect enters Phase 0: Q1 (Python) → Q2 (Library) → Q3 (None)
→ runs project-summary: 12 files, 800 lines
→ Q4 additional context → you say no
→ "This project seems small. Would you like to use Quick Mode?"
→ you: Yes
→ Phase 1: one scout (selected automatically), Phase 2: one arch
→ Phase 3: test plan → approved → tests run directly
→ Phase 4: "Run quick deep review?" → you: Yes
→ Round 1: deep-architect + deep-critic (architecture analysis)
→ Round 2: deep-security + deep-techdebt (security + tech debt scan)
→ compact plan + saved to deep-review-report.md
→ Phase 5: execute, test after each step
```

### Scenario 8: Deep review committee

```
you: full analysis with deep review
→ code-architect: "Do you want to run Full Analysis Mode?" → you: Yes
→ code-architect: "Any specific focus?" → you: cover everything
→ runs FA1-FA3 (scouts → architecture → tests)
→ FA4: "Would you like to add extra analysis before the final report?"
  [Run deep review committee / Show project-deconstruction / Just the standard report]
→ you: Run deep review committee
→ code-architect: "Also add project-deconstruction?" → you: Yes, both
→ Round 1: deep-architect + deep-critic — why design works / why it fails
→ Round 2: deep-security + deep-performance + deep-techdebt + deep-redteam
→ Round 3: deep-evidence + deep-confidence — exact file:line + confidence ratings
→ project-deconstruction runs in parallel
→ Final report includes: 7 standard sections + 8. Deep Review Committee Report
  with scores (X/10), evidence chain, future risk prediction
```

**Token cost**: ~100K tokens for a 50K-line project (scouts + archs + deep review + full report).

### Scenario 7: Resume after interruption

```
Session 1:
you: refactor the module structure
→ Phase 0-2 complete, Phase 3 in progress → terminal closes

Session 2 (next day):
you: (first message)
→ code-architect: "I found an interrupted pipeline at Phase 3.
  Do you want to resume it?" [Yes, resume / No, start fresh]
→ you: Yes
→ Phase 0 answers restored, Phase 1-2 marked done
→ continues from Phase 3 without re-asking anything
```

---

## Translations

This README is also available in other languages:

| Language | File |
|----------|------|
| Español | [README.es.md](i18n/README.es.md) |
| Français | [README.fr.md](i18n/README.fr.md) |
| Japanese | [README.ja.md](i18n/README.ja.md) |
| Русский | [README.ru.md](i18n/README.ru.md) |

---

## Design Principles

- **Ask before act** — agents suggest, user decides. Never guess the user's intent.
- **Skills per agent** — each agent has an isolated SKILL.md with domain knowledge. Permissions control which skills an agent can load.
- **On-demand loading** — general-purpose skills (brainstorming, debugging, writing-plans, progress-tracker) are only loaded after the user confirms. Never auto-loaded.
- **Intent-first routing** — every user message is classified into 1 of 5 levels before any action. Brief chat gets a brief reply; analysis requests enter the pipeline.
- **Read-only by default** — the pipeline does not modify files until Phase 5, which requires explicit user approval.
- **Dual log format** — progress-tracker maintains both a narrative log (PROGRESS.md) and a structured data file (SESSION_DATA.md) for decisions, lists, and pending items.
- **Safe rollback** — all version control operations use `git revert` (preserves history). Never `git reset --hard`.
- **Stdlib only** — Python scripts have no external dependencies. Zero pip installs.
- **Technical objectivity** — evaluate code purely on technical merit. Ignore popularity, brand, hype, contributor count, or project age. Same standard for every project.
- **Design & long-term lens** — every report covers three layers: design (abstraction, patterns, complexity), architecture (module boundaries, feature change scope, extension points), and long-term (growth impact, debt cost, timing). Surface findings are the starting point, not the conclusion.
- **Auto-resume** — the pipeline saves progress after every phase. If interrupted, it auto-detects the saved state and offers to resume.
- **Multi-agent deep review** — FA4 and Phase 4 offer an optional 8-agent committee (Architecture, Security, Performance, Tech Debt, Red Team, Evidence, Confidence) that runs in three parallel rounds. Each agent produces structured findings cited to exact file:line locations with confidence ratings.

---
