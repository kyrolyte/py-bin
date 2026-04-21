#!/usr/bin/env python3
"""
cbffmtscript.py
~~~~~~~~~~~~~~~~

A tiny helper that cleans up a Markdown file as described in
https://github.com/kyrolyte/misc/pmtdr/draft_cbffmtscript.md

Usage:
    python cbffmtscript.py /path/to/file.md
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import List

def read_markdown(path: Path) -> List[str]:
    """Read the file and return a list of lines including newlines."""
    return path.read_text(encoding="utf-8").splitlines(True)


def write_markdown(path: Path, lines: List[str]) -> None:
    """Write the list of lines back to *path*."""
    path.write_text("".join(lines), encoding="utf-8")


def merge_headers_and_paragraphs(lines: List[str]) -> List[str]:
    """
    Return a new list of lines after applying the two transformations.
    """
    out: List[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ---------- 1) Header merging -------------
        if stripped.startswith("## "):
            # flush any pending paragraph
            # (there should be none at this point, but we keep the logic for completeness)
            # gather h2 text
            h2_text = stripped[3:].strip()

            # skip following blank lines
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1

            # if we hit a h3 header immediately after skipping blanks
            if j < n and lines[j].strip().startswith("### "):
                h3_text = lines[j].strip()[4:].strip()
                new_header = f"## {h2_text} - {h3_text}\n"
                out.append(new_header)

                # skip the h3 line
                i = j + 1

                # skip any blank lines that follow the h3 header
                while i < n and lines[i].strip() == "":
                    i += 1

                # put a single blank line after the combined header
                out.append("\n")
                continue
            else:
                # no h3 under this h2 – keep the header as is
                out.append(line)
                i += 1
                continue

        # ---------- 2) Paragraph collapsing -------------
        # If this is a header (## or ###) keep it as is
        if stripped.startswith("#"):
            out.append(line)
            i += 1
            continue

        # Blank line – flush any pending paragraph
        if stripped == "":
            out.append(line)
            i += 1
            continue

        # Non‑header, non‑blank line – part of a paragraph
        # accumulate consecutive such lines
        paragraph = [line.rstrip("\n")]
        i += 1
        while i < n:
            nxt = lines[i]
            nxt_strip = nxt.strip()
            if nxt_strip == "" or nxt_strip.startswith("#"):
                break
            paragraph.append(nxt.rstrip("\n"))
            i += 1

        # Write the collapsed paragraph
        out.append(" ".join(paragraph) + "\n")
        # continue – i already points to the next line (header/blank)
    return out


def process_file(file_path: Path) -> None:
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    # 1. read original file
    original_lines = read_markdown(file_path)

    # 2. apply transformations
    transformed_lines = merge_headers_and_paragraphs(original_lines)

    # 3. create output directory (basename without extension)
    output_dir = file_path.with_suffix("").name
    output_dir_path = file_path.parent / output_dir
    output_dir_path.mkdir(exist_ok=True)

    # 4. write back to a file with the same name inside the new dir
    output_file = output_dir_path / file_path.name
    write_markdown(output_file, transformed_lines)

    print(f"Processed {file_path} → {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cbffmtscript.py /path/to/file.md")
        sys.exit(1)

    file_path = Path(sys.argv[1]).expanduser().resolve()
    try:
        process_file(file_path)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

