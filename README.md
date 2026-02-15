# Note-Taking Application

A text-based note-taking application with a CLI interface that supports links, tagging, note-to-note references, and automatic Git versioning.

## Features

- **Full CRUD Support**: Create, read, update, and delete notes.
- **Organization**: Add tags and specify the **origin** (source) of your notes.
- **Interconnectivity**: Reference other notes and track **back-references** automatically.
- **Git Integration**: Automatically commit changes (add, update, delete) if your storage directory is a Git repository.
- **Configurable Storage**: Store your notes in any directory on your system.
- **Smart Referencing**: Use note numbers from `list` or `search` results instead of typing full titles.
- **Advanced Search**:
  - Universal search across all fields (title, content, tags, links, origin).
  - Field-specific search (title, content, tag, or link).
  - Multi-criteria advanced search.
- **Clean Storage**: Uses a human-readable JSON format, omitting empty fields for a clean data structure.
- **Robustness**: Automatically handles long note titles by truncating filenames while preserving the full title in the content.

## Installation

Install in editable mode:

```bash
pip install -e .
```

The `note-taker` command will then be available globally or within your virtual environment.

## Configuration

The application stores its configuration in `~/.note_taker_config.json`.

### Initialize the application
```bash
# Initialize the notes directory and set up git repository (prompts for directory)
note-taker init

# Initialize with a specific directory
note-taker init --storage-dir /path/to/your/notes
```

### View or set storage directory
```bash
# View current config
note-taker config

# Change storage directory
note-taker config --storage-dir /path/to/your/notes
```

### Global config file option
You can specify an alternative configuration file for any command:
```bash
# Use a custom config file
note-taker --config-file /path/to/custom/config.json init
note-taker --config-file /path/to/custom/config.json list
```

### Enable Git Integration
To enable automatic commits, initialize a Git repository in your storage directory:
```bash
note-taker init-git
```
From then on, every creation, modification, or deletion will trigger an automatic Git commit.

## Usage

### Basic Operations
```bash
# Create a note with tags and origin
note-taker create "My Note" --content "Note content..." --tags tag1 --origin "Telegram"

# Alternative 'add' command (alias for create)
note-taker add "My Note" --content "Note content..." --tags tag1 --origin "Telegram"

# Read a note (shows only populated fields)
note-taker read "My Note"

# Alternative 'show' command (alias for read)
note-taker show "My Note"

# Update content or metadata
note-taker update "My Note" --content "New content" --origin "Web" --add-tag newtag

# Delete a note
note-taker delete "My Note"

# Alternative 'del' command (alias for delete)
note-taker del "My Note"

# List all notes with indices
note-taker list
```

### Referencing and Links
```bash
# Add/remove references between notes
note-taker add-ref "Note A" "Note B"
note-taker remove-ref "Note A" "Note B"

# Show references or back-references
note-taker show-refs "Note A"
note-taker show-back-refs "Note B"

# Dedicated URL management
note-taker add-url "Note A" "https://example.com"
note-taker show-urls "Note A"
```

### Search
```bash
# Universal search (searches all fields)
note-taker search "query"

# Field-specific search
note-taker field-search content "python"
note-taker field-search tag "important"

# Advanced search
note-taker advanced-search --title "Project" --tag "work"
```

### Number-based Referencing
After running `list` or `search`, you can use the displayed numbers instead of titles:
```bash
note-taker list
# 1. My First Note
# 2. Project Ideas

note-taker read 1
note-taker update 2 --add-tag urgent
```

### Handling Titles That Start With Dashes
If your note title starts with dashes (like `--help`), it may be interpreted as a command option. To avoid this issue:

1. Use numbered references (recommended):
```bash
note-taker list
# 1. --help
note-taker read 1  # Reads the note titled "--help"
```

2. Quote the title when creating/updating:
```bash
note-taker create "--my-option-note" --content "Content here"
```

3. Use the `--` separator to distinguish options from arguments:
```bash
note-taker create -- "--my-option-note" --content "Content here"
```

## Architecture

- `note.py`: Defines the `Note` class and serialization logic.
- `storage.py`: Handles file-based storage with Git integration and filename sanitization.
- `manager.py`: Orchestrates notes, storage, and search operations.
- `config.py`: Manages application settings.
- `cli.py`: Implements the command-line interface and command handlers.
- `main.py`: Entry point for the application.

## Development

This project has been vibe-coded using Qwen and Gemini free tiers, demonstrating the capabilities of AI-assisted development.
