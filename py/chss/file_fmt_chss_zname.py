#!/usr/bin/env python3
import os
import sys

def rename_files(directory):
    """
    Renames files in a directory that start with 'sermonout' 
    before the '_' to 'sermon'.
    """
    for filename in os.listdir(directory):
        if filename.startswith("sermonout_"):
            new_filename = "sermon_" + filename[len("sermonout_"):].replace("_", "")
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)

            try:
                os.rename(old_path, new_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found in '{directory}'")
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/dir")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        sys.exit(1)

    rename_files(directory)
