import json
import os
from pathlib import Path

DEFAULT_CONFIG_PATH = Path.home() / ".note_taker_config.json"
DEFAULT_STORAGE_DIR = Path.home() / "notes"

class Config:
    """
    Manages the application configuration.
    """
    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.data = self._load()

    def _load(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Default configuration
        return {
            "storage_dir": str(DEFAULT_STORAGE_DIR)
        }

    def save(self):
        """Save the current configuration to the config file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    @property
    def storage_dir(self) -> str:
        return self.data.get("storage_dir", str(DEFAULT_STORAGE_DIR))

    @storage_dir.setter
    def storage_dir(self, value: str):
        self.data["storage_dir"] = value
        self.save()
