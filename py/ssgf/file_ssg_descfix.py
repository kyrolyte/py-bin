import os
import re
from pathlib import Path

# Change this to your directory containing the markdown files
BASE_DIR = Path(".")

# Regex to match description lines like:
# description: some text
# description: "some text"
# description: 'some text'
DESCRIPTION_RE = re.compile(r'^(description\s*:\s*)(.*)$')

def escape_quotes(value: str) -> str:
    # Strip surrounding quotes (single or double) if present
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        inner = value[1:-1]
    else:
        inner = value

    # Escape both kinds of quotes
    inner = inner.replace('\\', '\\\\')  # preserve existing backslashes
    inner = inner.replace('"', '\\"')
    inner = inner.replace("'", "\\'")

    # Always write back as double-quoted YAML string
    return f'"{inner}"'

def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    lines = text.splitlines(keepends=True)
    if not lines or not lines[0].lstrip().startswith("---"):
        return  # no front matter at top

    # Find end of front matter
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].lstrip().startswith("---"):
            end_idx = i
            break

    if end_idx is None:
        return  # malformed front matter

    # Process only lines in the front matter (between the two --- lines)
    changed = False
    for i in range(1, end_idx):
        m = DESCRIPTION_RE.match(lines[i].strip("\n"))
        if not m:
            continue

        prefix, value = m.groups()
        value = value.strip()

        if not value:
            continue

        new_value = escape_quotes(value)
        new_line = prefix + new_value + "\n"
        if lines[i] != new_line:
            lines[i] = new_line
            changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")

def main():
    for root, _, files in os.walk(BASE_DIR):
        for name in files:
            if name.lower().endswith(".md"):
                process_file(Path(root) / name)

if __name__ == "__main__":
    main()

