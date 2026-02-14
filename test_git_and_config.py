import os
import sys
import tempfile
import subprocess
from pathlib import Path
import json

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from note import Note
from storage import StorageManager
from config import Config

def test_config_management():
    """Test configuration loading and saving."""
    print("Testing configuration management...")
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.json"
        storage_dir = Path(temp_dir) / "test_notes"
        
        # Test default config
        config = Config(config_path)
        assert "storage_dir" in config.data
        
        # Test updating config
        config.storage_dir = str(storage_dir)
        assert config.storage_dir == str(storage_dir)
        assert config_path.exists()
        
        # Test reloading config
        new_config = Config(config_path)
        assert new_config.storage_dir == str(storage_dir)
        print("Config management verified")

def test_git_integration():
    """Test Git automatic commits."""
    print("\nTesting Git integration...")
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_dir = temp_dir
        
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=storage_dir, check=True, capture_output=True)
        # Configure git user for the test environment to avoid errors
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=storage_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=storage_dir, check=True)
        
        storage = StorageManager(storage_dir)
        note = Note("Git Note", "This should be committed automatically")
        
        # Test save triggers commit
        success = storage.save_note(note)
        assert success
        
        # Check if committed
        result = subprocess.run(["git", "log", "-1", "--pretty=%s"], cwd=storage_dir, capture_output=True, text=True)
        assert "Update note: Git Note" in result.stdout
        print("Save triggers automatic commit")
        
        # Test delete triggers commit
        success = storage.delete_note("Git Note")
        assert success
        
        # Check if committed
        result = subprocess.run(["git", "log", "-1", "--pretty=%s"], cwd=storage_dir, capture_output=True, text=True)
        assert "Delete note: Git Note" in result.stdout
        print("Delete triggers automatic commit")

if __name__ == "__main__":
    try:
        test_config_management()
        test_git_integration()
        print("\nAll Git and Config tests passed!")
    except Exception as e:
        print(f"\nTests failed: {e}")
        sys.exit(1)
