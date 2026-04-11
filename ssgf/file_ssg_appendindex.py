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



def strip_front_matter(content):
    """
    Remove YAML front matter (--- ... ---) from Markdown content.
    """
    lines = content.splitlines(keepends=True)

    if len(lines) >= 2 and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "".join(lines[i + 1 :])

        # If front matter start found but no closing ---,
        # fall through and return full content

    return content

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
            with open(src, "r", encoding="utf-8") as f:
                src_content = f.read()

            src_content = strip_front_matter(src_content)

            # Append to destination
            with open(dst, "a", encoding="utf-8") as f:
                if not src_content.startswith("\n"):
                    f.write("\n")

                f.write(src_content)

            print(f"Replaced: {dst} from {src}")
        else:
            print(f"Skipped (no destination): {dst}")

if __name__ == "__main__":
    main()

