import os
import sys

def process_markdown_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)

        stripped = line.strip()

        # Match headers: #, ##, ###
        if stripped.startswith("#") and stripped.split()[0] in {"#", "##", "###"}:
            # Check next line exists
            if i + 1 < len(lines):
                next_line = lines[i + 1]

                # If next line is not blank, insert a blank line
                if next_line.strip() != "":
                    updated_lines.append("\n")
                    changed = True

        i += 1

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print(f"Updated: {path}")


def walk_directory(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".md"):
                full_path = os.path.join(root, file)
                process_markdown_file(full_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python fix_md_headers.py /path/to/directory")
        sys.exit(1)

    root_dir = sys.argv[1]

    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory")
        sys.exit(1)

    walk_directory(root_dir)


if __name__ == "__main__":
    main()

