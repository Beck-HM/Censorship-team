---
name: pipeline-orchestration
description: Decision framework and error recovery strategies for the code analysis pipeline
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides the orchestrator (code-architect) with decision-making guidance for each pipeline phase — how to handle failures, what to do when information is incomplete, and how to adapt to different project scenarios.

## Phase Decision Trees

### Phase 0 Edge Cases
- **User selects "Other" for language**: ask clarifying question about what tools/build system they use
- **User selects "Other" for project type**: probe deeper — is it a script, config generator, build tool?
- **User reports "Yes, I have more to add" but stays silent**: wait patiently, do not pressure
- **Phase 0 answers are contradictory**: e.g., says "Python" but mentions "React" — ask for clarification

### Phase 1 Exploration Decisions
- **scout-alpha or scout-beta fails to return**: retry once with more explicit instructions
- **scouts disagree on project structure**: trust the file listing over the code reading for structure
- **No config files found**: report as a finding — may indicate a non-standard project or missing tooling
- **Project is very large (>500 files)**: instruct scouts to focus on top-level modules and entry points
- **Project is very small (<10 files)**: instruct scouts to read every file

### Phase 2 Analysis Decisions
- **arch-alpha/beta reports are empty or minimal**: the scout reports may be insufficient — re-run scouts with more detail
- **Architecture doesn't match any known pattern**: describe what you see rather than forcing a label
- **Circular dependencies detected**: flag as high severity — always include in reports
- **No test files found at all**: note this prominently for Phase 3 planning

### Phase 3 Test Decisions
- **No test framework detected**: propose the most common framework for the project's language
- **Existing tests are all failing**: do not write new tests until existing ones pass — report to user
- **Test framework is unusual**: follow its conventions exactly, don't try to adapt to a standard
- **test-worker fails**: retry once with more context; if still failing, report and propose manual testing
- **User rejects test plan**: adjust based on their feedback, ask specifically what they want to change

### Phase 4 Plan Decisions
- **Architecture analysis found critical issues**: prioritize structural refactoring over cosmetic changes
- **No issues found**: still produce a plan with suggested improvements and maintenance recommendations
- **User wants to modify the plan**: accept their modifications and regenerate — do not argue
- **Test coverage is very low**: include writing tests as a high-priority step in the plan

### Phase 5 Execution Decisions
- **Conservative refactoring fails**: the change may be unsafe — report and ask user how to proceed
- **Aggressive refactoring causes 3+ test failures**: revert, switch to conservative for that module
- **Pattern refactoring doesn't fit**: revert and document why the pattern wasn't applied
- **Test suite takes >5 minutes**: still run it — do not skip verification
- **Step fails mid-way**: rollback and report, do not continue with remaining steps

## Pipeline Communication Patterns

### When Presenting to the User
- **Be concise**: 3-5 bullet points max per presentation
- **Use severity labels**: High / Medium / Low for each finding
- **Offer clear choices**: use the `question` tool, not open-ended chat
- **Include context**: remind the user what phase they're in and what comes next

### When Passing Context to Sub-Agents
Always include:
1. Phase 0 answers (language, type, framework, user notes)
2. All scout reports (for arch agents)
3. All arch reports (for test-worker)
4. Test results (for refactoring plan)

### Handling User Interruptions
- If user asks a question mid-pipeline, answer it directly, then ask "Shall I continue?"
- If user changes requirements, reset to the appropriate phase
- If user says "stop", finish the current sub-agent and wait

## Quick Mode

Quick Mode is a lighter variant of the full analysis pipeline for small to medium projects. It follows the same 5-phase structure but with fewer sub-agents, streamlined steps, and compact reporting.

Quick Mode is selected during Phase 0 by code-architect. You do not activate it yourself.

### Phase 1 — One Scout

Dispatch **one** scout instead of two. Use your judgment to pick:

- **scout-alpha** (project structure): better when you need build config, file layout, project conventions
- **scout-beta** (source code): better when you need code patterns, naming, module responsibilities

Selection guidance:
- For well-known frameworks (React, Django, Spring Boot) the structure is predictable → scout-beta is often more useful
- For unfamiliar or custom project types → scout-alpha first to understand layout
- When unsure → scout-alpha (structure is safer context for later steps)

Include Phase 0 answers and size scan data.

### Phase 2 — One Architecture Agent

Pass the scout report to **one** architecture agent:

- **arch-alpha** (structural): dependency graph, module boundaries, layer violations
- **arch-beta** (logical): data flow, state management, component communication

Selection guidance:
- Complex module dependencies or architectural concerns → arch-alpha
- Data-heavy, event-driven, or complex state → arch-beta
- When unsure → arch-alpha (structural data is more objective)

### Phase 3 — Test Plan + Direct Run

