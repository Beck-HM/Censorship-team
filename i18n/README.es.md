# Censorship Team

¿Estás cansado de que la IA escriba código que no entiendes? ¿De ver archivos que aparecen sin explicación de por qué existen o cómo encajan? ¿De perder tiempo ingeniando en reversa lo que hizo un modelo, solo para descubrir que la arquitectura es peor que antes?

Censorship Team soluciona esto.

**code-architect** enruta cada solicitud a través de un despacho de intención claro — no más adivinar lo que la IA está a punto de hacer. Cuando pides una revisión, **scout-alpha** y **scout-beta** primero mapean cada archivo y cada convención en tu proyecto. **arch-alpha** construye un grafo de dependencias para que puedas ver exactamente qué módulos tocan qué. **arch-beta** traza el flujo de datos y resalta dónde la gestión de estado es frágil.

Antes de escribir cualquier código, **test-worker** verifica qué pruebas existen y qué falta. Cuando comienza la refactorización, **refactor-conservative** avanza un paso a la vez, **refactor-aggressive** aborda grandes cambios transversales, y **refactor-pattern** aplica patrones de diseño probados — todo con pruebas ejecutadas después de cada paso.

Cada fase produce un informe legible. Cada cambio es registrado por **progress-tracker** en PROGRESS.md y SESSION_DATA.md, auto-commitado a git, y listo para revisar. ¿Necesitas explorar una idea primero? Carga **brainstorming**. ¿Encontraste un bug? Carga **debugging**. ¿Planeando una gran funcionalidad? Carga **writing-plans**.

Sin cambios ocultos. Sin sorpresas. Sin cajas negras. Solo agentes con trabajos claros, un pipeline que puedes seguir, e informes que realmente puedes leer.

---

Un paquete estructurado de habilidades para opencode destinado al análisis de código, refactorización y flujos de trabajo de proyectos. Construido en torno a un pipeline de agentes especializados y un conjunto de habilidades de propósito general que se cargan bajo demanda.

---

## Tabla de Contenidos

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

---

## Requirements

- **opencode** (cualquier versión que admita agentes y habilidades personalizados)
- **Node.js 18+** (`node.exe` debe estar en PATH)
- **Python 3.10+** (`python.exe` debe estar en PATH) — solo se necesita si usas las herramientas de análisis personalizadas

Los 6 scripts de Python usan solo la stdlib — no es necesario pip install.

---

## Installation

### Instalación rápida via npx

```bash
npx censorship-team
```

La CLI detecta tu directorio de configuración de opencode y copia todos los archivos automáticamente. Después de la instalación, inicia opencode y configura los modelos:

```
@installer configure skill models
```

### Manual: clonar

```bash
git clone <repo-url> Censorship-team
cd Censorship-team

# Para un proyecto específico:
cp -r agents skills tools scripts your-project/.opencode/

# O para uso global (todos los proyectos):
cp -r * ~/.config/opencode/
```

### Via el agente instalador

Después de copiar los archivos, invoca al instalador dentro de opencode:

```
@installer configure skill models
```

El instalador te guía en la asignación de modelos para cada agente, verifica la disponibilidad de Python/Node.js y escribe la configuración.

---

## Quick Start

### Primer contacto con un proyecto

```
you: full analysis on this project please
→ code-architect asks: "Do you want to run Full Analysis Mode?"
→ you say yes
→ agent runs scouts → architecture → test check → produces a report
```

### Corregir un error

```
you: there is a bug, the page list won't load
→ code-architect asks: "Do you want to load the debugging skill?"
→ you say yes
→ debugging skill guides you through reproduce → isolate → fix → verify
```

### Desarrollo diario con seguimiento

```
you: track my progress today
→ code-architect asks: "Do you want to load the progress-tracker?"
→ you say yes
→ agent asks: "Enable tracking?" → you say yes
→ every change from now on is auto-logged + committed
```

### Pipeline completo (revisión + refactorización)

```
you: review the code quality of this project
→ code-architect enters Phase 0 → asks language, type, framework, context
→ runs Phases 1-5 with user gates at test plan, review, and refactoring plan
```

---

## How It Works

El paquete gira en torno a **code-architect**, el agente principal. Cada mensaje del usuario pasa por un despacho de intención de 5 niveles antes de realizar cualquier acción:

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

**Regla clave**: Ante la duda, pregunta. Nunca adivines la intención del usuario.

---

## Agents

10 agentes en total. Los primeros 9 forman un pipeline; el 10.º es el instalador.

### Primario

