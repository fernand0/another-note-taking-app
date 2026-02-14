import re
from typing import List
from .note import Note
from .storage import StorageManager


class SearchEngine:
    """
    Provides search functionality across notes.
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager
        
    def search_by_content(self, query: str) -> List[str]:
        """
        Search for notes containing the query string in their content.
        
        Args:
            query: The search term to look for
            
        Returns:
            A list of note titles that match the query
        """
        matches = []
        all_notes = self.storage_manager.list_notes()
        
        for title in all_notes:
            note = self.storage_manager.load_note(title)
            if note and query.lower() in note.content.lower():
                matches.append(title)
                
        return matches
        
    def search_by_title(self, query: str) -> List[str]:
        """
        Search for notes with titles containing the query string.
        
        Args:
            query: The search term to look for in titles
            
        Returns:
            A list of note titles that match the query
        """
        matches = []
        all_notes = self.storage_manager.list_notes()
        
        for title in all_notes:
            if query.lower() in title.lower():
                matches.append(title)
                
        return matches
        
    def search_by_tag(self, tag: str) -> List[str]:
        """
        Search for notes containing the specified tag.
        
        Args:
            tag: The tag to search for
            
        Returns:
            A list of note titles that have the tag
        """
        matches = []
        all_notes = self.storage_manager.list_notes()
        
        for title in all_notes:
            note = self.storage_manager.load_note(title)
            if note and tag in [t.lower() for t in note.tags]:
                matches.append(title)
                
        return matches
        
    def search_by_link(self, link: str) -> List[str]:
        """
        Search for notes containing the specified link.
        
        Args:
            link: The link to search for
            
        Returns:
            A list of note titles that contain the link
        """
        matches = []
        all_notes = self.storage_manager.list_notes()
        
        for title in all_notes:
            note = self.storage_manager.load_note(title)
            if note and link in note.get_links():
                matches.append(title)
                
        return matches
        
    def advanced_search(self, content_query: str = None, title_query: str = None, 
                       tag_query: str = None, link_query: str = None) -> List[str]:
        """
        Perform an advanced search with multiple criteria.
        
        Args:
            content_query: Search term for content
            title_query: Search term for titles
            tag_query: Search term for tags
            link_query: Search term for links
            
        Returns:
            A list of note titles that match all specified criteria
        """
        # Start with all notes
        candidates = self.storage_manager.list_notes()
        results = []
        
        for title in candidates:
            note = self.storage_manager.load_note(title)
            if not note:
                continue
                
            # Check content if specified
            if content_query and content_query.lower() not in note.content.lower():
                continue
                
            # Check title if specified
            if title_query and title_query.lower() not in title.lower():
                continue
                
            # Check tags if specified
            if tag_query and tag_query not in [t.lower() for t in note.tags]:
                continue
                
            # Check links if specified
            if link_query and link_query not in note.get_links():
                continue
                
            results.append(title)
            
        return results

    def universal_search(self, query: str) -> List[str]:
        """
        Search across all fields: content, title, tags, links, and dedicated URLs.
        
        Args:
            query: The search term to look for in any field
            
        Returns:
            A list of note titles that match the query in any field
        """
        matches = set()
        all_notes = self.storage_manager.list_notes()
        
        for title in all_notes:
            note = self.storage_manager.load_note(title)
            if not note:
                continue
                
            # Check if query matches in any field
            if (query.lower() in title.lower() or
                query.lower() in note.content.lower() or
                query.lower() in ' '.join([t.lower() for t in note.tags]) or
                query in note.get_links() or
                query in note.get_urls()):  # Added dedicated URLs
                matches.add(title)
                
        return list(matches)