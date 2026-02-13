# Note-Taking Application

A text-based note-taking application with CLI interface that supports links, short texts, and references to other notes.

## Features

- Create, read, update, and delete notes
- Add tags to notes
- Reference other notes within a note
- Find notes that reference a particular note (back-references)
- Dedicated URL management:
  - Add URLs to notes
  - Remove URLs from notes
  - Show all URLs in a note
- Extract links from note content
- Number-based note referencing: Use note numbers from the list/search commands instead of full titles
- Search functionality:
  - Universal search (across all fields)
  - Search by content
  - Search by title
  - Search by tag
  - Search by link
  - Advanced search with multiple criteria
- Store all data in text files using JSON format

## Installation

```bash
pip install -e .
```

Or run directly:

```bash
python -m note_app.main
```

## Usage

### Create a note
```bash
note-taker create "My Note Title" --content "This is the content of my note." --tags tag1 tag2
```

### Read a note
```bash
note-taker read "My Note Title"
```

### Update a note
```bash
note-taker update "My Note Title" --content "Updated content here."
note-taker update "My Note Title" --add-tag newtag
note-taker update "My Note Title" --remove-tag oldtag
```

### Delete a note
```bash
note-taker delete "My Note Title"
```

### List all notes
```bash
note-taker list
```

### Add a reference to another note
```bash
note-taker add-ref "Current Note" "Referenced Note"
```

### Remove a reference
```bash
note-taker remove-ref "Current Note" "Referenced Note"
```

### Show references in a note
```bash
note-taker show-refs "My Note Title"
```

### Show back-references (notes that reference this note)
```bash
note-taker show-back-refs "My Note Title"
```

### Manage URLs in notes
```bash
# Add a URL to a note
note-taker add-url "Note Title" "https://example.com"

# Remove a URL from a note
note-taker remove-url "Note Title" "https://example.com"

# Show all URLs in a note
note-taker show-urls "Note Title"
```

### Search for notes
```bash
# Universal search (searches across all fields: content, title, tags, links, and dedicated URLs)
note-taker search "search term"

# Field-specific search
# Search by content
note-taker field-search content "search term"

# Search by title
note-taker field-search title "search term"

# Search by tag
note-taker field-search tag "tag_name"

# Search by link
note-taker field-search link "https://example.com"

# Advanced search with multiple criteria
note-taker advanced-search --content "content" --title "title" --tag "tag" --link "https://example.com"
```

### Number-based note referencing
```bash
# List notes with numbers
note-taker list

# Read a note using its number (shown in the list)
note-taker read 1

# Update a note using its number
note-taker update 1 --content "New content"

# Delete a note using its number
note-taker delete 2

# Add a reference from one note to another using numbers
note-taker add-ref 1 2

# Show references in a note using its number
note-taker show-refs 1

# Show back-references to a note using its number
note-taker show-back-refs 1

# Show URLs in a note using its number
note-taker show-urls 1
```

## Data Storage

All notes are stored in the `notes/` directory as JSON files. Each note is saved as a separate file named after its title (with invalid characters replaced).

## Architecture

- `note.py`: Defines the Note class
- `storage.py`: Handles file-based storage of notes
- `manager.py`: High-level operations combining note and storage functionality
- `cli.py`: Command-line interface
- `main.py`: Entry point for the application