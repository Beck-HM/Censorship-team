#!/usr/bin/env python3
"""Project summary: file counts, line counts, entry points, test ratio."""
import sys
from pathlib import Path
from collections import Counter

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

ENTRY_POINT_NAMES = {
    "main", "index", "app", "server", "cli",
    "manage", "wsgi", "asgi",
}

EXT_GROUPS = {
    "Python": {".py"},
    "TypeScript": {".ts", ".tsx"},
    "JavaScript": {".js", ".jsx", ".mjs", ".cjs"},
    "Rust": {".rs"},
    "Go": {".go"},
    "Java": {".java"},
    "Kotlin": {".kt", ".kts"},
    "C#": {".cs"},
    "Ruby": {".rb"},
    "C/C++": {".c", ".h", ".cpp", ".hpp", ".cc"},
    "Web": {".html", ".css", ".scss", ".less"},
    "Config": {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"},
    "Markup": {".md", ".mdx", ".rst", ".txt"},
    "Shell": {".sh", ".ps1", ".bat", ".cmd"},
}

TEST_PATTERNS = {
    ".test.", ".spec.", "test_", "_test", "_spec.",
}


def is_test_file(name: str) -> bool:
    return any(p in name.lower() for p in TEST_PATTERNS)


def scan(root: Path):
    stats = Counter()
    lang_lines = Counter()
    entry_points = []
    source_files = []
    test_files = []
    total_lines = 0
    all_files = []

    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if not f.is_file():
            continue
        if f.name.startswith("."):
            continue

        try:
            lines = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
        except Exception:
            lines = 0

        total_lines += lines
        all_files.append(f)

        ext = f.suffix.lower()
        stats[ext] += 1
        lang_lines[ext] += lines

        for lang, exts in EXT_GROUPS.items():
            if ext in exts:
                if is_test_file(f.name):
                    test_files.append(f)
                else:
                    source_files.append(f)

        if f.stem in ENTRY_POINT_NAMES:
            entry_points.append(rel)

    source_count = len(source_files)
    test_count = len(test_files)

    print("=" * 50)
    print("PROJECT SUMMARY")
    print("=" * 50)
    print(f"Root:             {root.resolve()}")
    print(f"Total files:      {len(all_files)}")
    print(f"Total lines:      {total_lines}")
    print()

    print("--- File Types ---")
    for ext, count in stats.most_common():
        grp = next((g for g, exts in EXT_GROUPS.items() if ext in exts), "Other")
        print(f"  {ext or '(no ext)'}  ->  {count:>5} files  ({grp})")

    print()

    print("--- Language Breakdown ---")
    for lang, exts in EXT_GROUPS.items():
        cnt = sum(stats[e] for e in exts if e in stats)
        lns = sum(lang_lines[e] for e in exts if e in lang_lines)
        if cnt > 0:
            print(f"  {lang:20}  {cnt:>5} files  {lns:>8} lines")

    print()

    print("--- Source vs Test ---")
    print(f"  Source files:  {source_count}")
    print(f"  Test files:    {test_count}")
    if source_count > 0:
        ratio = test_count / source_count * 100
        print(f"  Test ratio:    {ratio:.1f}%  ({test_count}/{source_count})")

    print()

    print("--- Entry Points ---")
    if entry_points:
        for ep in entry_points:
            print(f"  {ep}")
    else:
        print("  (none detected)")

    print("=" * 50)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(root)


if __name__ == "__main__":
    main()
