import sqlite3
# This file contains the CRUD code for a delete function.
# This file works with the cascade adjusted create_db.py.
def delete_note(note_id):
    try:
        with sqlite3.connect("bt.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Check if the note exists
            cursor.execute("SELECT NoteID FROM Notes WHERE NoteID = ?", (note_id,))
            exists = cursor.fetchone()

            if not exists:
                return f"Note with ID {note_id} not found."

            # Delete the note (BookNotes rows will cascade automatically)
            cursor.execute("DELETE FROM Notes WHERE NoteID = ?", (note_id,))
            conn.commit()

            return f"Note with ID {note_id} deleted successfully."

    except sqlite3.Error as error:
        return f"Database error: {error}"