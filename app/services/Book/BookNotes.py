import sqlite3
import json



SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
DB_PATH = "bt.db"

def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()


# 3.12.1 - Create Note
def create_note(json_input):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    isbn = json_input['ISBN']
    note_content = json_input['Note_Content']

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

# 3.12.2 - Read Note
def read_note(json_input):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    isbn = json_input['ISBN']
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


# 3.12.3 - Update Note
def update_note(json_input):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    note_id = json_input['Note_ID']
    note_content = json_input['Note_Content']

    update_query = """
        UPDATE Notes
        SET Note = ?
        WHERE NoteID = ?
    """

    cursor.execute(update_query, (note_content, note_id))
    conn.commit()
    conn.close()

    return {"status": "success"}

# 3.12.4 - Delete Note
def delete_note(json_input):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    note_id = json_input['Note_ID']

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










