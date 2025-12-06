#!/usr/bin/env python3

# This script will search for instances where three or more `.` characters appear
# Instead the dots, an &mdash; is used instead within the markdown file


import re
from pathlib import Path
import sys

# Regex: optional spaces, 3+ literal dots, optional spaces
pattern = re.compile(r' *\.{3,} *')

def clean_file(path: Path):
    text = path.read_text(encoding="utf-8")
    new_text = pattern.sub("&mdash;", text)
    if new_text != text:
        # Optional: backups can be created if working with a lot of files
        # backup = path.with_suffix(path.suffix + ".bak")
        # backup.write_text(text, encoding="utf-8")
        path.write_text(new_text, encoding="utf-8")
        print(f"Cleaned: {path}")

def main(root_dir: str):
    root = Path(root_dir)
    for path in root.rglob("*.md"):  # all markdown files recursively
        clean_file(path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} PATH_TO_DIRECTORY")
        sys.exit(1)
    main(sys.argv[1])

