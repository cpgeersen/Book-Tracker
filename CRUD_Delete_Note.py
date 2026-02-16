import sqlite3
# This file contains the CRUD code for a delete function.
# The target of this function is the Notes Table.  
# The target of this function contains a reference table. 
DB_PATH = "bt.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def delete_note(note_id: int):
    try:
        with _connect() as conn:
            cur = conn.cursor()

            # 1. Remove the reference from BookNotes
            cur.execute("""
                DELETE FROM BookNotes
                WHERE NoteID = ?
            """, (note_id,))

            # 2. Delete the note itself
            cur.execute("""
                DELETE FROM Notes
                WHERE NoteID = ?
            """, (note_id,))

            return True, f"Note {note_id} deleted successfully."

    except sqlite3.Error as e:
        return False, f"Database error: {e}"
