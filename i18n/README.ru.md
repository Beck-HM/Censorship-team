# Censorship Team

Устали от того, что ИИ пишет код, который вы не понимаете? Наблюдаете, как появляются файлы без объяснения, зачем они нужны или как они связаны? Тратите время на обратную разработку того, что сделала модель, только чтобы обнаружить, что архитектура стала хуже, чем была?

Censorship Team решает эту проблему.

**code-architect** направляет каждый запрос через чёткую диспетчеризацию намерений — больше не нужно гадать, что собирается делать ИИ. Когда вы запрашиваете ревью, **scout-alpha** и **scout-beta** сначала составляют карту каждого файла и каждого соглашения в вашем проекте. **arch-alpha** строит граф зависимостей, чтобы вы точно видели, какие модули что затрагивают. **arch-beta** отслеживает потоки данных и указывает, где управление состоянием ненадёжно.

Прежде чем будет написан хоть один код, **test-worker** проверяет, какие тесты существуют, а какие отсутствуют. Когда начинается рефакторинг, **refactor-conservative** движется шаг за шагом, **refactor-aggressive** берётся за крупные сквозные изменения, а **refactor-pattern** применяет проверенные паттерны проектирования — и всё это с запуском тестов после каждого шага.

Каждая фаза создаёт читаемый отчёт. Каждое изменение логируется **progress-tracker** в PROGRESS.md и SESSION_DATA.md, автоматически коммитится в git и готово к ревью. Нужно сначала изучить идею? Загрузите **brainstorming**. Нашли баг? Загрузите **debugging**. Планируете большую функциональность? Загрузите **writing-plans**.

Никаких скрытых изменений. Никаких сюрпризов. Никаких чёрных ящиков. Только агенты с чёткими ролями, конвейер, которому можно следовать, и отчёты, которые действительно можно прочитать.

---

Структурированный пакет навыков opencode для анализа кода, рефакторинга и рабочих процессов проектов. Построен вокруг конвейера специализированных агентов и набора навыков общего назначения, загружаемых по требованию.

---

## Содержание

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

- **opencode** (любая версия с поддержкой пользовательских агентов и навыков)
- **Node.js 18+** (`node.exe` должен быть в PATH)
- **Python 3.10+** (`python.exe` должен быть в PATH) — требуется только при использовании пользовательских инструментов анализа

6 Python-скриптов используют только stdlib — pip install не требуется.

---

## Installation

### Быстрая установка через npx

```bash
npx censorship-team
```

CLI определяет ваш каталог конфигурации opencode и автоматически копирует все файлы. После установки запустите opencode и настройте модели:

```
@installer configure skill models
```

### Вручную: клонирование

```bash
git clone <repo-url> Censorship-team
cd Censorship-team

# Для конкретного проекта:
cp -r agents skills tools scripts your-project/.opencode/

# Или для глобального использования (все проекты):
cp -r * ~/.config/opencode/
```

### Через агента установки

После копирования файлов вызовите установщик внутри opencode:

```
@installer configure skill models
```

Установщик проведёт вас через назначение моделей для каждого агента, проверит доступность Python/Node.js и запишет конфигурацию.

---

## Quick Start

### Первое знакомство с проектом

```
you: full analysis on this project please
→ code-architect asks: "Do you want to run Full Analysis Mode?"
→ you say yes
→ agent runs scouts → architecture → test check → produces a report
```

### Исправление ошибки

```
you: there is a bug, the page list won't load
→ code-architect asks: "Do you want to load the debugging skill?"
→ you say yes
→ debugging skill guides you through reproduce → isolate → fix → verify
```

### Ежедневная разработка с отслеживанием

```
you: track my progress today
→ code-architect asks: "Do you want to load the progress-tracker?"
→ you say yes
→ agent asks: "Enable tracking?" → you say yes
→ every change from now on is auto-logged + committed
```

### Полный конвейер (обзор + рефакторинг)

```
you: review the code quality of this project
→ code-architect enters Phase 0 → asks language, type, framework, context
→ runs Phases 1-5 with user gates at test plan, review, and refactoring plan
```

---

## How It Works

Пакет строится вокруг **code-architect** — основного агента. Каждое сообщение пользователя проходит через 5-уровневую диспетчеризацию намерений перед любым действием:

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

**Ключевое правило**: Если сомневаешься — спроси. Никогда не угадывай намерение пользователя.

---

## Agents

