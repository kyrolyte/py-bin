#!/usr/bin/env python3
"""
Update linkTitle strings in Markdown files.

For every Markdown file in the current directory this script searches
for the pattern:

    linkTitle: '{n}'

where `{n}` is an integer from 1 to 200 (inclusive).  Whenever that
pattern is found it is replaced with

    linkTitle: 'WORD {n}'

The original file is overwritten only when at least one replacement
has been made.  The script prints a short summary for each processed
file.

Usage
------
    python3 update_link_titles.py

Make sure you have write permission on the files you are updating.
"""

import pathlib
import re
import sys
from typing import Match


# --------------------------------------------------------------------------- #
# Regular expression that captures the number inside the quotes
# --------------------------------------------------------------------------- #
#   linkTitle: '{n}'
#   ^             ^
#   ^             |
#   |             number (1–200)
#
# We capture the number in a group so that we can test it in a
# replacement function.
PATTERN = re.compile(r"linkTitle:\s*'(\d{1,3})'")


def replacement(match: Match[str]) -> str:
    """
    Return the replacement string for a regex match.

    If the captured number is in the 1‑200 range we return
    ``linkTitle: 'WORD {n}'``.  Otherwise we return the original text
    unchanged so that numbers outside the desired range are left
    untouched.
    """
    n = int(match.group(1))
    if 1 <= n <= 200:
        return f"linkTitle: 'WORD {n}'"
    # No replacement – keep the original string
    return match.group(0)


def process_file(path: pathlib.Path) -> int:
    """
    Process a single Markdown file.

    Returns the number of replacements performed.
    """
    try:
        original = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"[!] Could not read {path}: {exc}", file=sys.stderr)
        return 0

    new_text, count = PATTERN.subn(replacement, original)
    if count:
        try:
            path.write_text(new_text, encoding="utf-8")
        except Exception as exc:
            print(f"[!] Could not write {path}: {exc}", file=sys.stderr)
            return 0
    return count


def main() -> None:
    # Find all *.md files in the current directory (no recursion)
    md_files = list(pathlib.Path(".").glob("*.md"))
    if not md_files:
        print("No Markdown files found in the current directory.")
        return

    total_files = 0
    total_replacements = 0

    for md_file in md_files:
        replacements = process_file(md_file)
        if replacements:
            print(f"{md_file}: {replacements} replacement(s) made.")
            total_replacements += replacements
            total_files += 1

    if total_files:
        print(f"\nProcessed {total_files} file(s) with {total_replacements} replacement(s).")
    else:
        print("\nNo replacements needed – all files already up‑to‑date.")


if __name__ == "__main__":
    main()

