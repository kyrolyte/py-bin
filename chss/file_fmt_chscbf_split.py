import sys
import re
from pathlib import Path

def split_markdown_by_h2(file_path):
    input_path = Path(file_path)
    
    if not input_path.exists():
        print(f"Error: File '{file_path}' not found.")
        return

    # Read the content of the source file
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split the content using H2 headers (##)
    # We use a lookahead (?=## ) to keep the delimiter (the header) in the resulting strings
    sections = re.split(r'\n(?=## )', content)
    
    # Handle cases where the file might start with text before the first H2
    # or starts immediately with an H2
    if sections[0].startswith('## '):
        start_index = 0
    else:
        # If there's content before the first H2, we skip it or 
        # treat it as section 0 depending on your preference.
        # Here, we'll start numbering from the first actual H2 found.
        start_index = 1

    count = 1
    for i in range(start_index, len(sections)):
        section_content = sections[i].strip()
        if not section_content:
            continue

        # Generate the new filename: originalname-number.md
        new_filename = f"{input_path.stem}-{count}{input_path.suffix}"
        output_path = input_path.parent / new_filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        print(f"Created: {new_filename}")
        count += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_md.py /path/to/file.md")
    else:
        split_markdown_by_h2(sys.argv[1])
