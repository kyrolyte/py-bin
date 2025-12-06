# This script removes that top front-matter from markdown files
# The use case is so that if the files are converted to other formats (i.e. pdf, epub, etc) the front matter is not captured
# In addition, removing the front matter is for when multiple files need to be combined

import os

def remove_front_matter_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Detect YAML front matter at the top of the file
    if len(lines) >= 3 and lines[0].strip() == "---":
        # Find where the closing --- occurs
        closing_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                closing_index = i
                break

        # If both opening and closing delimiters exist, remove that section
        if closing_index is not None:
            lines = lines[closing_index + 1:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".md"):
                file_path = os.path.join(root, filename)
                remove_front_matter_from_file(file_path)


if __name__ == "__main__":
    target_directory = input("Enter the path to the directory containing markdown files: ").strip()
    process_directory(target_directory)
    print("Front matter removed from markdown files.")

