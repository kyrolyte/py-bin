import sys
import re
from pathlib import Path

def format_block_quotes(text: str) -> str:
    """
    Detects multi-line quoted blocks (using quotation marks) and converts
    them into Markdown block quotes with trailing spaces for line breaks.
    """

    quote_pattern = re.compile(
        r'(^|\n)"([^"]*?\n[^"]*?)"(\n|$)',
        re.MULTILINE
    )

    def format_quote_block(match):
        quote_content = match.group(2).strip()
        formatted_lines = [
            f'> {line.strip()}   ' for line in quote_content.splitlines() if line.strip()
        ]
        return '\n' + '\n'.join(formatted_lines) + '\n'

    formatted_text = re.sub(quote_pattern, format_quote_block, text)
    return formatted_text.strip() + "\n"


def process_file(file_path: Path):
    """Format block quotes in a single markdown file."""
    if file_path.suffix.lower() != ".md":
        return

    content = file_path.read_text(encoding='utf-8')
    formatted = format_block_quotes(content)
    file_path.write_text(formatted, encoding='utf-8')
    print(f"Formatted markdown saved to '{file_path}'.")


def process_directory(dir_path: Path):
    """Process all Markdown files in the given directory (non-recursive)."""
    for file_path in dir_path.glob("*.md"):
        process_file(file_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.md | directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"Error: '{target}' not found.")
        sys.exit(1)

    if target.is_file():
        process_file(target)
    elif target.is_dir():
        process_directory(target)
        print("All Markdown files in the directory processed.")
    else:
        print(f"Error: '{target}' is neither a file nor a directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()

