#!/usr/bin/env python3
"""Find orphan files: source files not imported by any other project file."""
import sys
import re
from pathlib import Path
from collections import defaultdict

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".cs", ".java", ".rb"}

ENTRY_POINT_STEMS = {
    "main", "index", "app", "server", "cli", "manage",
    "wsgi", "asgi", "__init__", "mod",
}

IMPORT_EXTRACT = {
    ".py":  re.compile(r"(?:from\s+(\S+)|import\s+(\S+))"),
    ".ts":  re.compile(r"from\s+['\"](\S+)['\"]"),
    ".tsx": re.compile(r"from\s+['\"](\S+)['\"]"),
    ".js":  re.compile(r"(?:from|require)\s*\(?\s*['\"](\S+)['\"]"),
    ".jsx": re.compile(r"(?:from|require)\s*\(?\s*['\"](\S+)['\"]"),
    ".rs":  re.compile(r"(?:use|mod)\s+(\S+)"),
    ".go":  re.compile(r'import\s+(?:\S+\s+)?["\'](\S+)["\']'),
    ".cs":  re.compile(r"using\s+(\S+)"),
    ".java": re.compile(r"import\s+(\S+)"),
    ".rb":  re.compile(r"require\s+['\"](\S+)['\"]"),
}


def module_name(filepath: Path, root: Path) -> str:
    try:
        rel = filepath.relative_to(root)
    except ValueError:
        return filepath.stem
    parts = list(rel.parts)
    stem = parts[-1]
    stem = stem.rsplit(".", 1)[0] if "." in stem else stem
    if stem == "__init__":
        parts = parts[:-1]
    else:
        parts[-1] = stem
    return ".".join(parts)


def is_entry_point(filename: str, stem: str) -> bool:
    if stem in ENTRY_POINT_STEMS:
        return True
    return False


def scan(root: Path):
    source_files: list[Path] = []
    test_files: list[Path] = []

    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if f.suffix.lower() in SOURCE_EXTS and f.is_file():
            is_test = (
                ".test." in f.name or ".spec." in f.name or
                f.name.startswith("test_") or f.name.endswith("_test.go") or
                f.name.endswith("_test.rs") or f.name.endswith("_spec.rb")
            )
            if is_test:
                test_files.append(f)
            else:
                source_files.append(f)

    # Collect all imports from all source files
    referenced_modules: set[str] = set()
    module_to_file: dict[str, Path] = {}

    for f in source_files + test_files:
        mod = module_name(f, root)
        module_to_file[mod] = f
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        pat = IMPORT_EXTRACT.get(f.suffix.lower())
        if not pat:
            continue
        for m in pat.finditer(text):
            ref = next(g for g in m.groups() if g)
            if not ref:
                continue
            # Clean the reference
            ref = ref.replace('"', "").replace("'", "").strip()
            # Only consider local references (relative or module-like)
            if ref.startswith("."):
                continue
            if "/" in ref:
                ref = ref.replace("/", ".")
            # Check if it's a local module
            if ref in module_to_file:
                referenced_modules.add(ref)

    # Also track what's actually imported from each file
    file_imported_by: dict[str, set[str]] = defaultdict(set)
    for f in source_files + test_files:
        mod = module_name(f, root)
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        pat = IMPORT_EXTRACT.get(f.suffix.lower())
        if not pat:
            continue
        for m in pat.finditer(text):
            ref = next(g for g in m.groups() if g)
            if not ref:
                continue
            ref = ref.replace('"', "").replace("'", "").strip()
            if ref.startswith("."):
                continue
            if "/" in ref:
                ref = ref.replace("/", ".")
            if ref in module_to_file:
                file_imported_by[ref].add(mod)

    # Find orphans
    orphans = []
    for f in source_files:
        mod = module_name(f, root)
        if is_entry_point(f.name, f.stem):
            continue
        if mod in {"__init__", "mod"}:
            continue
        if mod not in file_imported_by or not file_imported_by[mod]:
            orphans.append(f)

    print("=" * 50)
    print("ORPHAN FILE ANALYSIS")
    print("=" * 50)
    print(f"\nSource files:  {len(source_files)}")
    print(f"Test files:    {len(test_files)}")
    print(f"Orphan files:  {len(orphans)}")
    print()

    if orphans:
        print("--- Orphan Files (not imported by any other file) ---")
        for f in orphans:
            rel = f.relative_to(root)
            lines = 0
            try:
                lines = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
            except Exception:
                pass
            print(f"  {rel:60}  {lines:>5} lines")
    else:
        print("(no orphan files found)")

    print()

    print("--- Entry Points (excluded from orphan check) ---")
    for f in source_files:
        if is_entry_point(f.name, f.stem):
            rel = f.relative_to(root)
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
