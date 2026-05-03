import argparse
import sys
import datetime
import os
import subprocess
from .note import Note
from .storage import StorageManager
from .config import Config
from .manager import NoteManager


class NoteAppCLI:
    """
    Command Line Interface for the note-taking application.
    """
    
    def __init__(self, storage_dir: str = None, config_path: str = None):
        self.config = Config(config_path=config_path)
        if storage_dir is None:
            storage_dir = self.config.storage_dir
        self.storage_manager = StorageManager(storage_dir)
        self.note_manager = NoteManager(storage_dir)
        
    def run(self):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(description="Text-based note-taking application")
        parser.add_argument('--config-file', help='Specify an alternative configuration file')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Create command
        create_parser = subparsers.add_parser('create', help='Create a new note')
        create_parser.add_argument('title', nargs='?', help='Title of the note')
        create_parser.add_argument('--content', '-c', help='Content of the note')
        create_parser.add_argument('--tags', '-t', nargs='*', help='Tags for the note')
        create_parser.add_argument('--origin', help='Origin/source of the note')

        # Add command (alias for create)
        add_parser = subparsers.add_parser('add', help='Create a new note (alias for create)')
        add_parser.add_argument('title', nargs='?', help='Title of the note')
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

        # Del command (alias for delete)
        del_parser = subparsers.add_parser('del', help='Delete a note (alias for delete)')
        del_parser.add_argument('title', help='Title of the note to delete')
        
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

        # Push command
        push_parser = subparsers.add_parser('push', help='Push changes to the git remote repository')

        # Join command
        join_parser = subparsers.add_parser('join', help='Join two notes into one')
        join_parser.add_argument('title1', help='Title or index of the first note')
        join_parser.add_argument('title2', help='Title or index of the second note')
        join_parser.add_argument('--title', '-t', help='New title for the joined note')
        
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
        elif args.command == 'delete' or args.command == 'del':
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
        elif args.command == 'push':
            self.handle_push(args)
        elif args.command == 'join':
            self.handle_join(args)
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

        title = self.note_manager.create_note(content=full_content)
        if title:
            print(f"Note '{title}' created successfully.")
        else:
            print("Failed to create note.")
            
    def handle_create(self, args):
        """Handle the create command."""
        title = self.note_manager.create_note(
            title=args.title, 
            content=args.content or "", 
            tags=args.tags, 
            origin=args.origin or ""
        )
        
        if title:
            print(f"Note '{title}' created successfully.")
        else:
            if not args.title and not args.content:
                print("Error: Either title or content must be provided.")
            else:
                print(f"Failed to create note '{args.title or 'with generated title'}'. It might already exist.")
            
    def handle_read(self, args):
        """Handle the read command."""
        note = self.note_manager.read_note(args.title)
        if note:
            # Get the position of this note in the list
            all_notes = self.storage_manager.list_notes()
            try:
                position = all_notes.index(note.title) + 1  # +1 to make it 1-indexed
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
            print(f"Note '{args.title}' not found.")
            
    def handle_update(self, args):
        """Handle the update command."""
        success = self.note_manager.update_note(
            title=args.title,
            content=args.content,
            origin=args.origin,
            add_tags=args.add_tag,
            remove_tags=args.remove_tag
        )
        if success:
            print(f"Note '{args.title}' updated successfully.")
        else:
            print(f"Note '{args.title}' not found or failed to update.")
            
    def handle_delete(self, args):
        """Handle the delete command."""
        success = self.note_manager.delete_note(args.title)
        if success:
            print(f"Note '{args.title}' deleted successfully.")
        else:
            print(f"Note '{args.title}' not found or failed to delete.")
            
    def handle_list(self, args):
        """Handle the list command."""
        notes = self.note_manager.list_notes()
        if notes:
            print(f"Found {len(notes)} note(s) in {self.storage_manager.storage_dir}:")
            for i, title in enumerate(notes, 1):
                print(f"{i}. {title}")
        else:
            print(f"No notes found in {self.storage_manager.storage_dir}.")
            
    def handle_join(self, args):
        """Handle the join command."""
        title = self.note_manager.join_notes(args.title1, args.title2, args.title)
        if title:
            print(f"Notes joined successfully into '{title}'.")
        else:
            print("Failed to join notes. Ensure both notes exist and the target title is not already taken.")
            
    def handle_add_ref(self, args):
        """Handle the add-ref command."""
        success = self.note_manager.add_reference(args.title, args.ref_title)
        if success:
            print(f"Reference to '{args.ref_title}' added to note '{args.title}'.")
        else:
            print(f"Failed to update note '{args.title}'.")
            
    def handle_remove_ref(self, args):
        """Handle the remove-ref command."""
        success = self.note_manager.remove_reference(args.title, args.ref_title)
        if success:
            print(f"Reference to '{args.ref_title}' removed from note '{args.title}'.")
        else:
            print(f"Failed to update note '{args.title}'.")
            
    def handle_show_refs(self, args):
        """Handle the show-refs command."""
        refs = self.note_manager.get_note_references(args.title)
        if refs:
            print(f"References in note '{args.title}':")
            for ref in refs:
                print(f"- {ref}")
        else:
            # Check if note exists
            if self.note_manager.read_note(args.title):
                print(f"Note '{args.title}' has no references.")
            else:
                print(f"Note '{args.title}' not found.")
            
    def handle_show_back_refs(self, args):
        """Handle the show-back-refs command."""
        back_refs = self.note_manager.get_back_references(args.title)
        if back_refs:
            print(f"Notes that reference '{args.title}':")
            for ref in back_refs:
                print(f"- {ref}")
        else:
            # Check if note exists
            if self.note_manager.read_note(args.title):
                print(f"No notes reference '{args.title}'.")
            else:
                print(f"Note '{args.title}' not found.")

    def handle_universal_search(self, args):
        """Handle the universal search command (searches all fields)."""
        if not args.query:
            print("Usage: note-taker search \"search_term\"")
            print("Searches across all fields: content, title, tags, links, and dedicated URLs")
            return
            
        results = self.note_manager.universal_search(args.query)
        
        if results:
            # Get the full list of notes to determine positions
            all_notes = self.note_manager.list_notes()
            print(f"Found {len(results)} note(s) matching your search across all fields:")
            for title in results:
                position = all_notes.index(title) + 1  # +1 to make it 1-indexed
                print(f"{position}. {title}")
        else:
            print("No notes found matching your search across all fields.")

    def handle_add_url(self, args):
        """Handle the add-url command."""
        note = self.note_manager.read_note(args.title)
        if not note:
            print(f"Note '{args.title}' not found.")
            return
            
        note.add_url(args.url)
        success = self.storage_manager.save_note(note)
        if success:
            print(f"URL '{args.url}' added to note '{note.title}'.")
        else:
            print(f"Failed to update note '{note.title}'.")
            
    def handle_remove_url(self, args):
        """Handle the remove-url command."""
        note = self.note_manager.read_note(args.title)
        if not note:
            print(f"Note '{args.title}' not found.")
            return
            
        note.remove_url(args.url)
        success = self.storage_manager.save_note(note)
        if success:
            print(f"URL '{args.url}' removed from note '{note.title}'.")
        else:
            print(f"Failed to update note '{note.title}'.")
            
    def handle_show_urls(self, args):
        """Handle the show-urls command."""
        note = self.note_manager.read_note(args.title)
        if not note:
            print(f"Note '{args.title}' not found.")
            return
            
        urls = note.get_urls()
        if urls:
            print(f"URLs in note '{note.title}':")
            for url in urls:
                print(f"- {url}")
        else:
            print(f"Note '{note.title}' has no dedicated URLs.")
            
    def handle_field_search(self, args):
        """Handle the field-specific search command."""
        if args.search_type == 'content':
            results = self.note_manager.search_content(args.query)
        elif args.search_type == 'title':
            results = self.note_manager.search_titles(args.query)
        elif args.search_type == 'tag':
            results = self.note_manager.search_tags(args.tag)
        elif args.search_type == 'link':
            results = self.note_manager.search_links(args.link)
        else:
            print("Invalid search type. Use: content, title, tag, or link")
            return
            
        if results:
            # Get the full list of notes to determine positions
            all_notes = self.note_manager.list_notes()
            print(f"Found {len(results)} note(s) matching your search:")
            for title in results:
                position = all_notes.index(title) + 1  # +1 to make it 1-indexed
                print(f"{position}. {title}")
        else:
            print("No notes found matching your search.")

    def handle_advanced_search(self, args):
        """Handle the advanced-search command."""
        results = self.note_manager.advanced_search(
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

    def handle_push(self, args):
        """Handle the push command."""
        storage_dir = self.storage_manager.storage_dir
        if not self.storage_manager._is_git_repo():
            print(f"No git repository found in {storage_dir}")
            return

        try:
            # Check if there is a remote to push to
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  cwd=storage_dir, 
                                  capture_output=True, 
                                  text=True)
            if result.returncode != 0:
                print(f"No remote repository configured in {storage_dir}")
                print("Use 'git remote add origin <repository-url>' to add a remote")
                return
            
            # Perform the git push
            result = subprocess.run(["git", "push"], 
                                  cwd=storage_dir, 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print("Successfully pushed changes to remote repository")
                if result.stdout.strip():
                    print(result.stdout)
            else:
                print(f"Failed to push changes: {result.stderr}")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to push changes: {e}")

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
