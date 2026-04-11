import os
import re

def process_line(line):
    """
    Process a line according to these rules:
    - If the line matches '** PartA &mdash;** PartB', then:
        * Keep 'PartA' unchanged (this is the unprocessed prefix).
        * Process 'PartB' (remove '*' and wrap in single '*...*').
        * Recombine as 'PartA ' + processed PartB.
    - If no pattern matches, process the entire line normally.
    """

    match = re.match(r"\*\*\s*(.*?)\s*&mdash;?\s*\*\*(.*)", line, re.IGNORECASE)

    if match:
        # Capture the "unprocessed" part and the part to review
        prefix = match.group(1).strip()
        to_review = match.group(2).strip()

        # Remove '*' and wrap processed content with one '*'
        cleaned = to_review.replace('*', '')
        processed_part = f"*{cleaned}*"

        # Combine prefix with processed portion
        combinedstre = f"**{prefix} &mdash;** {processed_part}".strip()
        return f"{combinedstre}\n"
    else:
        # No match → process the entire line
        cleaned = line.strip().replace('*', '')
        return f"*{cleaned}*\n"

def extract_and_replace(content):
    """
    Replace the text between the first H1 and first H2 with processed lines.
    """
    lines = content.splitlines()
    new_lines = []
    in_section = False
    section_started = False
    between_headers = []

    for line in lines:
        if line.startswith('##'):
            if in_section:
                in_section = False
                # Process captured lines
                processed = [process_line(l) for l in between_headers if l.strip()]
                new_lines.extend(processed)
                between_headers.clear()
            new_lines.append(line)
            continue

        elif line.startswith('# ') and not section_started:
            section_started = True
            in_section = True
            new_lines.append(f'{line}\n')
            continue

        if in_section:
            between_headers.append(line)
        else:
            new_lines.append(line)

    # If file had no H2 header — process to end
    if in_section:
        processed = [process_line(l) for l in between_headers if l.strip()]
        new_lines.extend(processed)

    return '\n'.join(new_lines) + '\n'

def process_markdown_files():
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            with open(filename, 'r', encoding='utf-8') as f:
                original = f.read()

            updated = extract_and_replace(original)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(updated)

            print(f"Updated: {filename}")

if __name__ == "__main__":
    process_markdown_files()

