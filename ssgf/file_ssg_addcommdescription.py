import os
import sys
import re
from pathlib import Path

def sanitize_folder_name(raw_folder):
    words = raw_folder.split()                                                                                                                    
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words) 

def process_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        content = "".join(lines)
        header_match = re.search(r'^#\s+.*?(\d+)\s*$', content, re.MULTILINE)
        outline_match = re.search(r'^## Chapter Outline(.*)', content, re.MULTILINE | re.DOTALL)

        if not header_match:
            print(f"Skipping {file_path}: No number found in first H1 header.")
            return
        
        if not outline_match:
            print(f"Skipping {file_path}: No chapter outline found.")
            return

        lines = content.splitlines()
        line_index = outline_match.end()
        description_value = ""

        for line in lines:
            if line.startswith("- "):
                description_value += line + ". "

        dv_cleaned = description_value.replace('- ', '').strip()

        extracted_number = header_match.group(1)
        raw_folder = file_path.parent.name
        folder_name_pre = raw_folder.capitalize().replace('_', ' ').replace('-', ' ')
        folder_name = sanitize_folder_name(folder_name_pre)
        new_title = f"{folder_name} {extracted_number}"
        updated_lines = []
        title_added = False
        
        for line in lines:
            if "weight:" in line and not title_added:
                updated_lines.append(f"title: \"{new_title} | Read the Matthew Henry Concise Bible Commentary Online\"\n")
                updated_lines.append(f"linkTitle: \"{extracted_number}\"\n")
                updated_lines.append(f"description: \"In this chapter: {dv_cleaned}\"\n")
                title_added = True
            if f"# Chapter {extracted_number}" in line:
                updated_lines.append(f"# {folder_name} {extracted_number} \n")
                continue;

            updated_lines.append(line + "\n")

        if title_added:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            print(f"Updated: {file_path} -> Title: {new_title}")
        else:
            print(f"Skipping {file_path}: Could not find 'weight:' in front matter.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py ./path/to/folder")
        return

    target_dir = Path(sys.argv[1])
    if not target_dir.is_dir():
        print(f"Error: {target_dir} is not a valid directory.")
        return

    for file in target_dir.rglob("*.md"):
        if file.name.startswith("_") or file.name.upper() == "README.MD":
            continue
        
        process_markdown_file(file)

if __name__ == "__main__":
    main()