Всего 10 агентов. Первые 9 образуют конвейер; 10-й — установщик.

### Основной

#### `code-architect`
Единственный агент, который общается с пользователем напрямую. Направляет каждое сообщение через 5-уровневую диспетчеризацию намерений перед любым действием — неформальный чат, простое редактирование, предложение навыка, анализ проекта или конвейер рефакторинга. Оркестрирует полный конвейер, отправляя подчинённых агентов через инструмент `task` и синтезируя их результаты. Никогда не изменяет файлы без явного одобрения пользователя.

- **Файл**: `agents/code-architect.md`
- **Режим**: основной
- **Доступ**: read, glob, grep, edit, bash, task, question; навыки: pipeline-orchestration, code-review, debugging, brainstorming, writing-plans, progress-tracker

---

### Исследование (Phase 1)

#### `scout-alpha`
Составляет карту физической структуры проекта. Обходит дерево каталогов, определяет файлы сборки, обнаруживает модульную структуру и каталогизирует точки входа. Создаёт структурную карту, которую нижестоящие агенты используют для понимания расположения кода.

- **Файл**: `agents/scout-alpha.md`
- **Цвет**: `#10b981`
- **Результат**: дерево каталогов, конфигурационные файлы, цели сборки, разбивка по типам файлов
- **Вызывается**: code-architect Phase 1 (выполняется параллельно с scout-beta)

#### `scout-beta`
Исследует организацию исходного кода и соглашения. Определяет шаблоны именования, соглашения о заголовках файлов, стиль импорта/экспорта, соглашения о размещении тестов и идиомы кода, используемые в проекте. Создаёт стилистический профиль, помогающий агентам рефакторинга соответствовать существующим шаблонам проекта.

- **Файл**: `agents/scout-beta.md`
- **Цвет**: `#34d399`
- **Результат**: соглашения об именовании, шаблоны импорта, наблюдения за стилем кода, расположение тестов
- **Вызывается**: code-architect Phase 1 (выполняется параллельно с scout-alpha)

---

### Анализ (Phase 2)

#### `arch-alpha`
Структурный анализ архитектуры. Строит граф зависимостей между модулями, определяет границы уровней, обнаруживает циклические зависимости и отмечает архитектурные нарушения (например, импорт низкоуровневых модулей в высокоуровневые). Создаёт карту зависимостей модулей и анализ связанности.

- **Файл**: `agents/arch-alpha.md`
- **Цвет**: `#f59e0b`
- **Результат**: граф зависимостей, метрики связанности, нарушения уровней, отчёт о циклических зависимостях
- **Вызывается**: code-architect Phase 2 (выполняется параллельно с arch-beta)

#### `arch-beta`
Логический анализ и анализ потоков данных. Прослеживает перемещение данных по системе, определяет подходы к управлению состоянием, отображает критические пути выполнения и выделяет области, где право собственности на данные неясно или разделяемое изменяемое состояние создаёт риски. Создаёт карту потоков данных и анализ критических путей.

- **Файл**: `agents/arch-beta.md`
- **Цвет**: `#f97316`
- **Результат**: диаграмма потоков данных, карта владения состоянием, критические пути, риски параллелизма
- **Вызывается**: code-architect Phase 2 (выполняется параллельно с arch-alpha)

---

### Тестирование (Phase 3)

#### `test-worker`
Пишет и запускает тесты. На основе отчётов об архитектуре составляет детальный план тестирования, охватывающий модульные тесты, интеграционные тесты, граничные случаи и сценарии ошибок для каждого модуля. После одобрения пользователя записывает тестовые файлы, используя существующий тестовый фреймворк и соглашения проекта, запускает их и сообщает результаты.

- **Файл**: `agents/test-worker.md`
- **Цвет**: `#ec4899`
- **Результат**: документ плана тестирования, новые тестовые файлы, результаты запуска тестов
- **Вызывается**: code-architect Phase 3 (после одобрения через пользовательский шлюз)

---

### Рефакторинг (Phase 5)

#### `refactor-conservative`
Вносит минимальные, безопасные изменения по одному шагу за раз. Сохраняет существующее поведение, публичный API и структуру кода. Подходит для точечных исправлений, небольших извлечений и переименований. После каждого изменения запускается набор тестов. Если шаг нарушает тесты — откатывает изменения и сообщает.

- **Файл**: `agents/refactor-conservative.md`
- **Цвет**: `#3b82f6`
- **Область**: изменения в одной функции или одном модуле, переименования, извлечения
- **Вызывается**: code-architect Phase 5 (как отдельные шаги рефакторинга)

