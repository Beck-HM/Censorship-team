---
name: writing-plans
description: Break approved designs or feature requests into executable implementation tasks with file paths, code snippets, and verification steps.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

Once a design is approved (or a clear requirement exists), turn it into a concrete implementation plan. Each task should be small enough to complete in one sitting and have clear acceptance criteria.

## When to Use

- After brainstorming produces an approved design
- Before entering the code-architect pipeline's execution phase
- The user says "I know what I want, help me plan it out"
- The task involves multiple steps and you need an ordered plan

## Process

### Step 1: Collect Context

First, gather everything you need:
- The approved design summary (if brainstorming was used)
- The current project structure (run `glob` or check directory)
- List of existing related files

Use the `question` tool: "I'm going to create an implementation plan. I have [context summary]. Is there anything else I should know before I start?" Options: "Go ahead" / "Let me add more context".

### Step 2: Break Down Work

Decompose the work into tasks. Each task must be:
- **Self-contained**: does one thing
- **Small**: 2-10 minutes of coding (if you think it'll take longer, split it)
- **Verifiable**: has a clear way to check it's done
- **Independent**: depends on earlier tasks but doesn't create unnecessary coupling

For each task, specify:
- **Task title**: what to do
- **Files**: exact file paths to create or modify
- **What to change**: brief description of the implementation
- **Verification**: how to check it's correct (test command, manual check, etc.)

### Step 3: Order Tasks

Arrange tasks in dependency order:
- Foundation first (types, interfaces, data structures)
- Core logic next (business logic, algorithms)
- Integration after (connecting components)
- Tests throughout (TDD: write test before code)
- Polish last (error messages, edge cases, docs)

### Step 4: Present Plan

Present the full plan to the user:

```
## Implementation Plan: <title>
**Total tasks**: <N>
**Estimated effort**: <small / medium / large>

### Task 1: <title>
**Files**: <path>
**What**: <description>
**Verify**: <command or assertion>

### Task 2: <title>
...
```

Use the `question` tool: header "Implementation Plan", question "Here's the plan. Shall I start executing?", options: "Yes, execute" / "Let me review tasks" / "Modify the plan".

- If "Let me review tasks", go through each task and ask for feedback.
- If "Modify the plan", take their input and regenerate.
- If "Yes, execute", proceed to execution. If the code-architect pipeline is available, suggest loading it for structured execution.

## Task Sizing Guidelines

| Size | Criterion | Example |
|------|-----------|---------|
| Too small | Trivial rename/format | Combine with adjacent task |
| Just right | One function, one concern | "Add validate() to User class" |
| Too big | Spans 3+ files or changes behavior | Split into subtasks |
| Way too big | Changes architecture | Go back to brainstorming |

## Template

```
## Task: <action> on <target>
- **Depends on**: <task numbers>
- **Files**: <paths>
- **Implementation**:
  `<code or description>`
- **Verify**: `<command>`
```

## Constraints

- Do NOT start implementation during planning. This is plan-only.
- If a task feels too vague to estimate, flag it for clarification.
- Keep the plan visible — the user needs to approve before execution starts.
