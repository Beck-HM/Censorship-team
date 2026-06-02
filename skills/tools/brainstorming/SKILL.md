---
name: brainstorming
description: Structured design discussion before coding. Clarifies requirements, explores alternatives, and produces an approved design document.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

Before writing code or entering the analysis pipeline, use this skill to make sure everyone understands what needs to be done and why. This prevents wasted work from unclear requirements.

## When to Use

- The user says "I want to..." but the goal is vague
- There are multiple possible approaches and you need to pick one
- The task is complex enough that you should plan before acting
- The user asks "What should I do about X?"

## Process

### Step 1: Clarify the Goal

Ask questions one at a time to understand:
- What is the actual problem being solved?
- What does success look like? (measurable outcome)
- Are there any constraints? (time, tech, compatibility, performance)
- Who is the end user or consumer of this change?

Use the `question` tool. Ask one question, wait for answer, ask the next. Don't dump all questions at once.

### Step 2: Explore Approaches

Based on the clarified goal, propose 2-3 approaches. For each:
- Brief description of the approach
- Pros and cons (keep it to 2-3 each)
- Estimated effort (small / medium / large)

Use the `question` tool: "Here are a few approaches I see. Which direction feels right?" with options naming each approach plus "I have a different idea".

### Step 3: Dig Into Details

Once an approach is selected, explore the details:
- What files/modules will be touched?
- What's the rough order of operations?
- Are there any risks or unknowns?
- Do we need to add tests first?

Use `question` tool to confirm each point. Don't move forward if key details are still unclear.

### Step 4: Produce Design Summary

Output a brief design document:

```
## Design: <title>
**Problem**: <one line>
**Approach**: <selected approach>
**Files affected**: <list>
**Steps**: <ordered list>
**Risks**: <list>
```

Present this to the user. Use the `question` tool: header "Design Approval", question "Does this design look good? Shall I proceed?", options: "Yes, proceed" / "Let me adjust" / "Start over".

- If "Let me adjust", make changes and show again.
- If "Start over", go back to Step 1.
- If "Yes, proceed", output the design summary and tell the user they can now proceed to implementation. If this is for a refactoring task, suggest loading the code-architect pipeline.

## Constraints

- Do NOT write any code during brainstorming — this is a planning-only phase.
- Keep questions concise. Don't write walls of text.
- If the user has a clear goal and just wants execution help, skip brainstorming and proceed directly.