#### `refactor-aggressive`
Выполняет масштабную реорганизацию. Устраняет антипаттерны, разделяет монолитные модули, модернизирует устаревший код и реструктурирует сквозные аспекты. Работает с несколькими файлами и модулями. Каждый шаг всё ещё тестируется, но допустимый риск выше — агент ожидает сбои тестов и исправляет их перед продолжением.

- **Файл**: `agents/refactor-aggressive.md`
- **Цвет**: `#ef4444`
- **Область**: изменения в нескольких модулях, архитектурная реструктуризация, устранение технического долга
- **Вызывается**: code-architect Phase 5 (как отдельные шаги рефакторинга)

#### `refactor-pattern`
Применяет шаблоны проектирования для улучшения структуры. Определяет, где шаблон (Strategy, Factory, Observer, Adapter и т.д.) решает конкретную проблему кода, и реализует его. В отличие от агрессивного рефакторинга, этот агент следует конкретному рецепту шаблона, а не свободной реструктуризации.

- **Файл**: `agents/refactor-pattern.md`
- **Цвет**: `#8b5cf6`
- **Область**: внедрение или миграция шаблонов (Strategy → enum dispatch, Observer → event bus и т.д.)
- **Вызывается**: code-architect Phase 5 (как отдельные шаги рефакторинга)

---

### Настройка моделей

#### `installer`
Настраивает конфигурацию моделей пакета. Проводит пользователя через назначение моделей каждому агенту, записывает файл конфигурации и проверяет доступность Python и Node.js. Пассивный агент — никогда не вызывается автоматически. Пользователь должен явно вызвать `@installer`.

- **Файл**: `agents/installer.md`
- **Цвет**: `#f59e0b`
- **Режим**: основной
- **Вызов**: только вручную пользователем

---

### Как вызываются подчинённые агенты

code-architect отправляет подчинённых агентов через инструмент `task`. Каждый подчинённый агент работает автономно в своём контексте навыков. Результаты собираются и синтезируются code-architect.

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (параллельно)
  ├── Phase 2: task arch-alpha + task arch-beta (параллельно)
  ├── Phase 3: task test-worker
  └── Phase 5: task refactor-* (последовательно, по одному на шаг)
