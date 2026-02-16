import sqlite3
# This file contains the CRUD code for a delete function.
# The Assumption no: ON DELETE CASCADE in FOREIGN KEY REFERENCES DEFINITION
DB_PATH = "bt.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def delete_book_cascading(isbn: str):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            #------------------------------------------
            # I. Delete References in Reference Tables.
            #------------------------------------------
            # 1.
            # A. Get all NoteIDs linked to this book
            cur.execute("""
                SELECT NoteID
                FROM BookNotes
                WHERE ISBN = ?
            """, (isbn,))
            note_ids = [row[0] for row in cur.fetchall()]

            # B. Delete from BookNotes first
            cur.execute("""
                DELETE FROM BookNotes
                WHERE ISBN = ?
            """, (isbn,))

            # C. Delete the Notes themselves
            if note_ids:
                cur.executemany("""
                    DELETE FROM Notes
                    WHERE NoteID = ?
                """, [(nid,) for nid in note_ids])
            #----------------------------------------
            # 2. Delete Reference Without Reference Tables.
            #----------------------------------------
            # A. Get All genre ID linked to this book
            cur.execute("""
                SELECT GenreID
                FROM BookGenre
                WHERE ISBN = ?
            """, (isbn,))
            genre_ids = [row[0] for row in cur.fetchall()]
            # B. Delete from BookGenre First.
            cur.execute("""
                DELETE FROM BookGenre
                WHERE ISBN = ?
            """, (isbn,))
            # C. I Decided not to delete the Genre Here... 
            #----------------------------------------------
            # 3. Delete the Book itself.
            #----------------------------------------------
            # A. Get All AuthorID linked to this book
            cur.execute("""
                SELECT AuthorID
                FROM BookAuthor
                WHERE ISBN = ?
            """, (isbn,))
            author_ids = [row[0] for row in cur.fetchall()]
            # B. Delete from BookAuthor First
            cur.execute("""
                DELETE FROM BookAuthor
                WHERE ISBN = ?
            """, (isbn,))
            # C. I Decided Not to Delete from the Authors Table

            # II. Delete Direct Table References
            #1.
            # A. Look up the TagID for this book 
            cur.execute("SELECT TagID FROM Books WHERE ISBN = ?", (isbn,)) 
            row = cur.fetchone() 
            if not row: 
                return False, f"No book found with ISBN {isbn}" 
            tag_id = row[0] 
            # B. Delete the tag row first (child) 
            cur.execute("DELETE FROM Tags WHERE TagID = ?", (tag_id,))
            # 2. 
            # A. I decided not to delete from publishers.

            # III. Delete the Book
            cur.execute("""
                DELETE FROM Books
                WHERE ISBN = ?
            """, (isbn,))

            return True, f"Book {isbn} and all related notes deleted."

    except sqlite3.Error as e:
        return False, f"Database error: {e}"

    finally:
        conn.close()