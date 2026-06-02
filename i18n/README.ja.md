# Censorship Team

AIが書いたコードが理解できずに困っていませんか？ファイルがなぜ存在するのか、どう関係するのか説明もなく表示されるのにうんざりしていませんか？モデルが何をしたかを逆解析するのに時間を浪費し、結局アーキテクチャが以前より悪化しているのを発見して落胆していませんか？

Censorship Team がそれを解決します。

**code-architect** は明確な意図ディスパッチを通じてすべてのリクエストをルーティングします — AI が何をしようとしているかを推測する必要はもうありません。レビューを依頼すると、**scout-alpha** と **scout-beta** がまずプロジェクトのすべてのファイルと規約をマッピングします。**arch-alpha** は依存関係グラフを構築し、どのモジュールが何に影響するかを正確に示します。**arch-beta** はデータフローをトレースし、ステート管理が脆弱な箇所を強調表示します。

コードが書かれる前に、**test-worker** が既存のテストと不足部分をチェックします。リファクタリングが始まると、**refactor-conservative** は一歩ずつ進み、**refactor-aggressive** は大規模な横断的変更に取り組み、**refactor-pattern** は実績のあるデザインパターンを適用します — すべてのステップ後にテストが実行されます。

各フェーズは読みやすいレポートを生成します。すべての変更は **progress-tracker** によって PROGRESS.md と SESSION_DATA.md に記録され、git に自動コミットされてレビュー可能になります。最初にアイデアを探求したい？ **brainstorming** をロードしてください。バグを見つけた？ **debugging** をロードしてください。大規模な機能を計画中？ **writing-plans** をロードしてください。

隠れた変更はありません。驚きはありません。ブラックボックスもありません。明確な役割を持つエージェント、追跡可能なパイプライン、そして実際に読めるレポートだけです。

---

