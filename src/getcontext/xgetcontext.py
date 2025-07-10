"""
xgetcontext - Non-interactive CLI tool for extracting and combining files into context files.
Automatically processes all files in a directory recursively.
"""

import os
import sys
from typing import Set

from .exporter import export_selected_files
from .utils.file_utils import is_path_ignored, is_processable_file, load_ignore_patterns
from .utils.logging import setup_logging


def find_all_processable_files(directory: str) -> Set[str]:
    """
    Recursively find all processable files in a directory, respecting .contextignore.
    """
    processable_files: Set[str] = set()
    ignore_patterns = load_ignore_patterns(directory)

    # Common non-source directories to always skip
    default_skip_dirs = {
        "__pycache__", "node_modules", ".git", ".venv", "venv", "env",
        "build", "dist", ".pytest_cache", ".mypy_cache", "target",
        "bin", "obj", "out",
    }

    for root, dirs, files in os.walk(directory, topdown=True):
        # Filter directories in-place to prevent os.walk from descending into them
        original_dirs = list(dirs)
        dirs[:] = []
        for d in original_dirs:
            dir_path = os.path.join(root, d)
            rel_dir_path = os.path.relpath(dir_path, directory)
            if not d.startswith(".") and d not in default_skip_dirs and not is_path_ignored(rel_dir_path, ignore_patterns):
                dirs.append(d)

        for file in files:
            if file.startswith("."):
                continue

            file_path = os.path.join(root, file)
            rel_file_path = os.path.relpath(file_path, directory)

            if is_path_ignored(rel_file_path, ignore_patterns):
                continue

            try:
                if is_processable_file(file_path):
                    processable_files.add(file_path)
            except Exception as e:
                print(f"Warning: Could not check file {file_path}: {e}")
                continue

    return processable_files


def main() -> None:
    """Entry point for the xgetcontext application."""
    setup_logging()

    if len(sys.argv) != 2:
        print("Usage: xgetcontext [directory_path]")
        print("Recursively processes all files in the directory and generates a context file.")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)

    directory_path = os.path.abspath(directory_path)

    print(f"Scanning directory: {directory_path}")
    if os.path.exists(os.path.join(directory_path, ".contextignore")):
        print("Found .contextignore, applying rules...")

    processable_files = find_all_processable_files(directory_path)

    if not processable_files:
        print("No processable files found in the directory.")
        sys.exit(0)

    print(f"Found {len(processable_files)} processable file(s):")

    file_types = {}
    for file_path in processable_files:
        ext = os.path.splitext(file_path)[1].lower() or "no extension"
        file_types[ext] = file_types.get(ext, 0) + 1

    for ext, count in sorted(file_types.items()):
        print(f"  {ext}: {count} file(s)")

    print("\nProcessing files...")

    original_cwd = os.getcwd()
    try:
        os.chdir(directory_path)

        relative_files = {os.path.relpath(p, directory_path) for p in processable_files}

        result = export_selected_files(relative_files)
        print(result)

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main()