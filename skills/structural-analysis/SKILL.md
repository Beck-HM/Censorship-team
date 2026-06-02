---
name: structural-analysis
description: Architectural pattern definitions, dependency analysis, and layer boundary detection
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides the knowledge to analyze a project's structural architecture — how modules are organized, how they depend on each other, and where architectural boundaries exist.

## Common Architectural Patterns

### Layered Architecture
- **Presentation layer**: UI components, controllers, views
- **Application layer**: use cases, orchestration, DTOs
- **Domain layer**: business logic, entities, value objects
- **Infrastructure layer**: databases, external APIs, file system, messaging
- **Smell**: UI logic leaking into domain, or domain logic in infrastructure

### Clean Architecture / Hexagonal
- Core domain is framework-independent
- Ports (interfaces) defined in core, adapters in outer layers
- Dependency rule: outer layers depend on inner layers, never inward
- **Smell**: framework imports in domain layer, port implementations leaking into core

### MVC (Model-View-Controller)
- **Model**: data and business logic
- **View**: presentation / UI rendering
- **Controller**: handles input, coordinates model and view
- **Smell**: fat controllers (business logic in controllers), anemic models

### Feature-Based / Module-Based
- Each feature is self-contained with its own components, services, tests
- Shared code goes into a common/shared module
- **Smell**: cross-feature dependencies, shared module becoming a dumping ground

### Event-Driven / CQRS
- Commands (writes) vs Queries (reads) separated
- Events for communication between aggregates/services
- Event bus, event handlers, event store
- **Smell**: commands doing query work, events used for tight coupling

## Dependency Analysis

### Metrics to Compute
- **Fan-in**: number of modules that import this module (high = utility/core module)
- **Fan-out**: number of modules this module imports (high = coordinator/controller)
- **Instability**: fan-out / (fan-in + fan-out) — 0 = stable, 1 = unstable
- **Abstractness**: ratio of abstract types to total types

### Smells to Flag
- **Circular dependency**: A imports B, B imports A (or longer cycle)
- **Hub module**: one module with excessively high fan-in and fan-out
- **Deep chain**: A → B → C → D → E (more than 3-4 levels suggests indirection)
- **God module**: single module with too many responsibilities
- **Dependency inversion violation**: high-level module depending on low-level concrete implementation
- **Scope creep**: imports from too many different unrelated modules

## Layer Boundary Detection

### How to Detect Boundaries
1. Look at import statements — what layers do they cross?
2. Check if UI/presentation code imports data access code directly
3. Look for framework annotations/imports in domain logic
4. Identify whether modules depend on abstractions or concrete implementations

### Healthy vs Unhealthy

| Pattern | Healthy | Unhealthy |
|---------|---------|-----------|
| Layer crossing | UI → App → Domain → Infra (one direction) | UI → Infra, Domain → UI |
| Abstraction | Depends on interfaces/contracts | Depends on concrete classes |
| Module size | Focused, single responsibility | One file over 500+ lines |
| Import count | 3-8 imports per file | 15+ imports from many domains |

## Entry Point Analysis

Trace how the application wires together:
- Dependency injection container or manual wiring
- Configuration loading (env, files, CLI args)
- Middleware/plugin registration
- Route/endpoint registration
- Start-up sequence — what initializes in what order

## Output Structure

Provide:
1. **Module Map**: table of modules with responsibilities
2. **Dependency Graph**: textual description of dependency relationships
3. **Layer Boundaries**: identified layers and cross-layer violations
4. **Entry Points**: how the app starts and wires together
5. **Structural Smells**: categorized issues with severity

## Available Tools

### `dependency-matrix` (custom tool)
- **Purpose**: extract import/require/use relationships, build dependency matrix, detect circular dependencies, compute fan-in/fan-out
- **When to use**: during architecture analysis to get objective coupling data
- **How to use**: call `dependency-matrix` tool directly; ask the user with the `question` tool first if you're unsure

### `complexity` (custom tool)
- **Purpose**: find the longest and most deeply nested functions in the project
- **When to use**: to identify functions that may need splitting or simplification
- **How to use**: call `complexity` tool directly; ask the user with the `question` tool first if you're unsure
