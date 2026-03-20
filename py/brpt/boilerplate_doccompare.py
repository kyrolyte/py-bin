# A draft script for comparing markdown files
# Uses a template file

import os
import re
import difflib
import json
from pathlib import Path

# Configuration
BOILERPLATE_FILE = "boilerplate.md"
OUTPUT_DIR = "cleaned_markdowns"
TEMPLATE_SECTIONS = [
    "Project Title",
    "Overview",
    "Requirements",
    "Installation",
    "Usage",
    "Contributing",
    "License",
]

# Load boilerplate content
def load_boilerplate(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

BOILERPLATE_TEXT = load_boilerplate(BOILABLE_FILE)

# Parse boilerplate sections into expected structure
def parse_boilerplate(content: str):
    sections = {}
    current_section = None

    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# ") and line[2:] not in SECTIONS:
            current_section = line[2:]
            sections[current_section] = []
        elif line and current_section:
            sections[current_section].append(line)
    return sections

TEMPLATE_STRUCTURE = parse_boilerplate(BOILERPLATE_TEXT)

# Compare a markdown file to the template
def compare_to_template(md_content: str, template_sections: dict):
    template_lines = [line for line in BOILERPLATE_TEXT.splitlines() if not line.startswith("---")]
    md_lines = md_content.splitlines()

    # Simple line-by-line comparison
    diff = difflib.ndiff(template_lines, md_lines, lineterm="")
    changes = "\n".join(diff)

    issues = []

    # Check for missing sections
    for section in template_sections:
        if section not in template_lines:
            issues.append(f"Missing required section: {section}")

    # Check for extra/misplaced sections
    for line in md_lines:
        if line.startswith("# ") and line[2:] in template_sections:
            continue
        else:
            issues.append(f"Unexpected line: '{line}'")

    return {
        "changes": changes,
        "missing_sections": issues,
        "extra_lines": [line for line in md_lines if line.strip() and not line.startswith("#")]
    }

# Apply basic fixes (e.g., insert missing headers)
def apply_suggestions(md_lines, changes):
    # Simple example: insert "Overview" if missing
    if "Overview" not in md_lines:
        md_lines.insert(1, "# Overview")

    # Add "---" separator if not present
    if not md_lines.endswith("---"):
        md_lines.append("---")

    return "\n".join(md_lines)

# Main function
def main():
    input_dir = Path(input("Enter directory path to scan: ").strip())
    output_dir = Path(OUTPUT_DIR)

    os.makedirs(output_dir, exist_ok=True)

    for md_file in input_dir.glob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            result = compare_to_template(content, TEMPLATE_STRUCTURE)
            fixed_content = apply_suggestions(result["changes"], content)

            output_path = output_dir / md_file.name
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)

            print(f"Processed: {md_file.name} -> {output_path}")
            print("  - Suggestions applied:")
            for issue in result["missing_sections"] + result["extra_lines"]:
                print(f"    • {issue}")

        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")

if __name__ == "__main__":
    main()


