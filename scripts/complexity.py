#!/usr/bin/env python3
"""Complexity heuristics: function length, nesting depth, longest functions."""
import sys
import re
from pathlib import Path

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".cs", ".java", ".rb"}

FUNCTION_PATTERNS = {
    ".py": re.compile(r"^\s*(?:async\s+)?def\s+(\w+)\s*\("),
    ".ts": re.compile(r"(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*\([^)]*\)\s*\{)"),
    ".tsx": re.compile(r"(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*\([^)]*\)\s*\{)"),
    ".js": re.compile(r"(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*\([^)]*\)\s*\{)"),
    ".jsx": re.compile(r"(?:function\s+(\w+)|(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*\([^)]*\)\s*\{)"),
    ".rs": re.compile(r"^\s*(?:pub\s+)?(?:unsafe\s+)?fn\s+(\w+)"),
    ".go": re.compile(r"^\s*func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)"),
    ".cs": re.compile(r"(?:public|private|protected|internal|static|async|unsafe)\s+\S+\s+(\w+)\s*\("),
    ".java": re.compile(r"(?:public|private|protected|static|final)\s+\S+\s+(\w+)\s*\("),
    ".rb": re.compile(r"^\s*(?:def\s+(\w+)|(\w+)\s*=\s*->)"),
}


def measure_nesting(lines: list[str]) -> int:
    max_depth = 0
    depth = 0
    for line in lines:
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#") or stripped.startswith("//"):
            continue
        depth = (len(line) - len(line.lstrip())) // 4
        max_depth = max(max_depth, depth)
    return max_depth


def scan_file(f: Path) -> list[dict]:
    try:
        text = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    lines = text.splitlines()
    pattern = FUNCTION_PATTERNS.get(f.suffix.lower())
    if not pattern:
        return []

    functions = []
    brace_depth = 0
    in_function = False
    func_start = 0
    func_name = ""
    func_lines: list[str] = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        fm = pattern.search(line) if pattern else None
        if fm and not stripped.startswith("//") and not stripped.startswith("#"):
            if in_function:
                functions.append({
                    "name": func_name,
                    "line": func_start + 1,
                    "length": i - func_start,
                    "body": func_lines,
                })
            func_name = next(g for g in fm.groups() if g) or "(anonymous)"
            func_start = i
            func_lines = [line]
            in_function = True
            brace_depth = line.count("{") - line.count("}")
            continue

        if not in_function:
            continue

        func_lines.append(line)
        for c in line:
            if c == "{":
                brace_depth += 1
            elif c == "}":
                brace_depth -= 1

        # Function ends when brace_depth returns to starting level (for brace langs)
        # For Python, function ends when indent returns to base level
        if f.suffix.lower() in {".py", ".rb"}:
            prev_indent = len(func_lines[0]) - len(func_lines[0].lstrip())
            curr_indent = len(line) - len(line.lstrip())
            if curr_indent <= prev_indent and i > func_start + 1 and stripped:
                functions.append({
                    "name": func_name,
                    "line": func_start + 1,
                    "length": i - func_start,
                    "body": func_lines[:-1],
                })
                func_lines = [line]
                func_name = ""
                in_function = False
        elif brace_depth <= 0 and i > func_start + 1:
            functions.append({
                "name": func_name,
                "line": func_start + 1,
                "length": i - func_start + 1,
                "body": func_lines,
            })
            func_lines = []
            func_name = ""
            in_function = False

    if in_function and func_lines:
        functions.append({
            "name": func_name,
            "line": func_start + 1,
            "length": len(lines) - func_start,
            "body": func_lines,
        })

    for fn in functions:
        fn["nesting"] = measure_nesting(fn["body"])
        fn["file"] = str(f)

    return functions


def scan(root: Path, top_n: int = 20):
    all_funcs = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if f.suffix.lower() in SOURCE_EXTS and f.is_file():
            all_funcs.extend(scan_file(f))

    if not all_funcs:
        print("No functions found.")
        return

    all_funcs.sort(key=lambda x: -x["length"])
    longest = all_funcs[:top_n]

    all_funcs.sort(key=lambda x: -x["nesting"])
    deepest = all_funcs[:top_n]

    avg_len = sum(f["length"] for f in all_funcs) / len(all_funcs)
    max_len = max(f["length"] for f in all_funcs)
    avg_nest = sum(f["nesting"] for f in all_funcs) / len(all_funcs)

    print("=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print(f"\nTotal functions:     {len(all_funcs)}")
    print(f"Average length:      {avg_len:.1f} lines")
    print(f"Longest function:    {max_len} lines")
    print(f"Average nesting:     {avg_nest:.1f} levels")
    print()

    print(f"--- Longest Functions (top {top_n}) ---")
    print(f"  {'Lines':>6}  {'Nesting':>8}  {'File:Line':<50}  {'Function'}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*50}  {'-'*20}")
    for fn in longest:
        loc = f"{fn['file']}:{fn['line']}"
        print(f"  {fn['length']:>6}  {fn['nesting']:>8}  {loc:<50}  {fn['name']}")

    print()

    print(f"--- Deepest Nesting (top {top_n}) ---")
    print(f"  {'Nesting':>8}  {'Lines':>6}  {'File:Line':<50}  {'Function'}")
    print(f"  {'-'*8}  {'-'*6}  {'-'*50}  {'-'*20}")
    for fn in deepest:
        loc = f"{fn['file']}:{fn['line']}"
        print(f"  {fn['nesting']:>8}  {fn['length']:>6}  {loc:<50}  {fn['name']}")

    print("=" * 60)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(root)


if __name__ == "__main__":
    main()