構造化された opencode スキルパッケージ。コード分析、リファクタリング、プロジェクトワークフローのためのものです。専門エージェントのパイプラインと、オンデマンドで読み込まれる汎用スキルセットを中心に構築されています。

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Agents](#agents)
- [Pipeline](#pipeline)
- [General-Purpose Skills](#general-purpose-skills)
- [Custom Tools](#custom-tools)
- [Full Analysis Mode](#full-analysis-mode)
- [Usage Scenarios](#usage-scenarios)
- [Design Principles](#design-principles)
- [License](#license)

---

## Requirements

- **opencode**（カスタムエージェントとスキルをサポートする任意のバージョン）
- **Node.js 18+**（`node.exe` が PATH に含まれている必要があります）
- **Python 3.10+**（`python.exe` が PATH に含まれている必要があります）— カスタム分析ツールを使用する場合のみ必要

6 つの Python スクリプトは stdlib のみを使用します — pip install は不要です。

---

## Installation

### Quick install via npx

```bash
npx censorship-team
```

CLI は opencode の設定ディレクトリを検出し、すべてのファイルを自動的にコピーします。インストール後、opencode を起動してモデルを設定します:

```
@installer configure skill models
```

### Manual: clone

```bash
git clone <repo-url> Censorship-team
cd Censorship-team

# For a specific project:
cp -r agents skills tools scripts your-project/.opencode/

# Or for global use (all projects):
cp -r * ~/.config/opencode/
```

### Via the installer agent

ファイルをコピーした後、opencode 内でインストーラーを呼び出します:

```
@installer configure skill models
```

インストーラーは各エージェントのモデル割り当てを案内し、Python/Node.js の利用可能性を確認し、設定を書き込みます。

---

## Quick Start

### First encounter with a project

```
you: full analysis on this project please
→ code-architect asks: "Do you want to run Full Analysis Mode?"
→ you say yes
→ agent runs scouts → architecture → test check → produces a report
```

### Fixing a bug

```
you: there is a bug, the page list won't load
→ code-architect asks: "Do you want to load the debugging skill?"
→ you say yes
→ debugging skill guides you through reproduce → isolate → fix → verify
```

### Daily development with tracking

```
you: track my progress today
→ code-architect asks: "Do you want to load the progress-tracker?"
→ you say yes
→ agent asks: "Enable tracking?" → you say yes
→ every change from now on is auto-logged + committed
```

### Full pipeline (review + refactor)

```
you: review the code quality of this project
→ code-architect enters Phase 0 → asks language, type, framework, context
→ runs Phases 1-5 with user gates at test plan, review, and refactoring plan
```

---

## How It Works

このパッケージは、プライマリエージェントである **code-architect** を中心に動作します。すべてのユーザーメッセージは、アクションが実行される前に 5 レベルのインテントディスパッチを経由します:

```
User message
    │
    ▼
┌─ Intent Dispatch ──────────────────────┐
│ Level 1: Casual / chit-chat            │ → short reply, do nothing
│ Level 2: Simple code op (rename, etc.) │ → do it directly
│ Level 3: Specific skill need           │ → ask: "load <skill>?"
│ Level 4: Analysis / refactor           │ → full analysis mode OR Phase 0-5
│ Level 5: Cannot determine              │ → ask: "what do you need?"
└────────────────────────────────────────┘
```

**重要なルール**: 迷ったら質問すること。ユーザーの意図を推測してはいけません。

---

## Agents

合計 10 のエージェント。最初の 9 つはパイプラインを構成し、10 番目はインストーラーです。

### Primary

#### `code-architect`
ユーザーと直接対話する唯一のエージェント。すべてのメッセージを 5 レベルのインテントディスパッチに通してからアクションを実行します — カジュアルな会話、簡単な編集、スキルの提案、プロジェクト分析、リファクタリングパイプライン。`task` ツールを介してサブエージェントをディスパッチし、それらの結果を統合することでパイプライン全体を調整します。明示的なユーザー承認なしにファイルを変更することはありません。

- **File**: `agents/code-architect.md`
- **Mode**: primary
- **Access**: read, glob, grep, edit, bash, task, question; skills: pipeline-orchestration, code-review, debugging, brainstorming, writing-plans, progress-tracker

---

### Exploration (Phase 1)

#### `scout-alpha`
プロジェクトの物理的な構造をマッピングします。ディレクトリツリーを走査し、ビルド設定ファイルを特定し、モジュールレイアウトを検出し、エントリーポイントをカタログ化します。下流のエージェントがコードの場所を理解するために使用する構造マップを生成します。

- **File**: `agents/scout-alpha.md`
- **Color**: `#10b981`
- **Output**: directory tree, config files, build targets, file-type breakdown
- **Invoked by**: code-architect Phase 1 (runs in parallel with scout-beta)

#### `scout-beta`
ソースコードの構成と規約を調査します。命名パターン、ファイルヘッダーの規則、インポート/エクスポートスタイル、テスト配置の規則、プロジェクト全体で使用されるコードイディオムを特定します。リファクタリングエージェントがプロジェクトの既存パターンに適合するのに役立つスタイルプロファイルを生成します。

- **File**: `agents/scout-beta.md`
- **Color**: `#34d399`
- **Output**: naming conventions, import patterns, code style observations, test layout
- **Invoked by**: code-architect Phase 1 (runs in parallel with scout-alpha)

---

### Analysis (Phase 2)

#### `arch-alpha`
構造的なアーキテクチャ分析を実行します。モジュール間の依存関係グラフを構築し、レイヤー境界を特定し、循環依存関係を検出し、アーキテクチャ違反（例: 低レベルモジュールが高レベルモジュールをインポートする）をフラグします。モジュール依存関係マップと結合度分析を生成します。

- **File**: `agents/arch-alpha.md`
- **Color**: `#f59e0b`
- **Output**: dependency graph, coupling metrics, layer violations, circular dependency report
- **Invoked by**: code-architect Phase 2 (runs in parallel with arch-beta)

#### `arch-beta`
論理的およびデータフローの分析を実行します。データがシステム内をどのように移動するかを追跡し、状態管理アプローチを特定し、重要な実行パスをマッピングし、データの所有権が不明確な領域や共有可変状態がリスクを生み出す領域を強調します。データフローマップとクリティカルパス分析を生成します。

- **File**: `agents/arch-beta.md`
- **Color**: `#f97316`
- **Output**: data flow diagram, state ownership map, critical paths, concurrency risks
- **Invoked by**: code-architect Phase 2 (runs in parallel with arch-alpha)

---

### Testing (Phase 3)

#### `test-worker`
テストを作成して実行します。アーキテクチャレポートに基づいて、各モジュールのユニットテスト、統合テスト、エッジケース、エラーケースをカバーする詳細なテスト計画を作成します。ユーザーの承認後、プロジェクトの既存のテストフレームワークと規約を使用してテストファイルを作成し、実行し、結果を報告します。

- **File**: `agents/test-worker.md`
- **Color**: `#ec4899`
- **Output**: test plan document, new test files, test run results
- **Invoked by**: code-architect Phase 3 (after user gate approval)

---

### Refactoring (Phase 5)

#### `refactor-conservative`
最小限で安全な変更を一度に 1 ステップずつ行います。既存の動作、公開 API、およびコード構造を保持します。対象を絞った修正、小さな抽出、および名前変更に適しています。各変更の後にテストスイートが実行されます。ステップがテストを壊した場合は、ロールバックして報告します。

- **File**: `agents/refactor-conservative.md`
- **Color**: `#3b82f6`
- **Scope**: single-function or single-module changes, renames, extractions
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

#### `refactor-aggressive`
大規模な改修を実行します。アンチパターンを排除し、モノリシックモジュールを分割し、レガシーコードを現代化し、横断的関心事を再構築します。複数のファイルとモジュールにわたって動作します。各ステップは依然としてテストされますが、リスク許容度は高く、エージェントはテストの失敗を想定し、先に進む前に修正します。

- **File**: `agents/refactor-aggressive.md`
- **Color**: `#ef4444`
- **Scope**: multi-module changes, architectural restructuring, tech debt elimination
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

#### `refactor-pattern`
設計パターンを適用して構造を改善します。パターン（Strategy、Factory、Observer、Adapter など）が具体的なコードの臭いを解決する場所を特定し、それを実装します。アグレッシブリファクタリングとは異なり、このエージェントは自由形式の再構築ではなく、特定のパターンレシピに従います。

- **File**: `agents/refactor-pattern.md`
- **Color**: `#8b5cf6`
- **Scope**: pattern introduction or migration (Strategy → enum dispatch, Observer → event bus, etc.)
- **Invoked by**: code-architect Phase 5 (as individual refactoring steps)

---

### Model configuration

#### `installer`
パッケージのモデル設定を行います。各エージェントへのモデル割り当てをユーザーに案内し、設定ファイルを作成し、Python と Node.js が利用可能であることを確認します。パッシブエージェント — 自動的に呼び出されることはありません。ユーザーが明示的に `@installer` を呼び出す必要があります。

- **File**: `agents/installer.md`
- **Color**: `#f59e0b`
- **Mode**: primary
- **Invoked**: manually by the user only

---

### How sub-agents are invoked

code-architect は `task` ツールを介してサブエージェントをディスパッチします。各サブエージェントは独自のスキルコンテキストで自律的に動作します。結果は code-architect によって収集され統合されます。

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (parallel)
  ├── Phase 2: task arch-alpha + task arch-beta (parallel)
  ├── Phase 3: task test-worker
  └── Phase 5: task refactor-* (sequential, one per step)
```

---

## Pipeline

code-architect は、コードレビューとリファクタリングタスクのための標準パイプラインを実行します。各フェーズには特定の目的があり、ほとんどにはユーザーゲートがあります。

```
Phase 0     Project Assessment ─── "what language/framework/context?"
   │
Phase 1     Project Exploration ─── scouts explore structure + code
   │
Phase 2     Architecture Analysis ─── arch agents analyse deps + data flow
   │              ┌────────────────────────────┐
Phase 3     Test  │  user gate: review plan     │
            │     │  "Shall I proceed?"         │
            │     └────────────────────────────┘
   │
Phase 3.5   Post-Test Review ─── "Ready for the refactoring plan?"
   │              ┌────────────────────────────┐
Phase 4     Plan  │  user gate: approve plan    │
            │     │  "Shall I execute?"         │
            │     └────────────────────────────┘
   │
Phase 5     Execute refactoring ─── step by step, test after each
```

### Intent Dispatch (always runs first)

| Level | Matches | Behaviour |
|-------|---------|-----------|
| 1 | Greetings, casual chat | Short reply, no action |
| 2 | "rename X", "change Y", "add comment" | Execute directly |
| 3 | "bug", "explore", "plan", "track" | Ask to load relevant skill |
| 4A | "full analysis", "scan project", "explore project" | Enter Full Analysis Mode |
| 4B | "review", "audit", "refactor", "optimise" | Enter Phase 0 pipeline |
| 5 | Ambiguous | Ask user what they need |

---

## General-Purpose Skills

`skills/tools/` にあります。これらはオンデマンドで読み込まれます — code-architect は読み込む前に最初にユーザーに確認します。

### brainstorming

**When**: ユーザーの目標があいまいな場合、または複数の可能なアプローチがある場合。

**Process**:
1. Clarify the goal (ask one question at a time)
2. Propose 2-3 approaches with pros/cons
3. Dig into details of the selected approach
4. Produce a design summary and ask for approval

### debugging

**When**: エラー、クラッシュ、予期しない動作など、何かが壊れている場合。

**Process**:
1. Reproduce the issue
2. Isolate the root cause (binary search through code path)
3. Propose and apply a minimal fix
4. Verify with tests
5. Add regression test

### writing-plans

**When**: タスクが大きく、具体的なステップに分割する必要がある場合。

**Process**:
1. Collect context (design summary, project structure)
2. Break down into small, self-contained tasks
3. Order by dependency
4. Present plan for approval

### progress-tracker

**When**: ユーザーが何が行われたかを追跡したい場合。

**Process**:
1. Ask: "Enable tracking?" (can be disabled at any time)
2. Maintain PROGRESS.md (narrative log — "what happened when")
3. Maintain SESSION_DATA.md (structured data — decisions, lists, pending tasks)
4. Auto-commit every file change to git at task level
5. Rollback support via `git revert` (user-triggered, shows commit list)

---

## Custom Tools

`tools/` にある 6 つの TypeScript ラッパーで、`scripts/` にある Python スクリプトを呼び出します。これらは **オプションの** ヘルパーです — パイプラインはこれらがなくても動作します。

| Tool | Script | Description |
|------|--------|-------------|
| `project-summary` | `scripts/project-summary.py` | File counts per language, total lines, test ratio, entry points |
| `dependency-matrix` | `scripts/dependency-matrix.py` | Import/use graph, circular dependency detection, fan-in/fan-out per module |
| `complexity` | `scripts/complexity.py` | Function length and nesting depth analysis, top-20 worst offenders |
| `test-gap` | `scripts/test-gap.py` | Compares source vs test files to find which modules lack tests |
| `find-orphans` | `scripts/find-orphans.py` | Files that are not imported or referenced anywhere |
| `duplicate-lines` | `scripts/duplicate-lines.py` | Cross-file duplicate or near-duplicate code blocks |

---

## Full Analysis Mode

code-architect に組み込まれた読み取り専用のショートカットです。何も変更せずにプロジェクトを理解したい場合に使用します。

**Trigger**: code-architect に対して「full analysis」「scan this project」「get to know the project」などと発言します。

**Flow**:
```
FA0: Ask one question ─── "Any specific focus?" (or "cover everything")
FA1: Scout-alpha + scout-beta (parallel project exploration)
FA2: Arch-alpha + arch-beta (parallel architecture analysis)
FA3: Test coverage check ─── run existing tests, note gaps
FA4: Produce comprehensive report ─── overview, structure, architecture,
     data flow, test coverage, risk assessment
FA5: Recommend next steps ─── suggest skills based on findings
```

**標準パイプラインとの主な違い**:
- Phase 0 なし（4 つの質問の代わりに 1 つの質問）
- テスト/計画段階でのユーザーゲートなし
- リファクタリング計画なし
- コード変更なし — 読み取り専用

**予想トークンコスト**: ~25K トークン（フルパイプラインの ~50K に対して）。

---

## Usage Scenarios

### Scenario 1: New project, first look

```
you: full analysis on this project please
→ code-architect: "Do you want to run Full Analysis Mode?"
→ you: Yes
→ code-architect: "Any specific focus?"
→ you: No, cover everything
→ runs FA1-FA4 automatically
→ outputs a comprehensive report (structure, architecture, tests, risks)
→ code-architect: "Based on the analysis, the test coverage is low.
  Shall I load writing-plans to break down the work?"
→ you: Yes
→ writing-plans helps you plan
```

### Scenario 2: Debug a production issue

```
you: users are getting 500 errors on login
→ code-architect: "It sounds like you need to debug a problem.
  Shall I load the debugging skill?"
→ you: Yes
→ debugging: "Can you provide the exact error message?"
→ you: <pastes error>
→ debugging: traces the code path, identifies the root cause,
  proposes a fix
→ you: approve
→ applies fix, runs tests, asks about regression test
```

### Scenario 3: Refactoring with tracking

```
you: refactor the module structure of this project
→ code-architect: enters Phase 0, asks 4 questions
→ you: answer
→ runs Phases 1-5 with user gates at test/plan/execution
→ at the refactoring plan stage, you see clear steps with risk assessment
→ you approve Phase 5
→ refactoring executes step by step, tests pass after each step
```

### Scenario 4: Daily work with progress tracking

```
you: enable progress tracking please
→ code-architect: "Shall I load progress-tracker?"
→ you: Yes
→ progress-tracker: "Enable tracking? This will log to PROGRESS.md
  and commit to git."
→ you: Yes
→ you make changes throughout the day
→ each change is logged + committed automatically
→ end of day: ask "what did we do today" and get a full log
```

### Scenario 5: Plan a new feature

```
you: I'm not sure how to implement the search feature, any ideas?
→ code-architect: "It sounds like you want to discuss a design.
  Shall I load the brainstorming skill?"
→ you: Yes
→ brainstorming walks through clarifying goals, proposing approaches,
  producing a design summary
→ you approve the design
→ code-architect: "Want to load writing-plans to break this into tasks?"
→ you: Yes
→ writing-plans produces a task plan
```

---

## Design Principles

- **Ask before act** — エージェントが提案し、ユーザーが決定します。ユーザーの意図を推測してはいけません。
- **Skills per agent** — 各エージェントは、ドメイン知識を持つ独立した SKILL.md を持ちます。権限によって、エージェントが読み込めるスキルを制御します。
- **On-demand loading** — 汎用スキル（brainstorming、debugging、writing-plans、progress-tracker）は、ユーザーが確認した後にのみ読み込まれます。自動読み込みはされません。
- **Intent-first routing** — すべてのユーザーメッセージは、アクションの前に 5 つのレベルのいずれかに分類されます。短いチャットには短い返信、分析リクエストはパイプラインに入ります。
- **Read-only by default** — パイプラインは Phase 5 までファイルを変更しません。Phase 5 には明示的なユーザー承認が必要です。
- **Dual log format** — progress-tracker は、決定事項、リスト、保留項目について、ナarrativeログ（PROGRESS.md）と構造化データファイル（SESSION_DATA.md）の両方を維持します。
- **Safe rollback** — すべてのバージョン管理操作は `git revert`（履歴を保持）を使用します。`git reset --hard` は使用しません。
- **Stdlib only** — Python スクリプトには外部依存関係がありません。pip install はゼロです。
