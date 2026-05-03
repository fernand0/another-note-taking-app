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
        
    def create_note(self, title: str = None, content: str = "", tags: list = None, origin: str = "") -> any:
        """Create a new note. If title is not provided, it is generated from content."""
        # Create Note object first to extract tags from content and title (if provided)
        note = Note(title=title or "", content=content, tags=tags or [], origin=origin)

        if not title:
            if not note.content:
                # If no title and no content after stripping tags, use first tag as title
                if note.tags:
                    base_title = note.tags[0]
                else:
                    return False
            else:
                # Generate a title from the cleaned content
                words = note.content.split()
                if len(words) > 5:
                    base_title = " ".join(words[:5])
                else:
                    base_title = note.content

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Ensure title doesn't exceed a reasonable length
            max_title_len = 100
            if len(base_title) > max_title_len - len(timestamp) - 1: # -1 for underscore
                base_title = base_title[:max_title_len - len(timestamp) - 1 - 3] + "..." # -3 for ellipsis
            
            note.title = f"{base_title}_{timestamp}"

        # Check if note already exists
        existing_note = self.storage_manager.load_note(note.title)
        if existing_note:
            return False  # Note already exists
            
        if self.storage_manager.save_note(note):
            return note.title
        return False
        
    def resolve_title(self, title_or_number: str) -> str:
        """
        Resolve a note title from either a string title or a number.
        If the input is a number, treat it as an index in the list of notes.
        """
        if title_or_number is None:
            return None
            
        try:
            index = int(title_or_number)
            all_notes = self.storage_manager.list_notes()
            if 0 < index <= len(all_notes):
                return all_notes[index - 1]  # Convert to 0-indexed
            else:
                return None  # Invalid index
        except (ValueError, TypeError):
            # Input is not a number, treat as title
            return str(title_or_number)

    def read_note(self, title: str) -> Note:
        """Read a note by title or index."""
        resolved_title = self.resolve_title(title)
        if not resolved_title:
            return None
        return self.storage_manager.load_note(resolved_title)
        
    def update_note(self, title: str, content: str = None, tags: list = None, 
                    add_tags: list = None, remove_tags: list = None, origin: str = None) -> bool:
        """Update an existing note."""
        resolved_title = self.resolve_title(title)
        if not resolved_title:
            return False
            
        note = self.storage_manager.load_note(resolved_title)
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
        """Delete a note by title or index."""
        resolved_title = self.resolve_title(title)
        if not resolved_title:
            return False
        return self.storage_manager.delete_note(resolved_title)
        
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
        resolved_title = self.resolve_title(note_title)
        resolved_ref_title = self.resolve_title(ref_title)
        
        if not resolved_title or not resolved_ref_title:
            return False
            
        note = self.storage_manager.load_note(resolved_title)
        if not note:
            return False
            
        note.add_reference(resolved_ref_title)
        return self.storage_manager.save_note(note)
        
    def remove_reference(self, note_title: str, ref_title: str) -> bool:
        """Remove a reference from one note to another."""
        resolved_title = self.resolve_title(note_title)
        resolved_ref_title = self.resolve_title(ref_title)
        
        if not resolved_title or not resolved_ref_title:
            return False
            
        note = self.storage_manager.load_note(resolved_title)
        if not note:
            return False
            
        note.remove_reference(resolved_ref_title)
        return self.storage_manager.save_note(note)
        
    def get_note_references(self, title: str) -> list:
        """Get all references in a note."""
        resolved_title = self.resolve_title(title)
        if not resolved_title:
            return []
            
        note = self.storage_manager.load_note(resolved_title)
        if not note:
            return []
            
        return note.references
        
    def get_back_references(self, title: str) -> list:
        """Find all notes that reference the given note."""
        resolved_title = self.resolve_title(title)
        if not resolved_title:
            return []
            
        all_notes = self.list_notes()
        back_refs = []

        for note_title in all_notes:
            note = self.storage_manager.load_note(note_title)
            if note and resolved_title in note.references:
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

    def join_notes(self, title1: str, title2: str, new_title: str = None) -> any:
        """
        Join two notes into one.
        Combines content, tags, references and URLs.
        If a note's content is empty and its title is a URL, the URL is moved to the content.
        """
        note1 = self.read_note(title1)
        note2 = self.read_note(title2)
        
        if not note1 or not note2:
            return False
            
        # Keep track of original titles for deletion
        orig_title1 = note1.title
        orig_title2 = note2.title
            
        # Combine content
        c1 = note1.content.strip()
        c2 = note2.content.strip()
        
        # If title is a URL and content is empty, use title as content
        if not c1 and note1.title.startswith('http'):
            c1 = note1.title
        if not c2 and note2.title.startswith('http'):
            c2 = note2.title
            
        combined_content = f"{c1}\n\n{c2}".strip()
        
        # Combine tags (using set for uniqueness)
        combined_tags = list(set(note1.tags + note2.tags))
        
        # Combine dedicated URLs
        combined_urls = list(set(note1.urls + note2.urls))
        
        # Combine references
        combined_refs = list(set(note1.references + note2.references))
        
        # Target title
        target_title = new_title or orig_title1
        
        # If it's a new title, we need to make sure it doesn't collide unless it's one of the originals
        if new_title and new_title not in [orig_title1, orig_title2]:
            if self.storage_manager.load_note(new_title):
                return False # Target already exists
        
        # Prepare the joined note
        joined_note = Note(
            title=target_title,
            content=combined_content,
            tags=combined_tags,
            urls=combined_urls,
            references=combined_refs,
            origin=note1.origin or note2.origin
        )
        
        # Save the joined note
        if self.storage_manager.save_note(joined_note):
            # If target_title is same as orig_title1, we already "overwrote" it in storage 
            # (though in git it's an update). 
            # If it's different, or it was title2, we might need to delete.
            
            # Delete title2 always (it's being merged)
            if target_title != orig_title2:
                self.storage_manager.delete_note(orig_title2)
            
            # Delete title1 if it's not the target_title
            if target_title != orig_title1:
                self.storage_manager.delete_note(orig_title1)
                
            return target_title
            
        return False

    def universal_search(self, query: str) -> list:
        """Search across all fields: content, title, tags, and links."""
        search_engine = SearchEngine(self.storage_manager)
        return search_engine.universal_search(query)
