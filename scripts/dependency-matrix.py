#!/usr/bin/env python3
"""Dependency matrix: extract import/require/use relationships, detect cycles, compute fan-in/fan-out."""
import sys
import re
from pathlib import Path
from collections import defaultdict

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

IMPORT_PATTERNS = {
    ".py": [
        re.compile(r"^\s*import\s+(\S+)"),
        re.compile(r"^\s*from\s+(\S+)\s+import"),
    ],
    ".ts": [
        re.compile(r'import\s+(?:\{[^}]*\}\s+from\s+)?["\']([^"\']+)["\']'),
        re.compile(r"import\s+(?:\{[^}]*\}\s+from\s+)?[']([^']+)[']"),
    ],
    ".tsx": [
        re.compile(r'import\s+(?:\{[^}]*\}\s+from\s+)?["\']([^"\']+)["\']'),
        re.compile(r"import\s+(?:\{[^}]*\}\s+from\s+)?[']([^']+)[']"),
    ],
    ".js": [
        re.compile(r'(?:import|require)\s*\(?["\']([^"\']+)["\']\)?'),
        re.compile(r'import\s+(?:\{[^}]*\}\s+from\s+)?["\']([^"\']+)["\']'),
    ],
    ".jsx": [
        re.compile(r'(?:import|require)\s*\(?["\']([^"\']+)["\']\)?'),
        re.compile(r'import\s+(?:\{[^}]*\}\s+from\s+)?["\']([^"\']+)["\']'),
    ],
    ".rs": [
        re.compile(r"^\s*use\s+([^;{]+)"),
        re.compile(r"^\s*mod\s+(\S+)"),
    ],
    ".go": [
        re.compile(r'^\s*import\s+["\']([^"\']+)["\']'),
        re.compile(r'^\s*import\s+\S+\s+["\']([^"\']+)["\']'),
    ],
    ".cs": [
        re.compile(r"^\s*using\s+(\S+)"),
    ],
    ".java": [
        re.compile(r"^\s*import\s+(\S+)"),
    ],
    ".rb": [
        re.compile(r"^\s*require\s+['\"]([^'\"]+)['\"]"),
    ],
}


def normalize(path: str) -> str:
    return path.replace("\\", "/").lower()


def resolve_import(imp: str, source_file: Path, root: Path) -> str | None:
    imp = imp.split(".")[0]
    if imp.startswith("."):
        return None
    candidates = [
        root / f"{imp}.py",
        root / f"{imp}/__init__.py",
        root / f"{imp}.ts",
        root / f"{imp}.tsx",
        root / f"{imp}.js",
        root / f"{imp}.jsx",
        root / f"{imp}.rs",
        root / f"{imp}/mod.rs",
        root / f"{imp}.go",
        root / f"{imp}.cs",
        root / f"{imp}.java",
        root / f"{imp}.rb",
    ]
    for c in candidates:
        if c.exists():
            try:
                return normalize(str(c.relative_to(root)))
            except ValueError:
                return None
    return None


def scan(root: Path):
    files = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if f.suffix.lower() in IMPORT_PATTERNS and f.is_file():
            files.append(f)

    imports: dict[str, set[str]] = {}
    file_imports: dict[str, set[str]] = {}

    for f in files:
        rel = normalize(str(f.relative_to(root)))
        imports[rel] = set()
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        patterns = IMPORT_PATTERNS.get(f.suffix.lower(), [])
        for pat in patterns:
            for m in pat.finditer(text):
                imp = m.group(1).strip()
                resolved = resolve_import(imp, f, root)
                if resolved and resolved != rel:
                    imports[rel].add(resolved)

        file_imports[rel] = imports[rel]

    fan_in: dict[str, int] = defaultdict(int)
    fan_out: dict[str, int] = {}
    deps: set[tuple[str, str]] = set()

    for src, targets in file_imports.items():
        fan_out[src] = len(targets)
        for tgt in targets:
            fan_in[tgt] += 1
            deps.add((src, tgt))

    # Cycle detection (DFS)
    adj: dict[str, list[str]] = {n: list(d) for n, d in file_imports.items()}
    visited: dict[str, int] = {}  # 0=unvisited, 1=in_stack, 2=done
    cycles: list[list[str]] = []

    def dfs(node: str, stack: list[str]) -> None:
        if node in visited:
            if visited[node] == 1:
                cycle_start = stack.index(node)
                cycle = stack[cycle_start:] + [node]
                cycles.append(cycle)
            return
        visited[node] = 1
        stack.append(node)
        for neighbor in adj.get(node, []):
            if neighbor in adj:
                dfs(neighbor, stack)
        stack.pop()
        visited[node] = 2

    for n in list(adj.keys()):
        if n not in visited:
            dfs(n, [])

    print("=" * 60)
    print("DEPENDENCY MATRIX")
    print("=" * 60)

    print(f"\nTotal modules scanned: {len(files)}")
    print(f"Modules with dependencies: {sum(1 for v in file_imports.values() if v)}")
    print()

    print("--- Fan-in / Fan-out ---")
    all_modules = sorted(set(list(fan_in.keys()) + list(fan_out.keys())))
    table = []
    for m in all_modules:
        fi = fan_in.get(m, 0)
        fo = fan_out.get(m, 0)
        instability = fo / (fi + fo) if (fi + fo) > 0 else 0
        table.append((m, fi, fo, instability))
    table.sort(key=lambda r: -r[1])

    print(f"  {'Module':40} {'Fan-In':>8} {'Fan-Out':>8} {'Instability':>12}")
    print(f"  {'-'*40} {'-'*8} {'-'*8} {'-'*12}")
    for mod, fi, fo, inst in table:
        inst_s = f"{inst:.2f}"
        print(f"  {mod:40} {fi:>8} {fo:>8} {inst_s:>12}")

    print()

    print("--- Circular Dependencies ---")
    if cycles:
        for cycle in cycles:
            print(f"  {' -> '.join(cycle)}")
    else:
        print("  (none found)")

    print()

    print("--- Dependency Pairs (top 30) ---")
    sorted_deps = sorted(deps, key=lambda x: (fan_in.get(x[1], 0), x[0]), reverse=True)
    for src, tgt in sorted_deps[:30]:
        print(f"  {src:40}  ->  {tgt}")

    print("=" * 60)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(root)


if __name__ == "__main__":
    main()
