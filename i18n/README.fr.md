# Censorship Team

En avez-vous assez que l'IA écrive du code que vous ne comprenez pas ? De voir des fichiers apparaître sans explication de pourquoi ils existent ou comment ils s'assemblent ? De perdre du temps à rétro-ingénierer ce qu'un modèle a fait, pour découvrir que l'architecture est pire qu'avant ?

Censorship Team résout cela.

**code-architect** achemine chaque requête via un dispatch d'intention clair — fini de deviner ce que l'IA s'apprête à faire. Quand vous demandez une revue, **scout-alpha** et **scout-beta** cartographient d'abord chaque fichier et chaque convention de votre projet. **arch-alpha** construit un graphe de dépendances pour que vous voyiez exactement quels modules touchent quoi. **arch-beta** trace le flux de données et met en évidence là où la gestion d'état est fragile.

Avant d'écrire du code, **test-worker** vérifie quels tests existent et ce qui manque. Quand le refactoring commence, **refactor-conservative** avance pas à pas, **refactor-aggressive** s'attaque aux grands changements transversaux, et **refactor-pattern** applique des patrons de conception éprouvés — le tout avec des tests exécutés après chaque étape.

Chaque phase produit un rapport lisible. Chaque modification est enregistrée par **progress-tracker** dans PROGRESS.md et SESSION_DATA.md, automatiquement commitée dans git, et prête à être revue. Besoin d'explorer une idée d'abord ? Chargez **brainstorming**. Trouvé un bug ? Chargez **debugging**. Vous planifiez une grosse fonctionnalité ? Chargez **writing-plans**.

Pas de changements cachés. Pas de surprises. Pas de boîtes noires. Juste des agents avec des rôles clairs, un pipeline que vous pouvez suivre, et des rapports que vous pouvez vraiment lire.

---

Un ensemble structuré de compétences opencode pour l'analyse de code, le refactoring et les workflows de projet. Construit autour d'un pipeline d'agents spécialisés et d'un ensemble de compétences polyvalentes chargées à la demande.

---

## Table des matières

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

## Prérequis

- **opencode** (toute version prenant en charge les agents et compétences personnalisés)
- **Node.js 18+** (`node.exe` doit être dans le PATH)
- **Python 3.10+** (`python.exe` doit être dans le PATH) — nécessaire uniquement si vous utilisez les outils d'analyse personnalisés

Les 6 scripts Python utilisent uniquement la bibliothèque standard — aucune installation pip nécessaire.

---

## Installation

### Installation rapide via npx

```bash
npx censorship-team
```

Le CLI détecte votre répertoire de configuration opencode et copie tous les fichiers automatiquement. Après l'installation, démarrez opencode et configurez les modèles :

```
@installer configure skill models
```

### Manuel : clonage

```bash
git clone <repo-url> Censorship-team
cd Censorship-team

# Pour un projet spécifique :
cp -r agents skills tools scripts your-project/.opencode/

# Ou pour une utilisation globale (tous les projets) :
cp -r * ~/.config/opencode/
```

### Via l'agent installer

Après avoir copié les fichiers, invoquez l'installateur dans opencode :

```
@installer configure skill models
```

L'installateur vous guide dans l'attribution des modèles à chaque agent, vérifie la disponibilité de Python/Node.js et écrit la configuration.

---

## Démarrage rapide

### Première rencontre avec un projet

```
you: full analysis on this project please
→ code-architect asks: "Do you want to run Full Analysis Mode?"
→ you say yes
→ agent runs scouts → architecture → test check → produces a report
```

### Correction d'un bug

```
you: there is a bug, the page list won't load
→ code-architect asks: "Do you want to load the debugging skill?"
→ you say yes
→ debugging skill guides you through reproduce → isolate → fix → verify
```

### Développement quotidien avec suivi

```
you: track my progress today
→ code-architect asks: "Do you want to load the progress-tracker?"
→ you say yes
→ agent asks: "Enable tracking?" → you say yes
→ every change from now on is auto-logged + committed
```

### Pipeline complet (révision + refactoring)

```
you: review the code quality of this project
→ code-architect enters Phase 0 → asks language, type, framework, context
→ runs Phases 1-5 with user gates at test plan, review, and refactoring plan
```

---

## Comment ça fonctionne

Le package s'articule autour de **code-architect**, l'agent principal. Chaque message utilisateur passe par un dispatch d'intention à 5 niveaux avant qu'une action ne soit entreprise :

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

**Règle clé** : En cas de doute, demandez. Ne devinez jamais l'intention de l'utilisateur.

---

## Agents

10 agents au total. Les 9 premiers forment un pipeline ; le 10e est l'installateur.

