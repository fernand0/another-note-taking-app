"""
Note-taking application with CLI interface.

This application allows users to create, read, update, and delete notes.
Notes can contain links, short texts, and references to other notes.
All data is stored in text files using JSON format.
"""

from .note import Note
from .storage import StorageManager
from .manager import NoteManager
from .cli import NoteAppCLI


def main():
    """Main entry point for the application."""
    app = NoteAppCLI()
    app.run()


if __name__ == "__main__":
    main()