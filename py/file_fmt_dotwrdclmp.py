import os
import re

root = "."  # start directory

pattern = re.compile(r'\.([A-Z])')

for dirpath, dirnames, filenames in os.walk(root):
    for fname in filenames:
        # Filter if you only want certain files, e.g. .md:
        if not fname.endswith(".md"):
            continue

        fpath = os.path.join(dirpath, fname)

        # Read file
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()

        # Replace ".X" with ". X"
        new_text = pattern.sub(r'. \1', text)

        # Only write back if changed
        if new_text != text:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"Updated: {fpath}")

