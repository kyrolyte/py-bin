# This script is for adding an extra hash to each `h` header in markdown
# Use-case is for when multiple files need to be added together, typically they fall under a new `h1`

import os
import re

def adjust_headers_in_file(filepath):
    """Adds one extra '#' to every Markdown header in the given file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    updated_lines = []
    header_pattern = re.compile(r'^(#{1,6})(\s+.*)')

    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Add one extra '#' at the front
            new_header = '#' + match.group(1) + match.group(2)
            updated_lines.append(new_header + '\n')
        else:
            updated_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)
    print(f"Updated headers in: {filepath}")

def recursively_adjust_markdown_headers(root_dir='.'):
    """Recursively finds all 'chapter.md' files and adjusts their headers."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if 'chapter' in filename.lower() or 'psalm' in filename.lower():
                filepath = os.path.join(dirpath, filename)
                adjust_headers_in_file(filepath)

if __name__ == '__main__':
    recursively_adjust_markdown_headers()

