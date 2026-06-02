---
name: project-exploration
description: Language-aware file discovery patterns and config file conventions for project exploration
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides detailed guidance for discovering and understanding a project's build configuration, directory layout, and toolchain — adapting to the project's language and framework identified in Phase 0.

## Language-Specific Lookup

When exploring a project, use the Phase 0 language/type/framework answers to determine what to look for.

### Config Files by Language

| Language | Priority Config Files | What to Extract |
|----------|---------------------|-----------------|
| TypeScript/JS | `package.json`, `tsconfig.json`, `eslint*`, `.prettier*`, `vitest.config*`, `jest.config*`, `turbo.json`, `nx.json` | Scripts, dependencies, compiler options, lint rules, test framework, monorepo config |
| Python | `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `Pipfile`, `poetry.lock`, `ruff.toml`, `mypy.ini`, `.pylintrc` | Build backend, dependencies, tool configs, test runner |
| Rust | `Cargo.toml`, `rustfmt.toml`, `clippy.toml`, `.cargo/config.toml` | Dependencies, features, workspace members, edition, lint config |
| Go | `go.mod`, `go.sum`, `.golangci.yml` | Module path, Go version, dependencies, lint config |
| Java/Kotlin | `pom.xml`, `build.gradle*`, `settings.gradle*` | Build plugins, dependencies, modules, test framework |
| C# | `*.csproj`, `*.sln`, `NuGet.config`, `Directory.Build.props` | Target framework, package references, solution structure |
| Ruby | `Gemfile`, `*.gemspec`, `.rubocop.yml` | Dependencies, gemspec metadata, lint rules |
| C/C++ | `CMakeLists.txt`, `Makefile`, `conanfile.*`, `vcpkg.json`, `meson.build` | Build targets, dependencies, compiler flags |

### Project Type Clues

| Project Type | Directory Structure Patterns |
|-------------|---------------------------|
| Web backend | `src/routes/`, `src/controllers/`, `src/middleware/`, `src/models/`, `src/services/`, `api/` |
| Frontend/UI | `src/components/`, `src/pages/`, `src/hooks/`, `public/`, `assets/`, `styles/` |
| CLI tool | `src/cli/`, `src/commands/`, `bin/`, `main.rs`, `cmd/` |
| Library/SDK | `src/lib/`, `src/index.ts`, `lib.rs`, `__init__.py` |
| Mobile app | `android/`, `ios/`, `lib/` (Flutter), `app/` (Android) |
| Data processing | `pipelines/`, `notebooks/`, `etl/`, `queries/`, `dags/` |
| Embedded/IoT | `src/hal/`, `src/drivers/`, `src/bsp/`, `linker.ld` |
| Game | `src/scenes/`, `src/entities/`, `src/systems/`, `assets/`, `resources/` |

### Framework-Specific Files to Check

- **React/Next.js**: `next.config.*`, `app/` or `pages/` directory, `middleware.ts`
- **Vue/Nuxt**: `nuxt.config.*`, `app.vue`, `pages/`, `composables/`
- **Django**: `manage.py`, `settings/*.py`, `urls.py`, `wsgi.py`, `asgi.py`
- **FastAPI**: `main.py`, `routers/`, `schemas/`, `dependencies/`
- **Spring Boot**: `application.yml`/`application.properties`, `@SpringBootApplication` class, `build.gradle*`
- **Actix-web/Rocket**: `main.rs`, `routes/`, `models/`, `handlers/`

## Scanning Heuristics

1. Start with a shallow directory listing to identify the project root structure.
2. Immediately find and read all config files — they tell you the toolchain.
3. Map the tree at least 3 levels deep, focusing on `src/`, `app/`, `lib/`, `packages/`.
4. Skip `node_modules/`, `venv/`, `target/`, `build/`, `dist/`, `.git/`, `__pycache__/`.
5. If you see a monorepo structure (workspaces, packages/), explore each workspace member.

## Output Structure

Always produce a structured report containing:
- Complete directory tree (3+ levels)
- Build toolchain and scripts
- Test framework configuration
- Linting and formatting rules
- External dependencies summary
- Key architectural decisions inferred from structure

## Available Tools

### `project-summary` (custom tool)
- **Purpose**: scan the project root and produce a structured report of files, lines, entry points, and test ratio
- **When to use**: at the start of exploration to quickly understand project scale and structure
- **How to use**: call `project-summary` tool directly; ask the user with the `question` tool first if you're unsure
