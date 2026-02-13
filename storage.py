import json
import os
from typing import Dict, List, Optional
try:
    from .note import Note
except ImportError:
    from note import Note  # For testing purposes


class StorageManager:
    """
    Manages the storage and retrieval of notes using text files.
    """
    
    def __init__(self, storage_dir: str = "notes"):
        self.storage_dir = storage_dir
        self.ensure_storage_dir_exists()
        
    def ensure_storage_dir_exists(self):
        """Create the storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def save_note(self, note: Note) -> bool:
        """
        Save a note to a text file in JSON format.
        
        Args:
            note: The Note object to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Sanitize the filename to remove invalid characters
            filename = self.sanitize_filename(note.title) + ".json"
            filepath = os.path.join(self.storage_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(note.to_dict(), f, indent=2, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"Error saving note: {e}")
            return False
            
    def load_note(self, title: str) -> Optional[Note]:
        """
        Load a note from a text file.
        
        Args:
            title: The title of the note to load
            
        Returns:
            The Note object if found, None otherwise
        """
        try:
            filename = self.sanitize_filename(title) + ".json"
            filepath = os.path.join(self.storage_dir, filename)
            
            if not os.path.exists(filepath):
                return None
                
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            return Note.from_dict(data)
        except Exception as e:
            print(f"Error loading note: {e}")
            return None
            
    def delete_note(self, title: str) -> bool:
        """
        Delete a note file.
        
        Args:
            title: The title of the note to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = self.sanitize_filename(title) + ".json"
            filepath = os.path.join(self.storage_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False
            
    def list_notes(self) -> List[str]:
        """
        List all note titles in the storage directory.
        
        Returns:
            A list of note titles
        """
        try:
            notes = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    # Remove the '.json' extension to get the title
                    title = filename[:-5]
                    # Unsanitize the title
                    title = self.unsanitize_filename(title)
                    notes.append(title)
            return notes
        except Exception as e:
            print(f"Error listing notes: {e}")
            return []
            
    def sanitize_filename(self, title: str) -> str:
        """
        Sanitize a note title to make it a valid filename.
        
        Args:
            title: The original title
            
        Returns:
            A sanitized version safe for filenames
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        sanitized = title
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')
        # Also replace spaces with underscores for consistency
        sanitized = sanitized.replace(' ', '_')
        return sanitized
        
    def unsanitize_filename(self, filename: str) -> str:
        """
        Reverse the sanitization to get the original title.
        
        Args:
            filename: The sanitized filename
            
        Returns:
            The original title
        """
        # Replace underscores back to spaces (this is a simplification)
        # Note: This won't perfectly reverse all sanitizations but works for most cases
        return filename.replace('_', ' ')