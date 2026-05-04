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
        # Extract tags from title
        processed_title, extracted_tags_title = self._extract_tags_from_content(title)
        self.title = processed_title
        self.tags = tags or []
        for tag in extracted_tags_title:
            if tag not in self.tags:
                self.tags.append(tag)
        
        # Extract tags from content
        processed_content, extracted_tags_content = self._extract_tags_from_content(content)
        self.content = processed_content
        for tag in extracted_tags_content:
            if tag not in self.tags:
                self.tags.append(tag)

        self.references = references or []  # For referencing other notes
        self.urls = urls or []  # For dedicated URLs
        self.origin = origin  # Source or origin of the note
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()

    def _extract_tags_from_content(self, text: str):
        """Extract hashtag tags from the end of the text (multi-line supported)."""
        if not text:
            return text, []
            
        # Strip trailing whitespace but remember it for later if we don't find tags
        original_text = text
        text = text.rstrip()
        if not text:
            return original_text, []
            
        lines = text.split('\n')
        all_extracted_tags = []
        
        # Process lines from bottom to top
        new_lines = []
        extracting = True
        
        for line in reversed(lines):
            if not extracting:
                new_lines.append(line)
                continue
                
            words = line.split()
            if not words:
                # Empty line at the end, keep looking
                new_lines.append(line)
                continue
                
            line_extracted_tags = []
            # Work backwards in the line
            while words and words[-1].startswith('#') and len(words[-1]) > 1:
                tag = words.pop().lstrip('#')
                if tag not in all_extracted_tags:
                    line_extracted_tags.append(tag)
            
            if line_extracted_tags:
                all_extracted_tags.extend(reversed(line_extracted_tags))
                new_line = " ".join(words)
                if new_line:
                    new_lines.append(new_line)
                    # Once we hit a line that has content before the hashtags, we stop extracting
                    extracting = False
                else:
                    # Line was only hashtags, continue to previous line
                    pass
            else:
                # No hashtags at the end of this line, stop extracting
                new_lines.append(line)
                extracting = False
        
        if all_extracted_tags:
            new_text = "\n".join(reversed(new_lines)).rstrip()
            return new_text, all_extracted_tags
            
        return original_text, []
        
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
        # Note: '-' is placed at the end of each character set to be treated as a literal
        url_pattern = r'https?://(?:[\w.-])+(?:[:\d]+)?(?:/(?:[\w/_.~-])*(?:\?(?:[\w&=%.~+-])*)?(?:#(?:[\w.~-])*)?)?'
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