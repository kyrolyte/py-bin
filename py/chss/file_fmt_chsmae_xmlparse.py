#!/usr/bin/env python3
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

MONTHS = {
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
}

def month_in_title(title: str) -> Optional[str]:
    """
    Returns the month name if the title contains one of the known month names,
    otherwise None.
    """
    for m in MONTHS:
        if m in title:
            return m
    return None


def get_text(element: ET.Element) -> str:
    """
    Return concatenated text content of an element, stripping leading/trailing
    whitespace. Works even when the element contains nested tags.
    """
    return " ".join(element.itertext()).strip()


def find_child_with_attrib(
    parent: ET.Element,
    tag: str,
    attrib_key: str,
    attrib_value: str,
) -> Optional[ET.Element]:
    """
    Find the first child of *parent* with tag *tag* and an attribute
    *attrib_key* equal to *attrib_value*.
    """
    for child in parent.iter(tag):
        if child.get(attrib_key) == attrib_value:
            return child
    return None


def find_all_children_with_attrib(
    parent: ET.Element,
    tag: str,
    attrib_key: str,
    attrib_value: str,
) -> list[ET.Element]:
    """
    Return a list of all children of *parent* with tag *tag* and an attribute
    *attrib_key* equal to *attrib_value*.
    """
    return [child for child in parent.iter(tag) if child.get(attrib_key) == attrib_value]


def process_xml_to_markdown(xml_root: ET.Element, md_path: Path) -> None:
    """
    Walks through the XML tree and writes a Markdown file following the spec.
    """
    with md_path.open("w", encoding="utf-8") as md:

        # 1. Find all div1 elements whose title contains a month name
        for div1 in xml_root.iter("div1"):
            div1_title = div1.get("title", "")
            month = month_in_title(div1_title)
            if not month:
                continue  # skip div1s that don't represent a month

            # Write the H1 header
            md.write(f"# {div1_title}\n\n")

            # 2. Inside this div1, find all div2 elements that contain the month
            #    AND a morning/evening prefix
            for div2 in div1.iter("div2"):
                div2_title = div2.get("title", "")
                # Quick sanity check – must contain month and either "Morning" or "Evening"
                if month not in div2_title:
                    continue
                if not re.search(r"\b(Morning|Evening)\b", div2_title, re.IGNORECASE):
                    continue

                # Write the H2 header
                md.write(f"## {div2_title}\n\n")

                # 3. Passage paragraph (<p class="passage">)
                passage_p = find_child_with_attrib(div2, "p", "class", "passage")
                passage_text = ""
                if passage_p is not None:
                    passage_text = get_text(passage_p)

                # 4. Optional script reference (<h3 class="scripPassage">)
                script_ref_text = ""
                h3_scrip = find_child_with_attrib(div2, "h3", "class", "scripPassage")
                if h3_scrip is not None:
                    scrip_ref = h3_scrip.find(".//scripRef")
                    if scrip_ref is not None:
                        script_ref_text = get_text(scrip_ref)

                # Combine passage and script reference
                if passage_text:
                    if script_ref_text:
                        md.write(f"{passage_text} — {script_ref_text}\n\n")
                    else:
                        md.write(f"{passage_text}\n\n")

                # 5. All normal paragraphs (<p class="normal">)
                normal_ps = find_all_children_with_attrib(div2, "p", "class", "normal")
                for p in normal_ps:
                    normal_text = get_text(p)
                    if normal_text:
                        md.write(f"{normal_text}\n\n")

        # If nothing was written (e.g., no matching div1/div2), create a note
        if md.tell() == 0:
            md.write("# No relevant content found\n\n")
    print(f"Markdown written to {md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a custom XML document into a readable Markdown file."
    )
    parser.add_argument(
        "xml_file",
        type=Path,
        help="Path to the input XML file.",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        help="Path to the output Markdown file. If omitted, the input filename is "
             "used with a .md extension.",
    )
    args = parser.parse_args()

    if not args.xml_file.is_file():
        sys.exit(f"Error: {args.xml_file} does not exist or is not a file.")

    # Parse XML
    try:
        tree = ET.parse(args.xml_file)
    except ET.ParseError as e:
        sys.exit(f"Error parsing XML: {e}")

    root = tree.getroot()

    # Determine output path
    out_path = args.out if args.out else args.xml_file.with_suffix(".md")

    # Process
    process_xml_to_markdown(root, out_path)


if __name__ == "__main__":
    main()

