import sqlite3
import json

#==========================================================
# Original Author: Christopher O'Brien
# Editors:
#
# [] Is this program worthy? N/Y?
#
# This file contain the CRUD_Delete_Books code. 
# [NOTE]: Java formatted wrapper || terminology misunderstood.
# Target
# Reference
#==========================================================
# This file contains the CRUD code for a delete function.
DB_PATH = "bt.db"
#---------------------------------------------------------------------
# Defining A JSON Wrapper Function:
#--------------------------------------------------------------------- 
def json_wrapper(func): 
    def wrapped(json_input):
        try:
            data = json.loads(json_input) # Take a single JSON object, unpack its keys, and pass them as keyword arguments.  

            if not isinstance(data, dict):
                raise ValueError("JSON input must be an object mapping to function arguments")
    # Wrapper calls the function **data.
            return func(**data)   # <-- unpack JSON keys into function parameters
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")
    return wrapped

#---------------------------------------------------------------------
# Main Function Call (I applied the wrapper to the method)
#---------------------------------------------------------------------

def main():
    while True:
        isbn = input("Enter the ISBN for a book you want to remove from your library (or press Enter to quit): ")

        # Exit condition
        if not isbn.strip():
            print("Exiting.")
            break

        try:
            success, title = delete_book_cascading(isbn)

            if success:
                print(f"Book '{title}' with ISBN {isbn} was successfully removed.")
            else:
                print(f"No book with ISBN {isbn} was found in your library.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
#---------------------------------------------------------------------
# This is the code to delete the book function 
# Considering Removing a current return flags.
#---------------------------------------------------------------------
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
# I need to either prompt the user to enter an ISBN for a book to delete:

# JSON integration point.
@json_wrapper()
def delete_book_cascading(isbn: str):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            #-----------------------------------------
            # Retrieve Book Title for Verification
            #-----------------------------------------
            cur.execute("""SELECT Title 
                           FROM Books 
                           WHERE ISBN = ?
                        """, (isbn,))
            row = cur.fetchone()
            if not row:
                # Put in a statement to break the main function. 
                return False, f"No book found with ISBN {ISBN}"
            else:
                TITLE = row[0]
                return TITLE
            
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
            # Delete This Block
            # if not row: 
            #    return False, f"No book found with ISBN {isbn}" 
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
            # Delete This Block
            # return True, f"Book {isbn} and all related notes deleted."
            #
    except sqlite3.Error as e:
        return False, f"Database error: {e}"

    finally:
        conn.close()
#--------------------------------------------------------------------------------
# Here I am adding a main function call.
#--------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
