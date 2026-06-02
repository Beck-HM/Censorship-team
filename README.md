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
- [General-Purpose Skills](#general-purpose-skills)
- [Custom Tools](#custom-tools)
- [Full Analysis Mode](#full-analysis-mode)
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
│ Level 4: Analysis / refactor           │ → full analysis mode OR Phase 0-5
│ Level 5: Cannot determine              │ → ask: "what do you need?"
└────────────────────────────────────────┘
```

**Key rule**: When in doubt, ask. Never guess the user's intent.

---

## Agents

10 agents in total. The first 9 form a pipeline; the 10th is the installer.

### Primary

#### `code-architect`
The only agent that talks to the user directly. Routes every message through a 5-level intent dispatch before taking any action — casual chat, simple edit, skill suggestion, project analysis, or refactoring pipeline. Orchestrates the full pipeline by dispatching sub-agents via the `task` tool and synthesising their results. Never modifies files without explicit user approval.

- **File**: `agents/code-architect.md`
- **Mode**: primary
- **Access**: read, glob, grep, edit, bash, task, question; skills: pipeline-orchestration, code-review, debugging, brainstorming, writing-plans, progress-tracker

---

### Exploration (Phase 1)

#### `scout-alpha`
Maps the project's physical structure. Walks the directory tree, identifies build configuration files, detects the module layout, and catalogues entry points. Produces a structural map that downstream agents use to understand where code lives.

- **File**: `agents/scout-alpha.md`
- **Color**: `#10b981`
- **Output**: directory tree, config files, build targets, file-type breakdown
- **Invoked by**: code-architect Phase 1 (runs in parallel with scout-beta)

#### `scout-beta`
Explores source code organisation and conventions. Identifies naming patterns, file header conventions, import/export style, test placement conventions, and code idioms used throughout the project. Produces a stylistic profile that helps refactoring agents match the project's existing patterns.

- **File**: `agents/scout-beta.md`
- **Color**: `#34d399`
- **Output**: naming conventions, import patterns, code style observations, test layout
- **Invoked by**: code-architect Phase 1 (runs in parallel with scout-alpha)

---

### Analysis (Phase 2)

#### `arch-alpha`
Structural architecture analysis. Builds a dependency graph between modules, identifies layer boundaries, detects circular dependencies, and flags architectural violations (e.g., low-level modules importing high-level ones). Produces a module dependency map and coupling analysis.

- **File**: `agents/arch-alpha.md`
- **Color**: `#f59e0b`
- **Output**: dependency graph, coupling metrics, layer violations, circular dependency report
- **Invoked by**: code-architect Phase 2 (runs in parallel with arch-beta)

#### `arch-beta`
Logical and data-flow analysis. Traces how data moves through the system, identifies state management approaches, maps critical execution paths, and highlights areas where data ownership is unclear or shared mutable state creates risk. Produces a data flow map and critical path analysis.

- **File**: `agents/arch-beta.md`
- **Color**: `#f97316`
- **Output**: data flow diagram, state ownership map, critical paths, concurrency risks
- **Invoked by**: code-architect Phase 2 (runs in parallel with arch-alpha)

---

### Testing (Phase 3)

#### `test-worker`
Writes and runs tests. Given the architecture reports, produces a detailed test plan covering unit tests, integration tests, edge cases, and error cases for each module. After user approval, writes the test files using the project's existing test framework and conventions, runs them, and reports results.

- **File**: `agents/test-worker.md`
- **Color**: `#ec4899`
- **Output**: test plan document, new test files, test run results
- **Invoked by**: code-architect Phase 3 (after user gate approval)

---

### Refactoring (Phase 5)

#### `refactor-conservative`
Makes minimal, safe changes one step at a time. Preserves existing behaviour, public API, and code structure. Suitable for targeted fixes, small extractions, and renaming. Each change is followed by running the test suite. If a step breaks tests, it rolls back and reports.

- **File**: `agents/refactor-conservative.md`
- **Color**: `#3b82f6`
- **Scope**: single-function or single-module changes, renames, extractions
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

#### `refactor-aggressive`
Performs large-scale renovation. Eliminates anti-patterns, splits monolithic modules, modernises legacy code, and restructures cross-cutting concerns. Operates across multiple files and modules. Each step is still tested, but the risk tolerance is higher — the agent expects test failures and fixes them before moving on.

- **File**: `agents/refactor-aggressive.md`
- **Color**: `#ef4444`
- **Scope**: multi-module changes, architectural restructuring, tech debt elimination
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

#### `refactor-pattern`
Applies design patterns to improve structure. Identifies where a pattern (Strategy, Factory, Observer, Adapter, etc.) solves a concrete code smell and implements it. Unlike aggressive refactoring, this agent follows a specific pattern recipe rather than free-form restructuring.

- **File**: `agents/refactor-pattern.md`
- **Color**: `#8b5cf6`
- **Scope**: pattern introduction or migration (Strategy → enum dispatch, Observer → event bus, etc.)
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

---

### Model configuration

#### `installer`
Sets up the package's model configuration. Guides the user through assigning models to each agent, writes the configuration file, and verifies that Python and Node.js are available. Passive agent — never invoked automatically. The user must explicitly call `@installer`.

- **File**: `agents/installer.md`
- **Color**: `#f59e0b`
- **Mode**: primary
- **Invoked**: manually by the user only

---

### How sub-agents are invoked

code-architect dispatches sub-agents via the `task` tool. Each sub-agent works autonomously with its own skill context. The results are collected and synthesised by code-architect.

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (parallel)
  ├── Phase 2: task arch-alpha + task arch-beta (parallel)
  ├── Phase 3: task test-worker
  └── Phase 5: task refactor-* (sequential, one per step)
```

---

## Pipeline

code-architect runs a standard pipeline for code review and refactoring tasks. Each phase has a specific purpose and most have user gates.

```
Phase 0     Project Assessment ─── "what language/framework/context?"
   │
Phase 1     Project Exploration ─── scouts explore structure + code
   │
Phase 2     Architecture Analysis ─── arch agents analyse deps + data flow
   │              ┌────────────────────────────┐
Phase 3     Test  │  user gate: review plan     │
            │     │  "Shall I proceed?"         │
            │     └────────────────────────────┘
   │
Phase 3.5   Post-Test Review ─── "Ready for the refactoring plan?"
   │              ┌────────────────────────────┐
Phase 4     Plan  │  user gate: approve plan    │
            │     │  "Shall I execute?"         │
            │     └────────────────────────────┘
   │
Phase 5     Execute refactoring ─── step by step, test after each
```

### Intent Dispatch (always runs first)

| Level | Matches | Behaviour |
|-------|---------|-----------|
| 1 | Greetings, casual chat | Short reply, no action |
| 2 | "rename X", "change Y", "add comment" | Execute directly |
| 3 | "bug", "explore", "plan", "track" | Ask to load relevant skill |
| 4A | "full analysis", "scan project", "explore project" | Enter Full Analysis Mode |
| 4B | "review", "audit", "refactor", "optimise" | Enter Phase 0 pipeline |
| 5 | Ambiguous | Ask user what they need |

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

---

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
FA4: Produce comprehensive report ─── overview, structure, architecture,
     data flow, test coverage, risk assessment
FA5: Recommend next steps ─── suggest skills based on findings
```

**Key differences from the standard pipeline**:
- No Phase 0 (single question instead of four)
- No user gates at test/plan stages
- No refactoring plan
- No code modification — read-only

**Expected token cost**: ~25K tokens (vs ~50K for the full pipeline).

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

---
