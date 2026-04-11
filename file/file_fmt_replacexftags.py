import os
import re

# Directory containing your .usfm files
DIRECTORY = "./"

# Tag replacements as (old_tag, new_tag)
REPLACEMENTS = [
    (r'\\x', r'\\f'),
    (r'\\xo', r'\\fr'),
    (r'\\xt', r'\\ft'),
]

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Apply all replacements using regex
    for old, new in REPLACEMENTS:
        content = re.sub(old, new, content)

    # Write changes back to the same file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Updated: {filepath}")

def main():
    for root, _, files in os.walk(DIRECTORY):
        for filename in files:
            if filename.endswith(".usfm"):
                filepath = os.path.join(root, filename)
                process_file(filepath)

if __name__ == "__main__":
    main()

