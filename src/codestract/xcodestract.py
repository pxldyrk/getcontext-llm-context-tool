"""
xcodestract - Non-interactive CLI tool for extracting and combining files into context files.
Automatically processes all files in a directory recursively.
"""

import os
import sys
from typing import Set

from .exporter import export_selected_files
from .utils.file_utils import is_processable_file
from .utils.logging import setup_logging


def find_all_processable_files(directory: str) -> Set[str]:
    """
    Recursively find all processable files in a directory.
    
    Args:
        directory: Path to the directory to search
        
    Returns:
        Set of file paths that can be processed
    """
    processable_files: Set[str] = set()
    
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
            '__pycache__', 'node_modules', '.git', '.venv', 'venv', 'env',
            'build', 'dist', '.pytest_cache', '.mypy_cache', 'target',
            'bin', 'obj', 'out'
        }]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                if is_processable_file(file_path):
                    processable_files.add(file_path)
            except Exception as e:
                print(f"Warning: Could not check file {file_path}: {e}")
                continue
    
    return processable_files


def main() -> None:
    """Entry point for the xcodestract application."""
    setup_logging()
    
    if len(sys.argv) != 2:
        print("Usage: xcodestract [directory_path]")
        print("Recursively processes all files in the directory and generates a context file.")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    
    # Validate directory path
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        sys.exit(1)
    
    # Get absolute path for consistent handling
    directory_path = os.path.abspath(directory_path)
    
    print(f"Scanning directory: {directory_path}")
    
    # Find all processable files
    processable_files = find_all_processable_files(directory_path)
    
    if not processable_files:
        print("No processable files found in the directory.")
        sys.exit(0)
    
    print(f"Found {len(processable_files)} processable file(s):")
    
    # Show file types summary
    file_types = {}
    for file_path in processable_files:
        ext = os.path.splitext(file_path)[1].lower() or 'no extension'
        file_types[ext] = file_types.get(ext, 0) + 1
    
    for ext, count in sorted(file_types.items()):
        print(f"  {ext}: {count} file(s)")
    
    print("\nProcessing files...")
    
    # Change to the target directory for relative path output
    original_cwd = os.getcwd()
    try:
        os.chdir(directory_path)
        
        # Convert absolute paths to relative paths for cleaner output
        relative_files = set()
        for file_path in processable_files:
            try:
                rel_path = os.path.relpath(file_path, directory_path)
                relative_files.add(rel_path)
            except ValueError:
                # If relative path can't be computed, use absolute path
                relative_files.add(file_path)
        
        # Export the files
        result = export_selected_files(relative_files)
        print(result)
        
    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    main() 