import re
from pathlib import Path

def is_sentence_terminator(ch):
    return ch in '.!?'

def find_break_after_mid(line, mid, max_search=None):
    """
    Find the earliest sentence break after mid that is not inside a quotation.
    Returns the index to break at (the position after the break character), or None.
    """
    if max_search is None:
        max_search = len(line)

    i = mid
    quotes = {'"': False, "'": False}

    while i < max_search:
        ch = line[i]

        # Update quote state
        if ch == '"' and not (i > 0 and line[i - 1] == '\\'):
            quotes['"'] = not quotes['"']
        elif ch == "'" and not (i > 0 and line[i - 1] == '\\'):
            quotes["'"] = not quotes["'"]

        # Check for sentence terminator
        if is_sentence_terminator(ch):
            next_is_space = (i + 1 < len(line)) and line[i + 1].isspace()
            end_of_line = i + 1 == len(line)
            in_any_quote = quotes['"'] or quotes["'"]
            if (next_is_space or end_of_line) and not in_any_quote:
                return i + 1
        i += 1
    return None

def split_long_paragraphs(lines, max_len=1200):
    """Split any long paragraph into two at a sentence boundary near the middle."""
    result = []
    for line in lines:
        if len(line) <= max_len:
            result.append(line)
            continue

        mid = len(line) // 2
        break_pos = find_break_after_mid(line, mid)

        # Fallback: look for sentence break before the midpoint
        if break_pos is None:
            for j in range(mid, 0, -1):
                if line[j] in '.!?':
                    if j + 1 == len(line) or line[j + 1].isspace():
                        break_pos = j + 1
                        break

        # Final fallback: exact middle
        if break_pos is None:
            break_pos = mid

        first = line[:break_pos].rstrip()
        second = line[break_pos:].lstrip()
        if first:
            result.append(first + "\n\n")
        if second:
            result.append(second + "")
    return result

def process_file(input_path, max_len=1200):
    input_path = Path(input_path)
    
    # Read the original file
    text = input_path.read_text(encoding='utf-8')

    # Create a backup file (no changes)
    # bak_path = input_path.with_suffix(input_path.suffix + ".bak")
    # if not bak_path.exists():
    #     bak_path.write_text(text, encoding='utf-8')

    lines = text.splitlines(keepends=True)
    new_lines = split_long_paragraphs(lines, max_len=max_len)

    # Write processed content to the same file
    output_path = input_path.with_suffix('.md') if input_path.suffix != '.md' else input_path
    output_path.write_text("".join(new_lines), encoding='utf-8')

    # If the input file didn't have '.md' extension, rename the processed file to add it
    if input_path.suffix != '.md':
        input_path.rename(output_path)

    print(f"Processed file written to: {output_path}")
    # print(f"Backup created at: {bak_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python split_paragraphs.py input.md [max_len]")
        sys.exit(1)

    input_file = sys.argv[1]
    max_len = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    process_file(input_file, max_len)

