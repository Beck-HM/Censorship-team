---
name: code-review
description: Language-agnostic code review covering security, performance, error handling, code style, type/contract safety, test coverage, and architecture. Use when asked to review, audit, inspect, assess, or check code quality in any language.
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## What This Skill Does

Provides a structured code review checklist across 7 dimensions. These principles apply to any programming language. Adapt the specifics (syntax, idioms, tooling) to the project's language.

## Review Checklist

### 1. Security
- Injection attacks: are user inputs properly sanitized or parameterized (SQL, command injection, etc.)?
- Cross-Site Scripting (XSS): is user-supplied data escaped before rendering in web contexts?
- Sensitive data exposure: are secrets, tokens, PII, or credentials kept out of logs, client bundles, and source code?
- Input validation: are all external inputs validated for type, length, range, and format?
- Authorization: are operations protected by proper access control?
- Dependencies: are there known-vulnerable packages in the dependency tree?

### 2. Performance
- Algorithmic efficiency: are there nested loops or O(n^2) operations that could be optimised?
- Memory usage: are large objects retained unnecessarily? Are there resource leaks?
- I/O and concurrency: are I/O operations batched or parallelised where possible?
- Bundle / binary size: are there unused imports or heavy dependencies that could be replaced with lighter alternatives?
- Caching: are expensive or repeated computations cached appropriately?

### 3. Code Style & Consistency
- Naming conventions: do identifiers follow the project's naming conventions?
- File organization: is each file focused on a single responsibility?
- Dead code: are there unused variables, parameters, imports, or unreachable branches?
- Magic values: are hardcoded numbers and strings extracted into named constants?
- Comments: are comments accurate, necessary, and not stating the obvious?

### 4. Error Handling
- Error boundaries: are there proper error-handling constructs around fallible operations (try/catch, Result types, etc.)?
- Unhandled failures: are all async operations, promises, futures, or callbacks handled?
- Edge cases: are null, None, nil, empty collections, zero, and falsy values handled explicitly?
- Error messages: are errors descriptive enough for debugging but not leaking internals?
- Graceful degradation: does the application handle failures, missing features, or offline states gracefully?

### 5. Type & Contract Safety
- Type misuse: are there avoidable dynamic types, loose casts, or unchecked type assumptions?
- Contracts: are function preconditions, postconditions, and invariants documented or enforced?
- Generics / templates: could utility code be made safer and more reusable with proper generic constraints?
- Runtime type mismatch: are types from external sources (API responses, file I/O, user input) validated at runtime?
- Language strict mode: is the language's strictest settings enabled (e.g. strict mode, warnings as errors)?

### 6. Test Coverage
- Missing tests: are there untested public functions, components, or modules?
- Assertion quality: do tests assert meaningful behaviour, not just that no error was thrown?
- Edge coverage: are boundary conditions, error states, and empty states covered?
- Test maintainability: are tests readable and isolated? Do they rely on implementation details?
- Test reliability: are tests deterministic, or do they have flaky dependencies (time, network, order)?

### 7. Architecture & Design
- Coupling: are modules tightly coupled? Could interfaces or dependency injection reduce coupling?
- Single Responsibility: do functions, classes, and modules have one clear responsibility?
- Dependency direction: do high-level modules depend on abstractions, not concrete details?
- Abstraction level: is the right amount of abstraction applied? Is the code over-abstracted or under-abstracted?
- State management: is state localised appropriately? Is global state minimal and well-structured?

## Output Format

For each review, produce a summary table:

| Dimension | Findings | Severity |
|-----------|----------|----------|
| Security | ... | High / Medium / Low |
| Performance | ... | High / Medium / Low |
| Code Style | ... | High / Medium / Low |
| Error Handling | ... | High / Medium / Low |
| Type & Contract Safety | ... | High / Medium / Low |
| Test Coverage | ... | High / Medium / Low |
| Architecture | ... | High / Medium / Low |

Follow with action items sorted by severity. Do not modify files unless the user explicitly asks for fixes.
