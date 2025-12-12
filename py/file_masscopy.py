import os
import shutil

def mass_copy(from_dir, to_dir):
    from_dir = os.path.abspath(from_dir)
    to_dir = os.path.abspath(to_dir)

    for root, dirs, files in os.walk(from_dir):
        rel_path = os.path.relpath(root, from_dir)
        # Skip the root itself; only process subdirectories
        if rel_path == ".":
            continue

        src_subdir = root
        dst_subdir = os.path.join(to_dir, rel_path)

        # Only copy if destination subdir exists
        if os.path.isdir(dst_subdir):
            for fname in files:
                src_file = os.path.join(src_subdir, fname)
                dst_file = os.path.join(dst_subdir, fname)
                # Create dest dir just in case (should already exist)
                os.makedirs(dst_subdir, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"Copied {src_file} -> {dst_file}")

if __name__ == "__main__":
    from_dir = input("From directory: ").strip()
    to_dir = input("To directory: ").strip()
    mass_copy(from_dir, to_dir)

