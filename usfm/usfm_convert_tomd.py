# This is a script that helps in converting a USFM document into a markdown document
# The use case for this particular script is limited as it applies to tags for a specific file
# The overall structure however serves as a useful boilerplate for creating a unique script for different USFM files

import os
import re
import sys

def sanitize_folder_name(name: str) -> str:
    name = name.strip()
    name = name.replace(" ", "-")
    return name

def extract_marker_and_text(line: str):
    line = line.rstrip("\n")
    if not line.startswith("\\"):
        return None, line
    parts = line.split(maxsplit=1)
    marker = parts[0]  # e.g. \c, \s1, \v, \r, etc.
    text = parts[1] if len(parts) > 1 else ""
    return marker, text

def process_footnotes(raw_text: str, footnote_counter: list):
    """
    Find USFM footnotes like \f ... \f* and convert them to markdown footnotes.
    Uses [^n] markers in the text and collects definitions like:
    [^n]: ref text

    - \fr content (reference) is optional and, if present, is placed before \ft.
    - \ft content (footnote text) is required to emit a definition.
    """
    footnotes_md = []
    pattern = r"\\f(.*?)\\f\*"

    def repl(match):
        inner = match.group(1)

        fr_match = re.search(r"\\fr\s+([^\\]+)", inner)
        fr_text = fr_match.group(1).strip() if fr_match else ""

        ft_match = re.search(r"\\ft\s+([^\\]+)", inner)
        if not ft_match:
            return ""

        ft_text = ft_match.group(1).strip()

        if fr_text:
            footnote_text = f"{fr_text} {ft_text}"
        else:
            footnote_text = ft_text

        footnote_number = footnote_counter[0]
        footnote_counter[0] += 1

        marker = f"[^{footnote_number}]"

        definition = f"[^{footnote_number}]: {footnote_text}"
        footnotes_md.append(definition)

        return marker

    new_text = re.sub(pattern, repl, raw_text)
    return new_text, footnotes_md

def format_verse_line(text: str, footnote_counter: list):
    """
    Example input: "5 This is some content \f ... \f* more"
    Output: "<sup>5</sup> This is some content[^1] more"
    plus footnote definitions as needed.
    """
    text = text.strip()
    if not text:
        return "", []

    parts = text.split(maxsplit=1)
    verse_num = parts[0]
    verse_rest = parts[1] if len(parts) > 1 else ""

    verse_rest, footnotes_md = process_footnotes(verse_rest, footnote_counter)

    md_line = f"<sup>{verse_num}</sup> {verse_rest}".strip()
    return md_line, footnotes_md

def usfm_to_markdown(usfm_path: str, global_footnote_counter: list):
    with open(usfm_path, encoding="utf-8") as f:
        lines = f.readlines()

    header_name = None
    for line in lines:
        marker, text = extract_marker_and_text(line)
        if marker == "\\h":
            header_name = text.strip()
            break

    if header_name is None:
        raise ValueError("No \\h tag found in USFM file.")

    folder_name = sanitize_folder_name(header_name)
    os.makedirs(folder_name, exist_ok=True)

    current_chapter = None
    chapter_file = None
    footnote_counter = global_footnote_counter

    pending_footnotes = []  # collected for the current chapter

    def open_new_chapter(chapter_num: str):
        nonlocal chapter_file, current_chapter, pending_footnotes
        if chapter_file:
            # write any pending footnotes before closing
            if pending_footnotes:
                chapter_file.write("\n\n")
                for fn in pending_footnotes:
                    chapter_file.write(fn + "\n")
            chapter_file.close()

        current_chapter = chapter_num
        pending_footnotes = []
        chapter_filename = f"chapter-{chapter_num}.md"
        chapter_path = os.path.join(folder_name, chapter_filename)
        chapter_file = open(chapter_path, "w", encoding="utf-8")
        chapter_file.write(f"# Chapter {chapter_num}")

    for line in lines:
        marker, text = extract_marker_and_text(line)
        if marker is None:
            if chapter_file and text.strip():
                # Append to previous verse/line
                chapter_file.write(" " + text.strip())
            continue

        if marker == "\\c":
            chap_num = text.strip()
            if chap_num:
                open_new_chapter(chap_num)
            continue

        if marker.startswith("\\s"):
            if chapter_file:
                content = text.strip()
                if content:
                    chapter_file.write(f"\n\n## {content}")
            continue

        if marker.startswith("\\qa"):
            if chapter_file:
                content = text.strip()
                if content:
                    chapter_file.write(f"\n\n### {content}")
            continue

        if marker == "\\r":
            if chapter_file:
                content = text.strip()
                if content:
                    chapter_file.write(f"\n\n**{content}**")
            continue

        if marker == "\\d":
            if chapter_file:
                content = text.strip()
                content_no_fn, fns = process_footnotes(content, footnote_counter)
                if content:
                    chapter_file.write(f"\n\n{content_no_fn}")
                if fns:
                    pending_footnotes.extend(fns)
            continue

        if marker == "\\v":
          if chapter_file:
              text = text.strip()
              if not text:
                  continue
    
              parts = text.split(maxsplit=1)
              verse_num = parts[0]
              verse_rest = parts[1] if len(parts) > 1 else ""
    
              # Process footnotes in the verse body
              verse_rest_no_fn, fns = process_footnotes(verse_rest, footnote_counter)
              verse_md = f"<sup>{verse_num}</sup> {verse_rest_no_fn}".strip()
    
              if verse_md:
                  chapter_file.write("\n\n" + verse_md)
              if fns:
                  pending_footnotes.extend(fns)
          continue

        if marker in ("\\b", "\\pmo", "\\pc", "\\m") or marker.startswith("\\q") or marker.startswith("\\li"):
            if chapter_file and text.strip():
                # First, process footnotes in this fragment
                fragment = text.strip()
                fragment_no_fn, fns = process_footnotes(fragment, footnote_counter)
        
                # Append the cleaned fragment to the current line
                if fragment_no_fn:
                    chapter_file.write(" " + fragment_no_fn)
        
                # Collect any new footnote definitions
                if fns:
                    pending_footnotes.extend(fns)
            continue


    if chapter_file:
        if pending_footnotes:
            chapter_file.write("\n\n")
            for fn in pending_footnotes:
                chapter_file.write(fn + "\n")
        chapter_file.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python usfm_to_md.py <input_directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)

    global_footnote_counter = [1]

    sfm_files = [f for f in os.listdir(directory_path) if f.endswith('.usfm')]
    
    if not sfm_files:
        print(f"No .sfm files found in '{directory_path}'.")
        sys.exit(0)

    print(f"Processing {len(sfm_files)} .sfm files...")

    for filename in sorted(sfm_files):  # sorted for consistent order
        filepath = os.path.join(directory_path, filename)
        try:
            print(f"  Processing {filename}...")
            usfm_to_markdown(filepath, global_footnote_counter)
        except ValueError as e:
            print(f"    Error in {filename}: {e}")
        except Exception as e:
            print(f"    Unexpected error in {filename}: {e}")

    print("Done.")

if __name__ == "__main__":
    main()
