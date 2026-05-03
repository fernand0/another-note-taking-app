import os
import sys
import tempfile
import shutil

from note_app.note import Note
from note_app.storage import StorageManager
from note_app.manager import NoteManager


def test_note_creation():
    """Test creating and storing a note."""
    print("Testing note creation...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        storage = StorageManager(temp_dir)
        
        # Create a note
        note = Note("Test Note", "This is a test note with a link: https://example.com")
        note.add_tag("test")
        note.add_tag("important")
        
        # Save the note
        success = storage.save_note(note)
        assert success, "Failed to save note"
        print("✓ Note saved successfully")
        
        # Load the note
        loaded_note = storage.load_note("Test Note")
        assert loaded_note is not None, "Failed to load note"
        assert loaded_note.title == "Test Note", "Title mismatch"
        assert "https://example.com" in loaded_note.get_links(), "Link not found"
        assert "test" in loaded_note.tags, "Tag not found"
        print("✓ Note loaded and verified successfully")


def test_note_manager():
    """Test the NoteManager functionality."""
    print("\nTesting NoteManager...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = NoteManager(temp_dir)
        
        # Create a note
        success = manager.create_note("First Note", "Content of first note")
        assert success, "Failed to create note"
        print("✓ Note created via manager")
        
        # Read the note
        note = manager.read_note("First Note")
        assert note is not None, "Failed to read note"
        assert note.content == "Content of first note", "Content mismatch"
        print("✓ Note read via manager")
        
        # Update the note
        success = manager.update_note("First Note", content="Updated content")
        assert success, "Failed to update note"
        
        # Verify update
        updated_note = manager.read_note("First Note")
        assert updated_note.content == "Updated content", "Update failed"
        print("✓ Note updated via manager")
        
        # Add a reference
        manager.create_note("Second Note", "Content of second note")
        success = manager.add_reference("First Note", "Second Note")
        assert success, "Failed to add reference"
        
        # Verify reference was added
        refs = manager.get_note_references("First Note")
        assert "Second Note" in refs, "Reference not found"
        print("✓ Reference added and verified")
        
        # Check back-references
        back_refs = manager.get_back_references("Second Note")
        assert "First Note" in back_refs, "Back-reference not found"
        print("✓ Back-reference found")
        
        # List notes
        notes = manager.list_notes()
        assert len(notes) == 2, f"Expected 2 notes, got {len(notes)}"
        print("✓ Notes listed correctly")
        
        # Delete a note
        success = manager.delete_note("Second Note")
        assert success, "Failed to delete note"
        
        # Verify deletion
        notes = manager.list_notes()
        assert len(notes) == 1, f"Expected 1 note after deletion, got {len(notes)}"
        print("✓ Note deleted successfully")


def test_hashtag_tags_extraction():
    """Test extracting hashtag tags from the end of the note content."""
    print("\nTesting hashtag tags extraction...")
    
    # Test case: Multiple tags at the end
    note = Note("Hashtag Test", "This is a note with hashtags #tag1 #tag2")
    assert "tag1" in note.tags, "tag1 not extracted"
    assert "tag2" in note.tags, "tag2 not extracted"
    assert note.content == "This is a note with hashtags", f"Content not stripped correctly: {note.content}"
    print("✓ Hashtags extracted and content stripped")
    
    # Test case: Hashtags in middle preserved
    note2 = Note("Hashtag Middle", "This #note has a hashtag in the middle")
    assert "note" not in note2.tags, "Middle hashtag should not be a tag"
    assert note2.content == "This #note has a hashtag in the middle"
    print("✓ Middle hashtags preserved")
    
    # Test case: Update content with hashtags
    note.update_content("New content #tag3")
    assert "tag3" in note.tags, "New tag not extracted during update"
    assert note.content == "New content", "Content not stripped during update"
    print("✓ Hashtags extracted during update")


def test_note_creation_without_title():
    """Test creating a note without an explicit title."""
    print("\nTesting note creation without title...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = NoteManager(temp_dir)
        
        content = "This is a note without a title"
        title = manager.create_note(content=content)
        
        assert title is not False, "Failed to create note without title"
        assert "This is a note without_" in title, f"Title not generated correctly: {title}"
        
        # Verify it can be read
        note = manager.read_note(title)
        assert note.content == content, "Content mismatch"
        print(f"✓ Note created with generated title: {title}")


def test_title_resolution():
    """Test resolving titles from indices."""
    print("\nTesting title resolution...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = NoteManager(temp_dir)
        
        manager.create_note("Note A", "Content A")
        manager.create_note("Note B", "Content B")
        
        # Test resolution
        assert manager.resolve_title("Note A") == "Note A"
        assert manager.resolve_title("1") == "Note A"
        assert manager.resolve_title("2") == "Note B"
        assert manager.resolve_title("3") is None
        print("✓ Basic title resolution works")
        
        # Test read by index
        note = manager.read_note("1")
        assert note is not None and note.title == "Note A"
        print("✓ Read by index works")
        
        # Test delete by index
        success = manager.delete_note("1")
        assert success
        assert len(manager.list_notes()) == 1
        assert manager.list_notes()[0] == "Note B"
        print("✓ Delete by index works")


def run_tests():
    """Run all tests."""
    print("Running tests for note-taking application...\n")
    
    try:
        test_note_creation()
        test_note_manager()
        test_hashtag_tags_extraction()
        test_note_creation_without_title()
        test_title_resolution()
        print("\n✓ All tests passed!")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    run_tests()