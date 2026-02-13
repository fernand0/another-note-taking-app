import os
import sys
import tempfile

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from note import Note
from storage import StorageManager
from manager import NoteManager


def test_universal_search():
    """Test the universal search functionality."""
    print("Testing universal search functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = NoteManager(temp_dir)
        
        # Create test notes
        manager.create_note("Python Tutorial", "Learn Python programming. Visit https://docs.python.org for documentation.", ["tutorial", "programming"])
        manager.create_note("Web Development", "Building websites with HTML, CSS, and JavaScript. Check out https://developer.mozilla.org", ["web", "programming"])
        manager.create_note("Data Science", "Python libraries for data science like pandas and numpy.", ["data", "python"])
        
        # Test universal search
        # This should find notes that contain "Python" in title, content, tags, or links
        python_results = manager.universal_search("Python")
        assert len(python_results) == 2, f"Expected 2 Python results, got {len(python_results)}"
        print("✓ Universal search finds content matches")
        
        # Test universal search for tag
        python_tag_results = manager.universal_search("python")  # lowercase
        assert len(python_tag_results) == 2, f"Expected 2 python tag results, got {len(python_tag_results)}"
        print("✓ Universal search finds tag matches")
        
        # Test universal search for link
        docs_results = manager.universal_search("https://docs.python.org")
        assert len(docs_results) == 1, f"Expected 1 docs result, got {len(docs_results)}"
        print("✓ Universal search finds link matches")
        
        # Test universal search for title
        tutorial_results = manager.universal_search("Tutorial")
        assert len(tutorial_results) == 1, f"Expected 1 Tutorial result, got {len(tutorial_results)}"
        print("✓ Universal search finds title matches")


def run_universal_search_tests():
    """Run universal search tests."""
    print("Running universal search tests for note-taking application...\n")
    
    try:
        test_universal_search()
        print("\n✓ All universal search tests passed!")
    except AssertionError as e:
        print(f"\n✗ Universal search test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error in universal search tests: {e}")
        return False
    
    return True


if __name__ == "__main__":
    run_universal_search_tests()