# Codestract — A lightweight CLI contextfile tool

A lightweight CLI tool for exporting and combining code files and documents into a single context file, perfect for working with Large Language Models (LLMs).

<div align="center">
  <img src="/assets/image.webp" alt="codestract-banner" width="1280"/>
</div>

## Features

- **Interactive File Selection**: Navigate and select files using an intuitive terminal interface
- **Document Support**: Process Word documents (*.docx), Excel spreadsheets (*.xlsx), and PDF files (*.pdf)
- **Smart File Filtering**: Automatically identifies and filters non-processable files
- **Text Extraction**: Extracts text content from documents including tables and structured data
- **Organized Output**: Generates descriptive context files with clear file separators and metadata
- **Project Statistics**: Shows real-time statistics about selected files
- **Native Experience**: Uses platform-native keyboard shortcuts and navigation patterns

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codestract.git
cd codestract

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m codestract [directory_path]
```

### Global Installation

Install the tool globally to use `codestract` from any directory:

```bash
# Clone and install globally
git clone https://github.com/yourusername/codestract.git
cd codestract
pip install -e .

# Now you can run from anywhere
codestract [directory_path]
```

To uninstall:

```bash
pip uninstall codestract
```

## Usage

### Interactive Mode (codestract)

1. Navigate the file tree using arrow keys
2. Press `Space` to toggle file selection
3. Use `Enter` to expand/collapse directories
4. Press `e` to export selected files
5. Press `q` to quit

### Automatic Mode (xcodestract)

For non-interactive processing of all files in a directory:

```bash
xcodestract [directory_path]
```

This will:
- Recursively scan the directory for all processable files
- Automatically process text files and documents (*.docx, *.xlsx, *.pdf)
- Generate a context file without any user interaction
- Skip common build/cache directories (node_modules, __pycache__, .git, etc.)

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle Selection |
| `Enter` | Expand/Collapse |
| `e` | Export Files |
| `f` | Show/Hide Files |
| `/` | Search |
| `q` | Quit |

## Output

Generated context files are saved in your current directory with:

- Intuitive naming: `{directory_name}_context_{timestamp}.txt`
- File metadata and statistics
- Clear file separators
- Project summary

## Requirements

- Python 3.8+
- Terminal with Unicode support
- For macOS: iTerm2, Kitty, or WezTerm recommended for best experience

## Supported File Types

- **Text Files**: All common text-based file formats (code, configuration, etc.)
- **Documents**: 
  - Word documents (*.docx)
  - Excel spreadsheets (*.xlsx)
  - PDF files (*.pdf)

## License

[MIT License](LICENSE)
