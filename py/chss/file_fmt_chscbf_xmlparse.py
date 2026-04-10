#!/usr/bin/env python3
"""
XML → Markdown Converter

Parses an XML file and extracts the following tags into a Markdown document:

* <div1> with a title attribute → H1 header
* <h3>                        → H3 header (title‑cased)
* <p> with class="IndexBook" or "Date" → H2 header (title‑cased, full month name)
* <p> with class="VerseQuote" → italicized quote, optionally followed by a scripRef
* <div class="Index"> → stop processing further elements

The resulting Markdown file is written to the same directory as the input XML,
with the same basename but a .md extension.
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

MONTH_MAP = {
    "Jan.": "January",
    "Feb.": "February",
    "Mar.": "March",
    "Apr.": "April",
    "May.": "May",
    "Jun.": "June",
    "Jul.": "July",
    "Aug.": "August",
    "Sep.": "September",
    "Oct.": "October",
    "Nov.": "November",
    "Dec.": "December",
}


def title_case_word(word: str) -> str:
    """
    Return the word with first character upper‑cased and the rest lower‑cased.
    Handles apostrophes correctly (e.g., "BIBLE'S" → "Bible's").
    """
    if not word:
        return word
    return word[0].upper() + word[1:].lower()


def title_case_sentence(text: str) -> str:
    """Apply title_case_word to every space‑separated token."""
    return " ".join(title_case_word(tok) for tok in text.split())


def convert_date(text: str) -> str:
    """Replace month abbreviation (e.g. 'Jan.') with full month name."""
    for abbr, full in MONTH_MAP.items():
        text = text.replace(abbr, full)
    return text


def get_full_text(element: ET.Element) -> str:
    """
    Return the concatenated string of all text nodes of the element,
    preserving whitespace but excluding tags.
    """
    return "".join(element.itertext()).strip()


def extract_verse_quote(p: ET.Element) -> str:
    """
    Build the Markdown representation of a VerseQuote paragraph.
    Handles optional <scripRef> child.
    """
    # Grab text before the first child (usually the quote)
    quote_part = p.text or ""

    # Find scripRef if present
    scrip_ref = p.find("scripRef")
    if scrip_ref is not None:
        # The part after the quote may be stored in scripRef.tail
        # but in the examples it's directly the scripRef text.
        ref_text = scrip_ref.text or ""
        # Build the line: italicized quote, em dash, reference
        line = f"*{quote_part}* &mdash; {ref_text}"
    else:
        # No reference, just italicize everything
        full_content = get_full_text(p)
        line = f"*{full_content}*"

    return line.strip()


# --------------------------------------------------------------------------- #
# Main conversion logic
# --------------------------------------------------------------------------- #

def process_xml_to_md(xml_path: Path, md_path: Path) -> None:
    """
    Parse the XML file and write the extracted content to a Markdown file.
    """
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        print(f"Error parsing XML file '{xml_path}': {e}", file=sys.stderr)
        sys.exit(1)

    root = tree.getroot()

    with md_path.open("w", encoding="utf-8") as md_file:
        # Iterate through all elements in document order
        for elem in root.iter():
            # Stop when we encounter <div class="Index">
            if elem.tag == "div" and elem.get("class") == "Index":
                break

            # --- <div1> with title attribute (H1) ---------------------------------
            if elem.tag == "div1" and "title" in elem.attrib:
                header = f"# {elem.attrib['title'].strip()}"
                md_file.write(header + "\n\n")
                continue

            # --- <h3> (H3) ---------------------------------------------------------
            if elem.tag == "h3":
                text = get_full_text(elem)
                header = f"### {title_case_sentence(text)}"
                md_file.write(header + "\n\n")
                continue

            # --- <p> ---------------------------------------------------------------
            if elem.tag == "p":
                p_class = elem.get("class", "")
                text = get_full_text(elem)

                # IndexBook or Date → H2
                if p_class in ("IndexBook", "Date"):
                    # Title case
                    if p_class == "Date":
                        text = convert_date(text)
                    header = f"## {title_case_sentence(text)}"
                    md_file.write(header + "\n\n")
                    continue

                # VerseQuote → italic quote with optional scripRef
                if p_class == "VerseQuote":
                    line = extract_verse_quote(elem)
                    md_file.write(line + "\n\n")
                    continue

                # Other <p> tags are written plainly
                md_file.write(text + "\n\n")
                continue

        # End of processing
    print(f"Markdown file written to: {md_path}")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/file.xml", file=sys.stderr)
        sys.exit(1)

    xml_path = Path(sys.argv[1]).expanduser().resolve()
    if not xml_path.is_file():
        print(f"File not found: {xml_path}", file=sys.stderr)
        sys.exit(1)

    # Create output .md file with same base name
    md_path = xml_path.with_suffix(".md")

    process_xml_to_md(xml_path, md_path)


if __name__ == "__main__":
    main()
