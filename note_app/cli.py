import argparse
import sys
import datetime
import os
import subprocess
from .note import Note
from .storage import StorageManager
from .config import Config


class NoteAppCLI:
    """
    Command Line Interface for the note-taking application.
    """
    
    def __init__(self, storage_dir: str = None, config_path: str = None):
        self.config = Config(config_path=config_path)
        if storage_dir is None:
            storage_dir = self.config.storage_dir
        self.storage_manager = StorageManager(storage_dir)
        
    def resolve_note_title(self, title_or_number: str) -> str:
        """
        Resolve a note title from either a string title or a number.
        If the input is a number, treat it as an index in the list of notes.
        """
        # Check if the input is a number
        try:
            index = int(title_or_number)
            all_notes = self.storage_manager.list_notes()
            if 0 < index <= len(all_notes):
                return all_notes[index - 1]  # Convert to 0-indexed
            else:
                return None  # Invalid index
        except ValueError:
            # Input is not a number, treat as title
            return title_or_number
        
    def run(self):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(description="Text-based note-taking application")
        parser.add_argument('--config-file', help='Specify an alternative configuration file')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Create command
        create_parser = subparsers.add_parser('create', help='Create a new note')
        create_parser.add_argument('title', help='Title of the note')
        create_parser.add_argument('--content', '-c', help='Content of the note')
        create_parser.add_argument('--tags', '-t', nargs='*', help='Tags for the note')
        create_parser.add_argument('--origin', help='Origin/source of the note')

        # Add command (alias for create)
        add_parser = subparsers.add_parser('add', help='Create a new note (alias for create)')
        add_parser.add_argument('title', help='Title of the note')
        add_parser.add_argument('--content', '-c', help='Content of the note')
        add_parser.add_argument('--tags', '-t', nargs='*', help='Tags for the note')
        add_parser.add_argument('--origin', help='Origin/source of the note')
        
        # Read command
        read_parser = subparsers.add_parser('read', help='Read a note')
        read_parser.add_argument('title', help='Title of the note to read')

        # Show command (alias for read)
        show_parser = subparsers.add_parser('show', help='Read a note (alias for read)')
        show_parser.add_argument('title', help='Title of the note to read')
        
        # Update command
        update_parser = subparsers.add_parser('update', help='Update a note')
        update_parser.add_argument('title', help='Title of the note to update')
        update_parser.add_argument('--content', '-c', help='New content for the note')
        update_parser.add_argument('--add-tag', action='append', help='Add a tag to the note')
        update_parser.add_argument('--remove-tag', action='append', help='Remove a tag from the note')
        update_parser.add_argument('--origin', help='Update the origin/source of the note')
        
        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a note')
        delete_parser.add_argument('title', help='Title of the note to delete')
        
        # List command
        list_parser = subparsers.add_parser('list', help='List all notes')
        
        # Add reference command
        add_ref_parser = subparsers.add_parser('add-ref', help='Add a reference to another note')
        add_ref_parser.add_argument('title', help='Title of the note to update')
        add_ref_parser.add_argument('ref_title', help='Title of the note to reference')
        
        # Remove reference command
        remove_ref_parser = subparsers.add_parser('remove-ref', help='Remove a reference from a note')
        remove_ref_parser.add_argument('title', help='Title of the note to update')
        remove_ref_parser.add_argument('ref_title', help='Title of the note reference to remove')
        
        # Show references command
        show_refs_parser = subparsers.add_parser('show-refs', help='Show all references in a note')
        show_refs_parser.add_argument('title', help='Title of the note to show references for')
        
        # Show back-references command
        show_back_refs_parser = subparsers.add_parser('show-back-refs', help='Show all notes that reference this note')
        show_back_refs_parser.add_argument('title', help='Title of the note to show back-references for')
        
        # Add URL command
        add_url_parser = subparsers.add_parser('add-url', 
            help='Add a URL to a note as a dedicated URL reference',
            description='Add a URL to a note as a dedicated URL reference')
        add_url_parser.add_argument('title', help='Title of the note to update')
        add_url_parser.add_argument('url', help='URL to add to the note')
        
        # Remove URL command
        remove_url_parser = subparsers.add_parser('remove-url', 
            help='Remove a URL from a note\'s dedicated URL references',
            description='Remove a URL from a note\'s dedicated URL references')
        remove_url_parser.add_argument('title', help='Title of the note to update')
        remove_url_parser.add_argument('url', help='URL to remove from the note')
        
        # Show URLs command
        show_urls_parser = subparsers.add_parser('show-urls', 
            help='Show all dedicated URLs in a note',
            description='Show all dedicated URLs in a note')
        show_urls_parser.add_argument('title', help='Title of the note to show URLs for')
        
        # Universal search command (searches all fields)
        universal_search_parser = subparsers.add_parser('search', 
            help='Search for notes across all fields: content, title, tags, links, and dedicated URLs',
            description='Search for notes across all fields: content, title, tags, links, and dedicated URLs')
        universal_search_parser.add_argument('query', nargs='?', help='Search query for all fields')
        
        # Separate search commands for specific fields
        search_parser = subparsers.add_parser('field-search', 
            help='Search for notes in specific fields: content, title, tag, or link',
            description='Search for notes in specific fields: content, title, tag, or link')
        search_subparsers = search_parser.add_subparsers(dest='search_type', help='Search types')
        
        # Search by content
        search_content_parser = search_subparsers.add_parser('content', help='Search notes by content')
        search_content_parser.add_argument('query', help='Search query')
        
        # Search by title
        search_title_parser = search_subparsers.add_parser('title', help='Search notes by title')
        search_title_parser.add_argument('query', help='Search query')
        
        # Search by tag
        search_tag_parser = search_subparsers.add_parser('tag', help='Search notes by tag')
        search_tag_parser.add_argument('tag', help='Tag to search for')
        
        # Search by link
        search_link_parser = search_subparsers.add_parser('link', help='Search notes by link')
        search_link_parser.add_argument('link', help='Link to search for')
        
        # Advanced search
        advanced_search_parser = subparsers.add_parser('advanced-search', 
            help='Advanced search with multiple criteria across different fields',
            description='Advanced search with multiple criteria across different fields: content, title, tag, or link')
        advanced_search_parser.add_argument('--content', help='Search term for content')
        advanced_search_parser.add_argument('--title', help='Search term for titles')
        advanced_search_parser.add_argument('--tag', help='Search term for tags')
        advanced_search_parser.add_argument('--link', help='Search term for links')

        # Config command
        config_parser = subparsers.add_parser('config', help='View or update configuration')
        config_parser.add_argument('--storage-dir', help='Update the storage directory')

        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize the notes directory and set up git repository')
        init_parser.add_argument('--storage-dir', help='Specify the directory for storing notes')

        # Init Git command
        init_git_parser = subparsers.add_parser('init-git', help='Initialize a git repository in the storage directory')
        
        # Get the list of known commands
        known_commands = list(subparsers.choices.keys())
        
        # Check if the first argument (if it exists) is NOT a known command
        # sys.argv[0] is the script name, sys.argv[1] is the first actual argument
        if len(sys.argv) > 1 and sys.argv[1] not in known_commands:
            # Assume the user is trying to create a default note
            self.handle_default_create(sys.argv[1:])
            return # Exit after handling default create

        # If it IS a known command, or no arguments, proceed with normal parsing
        args = parser.parse_args()
        
        if args.command == 'create' or args.command == 'add':
            self.handle_create(args)
        elif args.command == 'read' or args.command == 'show':
            self.handle_read(args)
        elif args.command == 'update':
            self.handle_update(args)
        elif args.command == 'delete':
            self.handle_delete(args)
        elif args.command == 'list':
            self.handle_list(args)
        elif args.command == 'add-ref':
            self.handle_add_ref(args)
        elif args.command == 'remove-ref':
            self.handle_remove_ref(args)
        elif args.command == 'show-refs':
            self.handle_show_refs(args)
        elif args.command == 'show-back-refs':
            self.handle_show_back_refs(args)
        elif args.command == 'add-url':
            self.handle_add_url(args)
        elif args.command == 'remove-url':
            self.handle_remove_url(args)
        elif args.command == 'show-urls':
            self.handle_show_urls(args)
        elif args.command == 'search':
            self.handle_universal_search(args)
        elif args.command == 'field-search':
            self.handle_field_search(args)
        elif args.command == 'advanced-search':
            self.handle_advanced_search(args)
        elif args.command == 'config':
            self.handle_config(args)
        elif args.command == 'init':
            self.handle_init(args)
        elif args.command == 'init-git':
            self.handle_init_git(args)
        else:
            parser.print_help()
            
    def handle_default_create(self, content_parts):
        """
        Handles the creation of a new note when no specific command is given,
        using the unparsed arguments as content.
        """
        full_content = " ".join(content_parts)

        if not full_content.strip():
            print("No content provided to create a note.")
            return

        # Generate a title from the content
        # Take the first 5 words or the entire content if shorter, then add timestamp for uniqueness
        words = full_content.split()
        if len(words) > 5:
            base_title = " ".join(words[:5])
        else:
            base_title = full_content

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # Ensure title doesn't exceed a reasonable length if content is very long
        max_title_len = 100
        if len(base_title) > max_title_len - len(timestamp) - 1: # -1 for underscore
            base_title = base_title[:max_title_len - len(timestamp) - 1 - 3] + "..." # -3 for ellipsis
        
        title = f"{base_title}_{timestamp}"

        # Create a dummy args object for handle_create
        class DefaultCreateArgs:
            def __init__(self, title, content):
                self.title = title
                self.content = content
                self.tags = None
                self.origin = None

        default_args = DefaultCreateArgs(title=title, content=full_content)
        self.handle_create(default_args)
            
    def handle_create(self, args):
        """Handle the create command."""
        # Check if note already exists
        existing_note = self.storage_manager.load_note(args.title)
        if existing_note:
            print(f"Note '{args.title}' already exists. Use 'update' to modify it.")
            return
            
        note = Note(title=args.title, content=args.content or "", origin=args.origin or "")
        
        # Add tags if provided
        if args.tags:
            for tag in args.tags:
                note.add_tag(tag)
                
        success = self.storage_manager.save_note(note)
        if success:
            print(f"Note '{args.title}' created successfully.")
        else:
            print(f"Failed to create note '{args.title}'.")
            
    def handle_read(self, args):
        """Handle the read command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = self.storage_manager.load_note(resolved_title)
        if note:
            # Get the position of this note in the list
            all_notes = self.storage_manager.list_notes()
            try:
                position = all_notes.index(resolved_title) + 1  # +1 to make it 1-indexed
                print(f"\nNote #{position}: {note.title}")
            except ValueError:
                print(f"\nTitle: {note.title}")
                
            if note.origin:
                print(f"Origin: {note.origin}")
                
            print(f"Created: {note.created_at}")
            print(f"Updated: {note.updated_at}")
            
            if note.tags:
                print(f"Tags: {', '.join(note.tags)}")
                
            if note.references:
                print(f"References: {', '.join(note.references)}")
                
            if note.get_urls():
                print(f"Dedicated URLs: {', '.join(note.get_urls())}")
                
            if note.get_links():
                print(f"Content-extracted links: {', '.join(note.get_links())}")
                
            print("\nContent:")
            print("-" * 40)
            print(note.content)
            print("-" * 40)
        else:
            print(f"Note '{resolved_title}' not found.")
            
    def handle_update(self, args):
        """Handle the update command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = self.storage_manager.load_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return

        # Update content if provided
        if args.content is not None:
            note.update_content(args.content)

        # Update origin if provided
        if args.origin is not None:
            note.origin = args.origin
            from datetime import datetime
            note.updated_at = datetime.now()

        # Add tags if provided
        if args.add_tag:
            for tag in args.add_tag:
                note.add_tag(tag)

        # Remove tags if provided
        if args.remove_tag:
            for tag in args.remove_tag:
                note.remove_tag(tag)

        success = self.storage_manager.save_note(note)
        if success:
            print(f"Note '{resolved_title}' updated successfully.")
        else:
            print(f"Failed to update note '{resolved_title}'.")
            
    def handle_delete(self, args):
        """Handle the delete command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        success = self.storage_manager.delete_note(resolved_title)
        if success:
            print(f"Note '{resolved_title}' deleted successfully.")
        else:
            print(f"Note '{resolved_title}' not found or failed to delete.")
            
    def handle_list(self, args):
        """Handle the list command."""
        notes = self.storage_manager.list_notes()
        if notes:
            print(f"Found {len(notes)} note(s) in {self.storage_manager.storage_dir}:")
            for i, title in enumerate(notes, 1):
                print(f"{i}. {title}")
        else:
            print(f"No notes found in {self.storage_manager.storage_dir}.")
            
    def handle_add_ref(self, args):
        """Handle the add-ref command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return

        # Also resolve the reference title if it's a number
        resolved_ref_title = self.resolve_note_title(args.ref_title)
        if resolved_ref_title is None:
            print(f"Invalid note number: {args.ref_title}")
            return

        note = self.storage_manager.load_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return

        note.add_reference(resolved_ref_title)
        success = self.storage_manager.save_note(note)
        if success:
            print(f"Reference to '{resolved_ref_title}' added to note '{resolved_title}'.")
        else:
            print(f"Failed to update note '{resolved_title}'.")
            
    def handle_remove_ref(self, args):
        """Handle the remove-ref command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return

        note = self.storage_manager.load_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return

        # Also resolve the reference title if it's a number
        resolved_ref_title = self.resolve_note_title(args.ref_title)
        if resolved_ref_title is None:
            print(f"Invalid note number: {args.ref_title}")
            return

        note.remove_reference(resolved_ref_title)
        success = self.storage_manager.save_note(note)
        if success:
            print(f"Reference to '{resolved_ref_title}' removed from note '{resolved_title}'.")
        else:
            print(f"Failed to update note '{resolved_title}'.")
            
    def handle_show_refs(self, args):
        """Handle the show-refs command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = self.storage_manager.load_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return
            
        if note.references:
            print(f"References in note '{resolved_title}':")
            for ref in note.references:
                print(f"- {ref}")
        else:
            print(f"Note '{resolved_title}' has no references.")
            
    def handle_show_back_refs(self, args):
        """Handle the show-back-refs command."""
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        # We need to use the manager to get back references
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        back_refs = manager.get_back_references(resolved_title)
        if back_refs:
            print(f"Notes that reference '{resolved_title}':")
            for ref in back_refs:
                print(f"- {ref}")
        else:
            print(f"No notes reference '{resolved_title}'.")

    def handle_universal_search(self, args):
        """Handle the universal search command (searches all fields)."""
        # We need to use the manager to perform searches
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        if not args.query:
            print("Usage: note-taker search \"search_term\"")
            print("Searches across all fields: content, title, tags, links, and dedicated URLs")
            return
            
        results = manager.universal_search(args.query)
        
        if results:
            # Get the full list of notes to determine positions
            all_notes = self.storage_manager.list_notes()
            print(f"Found {len(results)} note(s) matching your search across all fields:")
            for title in results:
                position = all_notes.index(title) + 1  # +1 to make it 1-indexed
                print(f"{position}. {title}")
        else:
            print("No notes found matching your search across all fields.")

    def handle_add_url(self, args):
        """Handle the add-url command."""
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = manager.read_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return
            
        note.add_url(args.url)
        success = manager.storage_manager.save_note(note)
        if success:
            print(f"URL '{args.url}' added to note '{resolved_title}'.")
        else:
            print(f"Failed to update note '{resolved_title}'.")
            
    def handle_remove_url(self, args):
        """Handle the remove-url command."""
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = manager.read_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return
            
        note.remove_url(args.url)
        success = manager.storage_manager.save_note(note)
        if success:
            print(f"URL '{args.url}' removed from note '{resolved_title}'.")
        else:
            print(f"Failed to update note '{resolved_title}'.")
            
    def handle_show_urls(self, args):
        """Handle the show-urls command."""
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        # Resolve the title from either text or number
        resolved_title = self.resolve_note_title(args.title)
        if resolved_title is None:
            print(f"Invalid note number: {args.title}")
            return
            
        note = manager.read_note(resolved_title)
        if not note:
            print(f"Note '{resolved_title}' not found.")
            return
            
        urls = note.get_urls()
        if urls:
            print(f"URLs in note '{resolved_title}':")
            for url in urls:
                print(f"- {url}")
        else:
            print(f"Note '{resolved_title}' has no dedicated URLs.")
            
    def handle_field_search(self, args):
        """Handle the field-specific search command."""
        # We need to use the manager to perform searches
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        if args.search_type == 'content':
            results = manager.search_content(args.query)
        elif args.search_type == 'title':
            results = manager.search_titles(args.query)
        elif args.search_type == 'tag':
            results = manager.search_tags(args.tag)
        elif args.search_type == 'link':
            results = manager.search_links(args.link)
        else:
            print("Invalid search type. Use: content, title, tag, or link")
            return
            
        if results:
            # Get the full list of notes to determine positions
            all_notes = self.storage_manager.list_notes()
            print(f"Found {len(results)} note(s) matching your search:")
            for title in results:
                position = all_notes.index(title) + 1  # +1 to make it 1-indexed
                print(f"{position}. {title}")
        else:
            print("No notes found matching your search.")

    def handle_advanced_search(self, args):
        """Handle the advanced-search command."""
        # We need to use the manager to perform searches
        from .manager import NoteManager
        manager = NoteManager(self.storage_manager.storage_dir)
        
        results = manager.advanced_search(
            content_query=args.content,
            title_query=args.title,
            tag_query=args.tag,
            link_query=args.link
        )
        
        if results:
            print(f"Found {len(results)} note(s) matching your search:")
            for i, title in enumerate(results, 1):
                print(f"{i}. {title}")
        else:
            print("No notes found matching your search.")

    def handle_config(self, args):
        """Handle the config command."""
        if args.storage_dir:
            self.config.storage_dir = os.path.abspath(args.storage_dir)
            print(f"Storage directory updated to: {self.config.storage_dir}")
        else:
            print(f"Current storage directory: {self.config.storage_dir}")
            print(f"Config file: {self.config.config_path}")

    def handle_init(self, args):
        """Handle the init command."""
        from pathlib import Path
        
        # Determine the storage directory to use
        if args.storage_dir:
            storage_dir = os.path.abspath(args.storage_dir)
        else:
            # Show default and ask for input interactively
            default_dir = str(Path.home() / "notes")
            user_input = input(f"Enter the directory for storing notes [default: {default_dir}]: ").strip()
            
            if user_input:
                storage_dir = os.path.abspath(user_input)
            else:
                storage_dir = default_dir
        
        # Create the storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        print(f"Notes directory initialized at: {storage_dir}")
        
        # Update the config with the new storage directory
        self.config.storage_dir = storage_dir
        print(f"Configuration updated with storage directory: {storage_dir}")
        
        # Initialize git repository in the storage directory if it doesn't exist
        if not os.path.exists(os.path.join(storage_dir, ".git")):
            try:
                subprocess.run(["git", "init"], cwd=storage_dir, check=True)
                print(f"Initialized empty Git repository in {storage_dir}")
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Failed to initialize Git repository: {e}")
        else:
            print(f"Git repository already exists in {storage_dir}")
        
        # Create a basic .gitignore file for the notes directory if it doesn't exist
        gitignore_path = os.path.join(storage_dir, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as f:
                f.write("# Ignore temporary files\n*.tmp\n*.temp\n.DS_Store\nThumbs.db\n")
            print(f"Created .gitignore file in {storage_dir}")
        else:
            print(f".gitignore file already exists in {storage_dir}")

    def handle_init_git(self, args):
        """Handle the init-git command."""
        storage_dir = self.storage_manager.storage_dir
        if os.path.exists(os.path.join(storage_dir, ".git")):
            print(f"Git repository already exists in {storage_dir}")
            return

        try:
            subprocess.run(["git", "init"], cwd=storage_dir, check=True)
            print(f"Initialized empty Git repository in {storage_dir}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to initialize Git repository: {e}")
