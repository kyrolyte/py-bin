# Purpose of this script is to print the USFM tags from files in a directory

import re
import os

def extract_tags_from_sfm(file_path):
    tag_pattern = r'\\[a-zA-Z0-9]+'
    tags = set()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                found_tags = re.findall(tag_pattern, line)
                tags.update(found_tags)

        return tags

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {e}")
    
    return set()

def extract_tags_from_directory(directory_path):
    all_tags = set()

    if not os.path.isdir(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return

    for filename in os.listdir(directory_path):
        # Process only .sfm files
        if filename.endswith('.sfm') or filename.endswith('.SFM') or filename.endswith('.usfm') or filename.endswith('.USFM'):
            file_path = os.path.join(directory_path, filename)
            print(f"Extracting tags from: {filename}")
            file_tags = extract_tags_from_sfm(file_path)
            all_tags.update(file_tags)

    if all_tags:
        print("\nTags found in all files:")
        for tag in sorted(all_tags):
            print(tag)
    else:
        print("No tags were found in the specified directory.")

if __name__ == '__main__':
    directory_path = input("Enter the path to the directory containing .sfm files: ")
    extract_tags_from_directory(directory_path)

