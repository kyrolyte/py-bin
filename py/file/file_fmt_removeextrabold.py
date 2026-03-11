#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path

def remove_bold_formatting(content):
    """
    Remove bold markdown formatting (**text**) while preserving inner content.
    Handles nested or repeated bold markers safely using non-greedy matching.
    """
    return re.sub(r'\*\*([^*]+)\*\*', r'\1', content)

def process_markdown_file(file_path):
    """
    Read, process, and write the markdown file after removing bold formatting.
    Uses atomic writing to prevent data loss on failure.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = remove_bold_formatting(content)

        if content != new_content:
            with open(file_path + '.tmp', 'w', encoding='utf-8') as tmp_f:
                tmp_f.write(new_content)
            os.replace(file_path + '.tmp', file_path)  # Atomic rename
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}", file=sys.stderr)

def process_directory(directory):
    """
    Recursively iterate through the given directory and process all .md files.
    """
    markdown_files = [
        f for f in Path(directory).rglob('*.md') if f.is_file()
    ]

    if not markdown_files:
        print("No Markdown files found.", file=sys.stderr)
        return

    for md_file in markdown_files:
        process_markdown_file(str(md_file))
        print(f"✓ Processed: {md_file}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <directory_path>", file=sys.stderr)
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.is_dir():
        print(f"❌ Error: '{directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    process_directory(directory)
    print("✅ Done!")

if __name__ == "__main__":
    main()
