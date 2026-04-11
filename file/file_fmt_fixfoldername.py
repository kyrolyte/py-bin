import os
import re

# Path to the parent directory (use "." for current directory)
BASE_DIR = "."

pattern = re.compile(r"(volume)[-_]?(\d+)", re.IGNORECASE)

for name in os.listdir(BASE_DIR):
    old_path = os.path.join(BASE_DIR, name)

    # Only process directories
    if not os.path.isdir(old_path):
        continue

    match = pattern.fullmatch(name)
    if not match:
        continue

    volume_word, number = match.groups()
    new_name = f"{volume_word.lower()}-{int(number)}"
    new_path = os.path.join(BASE_DIR, new_name)

    # Skip if already correctly named
    if name == new_name:
        continue

    # Avoid overwriting an existing directory
    if os.path.exists(new_path):
        print(f"Skipping '{name}' → '{new_name}' (target exists)")
        continue

    print(f"Renaming '{name}' → '{new_name}'")
    os.rename(old_path, new_path)

