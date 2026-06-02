---
name: aggressive-refactoring
description: Code smell detection guide and large-scale modernization patterns
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides guidance for aggressive, large-scale refactoring — identifying code smells, eliminating anti-patterns, and modernizing legacy code.

## Priority Smells to Eliminate

### 1. Duplicated Code
- **Detection**: use grep to find similar code blocks, or manual pattern recognition
- **Fix**: extract shared logic into a function/module, parameterize differences
- **Threshold**: 3+ lines duplicated in 2+ places → extract
- **Warning**: don't over-extract — if parameters differ too much, the duplication may be coincidental

### 2. Long Function
- **Detection**: any function over 30-50 lines
- **Fix**: extract logical groups of statements into named functions
- **Heuristic**: if you need a comment to describe a block, that block should be a function
- **Goal**: each function does ONE thing at ONE level of abstraction

### 3. Large Class / Module
- **Detection**: class over 300 lines, or with more than 10 methods
- **Fix**: split by responsibility, extract delegate classes
- **Question to ask**: "What is this class's single responsibility?"

### 4. Shotgun Surgery
- **Detection**: a single change requires modifying 5+ files
- **Fix**: consolidate the changed logic into one module
- **Example**: changing validation rules scattered across controllers → extract a validation module

### 5. Feature Envy
- **Detection**: a method in class A heavily uses data/methods of class B
- **Fix**: move the method (or parts of it) to the class it's envious of
- **Sign**: more `a.b` calls than `self`/`this` references

### 6. Switch / If-Else Chains Over Types
- **Detection**: `if type == "A"` / `switch(type)` blocks repeated across the codebase
- **Fix**: replace with polymorphism, strategy pattern, or language-appropriate dispatch (e.g., pattern matching)
- **Rule of thumb**: if you add a new type and must update 3+ switch statements, refactor

### 7. Mutable Global State
- **Detection**: global variables, singletons with mutable state, static mutable collections
- **Fix**: pass state explicitly, use dependency injection, or make immutable and return new instances
- **Priority**: higher for multi-threaded / async projects

### 8. Deep Nesting / Callback Hell
- **Detection**: 3+ levels of nesting (if inside loop inside callback)
- **Fix**: early returns, guard clauses, async/await, pipeline/chaining
- **Goal**: flatten to 2 levels max

## Modernization Patterns

### Language Feature Migration
| Legacy | Modern | Benefit |
|--------|--------|---------|
| Callbacks | `async`/`await` | Readable, linear flow |
| `for` loops | `.map()`, `.filter()`, `.reduce()` | Declarative, fewer bugs |
| Manual null checks | Optional chaining `?.` | Concise, safe |
| `var` | `const`/`let` | Block scoping |
| Constructor functions | Classes | Clearer OOP |
| `==` | `===` | Type-safe comparison |
| Prototype | `class` syntax | Standard OOP |
| Nested conditionals | Guard clauses | Flatter, clearer |
| String concatenation | Template literals / f-strings | Readable |
| `Any`/`Object` | Generics/templates | Type safety |

### Architecture Migration
| From | To | When |
|------|----|------|
| Inline SQL | ORM / query builder | Complex queries |
| Direct calls | Repository pattern | Multiple data sources |
| Static methods | Dependency injection | Testability needed |
| Global state | State management store | Complex state |
| Monolithic | Modular | Beyond 10K LOC |
| Synchronous | Async | I/O-bound operations |

## Workflow for Aggressive Refactoring

1. **Scan**: read the target module thoroughly — understand all code paths
2. **Plan**: identify the new structure, interfaces, and organization
3. **Execute in chunks**: one logical transformation at a time
4. **Test after each chunk**: no exceptions
5. **Fail-safe**: if tests break catastrophically, revert the chunk and escalate to conservative approach
6. **Document**: note any intentional behavioral changes (rare)

## Safety Valve

If aggressive refactoring causes **3 consecutive test failures**:
- Stop immediately
- Revert the last 3 changes
- Recommend using the conservative agent for the remaining work
- Report which areas need conservative treatment

## Measuring Success

| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Lines per function | >50 | <30 | <20 |
| Nesting depth | >3 | <3 | <2 |
| Duplicate blocks | >5 | <2 | 0 |
| Module coupling | High | Low | Minimal |
| Test pass rate | — | — | 100% |

## Available Tools

### `complexity` (custom tool)
- **Purpose**: identify the longest and most deeply nested functions — prime candidates for aggressive refactoring
- **When to use**: at the start of refactoring to prioritize targets
- **How to use**: call `complexity` tool directly; ask the user with the `question` tool first if you're unsure

### `duplicate-lines` (custom tool)
- **Purpose**: detect cross-file duplicate or near-duplicate code blocks
- **When to use**: to find duplicated code that should be extracted into shared functions
- **How to use**: call `duplicate-lines` tool directly; ask the user with the `question` tool first if you're unsure
