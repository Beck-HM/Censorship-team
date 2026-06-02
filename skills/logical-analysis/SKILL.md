---
name: logical-analysis
description: Data flow analysis, state management patterns, and component communication strategies
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides the knowledge to analyze a project's logical architecture — how data flows through the system, how components communicate, and where the critical execution paths are.

## Data Flow Analysis

### Trace the Path
For each major feature/user journey, trace:

1. **Entry**: How data enters (HTTP request, user input, file watcher, message queue, cron/scheduler)
2. **Validation**: Where and how data is validated (schema validation, type checks, business rules)
3. **Transformation**: How data is shaped between layers (DTOs, mappers, serializers)
4. **Processing**: Business logic applied (calculations, decisions, side effects)
5. **Storage**: Where data persists (database, cache, filesystem) and in what format
6. **Egress**: How data leaves (API response, file write, message publish, UI render)

### Data Flow Smells
- **Data clumps**: same group of fields passed together repeatedly (extract to type/class)
- **Shotgun data**: a single change requires updating many files in the data path
- **Hidden transformations**: data mutated silently without clear ownership
- **Over-fetching / under-fetching**: excessive or insufficient data transferred between layers
- **Tramp data**: data passed through a chain of functions that don't use it

## State Management Patterns

### Where State Lives
| Pattern | Description | Scale |
|---------|-------------|-------|
| Local state | Component-local (useState, local vars) | Small |
| Lifted state | State hoisted to common ancestor | Small-Medium |
| Global store | Redux, Zustand, Pinia, Vuex | Medium-Large |
| Context / DI | React Context, Angular DI, scoped services | Medium |
| URL state | Query params, route params | Small |
| Persistent state | Database, local storage, file | Large |
| Derived state | Computed from other state (selectors, computed) | Any |

### State Smells
- **Global state overuse**: everything in one store — breaks encapsulation
- **State duplication**: same data in multiple places with sync issues
- **Prop drilling**: deeply nested component chain passing unchanged props
- **Mutable shared state**: two modules modifying the same state with race conditions
- **Missing loading/error states**: component assumes data is always available

## Component Communication

### Communication Methods
| Method | Use Case | Coupling |
|--------|----------|----------|
| Direct import/call | Tightly related modules | High |
| Props/parameters | Parent → child in UI | Medium |
| Events/Callbacks | Child → parent notification | Medium |
| Global store | Distant components needing shared state | Low (via store) |
| Message bus / Pub-Sub | Decoupled modules, cross-cutting concerns | Low |
| Dependency injection | Framework-managed wiring | Low |
| File/Stream I/O | Process boundary communication | Very low |

### Communication Smells
- **Tight coupling**: component importing another component's internals
- **Chain of events**: A → B → C → D event cascade (hard to debug)
- **God connector**: single module that connects all others
- **Inconsistent patterns**: mixing too many communication methods randomly

## Critical Path Analysis

### Identify Critical Paths
1. **Performance-critical**: paths executed on every user interaction or request
2. **Error-prone**: paths with complex logic, many edge cases, external dependencies
3. **Frequently executed**: hot paths that run in tight loops or on every render
4. **Security-critical**: authentication, authorization, payment, data export

### For Each Critical Path
- List all functions/operations called in sequence
- Mark branching/decision points
- Highlight potential failure points
- Estimate complexity (cyclomatic complexity of each function)

## Integration Point Analysis

### External Integration Categories
- **HTTP/REST APIs**: outgoing calls, webhooks
- **Database**: read/write patterns, connection management
- **File system**: read/write/stream operations
- **Message queues**: publish/subscribe, produce/consume
- **Third-party SDKs**: library integration, version constraints
- **System commands**: exec/subprocess calls

### Integration Smells
- No retry or circuit breaker for external calls
- Credentials hardcoded or in source files
- No timeout configuration
- Sync calls over network in hot path
- No error handling for failed external calls

## Output Structure

Provide:
1. **Data Flow Diagrams** (textual): for each major feature
2. **State Management Review**: where state lives, how it changes
3. **Communication Map**: how components talk to each other
4. **Critical Paths**: identified hot paths with complexity notes
5. **Integration Points**: all external dependencies with risk assessment
