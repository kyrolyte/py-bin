# Purpose of this file is to print a list of the tags used in a USFM file

import re

def extract_tags_from_sfm(file_path):
    tag_pattern = r'\\[a-zA-Z0-9]+'
    tags = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Iterate through the file line by line
            for line in file:
                found_tags = re.findall(tag_pattern, line)
                tags.update(found_tags)

        print("Tags found in the file:")
        for tag in sorted(tags):
            print(tag)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    file_path = input("Enter the path to the .sfm file: ")
    extract_tags_from_sfm(file_path)

