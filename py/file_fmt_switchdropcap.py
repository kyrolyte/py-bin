# The purpose of this script is to create a placeholder for dropcaps. 
# For word processing documents like ODT, instead of a dedicated chapter header, a dropcap will be used instead
# A seperate script will be used as a pandoc filter to locate the span tag
# This script simply sets up the tag

import os
import re

# Function to process markdown files
def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_lines = []
    header_found = False
    chapter_number = None

    for i, line in enumerate(lines):
        # Check if the line is a header (starts with #)
        if line.startswith('# '):
            # Look for the number at the end of the header (e.g. "Chapter 2")
            match = re.search(r'(\d+)', line)
            if match:
                chapter_number = match.group(1)  # Extract the number from the header
                header_found = True
            # Skip this header line, since we will remove it
            continue

        # If a header was found, look for ^1^ or <sup>1</sup> and replace them
        if header_found:
            # Replace the instances of ^1^ or <sup>1</sup> with <span class="drop">{chapter_number}</span>
            line = re.sub(r'\^(\d+)\^', r'<span class="drop">\1</span>', line)
            line = re.sub(r'<sup>(\d+)</sup>', r'<span class="drop">\1</span>', line)
            
            # If we made a replacement, set header_found to False to stop further replacements
            if chapter_number:
                header_found = False

        new_lines.append(line)

    # Write the modified content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# Main function to iterate over markdown files in the current directory
def process_all_markdown_files():
    for filename in os.listdir('.'):
        if filename.endswith('.md'):  # Check if the file is a markdown file
            print(f"Processing file: {filename}")
            process_markdown_file(filename)

if __name__ == "__main__":
    process_all_markdown_files()

