---
name: setup-wizard
description: Platform detection, model configuration templates, and config file writing for multi-tool skills installation
license: MIT
compatibility: opencode
metadata:
  team: censorship-team
---

## Purpose

This skill provides the installer agent with platform-specific detection heuristics, configuration templates, and model assignment logic for each supported AI coding tool.

## Platform Detection

### Detection Methods

| Platform | Config File Check | Executable Check | Priority |
|----------|-----------------|------------------|----------|
| OpenCode | `~/.config/opencode/opencode.jsonc` | — | Always check |
| OpenCode (project) | `.opencode/opencode.jsonc` in project root | — | Always check |
| Claude Code | `~/.claude/CLAUDE.md` or project `CLAUDE.md` | `claude --version` | High |
| Cursor | `~/.cursor/config` or `.cursorrules` | — | Medium |
| Codex CLI | `~/.codex/config`, `~/.agents/skills/` | `codex --version` | Medium |
| Gemini CLI | `~/.config/gemini/` | `gemini --version` | Low |

### Detection Commands (by platform)

**OpenCode:**
- Global: `Test-Path "~/.config/opencode/opencode.jsonc"`
- Project: `Test-Path ".opencode/opencode.jsonc"`

**Claude Code:**
- Config: `Test-Path "~/.claude/CLAUDE.md"`
- Binary: `Get-Command claude -ErrorAction SilentlyContinue`

**Cursor:**
- Config: `Test-Path "~/.cursor/config"`
- Rules: `Test-Path ".cursorrules"`

**Codex CLI:**
- Config: `Test-Path "~/.codex/config"`
- Skills dir: `Test-Path "~/.agents/skills"`

**Gemini CLI:**
- Config: `Test-Path "~/.config/gemini/"`
- Binary: `Get-Command gemini -ErrorAction SilentlyContinue`

## Reading Existing Model Configs

### OpenCode
Read `opencode.jsonc` and look for:
- `agent.*.model` — per-agent model assignments
- `model` — global model override

### Claude Code
Check `CLAUDE.md` for lines mentioning `model` or the model name.

## Model Categories

### Role → Agent Mapping

| Role | Agents | Workload | Recommended Tier |
|------|--------|----------|-----------------|
| Scout | scout-alpha, scout-beta | File scanning, code reading, config detection | Lightweight |
| Analysis | arch-alpha, arch-beta | Dependency graphs, architecture patterns, data flow | Heavy |
| Refactoring | refactor-conservative, refactor-aggressive, refactor-pattern | Code modification, pattern application | Heavy |
| Testing | test-worker | Test writing, coverage analysis | Heavy |
| Orchestrator | code-architect | Pipeline coordination, user communication | Heavy |

### Common Models by Tier

| Tier | OpenAI | Anthropic | Gemini |
|------|--------|-----------|--------|
| Lightweight | `gpt-4o-mini`, `gpt-4.1-mini` | `claude-haiku-4-20250514` | `gemini-2.5-flash` |
| Heavy | `gpt-4o`, `gpt-4.1` | `claude-sonnet-4-20250514` | `gemini-2.5-pro` |

## Configuration Templates

### Template: OpenCode opencode.jsonc

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "scout-alpha":   { "model": "<scout-model>" },
    "scout-beta":    { "model": "<scout-model>" },
    "arch-alpha":    { "model": "<analysis-model>" },
    "arch-beta":     { "model": "<analysis-model>" },
    "refactor-conservative": { "model": "<refactor-model>" },
    "refactor-aggressive":   { "model": "<refactor-model>" },
    "refactor-pattern":      { "model": "<refactor-model>" },
    "test-worker":   { "model": "<test-model>" },
    "code-architect": { "model": "<orchestrator-model>" }
  }
}
```

### Template: Claude Code CLAUDE.md (model hint section)

```markdown
## Model Configuration
Scout agents (file exploration): {model}
Analysis agents (architecture): {model}
Refactoring agents (code changes): {model}
Test agents: {model}
Orchestrator: {model}
```

Claude Code does not support per-agent model config natively. The user must set the model globally in their Claude Code settings UI or config.

### Template: Cursor .cursorrules (model hint section)

```markdown
You are working with a custom skills pipeline.
Recommended model for analysis and refactoring tasks: {model}
```

Cursor does not support per-agent model config natively. Model is set in Cursor's UI Settings.

### Template: Codex CLI config

Codex CLI does not support per-agent model config natively. Model is set in the CLI or config file.

## Writing Config Files

### Write Strategy by Platform

| Platform | Write Action | Notes |
|----------|-------------|-------|
| OpenCode global | Read `opencode.jsonc`, update `agent.*.model`, write back | Direct edit |
| OpenCode project | Same as global but for `.opencode/opencode.jsonc` | Create if missing |
| Claude Code | Install skills to `~/.claude/skills/` + note about model config | Copy skills files |
| Cursor | Install skills to `.cursor/rules/` + note about model config | Copy or symlink |
| Codex CLI | Install skills to `~/.agents/skills/` | Symlink or copy |
| Gemini CLI | Install skills via native mechanism | Platform-specific |

### Notes for Non-OpenCode Platforms

When writing config for non-OpenCode platforms, always add a clear note that:
1. Skills have been installed to the platform's skills directory
2. Model configuration must be done in the platform's UI or settings
3. Provide a summary of which models were selected for which role

## Post-Install Verification

After writing config, verify by:
1. Re-reading the config file to confirm it was written correctly
2. Listing the skills directory to confirm skills are discoverable
3. Reporting any issues to the user
