import re
from pathlib import Path

ROOT = Path("./")

# capture the first letter after the colon
pattern = re.compile(r":([A-Za-z])")

for md_path in ROOT.rglob("*.md"):
    text = md_path.read_text(encoding="utf-8")
    # insert a space before the captured letter
    new_text = pattern.sub(r": \1", text)

    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"Fixed: {md_path}")

