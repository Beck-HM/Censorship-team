---
name: test-writing
description: Testing strategies, mock patterns, and coverage targets by language and framework
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides strategies for writing comprehensive tests — covering unit, integration, and edge cases — adapted to the project's language, framework, and existing test patterns.

## Test Types and Priorities

| Priority | Test Type | What to Test | When to Write |
|----------|-----------|-------------|---------------|
| P0 | Unit tests | Core business logic, utility functions | Always |
| P1 | Edge cases | Null/None, empty, boundary values, error inputs | Always |
| P2 | Integration | Module interactions, data flow paths | Critical flows |
| P3 | Error handling | Failed operations, exceptions, error states | Public APIs |
| P4 | Regression | Previously fixed bugs | After bug fixes |

## Language-Specific Framework Detection

| Language | Look for in config/source | Fallback framework |
|----------|-------------------------|-------------------|
| TypeScript | `jest.config*`, `vitest.config*`, `*.test.ts`, `*.spec.ts` | Vitest |
| JavaScript | `jest.config*`, `*.test.js`, `*.spec.js`, `mocha`, `ava` | Jest |
| Python | `pytest.ini`, `pyproject.toml` [tool.pytest], `conftest.py`, `test_*.py` | pytest |
| Rust | `#[cfg(test)]`, `#[test]` in source, `tests/` directory | built-in test harness |
| Go | `*_test.go` alongside source | `go test` |
| Java | `pom.xml` (JUnit), `build.gradle` (JUnit/TestNG) | JUnit 5 |
| C# | `.csproj` (xUnit/NUnit/MSTest), `*Test.cs` | xUnit |
| Ruby | `Gemfile` (rspec/minitest), `*_spec.rb` | RSpec |

## Writing Tests: Templates

### Unit Test Template
```
// Name: <function/module>_<scenario>_<expected>
// Given: <precondition>
// When: <action>
// Then: <assertion>

[Test]
public void CalculateTotal_WithDiscount_AppliesDiscountPercentage() {
    // Arrange
    // Act
    // Assert
}
```

### Edge Case Coverage Checklist
For every function that accepts inputs, test:
- [ ] Zero / empty input
- [ ] Single element (boundary)
- [ ] Maximum expected value
- [ ] Negative / invalid values
- [ ] Null / None / undefined
- [ ] Type boundary (min int, max float, etc.)
- [ ] Malformed data (wrong format, missing fields)
- [ ] Very large input (performance/stack overflow)

### Error Case Coverage
- [ ] External service returns error
- [ ] File not found / permission denied
- [ ] Network timeout
- [ ] Rate limiting / throttling
- [ ] Invalid credentials
- [ ] Concurrent access / race condition

## Mock Strategy Guide

### What to Mock
- External services (APIs, databases, message queues)
- Time-dependent operations
- Random/non-deterministic functions
- File system operations (prefer temp dirs)
- System clock / dates

### What NOT to Mock
- Value objects / pure data
- Simple utility functions
- Language/stdlib features
- Third-party SDK wrappers (test through integration instead)

### Mocking by Language
| Language | Recommended Tool | Notes |
|----------|----------------|-------|
| TypeScript | `vi.mock()`, `jest.mock()`, `sinon` | Use Vitest/Jest built-in mocks first |
| Python | `unittest.mock`, `pytest-mock` | `mocker` fixture with pytest |
| Rust | `mockall`, manual trait impls | Traits make mocking natural |
| Go | `mockgen`, manual interfaces | Interfaces enable easy mocks |
| Java | Mockito, EasyMock | Mockito with @Mock annotation |
| C# | Moq, NSubstitute | Prefer strict mocks |

## Test Code Quality Checklist

- [ ] Tests are independent — no shared mutable state between tests
- [ ] Tests are deterministic — same result every run
- [ ] Tests are fast — unit tests complete in milliseconds
- [ ] Tests have clear names — `function_scenario_expected` or `describe/it` pattern
- [ ] Tests test behavior, not implementation — refactoring shouldn't break tests
- [ ] No conditional logic in tests — no if/switch/loop
- [ ] One assertion concept per test (may have multiple assertions on same result)
- [ ] Arrange-Act-Assert structure is visibly separated

## Coverage Targets

| Coverage Type | Minimum Target | Stretch Goal |
|---------------|---------------|--------------|
| Line coverage | 70% | 85%+ |
| Branch coverage | 60% | 80%+ |
| Public API coverage | 90% | 100% |
| Critical path coverage | 100% | 100% |

## Test File Organization

Follow the project's existing convention:
- Co-located: `user.ts` + `user.test.ts` (TypeScript/Go/Rust)
- Mirror directory: `src/` → `tests/` (Python, some Rust)
- Test package: same package as source (Go, Python)

## Verification

1. Run the full test suite before and after writing tests
2. If existing tests fail, diagnose whether it's the test or source code
3. Fix test issues only (wrong mocks, incorrect assertions)
4. Do NOT fix source code bugs — report them in the output

## Available Tools

### `test-gap` (custom tool)
- **Purpose**: compare source files against test files to find untested modules
- **When to use**: before writing tests to know exactly which modules need coverage
- **How to use**: call `test-gap` tool directly; ask the user with the `question` tool first if you're unsure
