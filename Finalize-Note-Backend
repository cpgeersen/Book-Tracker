import sqlite3
# Contains functions for CRUD functionality for Notes table.

# 3.12.1 - Create Note
def create_note(json):
    try:
        isbn = json['ISBN']
        note_content = json['Note_Content']

        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        cursor.execute("BEGIN")

        cursor.execute(
            "INSERT INTO Notes (Note) VALUES (?)",
            (note_content,)
        )

        note_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO BookNotes (ISBN, NoteID) VALUES (?,?)",
            (isbn, note_id)
        )

        conn.commit()
        conn.close()

        return {
            "Note_ID": str(note_id),
            "Note_Content": note_content
        }

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {"error": "Failed to create note"}

# 3.12.2 - Read Note
def read_note(json):
    try:
        isbn = json['ISBN']

        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        read_query = """
            SELECT N.NoteID, N.Note
            FROM Notes AS N
            JOIN BookNotes AS B ON N.NoteID = B.NoteID
            WHERE B.ISBN = ?
        """

        cursor.execute(read_query, (isbn,))
        rows = cursor.fetchall()
        conn.close()

        notes = {}

        for note_id, note_content in rows:
            notes[str(note_id)] = note_content

        return notes

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {"error": "Failed to read notes"}

# 3.12.3 - Update Note
def update_note(json):
    try:
        note_id = json['Note_ID']
        note_content = json['Note_Content']

        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        update_query = """
            UPDATE Notes
            SET Note = ?
            WHERE NoteID = ?
        """

        cursor.execute(update_query, (note_content, note_id))
        conn.commit()
        conn.close()

        return {"status": "success"}

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {"status": "failure"}

# 3.12.4 - Delete Note
def delete_note(json):
    try:
        note_id = json['Note_ID']

        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        cursor.execute("BEGIN")

        cursor.execute(
            "DELETE FROM BookNotes WHERE NoteID = ?",
            (note_id,)
        )

        cursor.execute(
            "DELETE FROM Notes WHERE NoteID = ?",
            (note_id,)
        )

        conn.commit()
        conn.close()

        return {"status": "success"}

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return {"status": "failure"}