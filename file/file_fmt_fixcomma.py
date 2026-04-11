import os

def fix_comma_formatting(root_dir='.'):
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(subdir, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                # Replace ' , ' with ', '
                new_content = content.replace(' , ', ', ')
                # Only write if there was a change
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)

if __name__ == "__main__":
    fix_comma_formatting('.')

