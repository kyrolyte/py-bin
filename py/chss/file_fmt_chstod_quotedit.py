import sys
import re
import os

def find_and_fix_quotes(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    pattern = r'(?:\s*\*?\s*)?["\']\s+.*?(?:,\s+)?\s+["\'](?:\s*\*?\s*)?'

    for line_num, line in enumerate(lines, 1):
        matches = list(re.finditer(pattern, line))

        # We process matches in reverse order or by index to avoid index shifting if we were modifying the string in place immediately.
        # Since we are just reading and then replacing in the 'lines' list, forward iteration is fine as we replace the string object in the list.

        for match in matches:
            instance = match.group(0)
            start_idx = match.start()
            end_idx = match.end()

            # Calculate context (25 chars before and after)
            start_context = max(0, start_idx - 25)
            end_context = min(len(line), end_idx + 25)

            context = line[start_context:end_context]

            # Highlight the instance
            display_context = context[:start_idx - start_context] + "[" + instance + "]" + context[end_idx - start_context:]

            print(f"\n--- Line {line_num} ---")
            print(f"Found instance: {repr(instance)}")
            print(f"Context (25 chars before/after):")
            print(display_context)

            while True:
                user_input = input(f"Do you want to replace this instance? (yes/no): ").strip().lower()
                if user_input in ['yes', 'y']:
                    replacement = input("Enter the replacement text: ").strip()

                    # Perform replacement on the specific line in the lines list
                    lines[line_num - 1] = lines[line_num - 1].replace(instance, replacement)
                    print(f"Replaced '{instance}' with '{replacement}'.")
                    break
                elif user_input in ['no', 'n']:
                    print("Skipping this instance.")
                    break
                else:
                    print("Please enter 'yes' or 'no'.")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("\nFile saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_quotes.py <path_to_markdown_file>")
        sys.exit(1)

    filename = sys.argv[1]
    find_and_fix_quotes(filename)

