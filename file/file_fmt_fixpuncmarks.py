import os
import re

def fix_punctuation_in_file(file_path):
    # Define the patterns for punctuation correction
    patterns = {
        r'\s+(\!)\s+': r'\1 ',
        r'\s+(\?)\s+': r'\1 ',
        r'\s+(\,)\s+': r'\1 ',
        r'\s+(\;)\s+': r'\1 ',
        r'\s+(\:)\s+': r'\1 ',
        r'\s+(\.)\s+': r'\1 ',
        # Handle punctuation at the end of a line (optional)
        r'\s+(\!)$': r'\1',
        r'\s+(\?)$': r'\1',
        r'\s+(\,)$': r'\1',
        r'\s+(\;)$': r'\1',
        r'\s+(\:)$': r'\1',
        r'\s+(\.)$': r'\1'
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        original_content = content  # Keep for comparison

        # Apply each pattern replacement
        for pattern, replacement in patterns.items():
            content = re.sub(pattern, replacement, content)

        # If changes were made, overwrite the file
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated punctuation in: {file_path}")

    except (UnicodeDecodeError, PermissionError):
        # Skip binary or restricted files
        pass

def fix_punctuation_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            fix_punctuation_in_file(file_path)

if __name__ == "__main__":
    project_dir = input("Enter the path to your project directory: ").strip()
    fix_punctuation_in_directory(project_dir)
    print("Punctuation correction complete.")

