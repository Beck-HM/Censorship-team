---
name: safe-refactoring
description: Catalogue of safe, behavior-preserving refactoring operations with examples
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides a comprehensive catalogue of safe refactoring operations that preserve existing behavior. Use this to guide minimal, low-risk code improvements.

## Golden Rules

1. **One change at a time**: never batch multiple refactorings
2. **Test after every change**: run the suite, verify nothing broke
3. **Revert on failure**: if tests fail, undo immediately and try a different approach
4. **Preserve behavior**: no API signature changes, no runtime behavior changes
5. **Small scope**: prefer changing one file over many

## Safe Refactoring Catalogue

### Rename
| Operation | Example | Safety |
|-----------|---------|--------|
| Rename variable | `let x = 1` → `let count = 1` | ✅ Safe (single scope) |
| Rename function | `calc()` → `calculateTotal()` | ✅ Safe with find-replace in file |
| Rename parameter | `def f(name)` → `def f(user_name)` | ✅ Safe (callers use argument position) |
| Rename class/type | `class Usr` → `class User` | ⚠️ Check all references |
| Rename file | `utils.ts` → `string-utils.ts` | ⚠️ Update all imports |
| Rename test | `test_calc()` → `test_calculate_total()` | ✅ Safe |

### Extract
| Operation | Example | Safety |
|-----------|---------|--------|
| Extract variable | `return a * b + a * c` → `let base = a * b; return base + a * c` | ✅ Safe |
| Extract function | Inline block → named function | ✅ Safe |
| Extract constant | `"some_string"` → `const GREETING = "some_string"` | ✅ Safe |
| Extract type | Inline type → named type alias | ✅ Safe |
| Extract parameter | Hardcoded value → function parameter with default | ⚠️ Check callers |

### Inline
| Operation | Example | Safety |
|-----------|---------|--------|
| Inline variable | `let tmp = expr; return tmp + 1` → `return expr + 1` | ✅ Safe |
| Inline function | Simple delegation → direct code | ⚠️ Check if used elsewhere |
| Inline constant | `const X = 5; return X + 1` → `return 5 + 1` (if used once) | ⚠️ Check all usages |

### Simplify Conditionals
| Operation | Example | Safety |
|-----------|---------|--------|
| Simplify boolean | `if (x == true)` → `if (x)` | ✅ Safe |
| De Morgan's | `!(a && b)` → `!a \|\| !b` | ✅ Safe |
| Remove dead branch | `if (false) { ... }` → remove | ✅ Safe |
| Merge nested ifs | `if (a) { if (b) { ... } }` → `if (a && b) { ... }` | ✅ Safe |
| Ternary over if | `if (c) { x = 1 } else { x = 2 }` → `x = c ? 1 : 2` | ✅ Safe |
| Early return | Nested if → guard clause | ✅ Safe |

### Remove Dead Code
| Type | Detection | Safety |
|------|-----------|--------|
| Unused variable | Never read after assignment | ✅ Safe |
| Unused parameter | Not used in function body | ⚠️ Public API — check callers |
| Unused import | Not referenced in file | ✅ Safe |
| Unreachable code | After return/break/throw/continue | ✅ Safe |
| Dead function | Never called (private only) | ⚠️ Check with grep first |
| Commented code | Just delete it | ✅ Safe |

### Reformat / Restyle
| Operation | Safety |
|-----------|--------|
| Fix indentation | ✅ Safe |
| Reorder imports (grouped) | ✅ Safe |
| Add/remove whitespace | ✅ Safe |
| Fix line length (wrapping) | ✅ Safe |
| Standardize quotes | ⚠️ If mixed — use project style |

## Language-Specific Safe Operations

### TypeScript/JavaScript
- Add explicit `: type` annotations where inferred ✅
- Convert `var` to `const`/`let` ✅
- Convert function to arrow function ✅ (unless `this` binding needed)
- Add `readonly` to unchanged properties ✅
- Use optional chaining `?.` safe equivalent ✅

### Python
- Add type annotations ✅
- Convert to f-string ✅
- Use `pathlib` over `os.path` ✅
- Replace `== None` with `is None` ✅

### Rust
- Add type annotations ✅
- Convert `unwrap()` to `expect("msg")` ✅
- Replace `&x` with `x` where `Copy` trait exists ✅
- Use `let ... else` pattern ✅

## Safety Checklist for Each Change
- [ ] Does this change any public API? ❌ Stop
- [ ] Does this change runtime behavior? ❌ Stop
- [ ] Does this move code between modules? ❌ Stop
- [ ] Does this require updating callers? ⚠️ Check carefully
- [ ] Is there a test for this code path? ✅ Run it
- [ ] Can I undo this change easily? ✅ Proceed

## Available Tools

### `find-orphans` (custom tool)
- **Purpose**: find source files not imported by any other file — safe candidates for deletion
- **When to use**: before removing dead code to confirm a file is truly unreferenced
- **How to use**: call `find-orphans` tool directly; ask the user with the `question` tool first if you're unsure
