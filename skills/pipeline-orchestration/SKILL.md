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

## Quality Gates

Before advancing to the next phase, verify:
- Phase 0 → Phase 1: ✅ All 4 questions answered
- Phase 1 → Phase 2: ✅ Both scout reports complete
- Phase 2 → Phase 3: ✅ Both arch reports complete + user approved test plan
- Phase 3 → Phase 3.5: ✅ test-worker results received
- Phase 3.5 → Phase 4: ✅ User approved proceeding to plan
- Phase 4 → Phase 5: ✅ User explicitly approved the refactoring plan
- Phase 5 → Done: ✅ All steps executed, tests passing
