#!/usr/bin/env python3
import os
import sys

def is_markdown_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in {'.md', '.markdown', '.mdown', '.mdwn', '.mdtxt', '.mdt'}

def replace_double_hyphen_in_file(file_path: str) -> bool:
    """
    Replace all instances of -- with &mdash; in the given file.
    Returns True if any replacement occurred.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        # If UTF-8 fails, try with a more tolerant encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception:
            return False

    new_content = content.replace('--', '&mdash;')
    if new_content != content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except OSError:
            return False
        return True
    return False

def main(root_dir: str) -> int:
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a directory.", file=sys.stderr)
        return 2

    total_replacements = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)
            if is_markdown_file(path):
                if replace_double_hyphen_in_file(path):
                    total_replacements += 1

    print(f"Processed; files modified: {total_replacements}")
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/start/directory", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))

