import os
import re

# Function to process a single USFM file
def process_usfm_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace all instances of \+wh with ''
    content = content.replace(r'\+wh', '')
    
    # Replace all instances of \+wh* with ''
    content = content.replace(r'\+wh*', '')
    
    # Ensure encapsulated content (e.g., { } or \+xxx{content}) is preserved by excluding from replacements
    # Match any text like \+wh or \+wh* and avoid content inside curly braces
    content = re.sub(r'\\\+wh[^\}]*(?=\})', '', content)  # to remove \+wh in encapsulated content
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Iterate over all files in the current directory
def process_all_usfm_files():
    # Get list of all files in the current directory
    for filename in os.listdir('.'):
        # Check if the file is a USFM file
        if filename.endswith('.usfm'):
            print(f"Processing file: {filename}")
            process_usfm_file(filename)
            print(f"Finished processing: {filename}")

if __name__ == "__main__":
    # Process all USFM files in the current directory
    process_all_usfm_files()

