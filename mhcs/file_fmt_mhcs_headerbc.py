#!/usr/bin/env python3
import os
import re
import sys

def process_header(line: str) -> str:
    if not re.match(r'^(#{2,4})\s', line):
        return line

    def fix_parentheses(match):
        content = match.group(1).strip()
        content = re.sub(r'\.\s*$', '', content)
        def repl_year_abbrev(m):
            letters = (m.group(1) + m.group(2)).upper()  # BC or AD
            year = m.group(3)
            return f"{year} {letters}"

        content = re.sub(
            r'\b(b|a)\.\s*(c|d)\.\s*(\d+)\b',
            repl_year_abbrev,
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(
            r'\b(b|a)\.\s*(c|d)\.\b',
            lambda m: (m.group(1) + m.group(2)).upper(),
            content,
            flags=re.IGNORECASE,
        )

        content = re.sub(r'\.', '', content)

        content = re.sub(r'\s{2,}', ' ', content).strip()

        return f"({content})"

    line = re.sub(r'\(([^()]*)\)', fix_parentheses, line)
    line = re.sub(r'\.\s*(?=\()', ' ', line)
    line = re.sub(r'\.\s*$', '', line)
    return line


def process_markdown_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = [process_header(line) for line in lines]

    if updated_lines != lines:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        print(f"Updated: {filepath}")


def scan_directory(root_dir: str):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
            if filename.startswith('_') or filename.lower() == 'readme.md':
                continue
            full_path = os.path.join(dirpath, filename)
            process_markdown_file(full_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/directory")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    scan_directory(directory)