#### `code-architect`
El único agente que habla directamente con el usuario. Enruta cada mensaje a través de un despacho de intención de 5 niveles antes de tomar cualquier acción — charla informal, edición simple, sugerencia de habilidad, análisis de proyecto o pipeline de refactorización. Orquesta el pipeline completo despachando sub-agentes via la herramienta `task` y sintetizando sus resultados. Nunca modifica archivos sin la aprobación explícita del usuario.

- **Archivo**: `agents/code-architect.md`
- **Modo**: primary
- **Acceso**: read, glob, grep, edit, bash, task, question; habilidades: pipeline-orchestration, code-review, debugging, brainstorming, writing-plans, progress-tracker

---

### Exploración (Phase 1)

#### `scout-alpha`
Mapifica la estructura física del proyecto. Recorre el árbol de directorios, identifica archivos de configuración de compilación, detecta la organización de módulos y cataloga los puntos de entrada. Produce un mapa estructural que los agentes posteriores usan para entender dónde está el código.

- **Archivo**: `agents/scout-alpha.md`
- **Color**: `#10b981`
- **Salida**: árbol de directorios, archivos de configuración, objetivos de compilación, desglose por tipo de archivo
- **Invocado por**: code-architect Phase 1 (se ejecuta en paralelo con scout-beta)

#### `scout-beta`
Explora la organización del código fuente y las convenciones. Identifica patrones de nomenclatura, convenciones de encabezados de archivo, estilo de importación/exportación, convenciones de ubicación de pruebas y modismos utilizados en todo el proyecto. Produce un perfil estilístico que ayuda a los agentes de refactorización a mantener los patrones existentes del proyecto.

- **Archivo**: `agents/scout-beta.md`
- **Color**: `#34d399`
- **Salida**: convenciones de nomenclatura, patrones de importación, observaciones de estilo de código, disposición de pruebas
- **Invocado por**: code-architect Phase 1 (se ejecuta en paralelo con scout-alpha)

---

### Análisis (Phase 2)

#### `arch-alpha`
Análisis de arquitectura estructural. Construye un grafo de dependencias entre módulos, identifica los límites de capas, detecta dependencias circulares y señala violaciones arquitectónicas (por ejemplo, módulos de bajo nivel importando módulos de alto nivel). Produce un mapa de dependencias de módulos y un análisis de acoplamiento.

- **Archivo**: `agents/arch-alpha.md`
- **Color**: `#f59e0b`
- **Salida**: grafo de dependencias, métricas de acoplamiento, violaciones de capas, informe de dependencias circulares
- **Invocado por**: code-architect Phase 2 (se ejecuta en paralelo con arch-beta)

#### `arch-beta`
Análisis lógico y de flujo de datos. Rastrea cómo se mueven los datos a través del sistema, identifica enfoques de gestión de estado, mapea rutas de ejecución críticas y destaca áreas donde la propiedad de los datos no está clara o el estado mutable compartido genera riesgo. Produce un mapa de flujo de datos y un análisis de rutas críticas.

- **Archivo**: `agents/arch-beta.md`
- **Color**: `#f97316`
- **Salida**: diagrama de flujo de datos, mapa de propiedad de estado, rutas críticas, riesgos de concurrencia
- **Invocado por**: code-architect Phase 2 (se ejecuta en paralelo con arch-alpha)

---

### Pruebas (Phase 3)

#### `test-worker`
Escribe y ejecuta pruebas. Dados los informes de arquitectura, produce un plan de pruebas detallado que cubre pruebas unitarias, pruebas de integración, casos límite y casos de error para cada módulo. Tras la aprobación del usuario, escribe los archivos de prueba usando el framework y las convenciones existentes del proyecto, los ejecuta e informa los resultados.

- **Archivo**: `agents/test-worker.md`
- **Color**: `#ec4899`
- **Salida**: documento del plan de pruebas, nuevos archivos de prueba, resultados de ejecución de pruebas
- **Invocado por**: code-architect Phase 3 (después de la aprobación del usuario)

---

### Refactorización (Phase 5)

#### `refactor-conservative`
Realiza cambios mínimos y seguros, un paso a la vez. Preserva el comportamiento existente, la API pública y la estructura del código. Adecuado para correcciones específicas, pequeñas extracciones y renombrados. Cada cambio va seguido de la ejecución del conjunto de pruebas. Si un paso rompe las pruebas, se revierte y lo informa.

- **Archivo**: `agents/refactor-conservative.md`
- **Color**: `#3b82f6`
- **Alcance**: cambios en una sola función o un solo módulo, renombrados, extracciones
- **Invocado por**: code-architect Phase 5 (como pasos individuales de refactorización)

