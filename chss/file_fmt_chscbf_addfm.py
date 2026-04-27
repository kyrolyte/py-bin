#!/usr/bin/env python3
import sys
import os
import re
import yaml
from pathlib import Path
from collections import OrderedDict
from typing import List, Tuple

def read_file(path: Path) -> str:
    """Return the whole file content."""
    return path.read_text(encoding="utf-8")

def write_file(path: Path, content: str) -> None:
    """Overwrite the file with *content*."""
    path.write_text(content, encoding="utf-8")

def split_front_matter(content: str) -> Tuple[str, str]:
    lines = content.splitlines(True)   # keep line endings

    if not lines or lines[0].strip() != "---":
        raise ValueError("File does not start with '---'")

    # Find the next line that is exactly '---' (ignoring line ending).
    try:
        end_idx = next(i for i, l in enumerate(lines[1:], 1) if l.strip() == "---")
    except StopIteration:
        raise ValueError("No closing '---' found for YAML front‑matter")

    yaml_block = "".join(lines[:end_idx + 1])   # include closing '---'
    body = "".join(lines[end_idx + 1 :])
    return yaml_block, body

def parse_yaml(yaml_block: str) -> OrderedDict:
    """
    Parse the YAML block (excluding the surrounding '---' lines) into
    an OrderedDict so that the original key order is preserved.
    """
    # Remove the surrounding '---' lines
    yaml_text = "\n".join(yaml_block.splitlines(True)[1:-1]).strip()
    data = yaml.safe_load(yaml_text)
    if not isinstance(data, dict):
        raise ValueError("YAML front‑matter is not a mapping")
    return OrderedDict(data)

def build_new_yaml(old_yaml: OrderedDict, title: str,
                   link_title: str, description: str) -> OrderedDict:
    """
    Re‑order keys as:
        title, linkTitle, weight, description
    If any key is missing it is added.
    """
    new_yaml: OrderedDict = OrderedDict()

    new_yaml["title"] = title
    new_yaml["linkTitle"] = link_title

    # Preserve weight if present
    if "weight" in old_yaml:
        new_yaml["weight"] = old_yaml["weight"]

    new_yaml["description"] = description

    return new_yaml

def yaml_to_text(yaml_dict: OrderedDict) -> str:
    """
    Dump the OrderedDict back to a YAML string, surrounded by '---' lines.
    """
    # PyYAML can dump a plain dict while keeping order
    plain_dict = dict(yaml_dict)
    yaml_text = yaml.safe_dump(
        plain_dict,
        default_flow_style=False,
        sort_keys=False,
    )
    # Add the surrounding '---' and a trailing blank line
    return f"---\n{yaml_text}---\n\n"

def process_file(filepath: Path) -> None:
    """
    Process *filepath* in place – the front‑matter block is rewritten
    according to the rules described in the module docstring.
    """
    content = read_file(filepath)
    yaml_block, body = split_front_matter(content)
    yaml_dict = parse_yaml(yaml_block)

    # ----- 1. Get the H1 header ---------------------------------
    body_lines = body.splitlines(True)
    h1_line = next((l for l in body_lines if l.startswith("# ")), None)
    if h1_line is None:
        raise ValueError(f"No H1 header found in {filepath}")
    h1_text = h1_line[2:].strip()

    # Title: "<H1> | Read Online"
    new_title = f"{h1_text} | Online Daily Devotional"

    # ----- 2. linkTitle from file name ----------------------------
    number_match = re.search(r"(\d+)", filepath.name)
    if not number_match:
        raise ValueError(f"No numeric part found in file name {filepath.name}")
    link_title = number_match.group(1)

    # ----- 3. description from second paragraph --------------------
    # Find the second paragraph after the H1 header
    # Paragraphs are separated by blank lines.
    paragraphs: List[str] = []
    current: List[str] = []

    for l in body_lines[body_lines.index(h1_line) + 1 :]:
        if l.strip() == "":
            if current:
                paragraphs.append("".join(current).strip())
                current = []
        else:
            current.append(l)

    # Add the last paragraph if the file ends without a blank line
    if current:
        paragraphs.append("".join(current).strip())

    if len(paragraphs) < 2:
        raise ValueError(f"Less than two paragraphs after H1 in {filepath}")

    second_para = paragraphs[1]

    # Grab the first sentence (naïve approach – good enough for the use‑case)
    m = re.search(r"\.(?=\s|$)", second_para)
    first_sentence = second_para[: m.end()].strip() if m else second_para.strip()

    description = f"From Faith's Checkbook, Daily Devotionals by Charles Spurgeon. {first_sentence}"

    # ----- 4. Build the new YAML block ----------------------------
    new_yaml = build_new_yaml(yaml_dict, new_title, link_title, description)

    # ----- 5. Write it back ---------------------------------------
    new_yaml_text = yaml_to_text(new_yaml)
    new_content = new_yaml_text + body
    write_file(filepath, new_content)

    print(f"✓ Updated front‑matter in {filepath}")

# ------------------------------------------------------------------
#  Entry point – accepts a file or directory
# ------------------------------------------------------------------
def main(argv: List[str]) -> None:
    if not argv:
        print("Usage: python file_fmt_chscbf_addtitle.py /path/to/file_or_dir.md")
        sys.exit(1)

    path = Path(argv[0]).resolve()

    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        sys.exit(1)

    if path.is_file():
        process_file(path)
    else:
        # Walk the directory tree; process every *.md file
        md_files = sorted(path.rglob("*.md"))
        if not md_files:
            print(f"⚠ No *.md files found in {path}")
            sys.exit(1)

        print(f"🔍 Found {len(md_files)} *.md files – processing…")
        for md in md_files:
            process_file(md)

        print(f"✅ Finished processing {len(md_files)} files.")


if __name__ == "__main__":
    main(sys.argv[1:])

