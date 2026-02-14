from datetime import datetime
from .note import Note
from .storage import StorageManager
from .search import SearchEngine

class NoteManager:
    """
    Main manager class that combines note functionality with storage and CLI.
    """
    
    def __init__(self, storage_dir: str = "notes"):
        self.storage_manager = StorageManager(storage_dir)
        
    def create_note(self, title: str, content: str = "", tags: list = None, origin: str = "") -> bool:
        """Create a new note."""
        # Check if note already exists
        existing_note = self.storage_manager.load_note(title)
        if existing_note:
            return False  # Note already exists
            
        note = Note(title=title, content=content, tags=tags or [], origin=origin)
        return self.storage_manager.save_note(note)
        
    def read_note(self, title: str) -> Note:
        """Read a note by title."""
        return self.storage_manager.load_note(title)
        
    def update_note(self, title: str, content: str = None, tags: list = None, 
                    add_tags: list = None, remove_tags: list = None, origin: str = None) -> bool:
        """Update an existing note."""
        note = self.storage_manager.load_note(title)
        if not note:
            return False
            
        # Update content if provided
        if content is not None:
            note.update_content(content)
            
        # Update origin if provided
        if origin is not None:
            note.origin = origin
            note.updated_at = datetime.now()

        # Replace tags if provided
        if tags is not None:
            note.tags = tags
            
        # Add tags if provided
        if add_tags:
            for tag in add_tags:
                note.add_tag(tag)
                
        # Remove tags if provided
        if remove_tags:
            for tag in remove_tags:
                note.remove_tag(tag)
                
        return self.storage_manager.save_note(note)
        
    def delete_note(self, title: str) -> bool:
        """Delete a note by title."""
        return self.storage_manager.delete_note(title)
        
    def list_notes(self) -> list:
        """List all note titles."""
        return self.storage_manager.list_notes()
        
    def get_note_by_index(self, index: int) -> tuple:
        """Get a note by its index in the list (1-indexed) and return both the note and its title."""
        all_notes = self.storage_manager.list_notes()
        if 0 < index <= len(all_notes):
            title = all_notes[index - 1]  # Convert to 0-indexed
            note = self.storage_manager.load_note(title)
            return note, title
        return None, None
        
    def add_reference(self, note_title: str, ref_title: str) -> bool:
        """Add a reference from one note to another."""
        note = self.storage_manager.load_note(note_title)
        if not note:
            return False
            
        note.add_reference(ref_title)
        return self.storage_manager.save_note(note)
        
    def remove_reference(self, note_title: str, ref_title: str) -> bool:
        """Remove a reference from one note to another."""
        note = self.storage_manager.load_note(note_title)
        if not note:
            return False
            
        note.remove_reference(ref_title)
        return self.storage_manager.save_note(note)
        
    def get_note_references(self, title: str) -> list:
        """Get all references in a note."""
        note = self.storage_manager.load_note(title)
        if not note:
            return []
            
        return note.references
        
    def get_back_references(self, title: str) -> list:
        """Find all notes that reference the given note."""
        all_notes = self.list_notes()
        back_refs = []

        for note_title in all_notes:
            note = self.storage_manager.load_note(note_title)
            if note and title in note.references:
                back_refs.append(note_title)

        return back_refs

    def search_content(self, query: str) -> list:
        """Search for notes containing the query in their content."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.search_by_content(query)

    def search_titles(self, query: str) -> list:
        """Search for notes with titles containing the query."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.search_by_title(query)

    def search_tags(self, tag: str) -> list:
        """Search for notes containing the specified tag."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.search_by_tag(tag)

    def search_links(self, link: str) -> list:
        """Search for notes containing the specified link."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.search_by_link(link)

    def advanced_search(self, content_query: str = None, title_query: str = None,
                       tag_query: str = None, link_query: str = None) -> list:
        """Perform an advanced search with multiple criteria."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.advanced_search(content_query, title_query, tag_query, link_query)

    def universal_search(self, query: str) -> list:
        """Search across all fields: content, title, tags, and links."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.universal_search(query)
