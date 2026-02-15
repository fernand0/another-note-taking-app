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
    import argparse
    # Parse just the global options first
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--config-file', help='Specify an alternative configuration file')
    # Parse known args to get the config file option
    global_args, remaining_argv = parser.parse_known_args()
    
    # Pass the config file to the CLI
    app = NoteAppCLI(config_path=global_args.config_file)
    # Reconstruct sys.argv to exclude the global args for the main parser
    import sys
    sys.argv = [sys.argv[0]] + remaining_argv
    app.run()

if __name__ == "__main__":
    main()
