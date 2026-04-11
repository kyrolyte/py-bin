import os
import re

def clean_blockquotes_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    inside_blockquote = False
    blockquote_buffer = []

    def process_blockquote(blockquote):
        # Remove '>' prefix and leading spaces to inspect content
        content_lines = [line.lstrip("> ").rstrip("\n") for line in blockquote]
        if not content_lines:
            return blockquote

        # Strip optional quotes from first and last lines
        if content_lines[0].startswith(('"', "'")):
            content_lines[0] = content_lines[0][1:]
        if content_lines[-1].rstrip().endswith(('"', "'")):
            # remove trailing quote before trimming whitespace at end
            content_lines[-1] = re.sub(r'(["\'])\s*$', '', content_lines[-1])

        # Rebuild blockquote with proper formatting
        return ["> " + line.rstrip() + "    \n" for line in content_lines]

    for line in lines:
        if line.strip().startswith(">"):
            inside_blockquote = True
            blockquote_buffer.append(line)
        else:
            if inside_blockquote:
                # Process the blockquote before appending non-quote line
                cleaned_lines.extend(process_blockquote(blockquote_buffer))
                blockquote_buffer = []
                inside_blockquote = False
            cleaned_lines.append(line)

    # Handle end of file blockquote
    if blockquote_buffer:
        cleaned_lines.extend(process_blockquote(blockquote_buffer))

    # Write back to the file only if changes occurred
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)


def clean_all_markdown_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                print(f"Processing {md_path}...")
                clean_blockquotes_in_file(md_path)


if __name__ == "__main__":
    dir_path = input("Enter the directory path containing .md files: ").strip()
    clean_all_markdown_files(dir_path)
    print("Done cleaning blockquotes!")

