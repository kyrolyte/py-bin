#!/usr/bin/env python3
"""
Script to check markdown files in a directory recursively.
Files without an H1 header (#) will be listed in list.md at the same level as the target directory.
If the script is run from another location, use:
    python check_md.py /path/to/directory
"""

import os
import sys

def contains_h1_header(filepath):
    """Check if a markdown file contains an H1 header."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped.startswith('# ') or stripped == '#':
                    return True
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
    return False

def get_markdown_files(directory):
    """Get all markdown files in directory recursively."""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                md_files.append(os.path.join(root, filename))
    return md_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_md.py /path/to/directory")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)

    md_files = get_markdown_files(target_directory)

    if not md_files:
        print("No markdown files found in the specified directory.")
        return

    print(f"Found {len(md_files)} markdown file(s) to check.\n")

    files_without_h1 = []

    for filepath in md_files:
        basename = os.path.basename(filepath)
        if contains_h1_header(filepath):
            print(f"✓ Skipped: {filepath} (contains H1 header)")
        else:
            files_without_h1.append(basename)
            print(f"  ℹ️ Without H1 header: {filepath}")

    if files_without_h1:
        list_md_path = os.path.join(target_directory, "list.md")

        with open(list_md_path, 'a', encoding='utf-8') as f:
            for filename in files_without_h1:
                f.write(f"{filename}\n")

        print(f"\n✓ Added {len(files_without_h1)} file(s) without H1 headers to '{list_md_path}'")
    else:
        print("\n✓ All markdown files contain an H1 header.")

if __name__ == "__main__":
    main()
