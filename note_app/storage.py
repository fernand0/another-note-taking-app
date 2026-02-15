import json
import os
import subprocess
import hashlib
from typing import Dict, List, Optional
from .note import Note


class StorageManager:
    """
    Manages the storage and retrieval of notes using text files with Git integration.
    """
    
    def __init__(self, storage_dir: str = "notes"):
        self.storage_dir = os.path.abspath(storage_dir)
        self.ensure_storage_dir_exists()
        
    def ensure_storage_dir_exists(self):
        """Create the storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def _is_git_repo(self) -> bool:
        """Check if the storage directory is a git repository."""
        return os.path.exists(os.path.join(self.storage_dir, ".git"))

    def _run_git_command(self, args: List[str]) -> bool:
        """Run a git command in the storage directory."""
        try:
            subprocess.run(
                ["git"] + args,
                cwd=self.storage_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # We don't want to crash if git is not installed or command fails
            print(f"Git command failed: {e}")
            return False

    def save_note(self, note: Note) -> bool:
        """
        Save a note to a text file in JSON format and commit to git if applicable.
        
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
            
            if self._is_git_repo():
                # Use -- to separate options from filenames to prevent interpretation of filenames starting with dashes
                self._run_git_command(["add", "--", filename])
                self._run_git_command(["commit", "-m", f"Update note: {note.title}"])
                
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
        Delete a note file and commit to git if applicable.
        
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
                
                if self._is_git_repo():
                    # We use git rm if it's a git repo to properly stage the deletion
                    # Use -- to separate options from filenames to prevent interpretation of filenames starting with dashes
                    self._run_git_command(["rm", "--", filename])
                    self._run_git_command(["commit", "-m", f"Delete note: {title}"])
                
                return True
            else:
                return False
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False
            
    def list_notes(self) -> List[str]:
        """
        List all note titles by reading them from the stored JSON files.
        
        Returns:
            A list of note titles
        """
        try:
            notes = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if 'title' in data:
                                notes.append(data['title'])
                            else:
                                notes.append(self.unsanitize_filename(filename[:-5]))
                    except (json.JSONDecodeError, IOError):
                        notes.append(self.unsanitize_filename(filename[:-5]))
            return notes
        except Exception as e:
            print(f"Error listing notes: {e}")
            return []
            
    def sanitize_filename(self, title: str) -> str:
        """
        Sanitize a note title to make it a valid filename, with truncation for long titles.
        
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
        
        # Truncate to a safe length (e.g., 200 chars) to avoid OS errors
        # If we truncate, we add a hash of the original title to ensure uniqueness
        if len(sanitized) > 200:
            title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
            sanitized = sanitized[:190] + "_" + title_hash
            
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