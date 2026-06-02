#!/usr/bin/env python3
"""Test gap analysis: find source files without corresponding test files."""
import sys
from pathlib import Path
from collections import defaultdict

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".cs", ".java", ".rb"}

# How test files match source files (by convention)
TEST_CONVENTIONS = {
    ".py":  lambda name, stem: f"test_{stem}.py" in name or f"{stem}_test.py" in name,
    ".ts":  lambda name, stem: f"{stem}.test.ts" in name or f"{stem}.spec.ts" in name,
    ".tsx": lambda name, stem: f"{stem}.test.tsx" in name or f"{stem}.spec.tsx" in name,
    ".js":  lambda name, stem: f"{stem}.test.js" in name or f"{stem}.spec.js" in name,
    ".jsx": lambda name, stem: f"{stem}.test.jsx" in name or f"{stem}.spec.jsx" in name,
    ".rs":  lambda name, stem: f"{stem}_test.rs" in name,
    ".go":  lambda name, stem: f"{stem}_test.go" in name,
    ".cs":  lambda name, stem: f"{stem}Test.cs" in name or f"{stem}Tests.cs" in name,
    ".java": lambda name, stem: f"{stem}Test.java" in name or f"{stem}Tests.java" in name,
    ".rb":  lambda name, stem: f"{stem}_test.rb" in name or f"{stem}_spec.rb" in name,
}


def scan(root: Path):
    all_files = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if f.suffix.lower() in SOURCE_EXTS and f.is_file():
            all_files.append(f)

    source_by_ext: dict[str, list[Path]] = defaultdict(list)
    test_by_ext: dict[str, list[Path]] = defaultdict(list)

    for f in all_files:
        ext = f.suffix.lower()
        is_test = TEST_CONVENTIONS.get(ext, lambda n, s: False)(f.name, f.stem)
        if is_test:
            test_by_ext[ext].append(f)
        else:
            source_by_ext[ext].append(f)

    print("=" * 50)
    print("TEST GAP ANALYSIS")
    print("=" * 50)
    print(f"\nRoot: {root.resolve()}")
    print(f"Source files: {sum(len(v) for v in source_by_ext.values())}")
    print(f"Test files:   {sum(len(v) for v in test_by_ext.values())}")
    print()

    print("--- Coverage by Language ---")
    for ext in sorted(set(list(source_by_ext.keys()) + list(test_by_ext.keys()))):
        src_count = len(source_by_ext.get(ext, []))
        tst_count = len(test_by_ext.get(ext, []))
        ratio = (tst_count / src_count * 100) if src_count > 0 else 0
        print(f"  {ext:8}  {src_count:>5} source  {tst_count:>5} tests  {ratio:>5.1f}%")

    print()

    # Find untested modules
    print("--- Untested Modules ---")
    found_any = False
    for ext, src_files in sorted(source_by_ext.items()):
        conv = TEST_CONVENTIONS.get(ext, lambda n, s: False)
        for f in src_files:
            rel = f.relative_to(root)
            matched = False
            for t in test_by_ext.get(ext, []):
                if conv(t.name, f.stem):
                    matched = True
                    break
            if not matched:
                # Also check if file is itself a config/setup file to skip
                if f.stem in {"__init__", "manage", "wsgi", "asgi", "conftest", "setup", "conf"}:
                    continue
                print(f"  {rel}")
                found_any = True

    if not found_any:
        print("  (all modules have corresponding test files)")

    print()

    print("--- Test Files Found ---")
    for ext, tests in sorted(test_by_ext.items()):
        for t in tests:
            rel = t.relative_to(root)
            print(f"  {rel}")

    print("=" * 50)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(root)


if __name__ == "__main__":
    main()
