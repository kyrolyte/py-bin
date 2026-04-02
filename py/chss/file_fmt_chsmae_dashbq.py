#!/usr/bin/env python3
"""
===================

This script walks through a user‑supplied directory (recursively) and performs
two transformations on every Markdown (`*.md`) file it finds:

1. **Add block‑quote markers after H2 headers**  
   For each `##` header the script looks at the first paragraph that follows it.  
   If that paragraph exists it prefixes every line of the paragraph with `> `,
   turning the paragraph into a Markdown block quote.

2. **Replace dash‑like characters with the HTML entity `&mdash;`**  
   All occurrences of the Unicode *em dash* (`—`), *en dash* (`–`), and the
   ASCII hyphen (`-`) are replaced by the string `&mdash;`.

The file is overwritten in‑place.  A small log is printed for each file that is
modified.

Usage
-----
    python markdown_processor.py /path/to/markdown/root

"""

import sys
import pathlib
import re
from typing import List

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def find_md_files(root: pathlib.Path) -> List[pathlib.Path]:
    """
    Return a list of all .md files under `root` (recursively).
    """
    md_files = [
        p for p in root.rglob("*.md")
        if p.name not in {"_index.md", "README.md"}
    ]
    # return list(root.rglob("*.md"))
    return md_files


def process_paragraphs(lines: List[str]) -> List[str]:
    """
    Find each H2 header (##) and add block‑quote markers to the first paragraph
    that follows it.

    The function walks through the list of lines in order.  When it sees a line
    that starts with '##' it remembers that position and then looks ahead for
    the first non‑blank line.  That line starts the paragraph; the paragraph
    continues until the next blank line.  Every line of that paragraph is
    prefixed with '> ' (unless it already starts with a block‑quote marker).
    """
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.lstrip().startswith("##"):
            # Find first non‑blank line after the header
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1

            if j < n and lines[j].strip() != "":
                # Start of the first paragraph
                para_start = j
                # Find end of paragraph (blank line or EOF)
                k = j
                while k < n and lines[k].strip() != "":
                    k += 1
                para_end = k  # exclusive

                # Add block‑quote marker to each line in the paragraph
                for p in range(para_start, para_end):
                    stripped = lines[p].lstrip()
                    # Avoid double‑quoting if already a block‑quote
                    if not stripped.startswith(">"):
                        lines[p] = "> " + lines[p]
            i = j
        else:
            i += 1
    return lines


def replace_dashes(content: str) -> str:
    """
    Replace all em‑dash (—), en‑dash (–) and ASCII hyphen (-) with '&mdash;'.
    """
    # Unicode code points: EM DASH U+2014, EN DASH U+2013
    # We replace them all in a single regex for speed.
    return re.sub(r'[\u2014\u2013-]', '&mdash;', content)


# --------------------------------------------------------------------------- #
# Main processing routine
# --------------------------------------------------------------------------- #

def process_file(md_path: pathlib.Path) -> bool:
    """
    Process a single Markdown file.  Return True if the file was modified.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Could not read {md_path}: {e}")
        return False

    # Step 1: add block‑quote markers
    lines = text.splitlines()
    lines = process_paragraphs(lines)

    # Step 2: replace dash characters
    new_text = "\n".join(lines)
    new_text = replace_dashes(new_text)
    new_text = new_text.replace('&mdash;&mdash;&mdash;','---')
    new_text = new_text.replace('single&mdash;section','single-section')

    if new_text != text:
        # Overwrite the file
        try:
            md_path.write_text(new_text, encoding="utf-8")
            return True
        except Exception as e:
            print(f"⚠️  Could not write {md_path}: {e}")
            return False
    return False


def main(root_dir: pathlib.Path):
    if not root_dir.is_dir():
        print(f"❌ {root_dir} is not a directory.")
        sys.exit(1)

    md_files = find_md_files(root_dir)
    if not md_files:
        print("No Markdown files found.")
        return

    modified = 0
    for md_path in md_files:
        if process_file(md_path):
            modified += 1
            print(f"✅ Modified: {md_path}")

    print(f"\nFinished. {modified} file(s) modified.")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python markdown_processor.py /path/to/markdown/root")
        sys.exit(1)

    root = pathlib.Path(sys.argv[1]).expanduser().resolve()
    main(root)