Present a test plan to the user (same format as full pipeline). If approved:

- Do NOT dispatch test-worker
- Use `glob` to find test files matching the project's test patterns
- Run tests directly using the project's test command (detect from config, or ask the user)

Report results compactly:
```
Tests: X passed, Y failed, Z skipped
Command: <test command>
```

### Phase 4 — Compact Plan

Before writing the plan, use the `question` tool: header "Project Breakdown", question "Would you like to load project-deconstruction for a detailed narrative of how this project runs? (startup sequence, data flow, dependencies, critical paths)", options: "Yes, show me the breakdown" / "No, just the plan".

- If "Yes": call `skill({ name: "project-deconstruction" })` and follow its process, then append the breakdown to the plan.
- If "No": skip.

Write a refactoring plan with 3-5 items maximum. Include a brief **Design & Architecture Notes** block after the plan covering design layer, architecture layer, and long-term lens — 1-2 lines per layer.

```
## Plan
1. <action> — <file> — <risk>
2. <action> — <file> — <risk>
3. <action> — <file> — <risk>

### Design & Architecture Notes
**Design**: <1-2 lines>
**Architecture**: <1-2 lines>
**Long-Term**: <1-2 lines>
```

Present to user for approval (same question gate as full pipeline).

### Phase 5 — Execute

Same as full pipeline: one step at a time, test after each, report results.

### Boundary Cases

- **Scout or arch returns empty/minimal results**: retry once with more explicit instructions. If still empty, note the gap and continue — do not escalate.
- **Tests fail during verification**: report results, then use `question` tool: "Tests failed. Would you like to switch to the full pipeline for deeper investigation?" — do not force.
- **User changes their mind**: if the user says "this needs more detail" mid-process, acknowledge and suggest switching to the full pipeline.

## Pipeline State & Resume

The pipeline saves its progress to `.opencode/state/pipeline-state.json` at every save point. If the session is interrupted (closed terminal, timeout, crash, network loss), the next session can resume from where it left off.

### State File Overview

- **Location**: `.opencode/state/pipeline-state.json` (project root)
- **Format**: JSON with fields for phase number, Phase 0 answers, size scan, reports status, and Phase 5 step counter
- **Managed by**: code-architect saves at each save point and deletes on completion

### Resume Flow

1. code-architect detects the state file at startup and asks the user: "I found an interrupted pipeline at Phase X. Resume?"
2. If the user says yes, code-architect reads the file, restores saved data, and jumps to the saved phase.
3. If the user says no, the state file is deleted and a new pipeline starts fresh.

### Saved Data and How to Use It

| Saved data | Restore to |
|-----------|-----------|
| phase_0 (language, type, framework, context) | Pass to all sub-agents — no need to re-ask the user |
| size_scan (files, lines, test_ratio) | Reuse for context — no need to re-scan |
| mode (quick / full) | Continue in the correct mode |
| reports.scout / arch / test / plan | Skip already-completed phases |
| phase_5_step, phase_5_total | Continue from the next incomplete step |

### Resume by Phase

**Phase 0 → Phase 4 resume**: all saved data is available directly. Jump to the saved phase and continue as normal — no special handling needed.

**Phase 5 resume (mid-execution)**: the state file records which step was last completed. Start from `phase_5_step + 1`. Re-run the test suite first to confirm the last step didn't leave the project in a broken state. If tests fail, report to the user and ask how to proceed before continuing.

**Full Analysis Mode (FA4) resume**: the state file notes the mode is "full-analysis". The report was already delivered — inform the user that the analysis was completed and offer to re-run or start a new task.

### Edge Cases

- **State file exists but the project path has changed**: detect by comparing the saved `project_path` with the current working directory. If different, ask: "The state file is from a different project. Delete it and start fresh?" with "Yes, delete" / "No, keep it".
- **State file is corrupted or unreadable**: delete it automatically, inform the user, and start fresh.
- **State file exists but the user wants to do something unrelated**: the resume question comes before Intent Dispatch. If the user declines resume, the file is deleted and normal flow continues.

## Quality Gates

Before advancing to the next phase, verify:
- Phase 0 → Phase 1: ✅ All 4 questions answered
- Phase 1 → Phase 2: ✅ Both scout reports complete (full) / one scout report complete (Quick Mode)
- Phase 2 → Phase 3: ✅ Both arch reports complete + user approved test plan (full) / one arch report complete + user approved test plan (Quick Mode)
- Phase 3 → Phase 3.5: ✅ test-worker results received (full) / test results received (Quick Mode)
- Phase 3.5 → Phase 4: ✅ User approved proceeding to plan
- Phase 4 → Phase 5: ✅ User explicitly approved the refactoring plan
- Phase 5 → Done: ✅ All steps executed, tests passing
