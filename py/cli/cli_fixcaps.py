import os
import re
import sys

# Regex to capture words while preserving boundaries
WORD_RE = re.compile(r"\b[\w'-]+\b")

def has_multiple_uppercase(word: str) -> bool:
    return sum(1 for c in word if c.isupper()) > 1


def transform_word(word, action):
    if action == "u":
        return word.upper()
    elif action == "l":
        return word.lower()
    elif action == "s":
        return word[:1].upper() + word[1:].lower()
    return word

def bold(text):
    return f"\033[1m{text}\033[0m"

def process_file(filepath):
    print(f"\nProcessing: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(WORD_RE.finditer(content))
    content_list = list(content)
    offset = 0
    changed = False

    for match in matches:
        word = match.group()
        if not has_multiple_uppercase(word):
            continue

        start = match.start() + offset
        end = match.end() + offset

        # Show 10 characters of context before and after
        context_before_start = max(0, match.start() - 10)
        context_after_end = min(len(content), match.end() + 10)
        
        before = content[context_before_start:match.start()]
        after = content[match.end():context_after_end]
        
        if context_before_start == 0:
            before = "BOL" + before
        
        if context_after_end == len(content):
            after = after + "EOL"
        
        print(f"\nFound word in context: '{before}{bold(word)}{after}'")

        action = input("[u] uppercase | [l] lowercase | [s] sentence-case | other=skip: ").strip().lower()

        if action not in {"u", "l", "s"}:
            continue

        new_word = transform_word(word, action)

        if new_word != word:
            content_list[start:end] = list(new_word)
            offset += len(new_word) - len(word)
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("".join(content_list))
        print("File updated.")
    else:
        print("No changes made.")


def iter_markdown_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for name in files:
            if name.lower().endswith(".md"):
                yield os.path.join(root, name)


def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("Enter directory to scan: ").strip()

    if not os.path.isdir(directory):
        print("Invalid directory.")
        return

    for filepath in iter_markdown_files(directory):
        process_file(filepath)

    print("\nDone.")


if __name__ == "__main__":
    main()
