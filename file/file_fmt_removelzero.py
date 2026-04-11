#!/usr/bin/env python3
import os
import sys
import re

def remove_leading_zeros(filename: str) -> str:
    """
    Remove leading zeros from numeric sequences in the filename.
    Examples:
        file-001.md -> file-1.md
        doc-0042-draft.txt -> doc-42-draft.txt
        000123.md -> 123.md
    """
    def replace_numbers(match):
        num = match.group(0)
        return str(int(num))
    
    return re.sub(r'\d+', replace_numbers, filename)

def rename_files_in_directory(directory: str, recursive: bool = False) -> int:
    """
    Rename files in the given directory, removing leading zeros.
    Returns the count of renamed files.
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        return -1
    
    renamed_count = 0
    
    if recursive:
        for dirpath, _, filenames in os.walk(directory):
            renamed_count += process_directory(dirpath, filenames)
    else:
        filenames = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        renamed_count = process_directory(directory, filenames)
    
    return renamed_count

def process_directory(dirpath: str, filenames: list) -> int:
    """Process files in a single directory."""
    renamed_count = 0
    
    for filename in filenames:
        new_filename = remove_leading_zeros(filename)
        
        if new_filename != filename:
            old_path = os.path.join(dirpath, filename)
            new_path = os.path.join(dirpath, new_filename)
            
            # Check if target filename already exists
            if os.path.exists(new_path):
                print(f"Skipping '{filename}': target '{new_filename}' already exists", file=sys.stderr)
                continue
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{filename}': {e}", file=sys.stderr)
    
    return renamed_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py /path/to/directory [-r]", file=sys.stderr)
        print("  -r: recursively process subdirectories", file=sys.stderr)
        sys.exit(1)
    
    directory = sys.argv[1]
    recursive = '-r' in sys.argv or '--recursive' in sys.argv
    
    renamed_count = rename_files_in_directory(directory, recursive)
    
    if renamed_count >= 0:
        print(f"\nTotal files renamed: {renamed_count}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

