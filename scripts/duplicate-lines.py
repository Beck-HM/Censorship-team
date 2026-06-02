#!/usr/bin/env python3
"""Detect cross-file duplicate or near-duplicate code blocks."""
import sys
import re
import hashlib
from pathlib import Path
from collections import defaultdict

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "target", "build", "dist",
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".opencode", ".claude", ".agents",
}

SOURCE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".cs", ".java", ".rb"}

MIN_BLOCK_LINES = 4
MIN_SIMILARITY = 0.85


def normalize_line(line: str) -> str:
    line = line.strip()
    # Remove comments
    for marker in ["#", "//", "--"]:
        if marker in line:
            line = line.split(marker)[0]
    # Normalize whitespace
    line = " ".join(line.split())
    return line


def line_fingerprint(line: str) -> str:
    """Fingerprint: lowercase, remove specific tokens (identifiers, numbers)."""
    n = normalize_line(line)
    n = re.sub(r'\b[a-zA-Z_]\w*\b', 'ID', n)
    n = re.sub(r'\b\d+\b', 'NUM', n)
    n = re.sub(r'["\'][^"\']*["\']', 'STR', n)
    return n


def extract_blocks(filepath: Path, min_lines: int = MIN_BLOCK_LINES) -> list[dict]:
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    lines = text.splitlines()
    if len(lines) < min_lines:
        return []

    blocks = []
    # Sliding window: extract overlapping blocks of `min_lines` length
    for i in range(len(lines) - min_lines + 1):
        block_lines = lines[i:i + min_lines]
        fp = "|".join(line_fingerprint(l) for l in block_lines)
        raw = "\n".join(normalize_line(l) for l in block_lines)
        if not raw.strip():
            continue
        h = hashlib.md5(fp.encode()).hexdigest()
        blocks.append({
            "hash": h,
            "file": str(filepath),
            "start_line": i + 1,
            "end_line": i + min_lines,
            "raw": raw,
        })

    return blocks


def scan(root: Path):
    all_blocks: list[dict] = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if any(p in rel.parts for p in EXCLUDE_DIRS):
            continue
        if f.suffix.lower() in SOURCE_EXTS and f.is_file():
            all_blocks.extend(extract_blocks(f))

    if not all_blocks:
        print("No code blocks found.")
        return

    # Group by hash (identical fingerprint = similar code)
    groups: dict[str, list[dict]] = defaultdict(list)
    for b in all_blocks:
        groups[b["hash"]].append(b)

    # Filter groups with duplicates across different files
    duplicates = []
    for h, blocks in groups.items():
        unique_files = set(b["file"] for b in blocks)
        if len(unique_files) > 1:
            duplicates.append((h, blocks, len(unique_files)))

    # Sort by number of affected files
    duplicates.sort(key=lambda x: -x[2])

    print("=" * 60)
    print("DUPLICATE CODE ANALYSIS")
    print("=" * 60)
    print(f"\nFiles scanned:    {len(set(b['file'] for b in all_blocks))}")
    print(f"Blocks analyzed: {len(all_blocks)}")
    print(f"Duplicate groups: {len(duplicates)}")
    print(f"Min block size:  {MIN_BLOCK_LINES} lines")
    print()

    shown = 0
    for h, blocks, file_count in duplicates[:20]:
        b0 = blocks[0]
        print(f"--- Duplicate Group (across {file_count} files) ---")
        for b in blocks[:6]:
            loc = f"{b['file']}:{b['start_line']}-{b['end_line']}"
            print(f"  {loc}")
        if len(blocks) > 6:
            print(f"  ... and {len(blocks) - 6} more occurrences")
        print(f"  Preview:\n{b0['raw'][:200]}")
        print()
        shown += 1

    if shown < len(duplicates):
        print(f"... and {len(duplicates) - shown} more duplicate groups")
    print("=" * 60)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    scan(root)


if __name__ == "__main__":
    main()
