---
name: pattern-refactoring
description: Design pattern catalogue with applicability heuristics and language-specific implementations
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides a decision framework for applying design patterns in refactoring — diagnose the problem first, then select the right pattern.

## Core Principle

**Diagnose before prescribing.** Never apply a pattern because it's "clean" or "correct." Apply it because it solves a real, measurable problem in the code.

## Problem → Pattern Mapping

### Conditional Complexity
| Symptom | Suitable Pattern | When NOT to Use |
|---------|-----------------|-----------------|
| `if/else` or `switch` over types | Strategy, State, Polymorphism | Only 2 variants, unlikely to grow |
| Complex boolean expressions | Specification pattern | Simple AND/OR only |
| Multiple conditions before action | Guard clause / early return | Business logic requires all checks |

### Object Creation
| Symptom | Suitable Pattern | When NOT to Use |
|---------|-----------------|-----------------|
| Complex object construction across many callers | Factory, Factory Method | Constructor is simple |
| Object has many optional parameters | Builder | 3 or fewer parameters |
| Different object variants based on context | Abstract Factory | Only one variant exists |

### Coupling
| Symptom | Suitable Pattern | When NOT to Use |
|---------|-----------------|-----------------|
| Tight coupling to external library | Adapter | Library is stable, unlikely to change |
| Complex subsystem | Facade | Callers use the subsystem directly without issue |
| Many-to-many object connections | Mediator | Connections are 1:1 or simple tree |
| Unstable dependency | Proxy | Dependency is already stable |

### Cross-Cutting Concerns
| Symptom | Suitable Pattern | When NOT to Use |
|---------|-----------------|-----------------|
| Logging/metrics/auth in business logic | Decorator, Middleware | Only one concern, one layer deep |
| Multiple orthogonal behaviors | Chain of Responsibility | Behaviors are simple and few |
| Need undo/redo | Command | Operation is trivial |

### State & Behavior
| Symptom | Suitable Pattern | When NOT to Use |
|---------|-----------------|-----------------|
| Object changes behavior based on state | State | Simple boolean flag suffices |
| Complex state transitions | State | 2-3 states with linear transitions |
| Notify many objects of changes | Observer / Event | Only one listener |
| Algorithms vary by context | Template Method, Strategy | Single algorithm, stable |

## Pattern Catalogue

### Strategy
- **Problem**: multiple algorithms for the same task, selected at runtime
- **Structure**: interface → concrete implementations → context
- **Example**: payment processing (credit card, PayPal, crypto)
- **Refactoring target**: long `if/else` chains, switch statements
- **Language note**: use function pointers/traits in Rust, lambdas in functional languages

### Factory / Factory Method
- **Problem**: object creation logic is scattered or duplicated
- **Structure**: creation method in base class (Factory Method) or separate class (Factory)
- **Example**: creating different types of documents from a template
- **Refactoring target**: `new` keyword with conditionals, repeated construction
- **Language note**: no `new` keyword needed — any function that returns instances counts

### Builder
- **Problem**: object with many optional parameters or complex construction steps
- **Structure**: builder class with chainable setters → `build()`
- **Example**: constructing HTTP requests, query builders, UI components
- **Refactoring target**: telescoping constructors, huge constructor parameter lists
- **Language note**: named parameters (Python, Kotlin, C#) reduce Builder necessity

### Adapter
- **Problem**: incompatible interfaces that need to work together
- **Structure**: adapter wraps adaptee → implements target interface
- **Example**: wrapping third-party SDK to match application interface
- **Refactoring target**: scattered calls to external library throughout codebase
- **Language note**: trait impl in Rust, extension methods in C#, monkey-patching in JS

### Decorator
- **Problem**: adding behavior to individual objects without affecting others
- **Structure**: wrapper implements same interface → delegates + adds behavior
- **Example**: adding caching, logging, validation to a service
- **Refactoring target**: cross-cutting concerns mixed into business logic
- **Language note**: Python decorators, JS higher-order functions, Rust middlewares

### Observer / Event Emitter
- **Problem**: one-to-many notification when something happens
- **Structure**: Subject maintains observer list → notifies on state change
- **Example**: UI events, domain events, websocket broadcast
- **Refactoring target**: tight coupling between event source and listeners
- **Language note**: use language's event system (C# events, Rust channels, JS EventTarget)

### State
- **Problem**: object behaves differently based on internal state
- **Structure**: state interface → concrete states → context delegates to current state
- **Example**: document workflow (draft → review → published → archived)
- **Refactoring target**: large switch statements over state, many boolean flags
- **Language note**: enum + match in Rust, discriminated unions in TypeScript

## Anti-Patterns

### Pattern Overuse
- **Symptom**: 15 classes for 3 variants
- **Fix**: go back to simple if/else
- **Rule**: if the pattern adds more code than it saves, don't use it

### Overengineering
- **Symptom**: Strategy pattern for a boolean flag
- **Fix**: `if (flag) { doA() } else { doB() }` is fine
- **Rule**: solve today's problem, not imaginary future ones

### Pattern Jargon
- **Symptom**: classes named `AbstractUserFactoryStrategyImpl`
- **Fix**: name by purpose, not pattern (`UserFactory` → better: `UserCreator`)
- **Rule**: the reader should understand the code without knowing design patterns

### Premature Abstraction
- **Symptom**: interfaces for everything, even single implementations
- **Fix**: start concrete, extract interface when a second implementation appears
- **Rule**: YAGNI — You Aren't Gonna Need It

## Verification Checklist

Before applying any pattern, ask:
- [ ] Does this pattern solve an existing, confirmed problem?
- [ ] Is the pattern idiomatic in this language?
- [ ] Will the team/maintainers understand this pattern?
- [ ] Does the pattern reduce total complexity (code size + mental model)?
- [ ] Can I implement this without changing public APIs?
- [ ] Is there a simpler alternative I'm overlooking?
