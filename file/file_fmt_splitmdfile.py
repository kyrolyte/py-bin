#!/usr/bin/env python3
"""
split_markdown.py

Split a Markdown file into multiple files, one per H1 header.

Usage:
    python split_markdown.py /path/to/file.md
"""

import argparse
import os
import re
import sys
from pathlib import Path


def sanitize_filename(header: str) -> str:
    """
    Convert a header string to a safe, lowercase file‑name:
    * strip leading/trailing whitespace
    * replace internal spaces with dashes
    * keep only alphanumerics, dashes, and underscores
    * add a .md extension
    """
    header = header.strip()
    # Replace spaces with dashes
    header = header.replace(" ", "-")
    # Keep only allowed characters
    header = re.sub(r"[^a-zA-Z0-9\-_]", "", header)
    # Make lowercase
    header = header.lower()
    # Append .md
    return f"{header}.md"


def split_markdown(source_path: Path) -> None:
    """
    Split the Markdown file at `source_path` into separate files.
    Each H1 header (# ) starts a new file.
    """
    if not source_path.is_file():
        raise FileNotFoundError(f"File not found: {source_path}")

    # Read the whole file once
    content = source_path.read_text(encoding="utf-8")

    # Regex to capture H1 lines and the text that follows
    # It splits on lines that start with a single '# '.
    # The split keeps the header lines as separate tokens.
    pattern = re.compile(r"(^# .+?$)", flags=re.MULTILINE)
    parts = pattern.split(content)

    # parts will look like:
    # [text_before_first_header, '# Header 1', text_after_header1, '# Header 2', ...]
    # We ignore any leading text before the first H1 header.

    output_dir = source_path.parent
    current_header = None
    buffer = []

    for part in parts:
        if part.startswith("# "):
            # Found a header – write the previous buffer
            if current_header is not None:
                file_name = sanitize_filename(current_header)
                out_path = output_dir / file_name
                out_path.write_text("\n".join(buffer).lstrip("\n"), encoding="utf-8")
                print(f"Written: {out_path}")

            # Start new block
            current_header = part[2:].strip()  # remove '# ' prefix
            buffer = []
        else:
            # Regular content – keep as-is
            buffer.append(part)

    # Write the last block if there was at least one header
    if current_header is not None:
        file_name = sanitize_filename(current_header)
        out_path = output_dir / file_name
        out_path.write_text("\n".join(buffer).lstrip("\n"), encoding="utf-8")
        print(f"Written: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a Markdown file into separate files per H1 header."
    )
    parser.add_argument(
        "markdown_file",
        help="Path to the Markdown file to split.",
    )
    args = parser.parse_args()

    source_path = Path(args.markdown_file).expanduser().resolve()
    try:
        split_markdown(source_path)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
