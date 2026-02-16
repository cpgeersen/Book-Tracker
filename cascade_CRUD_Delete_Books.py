import sqlite3
# This file contains the CRUD code for a delete function.
# This file works with the cascade adjusted create_db.py.
DB_PATH = "bt.db"
def delete_book(isbn):
    try:
        with sqlite3.connect("bt.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Check if the book exists
            cursor.execute("SELECT ISBN FROM Books WHERE ISBN = ?", (isbn,))
            exists = cursor.fetchone()

            if not exists:
                return f"Book with ISBN {isbn} not found."

            # Delete the book (cascades to BookAuthor, BookGenre, BookNotes)
            cursor.execute("DELETE FROM Books WHERE ISBN = ?", (isbn,))
            conn.commit()

            return f"Book with ISBN {isbn} deleted successfully."

    except sqlite3.Error as error:
        return f"Database error: {error}"