#### `refactor-aggressive`
Realiza renovaciones a gran escala. Elimina antipatrones, divide módulos monolíticos, moderniza código heredado y reestructura preocupaciones transversales. Opera a través de múltiples archivos y módulos. Cada paso sigue siendo probado, pero la tolerancia al riesgo es mayor — el agente espera fallos en las pruebas y los corrige antes de continuar.

- **Archivo**: `agents/refactor-aggressive.md`
- **Color**: `#ef4444`
- **Alcance**: cambios multi-módulo, reestructuración arquitectónica, eliminación de deuda técnica
- **Invocado por**: code-architect Phase 5 (como pasos individuales de refactorización)

#### `refactor-pattern`
Aplica patrones de diseño para mejorar la estructura. Identifica dónde un patrón (Strategy, Factory, Observer, Adapter, etc.) resuelve un problema concreto de código y lo implementa. A diferencia de la refactorización agresiva, este agente sigue una receta de patrón específica en lugar de una reestructuración libre.

- **Archivo**: `agents/refactor-pattern.md`
- **Color**: `#8b5cf6`
- **Alcance**: introducción o migración de patrones (Strategy → enum dispatch, Observer → event bus, etc.)
- **Invocado por**: code-architect Phase 5 (como pasos individuales de refactorización)

---

### Configuración de modelos

#### `installer`
Configura la configuración de modelos del paquete. Guía al usuario en la asignación de modelos a cada agente, escribe el archivo de configuración y verifica que Python y Node.js estén disponibles. Agente pasivo — nunca se invoca automáticamente. El usuario debe llamar explícitamente a `@installer`.

- **Archivo**: `agents/installer.md`
- **Color**: `#f59e0b`
- **Modo**: primary
- **Invocado**: solo manualmente por el usuario

---

### Cómo se invocan los sub-agentes

code-architect despacha sub-agentes via la herramienta `task`. Cada sub-agente trabaja de forma autónoma con su propio contexto de habilidades. Los resultados son recopilados y sintetizados por code-architect.

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (paralelo)
  ├── Phase 2: task arch-alpha + task arch-beta (paralelo)
  ├── Phase 3: task test-worker
  └── Phase 5: task refactor-* (secuencial, uno por paso)
```

---

## Pipeline

code-architect ejecuta un pipeline estándar para tareas de revisión de código y refactorización. Cada fase tiene un propósito específico y la mayoría tienen compuertas de usuario.

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

### Despacho de Intención (siempre se ejecuta primero)

| Nivel | Coincide con | Comportamiento |
|-------|--------------|----------------|
| 1 | Saludos, charla informal | Respuesta breve, sin acción |
| 2 | "renombrar X", "cambiar Y", "agregar comentario" | Ejecutar directamente |
| 3 | "error", "explorar", "planificar", "rastrear" | Preguntar si cargar la habilidad relevante |
| 4A | "análisis completo", "escanear proyecto", "explorar proyecto" | Entrar en Full Analysis Mode |
| 4B | "revisar", "auditar", "refactorizar", "optimizar" | Entrar en el pipeline Phase 0 |
| 5 | Ambiguo | Preguntar al usuario qué necesita |

---

## General-Purpose Skills

Ubicadas en `skills/tools/`. Se cargan bajo demanda — code-architect le pregunta al usuario primero antes de cargar cualquiera de ellas.

### brainstorming

**Cuándo**: El objetivo del usuario es vago, o hay múltiples enfoques posibles.

**Proceso**:
1. Clarificar el objetivo (hacer una pregunta a la vez)
2. Proponer 2-3 enfoques con pros/contra
3. Profundizar en los detalles del enfoque seleccionado
4. Producir un resumen de diseño y pedir aprobación

### debugging

**Cuándo**: Algo está roto — errores, fallos, comportamiento inesperado.

**Proceso**:
1. Reproducir el problema
2. Aislar la causa raíz (búsqueda binaria a través de la ruta de código)
3. Proponer y aplicar una corrección mínima
4. Verificar con pruebas
5. Agregar prueba de regresión

### writing-plans

**Cuándo**: Una tarea es grande y necesita dividirse en pasos concretos.

**Proceso**:
1. Recopilar contexto (resumen de diseño, estructura del proyecto)
2. Dividir en tareas pequeñas e independientes
3. Ordenar por dependencia
4. Presentar el plan para aprobación

### progress-tracker

**Cuándo**: El usuario quiere rastrear lo que se ha hecho.

**Proceso**:
1. Preguntar: "¿Habilitar seguimiento?" (se puede deshabilitar en cualquier momento)
2. Mantener PROGRESS.md (registro narrativo — "qué pasó y cuándo")
3. Mantener SESSION_DATA.md (datos estructurados — decisiones, listas, tareas pendientes)
4. Auto-commit de cada cambio de archivo a git a nivel de tarea
5. Soporte de reversión via `git revert` (activado por el usuario, muestra la lista de commits)

---

## Custom Tools

6 envoltorios TypeScript en `tools/` que llaman a scripts de Python en `scripts/`. Son ayudantes **opcionales** — el pipeline funciona sin ellos.

| Herramienta | Script | Descripción |
|-------------|--------|-------------|
| `project-summary` | `scripts/project-summary.py` | Conteo de archivos por lenguaje, total de líneas, proporción de pruebas, puntos de entrada |
| `dependency-matrix` | `scripts/dependency-matrix.py` | Grafo de importación/uso, detección de dependencias circulares, fan-in/fan-out por módulo |
| `complexity` | `scripts/complexity.py` | Análisis de longitud de funciones y profundidad de anidamiento, top 20 peores infractores |
| `test-gap` | `scripts/test-gap.py` | Compara archivos fuente vs archivos de prueba para encontrar qué módulos carecen de pruebas |
| `find-orphans` | `scripts/find-orphans.py` | Archivos que no son importados ni referenciados en ningún lugar |
| `duplicate-lines` | `scripts/duplicate-lines.py` | Bloques de código duplicado o casi duplicado entre archivos |

---

## Full Analysis Mode

Un atajo de solo lectura integrado en code-architect. Úsalo cuando quieras entender un proyecto sin modificar nada.

**Activación**: Di "full analysis" / "scan this project" / "get to know the project" a code-architect.

**Flujo**:
```
FA0: Ask one question ─── "Any specific focus?" (or "cover everything")
FA1: Scout-alpha + scout-beta (exploración paralela del proyecto)
FA2: Arch-alpha + arch-beta (análisis de arquitectura en paralelo)
FA3: Test coverage check ─── ejecutar pruebas existentes, notar carencias
FA4: Produce comprehensive report ─── overview, structure, architecture,
     data flow, test coverage, risk assessment
