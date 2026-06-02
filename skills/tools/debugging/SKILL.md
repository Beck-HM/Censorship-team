---
name: debugging
description: Structured bug investigation process. Reproduce, isolate root cause, fix, and verify with regression tests.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

When something is broken, don't guess. Follow a repeatable process to find the root cause, fix it, and confirm it stays fixed.

## When to Use

- The user reports unexpected behavior or errors
- A test is failing and the reason isn't obvious
- The user says "X used to work but now it doesn't"
- Build/compilation errors that aren't straightforward

## Process

### Phase 1: Reproduce

1. Ask the user for exact steps to reproduce, or the exact error message.
2. If they have a reproduction scenario, try to run it or trace through the code.
3. Use the `question` tool: "I understand the issue is [description]. Let me investigate. Shall I start tracing the code path?" Options: "Yes, investigate" / "Let me clarify".

Report: "Reproduction confirmed at [location]."

### Phase 2: Isolate

Narrow down the root cause systematically:

1. **Identify the failing component**: Which module/function produces the incorrect output?
2. **Trace the input**: What data entered this component? Is it valid?
3. **Check assumptions**: What preconditions does this code assume? Are they met?
4. **Binary search**: If the code path is long, check the midpoint to determine which half contains the bug.

For each check, use the `question` tool to report findings and ask "Shall I continue narrowing down?" before proceeding.

Report: "Root cause identified at [file:line]. [explanation of what went wrong and why]."

### Phase 3: Fix

1. Determine the minimal fix — don't refactor unrelated code during debugging.
2. Use the `question` tool: "The root cause is [explanation]. My proposed fix: [description]. Shall I apply it?" Options: "Yes, apply the fix" / "I have a different fix in mind" / "Let me review the code first".
3. Apply the fix using the `edit` tool.

Report: "Fix applied. Changed [file:line]: [summary of change]."

### Phase 4: Verify

1. Run the relevant tests:
   - The specific test that was failing (if any)
   - The module's test suite
   - A broad test to check for regressions
2. Use the `question` tool to report results: "Tests [passed/failed]. Any edge cases I should check?"
3. If the user suggests edge cases, test them.
4. If tests fail, go back to Phase 2 — the fix may be incomplete or wrong.

Report: "Verification complete. [N] tests passed, [M] edge cases checked."

### Phase 5: Prevent Regression

1. Check if there's already a test covering this exact scenario.
2. If not, use the `question` tool: "There's no test covering this bug scenario. Shall I add a regression test?" Options: "Yes, add it" / "No, skip it".
3. If yes, write a test that triggers the bug and asserts the correct behavior.
4. Run the test suite one final time.

Report: "Regression test added at [path]. All tests passing."

## Error Type Quick Reference

| Symptom | Likely Causes | First Check |
|---------|--------------|-------------|
| Crash/panic | Null pointer, out-of-bounds, type error | Input validation at crash site |
| Wrong output | Logic error, wrong branch taken | Trace the data transformation |
| Performance | Infinite loop, N+1 query, missing index | Loop boundaries, query count |
| Build error | Missing dependency, version mismatch, syntax | Error message, package config |
| Race condition | Shared state, missing lock, wrong ordering | Concurrent access points |
| Test flaky | Shared test state, time dependency, ordering | Test isolation, mocks |

## Constraints

- Fix the bug, nothing else. Resist the urge to refactor.
- Always verify the fix before declaring done.
- Do NOT modify production code without user approval via the `question` tool.
