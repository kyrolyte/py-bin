#!/usr/bin/env python3
import sys
import os
import shutil

def collect_index_paths(root_dir):
    """
    Return a list of relative paths to _index.md files under root_dir.
    """
    paths = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            if name == "_index.md":
                full_path = os.path.join(dirpath, name)
                rel_path = os.path.relpath(full_path, root_dir)
                paths.append(rel_path)
    return paths

def main():
    if len(sys.argv) != 3:
        print("Usage: python replace_index_md.py <from_dir> <to_dir>")
        sys.exit(2)

    from_dir = os.path.abspath(sys.argv[1])
    to_dir = os.path.abspath(sys.argv[2])

    if not os.path.isdir(from_dir):
        print(f"Error: from_dir '{from_dir}' is not a directory.")
        sys.exit(1)
    if not os.path.isdir(to_dir):
        print(f"Error: to_dir '{to_dir}' is not a directory.")
        sys.exit(1)

    from_paths = collect_index_paths(from_dir)

    if not from_paths:
        print("No _index.md files found under the from_dir.Nothing to copy.")
        sys.exit(0)

    for rel_path in from_paths:
        src = os.path.join(from_dir, rel_path)
        dst = os.path.join(to_dir, rel_path)

        if os.path.exists(dst):
            dst_dir = os.path.dirname(dst)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Replaced: {dst} from {src}")
        else:
            print(f"Skipped (no destination): {dst}")

if __name__ == "__main__":
    main()