### Principal

#### `code-architect`
Le seul agent qui parle directement à l'utilisateur. Achemine chaque message via un dispatch d'intention à 5 niveaux avant d'agir — discussion informelle, modification simple, suggestion de compétence, analyse de projet ou pipeline de refactoring. Orchestre l'ensemble du pipeline en répartissant les sous-agents via l'outil `task` et en synthétisant leurs résultats. Ne modifie jamais de fichiers sans approbation explicite de l'utilisateur.

- **Fichier** : `agents/code-architect.md`
- **Mode** : primary
- **Accès** : read, glob, grep, edit, bash, task, question ; compétences : pipeline-orchestration, code-review, debugging, brainstorming, writing-plans, progress-tracker

---

### Exploration (Phase 1)

#### `scout-alpha`
Cartographie la structure physique du projet. Parcourt l'arborescence des répertoires, identifie les fichiers de configuration de build, détecte l'organisation des modules et catalogue les points d'entrée. Produit une carte structurelle que les agents aval utilisent pour comprendre où se trouve le code.

- **Fichier** : `agents/scout-alpha.md`
- **Couleur** : `#10b981`
- **Sortie** : arborescence, fichiers de configuration, cibles de build, répartition par type de fichier
- **Invoqué par** : code-architect Phase 1 (s'exécute en parallèle avec scout-beta)

#### `scout-beta`
Explore l'organisation et les conventions du code source. Identifie les motifs de nommage, les conventions d'en-tête de fichier, le style d'import/export, les conventions de placement des tests et les idiomes de code utilisés dans le projet. Produit un profil stylistique qui aide les agents de refactoring à respecter les motifs existants du projet.

- **Fichier** : `agents/scout-beta.md`
- **Couleur** : `#34d399`
- **Sortie** : conventions de nommage, motifs d'import, observations de style de code, disposition des tests
- **Invoqué par** : code-architect Phase 1 (s'exécute en parallèle avec scout-alpha)

---

### Analyse (Phase 2)

#### `arch-alpha`
Analyse structurelle de l'architecture. Construit un graphe de dépendances entre les modules, identifie les limites de couches, détecte les dépendances circulaires et signale les violations architecturales (ex. : modules de bas niveau important des modules de haut niveau). Produit une carte des dépendances des modules et une analyse du couplage.

- **Fichier** : `agents/arch-alpha.md`
- **Couleur** : `#f59e0b`
- **Sortie** : graphe de dépendances, métriques de couplage, violations de couches, rapport de dépendances circulaires
- **Invoqué par** : code-architect Phase 2 (s'exécute en parallèle avec arch-beta)

#### `arch-beta`
Analyse logique et du flux de données. Trace comment les données circulent dans le système, identifie les approches de gestion d'état, cartographie les chemins d'exécution critiques et met en évidence les zones où la propriété des données est floue ou où un état mutable partagé crée des risques. Produit un diagramme de flux de données et une analyse des chemins critiques.

- **Fichier** : `agents/arch-beta.md`
- **Couleur** : `#f97316`
- **Sortie** : diagramme de flux de données, carte de propriété d'état, chemins critiques, risques de concurrence
- **Invoqué par** : code-architect Phase 2 (s'exécute en parallèle avec arch-alpha)

---

### Tests (Phase 3)

#### `test-worker`
Écrit et exécute des tests. À partir des rapports d'architecture, produit un plan de test détaillé couvrant les tests unitaires, les tests d'intégration, les cas limites et les cas d'erreur pour chaque module. Après approbation de l'utilisateur, écrit les fichiers de test en utilisant le framework et les conventions de test existants du projet, les exécute et rapporte les résultats.

- **Fichier** : `agents/test-worker.md`
- **Couleur** : `#ec4899`
- **Sortie** : document du plan de test, nouveaux fichiers de test, résultats d'exécution des tests
- **Invoqué par** : code-architect Phase 3 (après approbation via la porte utilisateur)

---

### Refactoring (Phase 5)

#### `refactor-conservative`
Effectue des modifications minimales et sûres, une étape à la fois. Préserve le comportement existant, l'API publique et la structure du code. Convient pour les corrections ciblées, les petites extractions et les renommages. Chaque modification est suivie de l'exécution de la suite de tests. Si une étape casse les tests, elle fait marche arrière et le signale.

- **Fichier** : `agents/refactor-conservative.md`
- **Couleur** : `#3b82f6`
- **Périmètre** : modifications d'une seule fonction ou d'un seul module, renommages, extractions
- **Invoqué par** : code-architect Phase 5 (en tant qu'étapes de refactoring individuelles)

#### `refactor-aggressive`
Effectue des rénovations à grande échelle. Élimine les anti-patrons, scinde les modules monolithiques, modernise le code legacy et restructure les préoccupations transversales. Opère sur plusieurs fichiers et modules. Chaque étape est toujours testée, mais la tolérance au risque est plus élevée — l'agent s'attend à des échecs de test et les corrige avant de passer à la suite.

- **Fichier** : `agents/refactor-aggressive.md`
- **Couleur** : `#ef4444`
- **Périmètre** : modifications multi-modules, restructuration architecturale, élimination de la dette technique
- **Invoqué par** : code-architect Phase 5 (en tant qu'étapes de refactoring individuelles)

#### `refactor-pattern`
Applique des patrons de conception pour améliorer la structure. Identifie où un patron (Strategy, Factory, Observer, Adapter, etc.) résout un défaut de code concret et l'implémente. Contrairement au refactoring agressif, cet agent suit une recette de patron spécifique plutôt qu'une restructuration libre.

- **Fichier** : `agents/refactor-pattern.md`
- **Couleur** : `#8b5cf6`
- **Périmètre** : introduction ou migration de patron (Strategy → enum dispatch, Observer → event bus, etc.)
- **Invoqué par** : code-architect Phase 5 (en tant qu'étapes de refactoring individuelles)

---

### Configuration des modèles

#### `installer`
Configure la configuration des modèles du package. Guide l'utilisateur dans l'attribution des modèles à chaque agent, écrit le fichier de configuration et vérifie que Python et Node.js sont disponibles. Agent passif — jamais invoqué automatiquement. L'utilisateur doit appeler explicitement `@installer`.

- **Fichier** : `agents/installer.md`
- **Couleur** : `#f59e0b`
- **Mode** : primary
- **Invoqué** : manuellement par l'utilisateur uniquement

---

### Comment les sous-agents sont invoqués

code-architect répartit les sous-agents via l'outil `task`. Chaque sous-agent travaille de manière autonome avec son propre contexte de compétence. Les résultats sont collectés et synthétisés par code-architect.

```
code-architect
  ├── Phase 1: task scout-alpha + task scout-beta (parallel)
  ├── Phase 2: task arch-alpha + task arch-beta (parallel)
  ├── Phase 3: task test-worker
  └── Phase 5: task refactor-* (sequential, one per step)
```

---

## Pipeline

code-architect exécute un pipeline standard pour les tâches de révision de code et de refactoring. Chaque phase a un objectif spécifique et la plupart ont des portes utilisateur.

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

### Dispatch d'intention (s'exécute toujours en premier)

| Niveau | Correspond à | Comportement |
|--------|--------------|--------------|
| 1 | Salutations, discussion informelle | Réponse courte, aucune action |
| 2 | "renommer X", "changer Y", "ajouter un commentaire" | Exécuter directement |
| 3 | "bug", "explorer", "planifier", "suivre" | Proposer de charger la compétence appropriée |
| 4A | "analyse complète", "analyser le projet", "explorer le projet" | Entrer en mode Full Analysis Mode |
| 4B | "réviser", "auditer", "refactoriser", "optimiser" | Entrer dans le pipeline Phase 0 |
| 5 | Ambigu | Demander à l'utilisateur ce dont il a besoin |

---

## Compétences polyvalentes

Situées dans `skills/tools/`. Elles sont chargées à la demande — code-architect demande d'abord à l'utilisateur avant d'en charger une.

### brainstorming

**Quand** : L'objectif de l'utilisateur est vague, ou il existe plusieurs approches possibles.

**Processus** :
1. Clarifier l'objectif (poser une question à la fois)
2. Proposer 2-3 approches avec avantages/inconvénients
3. Approfondir les détails de l'approche choisie
4. Produire un résumé de conception et demander une approbation

### debugging

**Quand** : Quelque chose est cassé — erreurs, plantages, comportement inattendu.

**Processus** :
1. Reproduire le problème
2. Isoler la cause racine (recherche binaire dans le chemin de code)
3. Proposer et appliquer une correction minimale
4. Vérifier avec des tests
5. Ajouter un test de régression

### writing-plans

**Quand** : Une tâche est volumineuse et doit être décomposée en étapes concrètes.

**Processus** :
1. Collecter le contexte (résumé de conception, structure du projet)
2. Décomposer en petites tâches autonomes
3. Ordonner par dépendance
4. Présenter le plan pour approbation

### progress-tracker

**Quand** : L'utilisateur veut suivre ce qui a été fait.

**Processus** :
1. Demander : "Activer le suivi ?" (peut être désactivé à tout moment)
2. Maintenir PROGRESS.md (journal narratif — "ce qui s'est passé et quand")
3. Maintenir SESSION_DATA.md (données structurées — décisions, listes, tâches en attente)
4. Valider automatiquement chaque modification de fichier dans git au niveau de la tâche
5. Support d'annulation via `git revert` (déclenché par l'utilisateur, affiche la liste des commits)

---

## Outils personnalisés

6 wrappers TypeScript dans `tools/` qui appellent des scripts Python dans `scripts/`. Ce sont des aides **optionnelles** — le pipeline fonctionne sans elles.

| Outil | Script | Description |
|-------|--------|-------------|
| `project-summary` | `scripts/project-summary.py` | Nombre de fichiers par langage, total de lignes, ratio de tests, points d'entrée |
| `dependency-matrix` | `scripts/dependency-matrix.py` | Graphe d'import/utilisation, détection de dépendances circulaires, fan-in/fan-out par module |
| `complexity` | `scripts/complexity.py` | Analyse de la longueur des fonctions et de la profondeur d'imbrication, top 20 des pires contrevenants |
| `test-gap` | `scripts/test-gap.py` | Compare les fichiers source et de test pour trouver les modules sans tests |
| `find-orphans` | `scripts/find-orphans.py` | Fichiers qui ne sont ni importés ni référencés nulle part |
| `duplicate-lines` | `scripts/duplicate-lines.py` | Blocs de code dupliqués ou quasi-dupliqués entre fichiers |

---

## Mode d'analyse complète

Un raccourci en lecture seule intégré dans code-architect. Utilisez-le lorsque vous souhaitez comprendre un projet sans rien modifier.

**Déclencheur** : Dites "full analysis" / "scan this project" / "get to know the project" à code-architect.

**Flux** :
```
FA0: Ask one question ─── "Any specific focus?" (or "cover everything")
FA1: Scout-alpha + scout-beta (parallel project exploration)
FA2: Arch-alpha + arch-beta (parallel architecture analysis)
FA3: Test coverage check ─── run existing tests, note gaps
FA4: Produce comprehensive report ─── overview, structure, architecture,
     data flow, test coverage, risk assessment
FA5: Recommend next steps ─── suggest skills based on findings
```

**Différences clés avec le pipeline standard** :
- Pas de Phase 0 (une seule question au lieu de quatre)
- Pas de portes utilisateur aux étapes de test/planification
- Pas de plan de refactoring
- Aucune modification de code — lecture seule

**Coût en tokens estimé** : ~25K tokens (contre ~50K pour le pipeline complet).

---

## Scénarios d'utilisation

### Scénario 1 : Nouveau projet, premier aperçu

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

### Scénario 2 : Déboguer un problème de production

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

### Scénario 3 : Refactoring avec suivi

```
you: refactor the module structure of this project
→ code-architect: enters Phase 0, asks 4 questions
→ you: answer
→ runs Phases 1-5 with user gates at test/plan/execution
→ at the refactoring plan stage, you see clear steps with risk assessment
→ you approve Phase 5
→ refactoring executes step by step, tests pass after each step
```

### Scénario 4 : Travail quotidien avec suivi de progression

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

### Scénario 5 : Planifier une nouvelle fonctionnalité

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

## Principes de conception

- **Demander avant d'agir** — les agents suggèrent, l'utilisateur décide. Ne devinez jamais l'intention de l'utilisateur.
- **Compétences par agent** — chaque agent a un SKILL.md isolé avec des connaissances du domaine. Les permissions contrôlent quelles compétences un agent peut charger.
- **Chargement à la demande** — les compétences polyvalentes (brainstorming, debugging, writing-plans, progress-tracker) ne sont chargées qu'après confirmation de l'utilisateur. Jamais chargées automatiquement.
- **Routage basé sur l'intention** — chaque message utilisateur est classé dans 1 des 5 niveaux avant toute action. Une discussion brève reçoit une réponse brève ; les demandes d'analyse entrent dans le pipeline.
- **Lecture seule par défaut** — le pipeline ne modifie pas les fichiers avant la Phase 5, qui nécessite une approbation explicite de l'utilisateur.
- **Double format de journal** — progress-tracker maintient à la fois un journal narratif (PROGRESS.md) et un fichier de données structurées (SESSION_DATA.md) pour les décisions, listes et éléments en attente.
- **Annulation sécurisée** — toutes les opérations de contrôle de version utilisent `git revert` (préserve l'historique). Jamais `git reset --hard`.
- **Bibliothèque standard uniquement** — les scripts Python n'ont aucune dépendance externe. Zéro installation pip.
