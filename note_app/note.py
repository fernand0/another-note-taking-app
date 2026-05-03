import re
from datetime import datetime
from typing import List, Optional


class Note:
    """
    Represents a single note with content, metadata, and references to other notes.
    """
    
    def __init__(self, title: str, content: str = "", tags: List[str] = None, 
                 references: List[str] = None, urls: List[str] = None, 
                 origin: str = "", created_at: datetime = None):
        self.title = title
        self.tags = tags or []
        
        # Extract tags from content if they are at the end
        processed_content, extracted_tags = self._extract_tags_from_content(content)
        self.content = processed_content
        for tag in extracted_tags:
            if tag not in self.tags:
                self.tags.append(tag)

        self.references = references or []  # For referencing other notes
        self.urls = urls or []  # For dedicated URLs
        self.origin = origin  # Source or origin of the note
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()

    def _extract_tags_from_content(self, content: str):
        """Extract hashtag tags from the end of the content."""
        if not content:
            return content, []
            
        lines = content.split('\n')
        if not lines:
            return content, []
            
        last_line = lines[-1]
        words = last_line.split()
        
        extracted_tags = []
        # Work backwards from the end
        while words and words[-1].startswith('#') and len(words[-1]) > 1:
            tag = words.pop().lstrip('#')
            if tag not in extracted_tags:
                extracted_tags.append(tag)
        
        if extracted_tags:
            # Reconstruct the last line without the extracted tags
            new_last_line = " ".join(words)
            lines[-1] = new_last_line
            # Join lines back, rstrip to remove any trailing whitespace/newlines left from removal
            new_content = "\n".join(lines).rstrip()
            return new_content, list(reversed(extracted_tags))
            
        return content, []
        
    def add_tag(self, tag: str):
        """Add a tag to the note."""
        if tag not in self.tags:
            self.tags.append(tag)
            
    def remove_tag(self, tag: str):
        """Remove a tag from the note."""
        if tag in self.tags:
            self.tags.remove(tag)
            
    def add_reference(self, note_title: str):
        """Add a reference to another note."""
        if note_title not in self.references:
            self.references.append(note_title)
            
    def remove_reference(self, note_title: str):
        """Remove a reference to another note."""
        if note_title in self.references:
            self.references.remove(note_title)
            
    def update_content(self, new_content: str):
        """Update the content of the note."""
        processed_content, extracted_tags = self._extract_tags_from_content(new_content)
        self.content = processed_content
        for tag in extracted_tags:
            if tag not in self.tags:
                self.tags.append(tag)
        self.updated_at = datetime.now()
        
    def get_links(self) -> List[str]:
        """Extract all URLs from the note content."""
        # Regular expression to find URLs in the content
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        return re.findall(url_pattern, self.content)
        
    def add_url(self, url: str):
        """Add a URL to the note's dedicated URLs list."""
        if url not in self.urls:
            self.urls.append(url)
            self.updated_at = datetime.now()
            
    def remove_url(self, url: str):
        """Remove a URL from the note's dedicated URLs list."""
        if url in self.urls:
            self.urls.remove(url)
            self.updated_at = datetime.now()
            
    def get_urls(self) -> List[str]:
        """Get URLs that were specifically added using add_url method."""
        return self.urls.copy()  # Return a copy to prevent external modification
        
    def to_dict(self) -> dict:
        """Convert the note to a dictionary for serialization."""
        data = {
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if self.tags:
            data['tags'] = self.tags
        if self.references:
            data['references'] = self.references
        if self.urls:
            data['urls'] = self.urls
        if self.origin:
            data['origin'] = self.origin
        return data
        
    @classmethod
    def from_dict(cls, data: dict):
        """Create a Note instance from a dictionary."""
        note = cls(
            title=data['title'],
            content=data.get('content', ''),
            tags=data.get('tags', []),
            references=data.get('references', []),
            urls=data.get('urls', []),
            origin=data.get('origin', '')
        )
        note.created_at = datetime.fromisoformat(data['created_at'])
        note.updated_at = datetime.fromisoformat(data['updated_at'])
        return note
        
    def __str__(self):
        """String representation of the note."""
        return f"Note(title='{self.title}', tags={self.tags}, references={self.references})"
        
    def __repr__(self):
        """Detailed string representation of the note."""
        return f"Note(title='{self.title}', content='{self.content[:50]}...', tags={self.tags})"