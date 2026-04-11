import os
import re

def clean_blockquote_line(line: str) -> str:
    # Remove leading '>' (blockquote) and any whitespace at the end of the line
    line = line.lstrip('> ').rstrip()
    
    # Remove trailing quotation marks (both single and double)
    line = re.sub(r"[\"'’]+$", "", line)
    
    return line

def process_markdown_files(directory: str):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Only process markdown files (.md)
        if os.path.isfile(file_path) and filename.endswith('.md'):
            print(f"Processing {filename}...")
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Find the first blockquote line and clean it
            for i, line in enumerate(lines):
                if line.startswith('>'):
                    lines[i] = '> ' + clean_blockquote_line(line[1:]) + '    \n'  # Keep the '>' for blockquote
                    break  # Only modify the first blockquote line

            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)
            print(f"Finished processing {filename}")

# Set the directory where your markdown files are located
directory = '/home/username/project'  # Change this to the directory you want to process

process_markdown_files(directory)

