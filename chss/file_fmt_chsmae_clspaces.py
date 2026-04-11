#!/usr/bin/env python3
"""
markdown_cleaner.py

Iterate through all Markdown files in a directory tree and replace
every run of two or more spaces with a single space – **but only
after the YAML front‑matter** (the block between the first two
lines that contain exactly `---`).

Usage:
    python markdown_cleaner.py /path/to/markdown/files
"""

import argparse
import pathlib
import re
import sys
from typing import List


def collapse_spaces(text: str) -> str:
    """
    Replace any run of two or more spaces with a single space.
    """
    return re.sub(r" {2,}", " ", text)


def process_file(md_path: pathlib.Path) -> None:
    """
    Read *md_path*, keep the front‑matter untouched and collapse
    spaces in the rest of the file.  Overwrite the original file.
    """
    # Read the file in UTF‑8 (most Markdown files are UTF‑8)
    try:
        lines = md_path.read_text(encoding="utf-8").splitlines(True)  # keep line endings
    except Exception as exc:
        print(f"[ERROR] Failed to read {md_path}: {exc}", file=sys.stderr)
        return

    # Find the first two '---' lines that define the front‑matter.
    # We only look at the top of the file.
    front_start: int | None = None
    front_end: int | None = None

    for idx, line in enumerate(lines):
        if line.strip() == "---":
            if front_start is None:
                front_start = idx
            else:
                front_end = idx
                break

    if front_start is not None and front_end is not None:
        # Keep everything up to and including the second '---' line
        front_matter = lines[: front_end + 1]
        body_lines = lines[front_end + 1 :]
    else:
        # No proper front‑matter – treat whole file as body
        front_matter = []
        body_lines = lines

    body_text = "".join(body_lines)
    cleaned_body = collapse_spaces(body_text)
    cleaned_body = cleaned_body.replace(' : ', ': ')
    cleaned_body = cleaned_body.replace(' ; ', '; ')
    cleaned_body = cleaned_body.replace(' . ', '. ')
    cleaned_body = cleaned_body.replace(' , ', ', ')
    cleaned_body = cleaned_body.replace(' ? ', '? ')
    cleaned_body = cleaned_body.replace(' ! ', '! ')

    # Write the cleaned content back
    try:
        md_path.write_text("".join(front_matter) + cleaned_body, encoding="utf-8")
        print(f"✅  {md_path}")
    except Exception as exc:
        print(f"[ERROR] Failed to write {md_path}: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean up double spaces in Markdown files while preserving front‑matter."
    )
    parser.add_argument(
        "directory",
        type=pathlib.Path,
        help="Path to the directory that contains Markdown files",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print a line for every processed file",
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"[ERROR] {args.directory!s} is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Recursively find all *.md files
    md_files: List[pathlib.Path] = list(args.directory.rglob("*.md"))

    if not md_files:
        print(f"[INFO] No Markdown files found in {args.directory}.", file=sys.stderr)
        sys.exit(0)

    for md_file in md_files:
        process_file(md_file)

    print(f"\nFinished processing {len(md_files)} file(s).")


if __name__ == "__main__":
    main()

