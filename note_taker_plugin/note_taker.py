from errbot import BotPlugin, botcmd, arg_botcmd
from note_app.manager import NoteManager
from note_app.config import Config

class NoteTaker(BotPlugin):
    """
    A plugin to manage your notes via Errbot.
    """

    def activate(self):
        """
        Triggered when the plugin is activated.
        """
        super().activate()
        self.config_manager = Config()
        self.note_manager = NoteManager(self.config_manager.storage_dir)

    @botcmd
    def note_list(self, msg, args):
        """List all your notes."""
        notes = self.note_manager.list_notes()
        if not notes:
            return "No notes found."
        
        response = f"Found {len(notes)} note(s):\n"
        for i, title in enumerate(notes, 1):
            response += f"{i}. {title}\n"
        return response

    @arg_botcmd('title', type=str)
    @arg_botcmd('--content', type=str, default="")
    @arg_botcmd('--tags', type=str, nargs='*', default=[])
    def note_create(self, msg, title=None, content=None, tags=None):
        """Create a new note."""
        # Detect origin from the message source (e.g., Telegram, Slack, etc.)
        origin = f"Errbot ({self._bot.mode})"
        
        success = self.note_manager.create_note(
            title=title, 
            content=content, 
            tags=tags, 
            origin=origin
        )
        
        if success:
            return f"Note '{title}' created successfully with origin '{origin}'."
        else:
            return f"Failed to create note '{title}'. It might already exist."

    @arg_botcmd('title_or_num', type=str)
    def note_read(self, msg, title_or_num=None):
        """Read a note by title or number."""
        # Try to resolve title if it's a number
        resolved_title = self._resolve_title(title_or_num)
        
        note = self.note_manager.read_note(resolved_title)
        if not note:
            return f"Note '{resolved_title}' not found."

        response = f"**{note.title}**\n"
        if note.origin:
            response += f"_Origin: {note.origin}_\n"
        response += f"_Created: {note.created_at}_\n"
        
        if note.tags:
            response += f"Tags: {', '.join(note.tags)}\n"
        
        response += "\n" + note.content
        return response

    @arg_botcmd('query', type=str)
    def note_search(self, msg, query=None):
        """Search across all note fields."""
        results = self.note_manager.universal_search(query)
        if not results:
            return f"No notes found matching '{query}'."
        
        response = f"Search results for '{query}':\n"
        for i, title in enumerate(results, 1):
            response += f"{i}. {title}\n"
        return response

    @arg_botcmd('title_or_num', type=str)
    def note_delete(self, msg, title_or_num=None):
        """Delete a note by title or number."""
        resolved_title = self._resolve_title(title_or_num)
        
        # Verify it exists first
        if not self.note_manager.read_note(resolved_title):
            return f"Note '{resolved_title}' not found."
            
        success = self.note_manager.delete_note(resolved_title)
        if success:
            return f"Note '{resolved_title}' deleted successfully."
        else:
            return f"Failed to delete note '{resolved_title}'."

    def _resolve_title(self, input_str):
        """Helper to resolve a title from either a string or a list index."""
        try:
            idx = int(input_str)
            all_notes = self.note_manager.list_notes()
            if 0 < idx <= len(all_notes):
                return all_notes[idx - 1]
        except ValueError:
            pass
        return input_str
