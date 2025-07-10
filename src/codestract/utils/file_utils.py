"""
Utility functions for file filtering operations.
"""

import fnmatch
import os
from typing import List

from .document_processor import is_document_file


def load_ignore_patterns(start_path: str) -> List[str]:
    """Loads patterns from .contextignore found in start_path."""
    ignore_file = os.path.join(start_path, ".contextignore")
    if not os.path.exists(ignore_file):
        return []
    with open(ignore_file, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def is_path_ignored(relative_path: str, ignore_patterns: List[str]) -> bool:
    """Checks if a relative path matches any of the ignore patterns."""
    path_as_posix = relative_path.replace(os.sep, "/")
    # Also check against the path as a directory for patterns like 'build/'
    path_components = path_as_posix.split("/")

    for pattern in ignore_patterns:
        # Match against the full relative path
        if fnmatch.fnmatch(path_as_posix, pattern):
            return True

        # Handle directory-only patterns (e.g., "build/" or "*.egg-info/")
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            # Check if any directory component of the path matches the pattern
            # We check all components except the last if it's a file
            for part in path_components[:-1]:
                if fnmatch.fnmatch(part, dir_pattern):
                    return True
            # Also handle if the directory itself is being checked
            if os.path.isdir(path_as_posix) and fnmatch.fnmatch(path_components[-1], dir_pattern):
                 return True


        # Match against basename for file-specific patterns (e.g., "*.log")
        if not pattern.endswith("/") and fnmatch.fnmatch(path_components[-1], pattern):
            return True
            
    return False


def is_text_file(file_path: str) -> bool:
    """Check if a file is a text file."""
    BINARY_EXTENSIONS = {
        ".gif", ".jpg", ".jpeg", ".png", ".ico", ".pyc", ".exe", ".dll",
        ".so", ".dylib", ".zip", ".tar", ".gz", ".rar", ".7z", ".db",
        ".sqlite", ".bin", ".dat",
    }
    GIT_FILES = {".git/index", ".git/HEAD", ".git/COMMIT_EDITMSG"}

    ext = os.path.splitext(file_path)[1].lower()
    base = os.path.basename(file_path)

    if ext in BINARY_EXTENSIONS or base in GIT_FILES:
        return False

    try:
        with open(file_path, "tr") as f:
            f.read(1024)  # Try reading first 1KB
            return True
    except (UnicodeDecodeError, FileNotFoundError, OSError):
        return False


def is_processable_file(file_path: str) -> bool:
    """Check if a file can be processed (either text or supported document)."""
    if is_document_file(file_path):
        return True
    return is_text_file(file_path)