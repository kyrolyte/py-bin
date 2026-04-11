import os
import re
from pathlib import Path

# Pattern: lowercase letter followed immediately by a capitalized word
CLUMP_PATTERN = re.compile(r'([a-z])([A-Z][a-zA-Z]*)')

def should_ignore_word(word):
    """Check if word should be ignored (Mc/Mac names)."""
    return word.startswith('Mc') or word.startswith('Mac')

def fix_clumps_in_line(line):
    """Fix clumps in a single line, return (fixed_line, changes) where changes is list of (old, new)."""
    changes = []
    def replace_match(match):
        before = match.group(1)
        word = match.group(2)
        if should_ignore_word(word):
            return before + word  # No change
        new_text = before + ' ' + word
        changes.append((before + word, new_text))
        return new_text
    
    fixed_line = CLUMP_PATTERN.sub(replace_match, line)
    return fixed_line, changes

def fix_markdown_file(path):
    """Fix clumps in a markdown file and report changes."""
    original_lines = []
    fixed_lines = []
    all_changes = []
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        original_lines = f.readlines()
    
    for lineno, line in enumerate(original_lines, start=1):
        fixed_line, changes = fix_clumps_in_line(line.rstrip('\n'))
        if changes:
            all_changes.extend([(lineno, ch[0], ch[1]) for ch in changes])
        fixed_lines.append(fixed_line + '\n')
    
    if all_changes:
        # Write fixed content back to file
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        
        # Report changes
        print(f"Fixed {len(all_changes)} clump(s) in {path}:")
        for lineno, old, new in all_changes:
            print(f"  Line {lineno}: '{old}' → '{new}'")
        print()
    else:
        print(f"No changes needed in {path}")

def fix_directory(root_dir):
    """Recursively fix markdown files in directory."""
    root = Path(root_dir)
    md_files = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.lower().endswith('.md'):
                full_path = Path(dirpath) / filename
                md_files.append(full_path)
    
    if not md_files:
        print("No .md files found.")
        return
    
    print(f"Scanning {len(md_files)} markdown file(s) in {root_dir}...\n")
    for file_path in md_files:
        fix_markdown_file(file_path)

if __name__ == "__main__":
    # Change this to your markdown root directory
    directory_to_fix = "."
    fix_directory(directory_to_fix)

