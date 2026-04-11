import sys
import os
import re
from pathlib import Path

def clean_description(text):
    """
    Remove wrapping double quotes and clean common YAML escape sequences.
    """
    text = text.strip()

    # Remove surrounding double quotes if present
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    # Clean common unnecessary escapes
    text = text.replace(r"\'", "'")
    text = text.replace(r"\"", '"')
    text = text.replace(r"\/", "/")

    return text.strip()


def remove_markdown_references(text: str) -> str:
    cleaned = re.sub(r'\[\^[^\]]+\]', '', text)
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
    
    return cleaned

def convert_description_to_block(front_matter):
    """
    Convert description field to YAML block style (>) if it exists.
    """
    lines = front_matter.splitlines()
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Match description line (simple scalar only)
        match = re.match(r'^description:\s*(.+)', line)
        if match:
            value = match.group(1)
            truncated = remove_markdown_references(value)
            cleaned = clean_description(truncated)

            # Replace with block style
            new_lines.append("description: >")
            new_lines.append(f"  {cleaned}")

        else:
            new_lines.append(line)

        i += 1

    return "\n".join(new_lines)


def process_file(filepath):
    content = filepath.read_text(encoding="utf-8")

    # Check for YAML front matter
    if not content.startswith("---"):
        return

    parts = content.split("---", 2)
    if len(parts) < 3:
        return

    _, front_matter, rest = parts

    if "description:" not in front_matter:
        return

    new_front_matter = convert_description_to_block(front_matter)

    new_content = f"---{new_front_matter}\n---{rest}"

    filepath.write_text(new_content, encoding="utf-8")
    print(f"Updated: {filepath}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/folder")
        sys.exit(1)

    root = Path(sys.argv[1])

    if not root.exists():
        print("Directory does not exist.")
        sys.exit(1)

    for md_file in root.rglob("*.md"):
        process_file(md_file)


if __name__ == "__main__":
    main()
