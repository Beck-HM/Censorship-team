---
name: project-deconstruction
description: Reads analysis reports and source code to produce a narrative breakdown of how the project runs — startup, data flow, dependencies, critical paths.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

After the standard analysis (scout, arch, tests) is complete, this skill produces a narrative "how this project runs" appendix. It does not re-analyse — it reads existing reports and key source files, then explains the project's runtime behaviour in plain terms.

## When to Use

- The user wants to understand how the project works, not just its structure
- After Full Analysis (FA4) or Refactoring Plan (Phase 4) — offered as an optional supplement
- The user asks "how does this project actually run?" or "explain the architecture"

## Input

This skill expects:
- Phase 0 answers (language, type, framework)
- Scout reports (structure, code patterns)
- Architecture reports (dependencies, data flow)
- Test results (if available)
- Project source code (for reading key files)

## Process

### Step 1: Understand the Project Type

Read Phase 0 answers. Know the project type — web backend, CLI tool, library, mobile app, etc. This shapes what kind of narrative to write.

### Step 2: Read Existing Reports

Review all available scout, arch, and test reports.

### Step 3: Trace the Runtime

Based on the project type and framework, think about how this kind of project typically runs:

- Where does execution start?
- What initialises in what order?
- How does data flow through the system?
- What are the key module dependencies?
- What external systems does it touch?

Use `glob` and `read` on the relevant source files: entry points, config/wiring modules, key business logic files.

### Step 4: Write the Narrative

Produce 3-6 narrative paragraphs. Each covers one aspect of how the project runs:

- Start with the entry point and initialisation sequence
- Describe the main data/request/event flow
- Explain module dependencies and connections
- Note external dependencies and side effects
- Identify critical paths or hot routes
- Call out notable design decisions or risks

Use file paths and function names. Keep each paragraph to 3-8 lines. Do not repeat what the standard report already covers — this is a supplement, not a replacement.

### Step 5: Output

Append the narrative to the existing report:

```markdown
## Project Breakdown

### How It Starts
...

### Data Flow
...

### Dependencies and Side Effects
...

### Critical Paths
...
```

### Step 6: Generate ASCII Diagram

After the narrative, draw one box diagram using Unicode box-drawing characters.

Decide what to diagram based on the project type and what you learned from reading the code:

- Web backend — request lifecycle or module dependency flow
- Frontend / UI — component tree or state flow
- CLI tool — command dispatch chain
- Library / SDK — public API surface structure
- Data processing — pipeline stage flow
- Embedded / IoT — startup sequence or interrupt chain
- Game — main loop or entity lifecycle
- Other — module dependency graph

Use these characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ → ▼ ▲ ◀ ▶`

Keep the diagram compact — under 30 lines. Use the diagram to show relationships, not list every file.

Append it after the narrative paragraphs under a `### Diagram` heading.

## Constraints

- Do NOT re-analyse the project — use existing reports and targeted file reads only.
- Do NOT write narrative for areas you can't verify from source code or reports.
- If there isn't enough information to trace a flow, say so rather than guessing.
- Keep total narrative under 60 lines.
- Plain markdown prose — no tables.
- ASCII diagram under 30 lines, appended after narrative.
