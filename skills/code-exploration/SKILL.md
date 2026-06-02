---
name: code-exploration
description: Source code reading strategies and naming conventions by language and framework
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides strategies for reading and understanding source code in unfamiliar projects, adapting to the project's language, type, and framework.

## Reading Order by Priority

When exploring a large project, read files in this order:

1. **Entry points** — `main.rs`, `main.py`, `index.ts`, `App.tsx`, `cmd/`, `bin/`
2. **Core types/models** — Where the primary data structures are defined
3. **API layer / routes** — How the system exposes its functionality
4. **Business logic / services** — The core domain logic
5. **Data access layer** — Database, filesystem, external API calls
6. **Utilities / helpers** — Shared infrastructure

## Module Analysis Template

For each module you read, document:
- **Responsibility**: one-line purpose
- **Key exports**: classes, functions, types, constants
- **Imports**: which other modules it depends on (to build dependency graph)
- **Code patterns**: OOP vs functional, error handling style, async model

## Language-Specific Reading Strategies

### TypeScript / JavaScript
- Start with `package.json` scripts and `tsconfig.json` paths
- Check for barrel files (`index.ts`) to understand module exports
- Look at component props/types first in React projects
- Identify the state management pattern: Redux, Zustand, Context, or local

### Python
- Start with `__init__.py` to see public API of packages
- Check type annotations — they reveal expected interfaces
- Look for decorators to understand framework integration
- Identify the async model: `asyncio`, `threading`, or sync

### Rust
- Start with `lib.rs` or `main.rs` module declarations
- Check `Cargo.toml` features to understand conditional compilation
- Look at trait definitions for abstraction boundaries
- Identify ownership patterns: borrowed vs owned data flow
- Check unsafe blocks carefully

### Go
- Start with `main.go` or `cmd/` entry points
- Look at interface definitions for contract boundaries
- Check for the `error` return pattern — always handle errors
- Identify the concurrency model: goroutines, channels, mutexes

## Naming Convention Quick Reference

| Language | Convention | Examples |
|----------|-----------|----------|
| TypeScript/JS | camelCase for variables/functions, PascalCase for classes/types, kebab-case for files | `getUser()`, `UserProfile`, `user-profile.ts` |
| Python | snake_case for everything, PascalCase for classes | `get_user()`, `UserProfile`, `snake_case.py` |
| Rust | snake_case for functions/vars, PascalCase for types/traits, SCREAMING_SNAKE for constants | `get_user()`, `UserProfile`, `MAX_SIZE` |
| Go | camelCase for unexported, PascalCase for exported, snake_case for file names | `getUser()`, `GetUser()`, `user_profile.go` |
| Java | camelCase for methods/vars, PascalCase for classes | `getUser()`, `UserProfile` |
| C# | PascalCase for everything public, camelCase for private | `GetUser()`, `UserProfile` |

## Pattern Detection Guide

Look for these patterns during exploration and note their presence/absence:

- **Error handling**: try/catch, Result type, error monad, panic, exception hierarchy
- **Async model**: async/await, promises, callbacks, threads, goroutines, green threads
- **State management**: Redux, Zustand, Context, MobX, Vuex/Pinia, signals, observable
- **Dependency injection**: constructor injection, DI container, manual wiring, service locator
- **Testing approach**: Jest, Vitest, pytest, Go test, JUnit, doctest, integration vs unit

## Output Rules

- Do NOT read every file — focus on representative samples from each module
- For large projects, prioritize: entry points > core modules > utilities > config
- Group findings by module and provide a summary table

## Available Tools

### `find-orphans` (custom tool)
- **Purpose**: find source files that are not imported by any other project file (potential dead code)
- **When to use**: while exploring modules to identify potentially unused files
- **How to use**: call `find-orphans` tool directly; ask the user with the `question` tool first if you're unsure
