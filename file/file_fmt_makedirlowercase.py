# Useful if a directory has a lot of sub-directories with mixed casing

import os

def lowercase_folders():
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            lower_name = item.lower()
            lower_path = os.path.join(current_dir, lower_name)
            if item != lower_name:
                os.rename(item_path, lower_path)
                print(f'Renamed: {item} -> {lower_name}')

if __name__ == "__main__":
    lowercase_folders()

