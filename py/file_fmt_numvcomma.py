# Purpose of this script is to space out clumped words that follow a number and comma
# For example: something like this `9,content` becomes `9, content`

import os
import re

# Adjust this if you want to restrict to certain extensions, e.g. ('.md',)
FILE_EXTENSIONS = ('.md',)

# Regex: digit,capital-letter  -> capture digit and letter
pattern = re.compile(r'([0-9]),([A-Z])')

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Perform replacement
    modified = pattern.sub(r'\1, \2', original)

    # Only write back if something changed
    if modified != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated: {path}")

def main(root='.'):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            # Optionally restrict to markdown files
            if FILE_EXTENSIONS and not filename.endswith(FILE_EXTENSIONS):
                continue
            full_path = os.path.join(dirpath, filename)
            fix_file(full_path)

if __name__ == '__main__':
    # Use the current directory as the project root
    main('.')