```

---

## Pipeline

code-architect запускает стандартный конвейер для задач обзора кода и рефакторинга. Каждая фаза имеет определённую цель, и большинство имеют пользовательские шлюзы.

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

### Intent Dispatch (всегда выполняется первым)

| Уровень | Совпадения | Поведение |
|---------|------------|-----------|
| 1 | Приветствия, неформальный чат | Краткий ответ, без действий |
| 2 | "rename X", "change Y", "add comment" | Выполнить напрямую |
| 3 | "bug", "explore", "plan", "track" | Предложить загрузить соответствующий навык |
| 4A | "full analysis", "scan project", "explore project" | Вход в режим полного анализа |
| 4B | "review", "audit", "refactor", "optimise" | Вход в конвейер Phase 0 |
| 5 | Неоднозначно | Спросить пользователя, что нужно |

---

## General-Purpose Skills

Расположены в `skills/tools/`. Загружаются по требованию — code-architect сначала спрашивает пользователя перед загрузкой любого из них.

### brainstorming

**Когда**: Цель пользователя неясна, или есть несколько возможных подходов.

**Процесс**:
1. Уточнить цель (задавать по одному вопросу за раз)
2. Предложить 2-3 подхода с плюсами/минусами
3. Углубиться в детали выбранного подхода
4. Подготовить сводку дизайна и запросить одобрение

### debugging

**Когда**: Что-то сломано — ошибки, сбои, неожиданное поведение.

**Процесс**:
1. Воспроизвести проблему
2. Изолировать первопричину (бинарный поиск по пути кода)
3. Предложить и применить минимальное исправление
4. Проверить с помощью тестов
5. Добавить регрессионный тест

### writing-plans

**Когда**: Задача большая и требует разбивки на конкретные шаги.

**Процесс**:
1. Собрать контекст (сводка дизайна, структура проекта)
2. Разбить на небольшие самостоятельные задачи
3. Упорядочить по зависимостям
4. Представить план на утверждение

### progress-tracker

**Когда**: Пользователь хочет отслеживать, что было сделано.

**Процесс**:
1. Спросить: "Enable tracking?" (можно отключить в любой момент)
2. Вести PROGRESS.md (повествовательный журнал — "что произошло и когда")
3. Вести SESSION_DATA.md (структурированные данные — решения, списки, ожидающие задачи)
4. Автоматически коммитить каждое изменение файла в git на уровне задачи
5. Поддержка отката через `git revert` (инициируется пользователем, показывает список коммитов)

---

## Custom Tools

6 TypeScript-обёрток в `tools/`, которые вызывают Python-скрипты из `scripts/`. Они являются **необязательными** помощниками — конвейер работает и без них.

| Инструмент | Скрипт | Описание |
|------------|--------|----------|
| `project-summary` | `scripts/project-summary.py` | Количество файлов по языкам, всего строк, соотношение тестов, точки входа |
| `dependency-matrix` | `scripts/dependency-matrix.py` | Граф импорта/использования, обнаружение циклических зависимостей, fan-in/fan-out на модуль |
| `complexity` | `scripts/complexity.py` | Анализ длины функций и глубины вложенности, топ-20 худших |
| `test-gap` | `scripts/test-gap.py` | Сравнивает исходные и тестовые файлы для поиска модулей без тестов |
| `find-orphans` | `scripts/find-orphans.py` | Файлы, которые нигде не импортируются и не используются |
| `duplicate-lines` | `scripts/duplicate-lines.py` | Межфайловые дублирующиеся или почти дублирующиеся блоки кода |

---

## Full Analysis Mode

Режим только для чтения, встроенный в code-architect. Используйте его, когда хотите понять проект без внесения изменений.

**Активация**: Скажите "full analysis" / "scan this project" / "get to know the project" агенту code-architect.

**Процесс**:
```
FA0: Ask one question ─── "Any specific focus?" (or "cover everything")
FA1: Scout-alpha + scout-beta (parallel project exploration)
FA2: Arch-alpha + arch-beta (parallel architecture analysis)
FA3: Test coverage check ─── run existing tests, note gaps
FA4: Produce comprehensive report ─── overview, structure, architecture,
     data flow, test coverage, risk assessment
FA5: Recommend next steps ─── suggest skills based on findings
```

**Ключевые отличия от стандартного конвейера**:
- Нет Phase 0 (один вопрос вместо четырёх)
- Нет пользовательских шлюзов на этапах тестирования/планирования
- Нет плана рефакторинга
- Нет изменения кода — только чтение

**Ожидаемая стоимость токенов**: ~25K токенов (против ~50K для полного конвейера).

---

## Usage Scenarios

### Сценарий 1: Новый проект, первое знакомство

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

### Сценарий 2: Отладка проблемы на продакшене

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

### Сценарий 3: Рефакторинг с отслеживанием

```
you: refactor the module structure of this project
→ code-architect: enters Phase 0, asks 4 questions
→ you: answer
→ runs Phases 1-5 with user gates at test/plan/execution
→ at the refactoring plan stage, you see clear steps with risk assessment
→ you approve Phase 5
→ refactoring executes step by step, tests pass after each step
```

### Сценарий 4: Ежедневная работа с отслеживанием прогресса

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

### Сценарий 5: Планирование новой функции

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

- **Сначала спроси, потом действуй** — агенты предлагают, пользователь решает. Никогда не угадывай намерение пользователя.
- **Навыки для каждого агента** — у каждого агента есть изолированный SKILL.md с знаниями предметной области. Права доступа контролируют, какие навыки может загружать агент.
- **Загрузка по требованию** — навыки общего назначения (brainstorming, debugging, writing-plans, progress-tracker) загружаются только после подтверждения пользователя. Никогда не загружаются автоматически.
- **Маршрутизация по намерению** — каждое сообщение пользователя классифицируется на 1 из 5 уровней перед любым действием. Краткий чат получает краткий ответ; запросы на анализ поступают в конвейер.
- **Только чтение по умолчанию** — конвейер не изменяет файлы до Phase 5, которая требует явного одобрения пользователя.
- **Двойной формат журнала** — progress-tracker ведёт как повествовательный журнал (PROGRESS.md), так и структурированный файл данных (SESSION_DATA.md) для решений, списков и ожидающих задач.
- **Безопасный откат** — все операции управления версиями используют `git revert` (сохраняет историю). Никогда `git reset --hard`.
- **Только stdlib** — Python-скрипты не имеют внешних зависимостей. Никаких pip install.
