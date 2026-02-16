import os
import sys
import tempfile
import shutil

from note_app.note import Note
from note_app.storage import StorageManager
from note_app.manager import NoteManager
from note_app.search import SearchEngine


def test_search_functionality():
    """Test the search functionality."""
    print("Testing search functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = NoteManager(temp_dir)
        
        # Create test notes
        manager.create_note("Python Tutorial", "Learn Python programming. Visit https://docs.python.org for documentation.", ["tutorial", "programming"])
        manager.create_note("Web Development", "Building websites with HTML, CSS, and JavaScript. Check out https://developer.mozilla.org", ["web", "programming"])
        manager.create_note("Data Science", "Python libraries for data science like pandas and numpy.", ["data", "python"])
        
        # Test content search
        python_results = manager.search_content("Python")
        assert len(python_results) == 2, f"Expected 2 Python results, got {len(python_results)}"
        print("✓ Content search works")
        
        # Test title search
        tutorial_results = manager.search_titles("Tutorial")
        assert len(tutorial_results) == 1, f"Expected 1 Tutorial result, got {len(tutorial_results)}"
        print("✓ Title search works")
        
        # Test tag search
        programming_results = manager.search_tags("programming")
        assert len(programming_results) == 2, f"Expected 2 programming results, got {len(programming_results)}"
        print("✓ Tag search works")
        
        # Test link search
        docs_results = manager.search_links("https://docs.python.org")
        assert len(docs_results) == 1, f"Expected 1 docs result, got {len(docs_results)}"
        print("✓ Link search works")
        
        # Test advanced search
        advanced_results = manager.advanced_search(content_query="Python", tag_query="python")
        assert len(advanced_results) >= 1, f"Expected at least 1 advanced search result, got {len(advanced_results)}"
        print("✓ Advanced search works")


def run_search_tests():
    """Run search tests."""
    print("Running search tests for note-taking application...\n")
    
    try:
        test_search_functionality()
        print("\n✓ All search tests passed!")
    except AssertionError as e:
        print(f"\n✗ Search test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error in search tests: {e}")
        return False
    
    return True


if __name__ == "__main__":
    run_search_tests()