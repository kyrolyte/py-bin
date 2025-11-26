# This script was used for cleaning up file names for a static site generator; it removes extra zero characters and replaces underscores with hyphens.
# To use this script, simply run directly using Python and specify the directory where you would like to run it.

import os
import re

def rename_files_in_directory(base_path):
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            match = re.search(r'(\d+)', filename)
            if match:
                number_str = match.group(1)
                number = str(int(number_str))  # example: converts '001' -> '1'
                
                new_filename = re.sub(number_str, number, filename)
                new_filename = new_filename.replace('_', '-')
                
                old_file = os.path.join(root, filename)
                new_file = os.path.join(root, new_filename)

                if old_file != new_file:
                    print(f"Renaming: {filename} -> {new_filename}")
                    os.rename(old_file, new_file)

if __name__ == "__main__":
    target_directory = input("Enter the directory path to process: ").strip()
    if os.path.isdir(target_directory):
        rename_files_in_directory(target_directory)
        print("Renaming complete.")
    else:
        print("Invalid directory path.")
