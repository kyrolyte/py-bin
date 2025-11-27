# This script adds a markdown front-matter to the file
# The purpose of this is so that documentation pages have an organized weight
# This script can be expanded to add other variables

import os
import re

def extract_title_and_weight(content):
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if not h1_match:
        return None, None
    
    title = h1_match.group(1).strip()
    number_match = re.search(r'\d+', title)
    weight = number_match.group(0) if number_match else None
    
    return title, weight

def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if content.startswith('---'):
        print(f"Skipping {filepath} - front matter already exists")
        return
    
    title, weight = extract_title_and_weight(content)
    
    if not title:
        print(f"Skipping {filepath} - no H1 header found")
        return
    
    front_matter = "---\n"
    if weight:
        front_matter += f"weight: {weight}\n"
    front_matter += "---\n\n"
    
    new_content = front_matter + content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filepath} - Weight: {weight}")

def process_directory(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md') and '_index' not in filename:
                filepath = os.path.join(dirpath, filename)
                process_markdown_file(filepath)

process_directory('.')  

