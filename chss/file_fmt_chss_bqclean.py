import sys
import re
from pathlib import Path

def format_block_quotes(text: str) -> str:
    """
    Detects multi-line quoted blocks (using quotation marks) and converts
    them into Markdown block quotes with trailing spaces for line breaks.
    """

    # Pattern matches quotes starting and ending with a double quote on lines by themselves
    quote_pattern = re.compile(
        r'(^|\n)"([^"]*?\n[^"]*?)"(\n|$)',  # Match multiline quoted block
        re.MULTILINE
    )

    def format_quote_block(match):
        # Extract the quoted content
        quote_content = match.group(2).strip()
        # Preserve each line, prefix with '> ' and two spaces at end
        formatted_lines = [
            f'> {line.strip()}   ' for line in quote_content.splitlines() if line.strip()
        ]
        return '\n' + '\n'.join(formatted_lines) + '\n'

    # Replace all detected quote blocks
    formatted_text = re.sub(quote_pattern, format_quote_block, text)
    return formatted_text.strip() + "\n"


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.md>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # Read file
    content = file_path.read_text(encoding='utf-8')

    # Process markdown content
    formatted = format_block_quotes(content)

    # Save back to same file
    file_path.write_text(formatted, encoding='utf-8')
    print(f"Formatted markdown saved to '{file_path}'.")


if __name__ == "__main__":
    main()

