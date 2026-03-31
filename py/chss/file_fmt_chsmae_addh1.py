#!/usr/bin/env python3
"""
add_h1_header.py

Recursively add a top‑level (#) header to Markdown files
that lack one.  The header is derived from the file name,
with hyphens replaced by spaces and title‑cased.

Usage:
    python add_h1_header.py /path/to/docs

The script will modify the files *in place*.
"""

import argparse
import pathlib
import re
import sys
from typing import Iterable

# ---------------------------------------------------------------------------

def has_h1(content: str) -> bool:
    """
    Return True if the Markdown content contains an H1 header
    (# …) anywhere in the file.  We look for a line that starts
    with optional whitespace followed by a single # and a space.
    """
    return bool(re.search(r'^\s*#\s+', content, flags=re.MULTILINE))

def header_from_filename(stem: str) -> str:
    """
    Convert a filename (without extension) to the header text.
    Hyphens are replaced by spaces and the result is title‑cased.
    """
    # Replace hyphens, keep other characters (numbers, etc.)
    cleaned = stem.replace('-', ' ')
    # Title‑case: each word capitalised.  This matches the example
    # ("january-30" → "January 30").
    return cleaned.title()

def process_file(md_path: pathlib.Path) -> None:
    """
    Read the Markdown file, add an H1 header at the top if it does
    not already contain one, and overwrite the file.
    """
    content = md_path.read_text(encoding='utf-8')
    if has_h1(content):
        # Already has an H1 – nothing to do
        return

    # Build the header
    header = header_from_filename(md_path.stem)
    new_content = f'# {header}\n\n{content}'
    md_path.write_text(new_content, encoding='utf-8')
    print(f'Added header to: {md_path}')

def walk_markdown(root: pathlib.Path) -> Iterable[pathlib.Path]:
    """
    Yield all Markdown files under *root* (recursively) except
    those whose names are in the ignore list.
    """
    ignore_names = {'_index.md', 'README.md'}
    for md in root.rglob('*.md'):
        if md.name in ignore_names:
            continue
        yield md

# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Add an H1 header to Markdown files that lack one.'
    )
    parser.add_argument(
        'directory',
        type=pathlib.Path,
        help='Directory to scan (recursively).'
    )
    args = parser.parse_args()

    root = args.directory.expanduser().resolve()
    if not root.is_dir():
        print(f'Error: {root} is not a directory.', file=sys.stderr)
        sys.exit(1)

    total, added = 0, 0
    for md_path in walk_markdown(root):
        total += 1
        prev = md_path.read_text(encoding='utf-8')
        if has_h1(prev):
            continue
        process_file(md_path)
        added += 1

    print(f'\nProcessed {total} Markdown files – added header to {added} of them.')

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    main()

