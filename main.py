#!/usr/bin/env python3
"""
Entry point for the note-taking application.
"""

import sys
import os

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cli import NoteAppCLI
except ImportError:
    from .cli import NoteAppCLI

def main():
    app = NoteAppCLI()
    app.run()

if __name__ == "__main__":
    main()