FA5: Recommend next steps ─── suggest skills based on findings
```

**Diferencias clave con el pipeline estándar**:
- Sin Phase 0 (una sola pregunta en lugar de cuatro)
- Sin compuertas de usuario en las etapas de pruebas/plan
- Sin plan de refactorización
- Sin modificación de código — solo lectura

**Costo esperado de tokens**: ~25K tokens (frente a ~50K para el pipeline completo).

---

## Usage Scenarios

### Escenario 1: Proyecto nuevo, primera mirada

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

### Escenario 2: Depurar un problema de producción

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

### Escenario 3: Refactorización con seguimiento

```
you: refactor the module structure of this project
→ code-architect: enters Phase 0, asks 4 questions
→ you: answer
→ runs Phases 1-5 with user gates at test/plan/execution
→ at the refactoring plan stage, you see clear steps with risk assessment
→ you approve Phase 5
→ refactoring executes step by step, tests pass after each step
```

### Escenario 4: Trabajo diario con seguimiento de progreso

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

### Escenario 5: Planificar una nueva funcionalidad

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

- **Preguntar antes de actuar** — los agentes sugieren, el usuario decide. Nunca adivinar la intención del usuario.
- **Habilidades por agente** — cada agente tiene un SKILL.md aislado con conocimiento del dominio. Los permisos controlan qué habilidades puede cargar un agente.
- **Carga bajo demanda** — las habilidades de propósito general (brainstorming, debugging, writing-plans, progress-tracker) solo se cargan después de que el usuario lo confirme. Nunca se cargan automáticamente.
- **Enrutamiento por intención primero** — cada mensaje del usuario se clasifica en 1 de 5 niveles antes de cualquier acción. Una charla breve recibe una respuesta breve; las solicitudes de análisis entran al pipeline.
- **Solo lectura por defecto** — el pipeline no modifica archivos hasta Phase 5, que requiere aprobación explícita del usuario.
- **Formato de registro dual** — progress-tracker mantiene tanto un registro narrativo (PROGRESS.md) como un archivo de datos estructurados (SESSION_DATA.md) para decisiones, listas y elementos pendientes.
- **Reversión segura** — todas las operaciones de control de versiones usan `git revert` (preserva el historial). Nunca `git reset --hard`.
- **Solo stdlib** — los scripts de Python no tienen dependencias externas. Zero pip installs.
