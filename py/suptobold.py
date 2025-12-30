import os
import re
from pathlib import Path

SUPERSCRIPT_MAP = {
    '0': '⁰',  # U+2070
    '1': '¹',  # U+00B9
    '2': '²',  # U+00B2
    '3': '³',  # U+00B3
    '4': '⁴',  # U+2074
    '5': '⁵',  # U+2075
    '6': '⁶',  # U+2076
    '7': '⁷',  # U+2077
    '8': '⁸',  # U+2078
    '9': '⁹',  # U+2079
}

def superscript_repl(match):
    inner = match.group(1)
    if inner.isdigit():
        return ''.join(SUPERSCRIPT_MAP.get(ch, ch) for ch in inner)
    return ''.join(SUPERSCRIPT_MAP.get(ch, ch) for ch in inner)

def transform_line(line: str) -> str:
    pattern = re.compile(r'<sup>(.*?)</sup>')

    def repl(m):
        inner = m.group(1)
        supers = ''.join(SUPERSCRIPT_MAP.get(ch, ch) for ch in inner if ch.isdigit() or ch.isnumeric() or True)
        converted = ''.join(SUPERSCRIPT_MAP.get(ch, ch) for ch in inner)
        return f'**{converted}**'

    return pattern.sub(repl, line)

def process_file(filepath: Path) -> None:
    try:
        with filepath.open('r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with filepath.open('r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

    changed = False
    new_lines = []
    for line in lines:
        new_line = transform_line(line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)

    if changed:
        with filepath.open('w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated: {filepath}")

def is_markdown_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in {'.md', '.markdown', '.mdown', '.mdx'}

def walk_and_process(root_dir: Path) -> None:
    for path in root_dir.rglob('*'):
        if path.is_file() and is_markdown_file(path):
            process_file(path)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert <sup>n</sup> to bolded superscript in Markdown files.")
    parser.add_argument('directory', nargs='?', default='.', help="Directory to search (defaults to current directory)")
    args = parser.parse_args()

    root = Path(args.directory).resolve()
    if not root.exists():
        print(f"Directory not found: {root}")
        return

    walk_and_process(root)

if __name__ == '__main__':
    main()

