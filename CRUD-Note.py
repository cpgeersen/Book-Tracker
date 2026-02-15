import sqlite3

# Contains functions for CRUD functionality for Notes table. 
# Read functionality retreives binary files - May need to further refine to accommodate potential extensions. 


# Inserts new BLOB file into Note column, adds generated NoteID to BookNote table and assoicates with an ISBN.
def create_note(ISBN_value, blob_file):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("blobtest.db")
        cursor = conn.cursor()

        # Read provided file as binary
        with open(blob_file, 'rb') as file:
            data = file.read()
        
        # Begin the transaction
        conn.execute("BEGIN")
        cursor.execute("INSERT INTO Notes (Note) VALUES (?)", (data,))

        # Get generated NoteID and insert into BookNotes, associating with ISBN. 
        noteID = cursor.lastrowid
        cursor.execute("INSERT INTO BookNotes (ISBN, NoteID) VALUES (?,?)", (ISBN_value, noteID))
        conn.commit()
        return print("Note successfully created.")

    # Handle exceptions and close database connection.    
    except sqlite3.Error as error:
        print(f"Database error: {error}")

    except FileNotFoundError:
        print(f"File not found: {blob_file}")

    finally:
        conn.close()


# Reads BLOB file(s) from Note column, filtered by ISBN.  Returns a list of notes.  
def read_note(ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("blobtest.db")
        cursor = conn.cursor()

        # Query Note column, filtering by ISBN column in BookNotes. 
        read_query = "SELECT N.Note FROM Notes as N JOIN BookNotes as B on N.NoteID = B.NoteID WHERE B.ISBN = ?"
        criteria = (ISBN_value,)
        cursor.execute(read_query, criteria)
        rows = cursor.fetchall()

        # Return list of notes associated with ISBN.  Returns as bin files as extension may vary. 
        if not rows:
            return print(f"No notes found for ISBN: {ISBN_value}")
        
        else:
            notes_list = []
            for index, (blob_data,) in enumerate(rows, start=1):
                file_name = f"Note_{index}.bin"
                with open(file_name, "wb") as file:
                    file.write(blob_data)
                    notes_list.append(file_name)
        return print("Notes: ", notes_list)
    
    # Handle exceptions and close database connection.    
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        conn.close()


# Updates Note in Notes table based on NoteID and ISBN from BookNotes table. 
def update_note(ISBN_value, note_num, new_blob):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("blobtest.db")
        cursor = conn.cursor()

        # Convert new_blob file to a binary file. 
        with open(new_blob, "rb") as file:
            updated_blob_data = file.read()
     
        # Updates Note to new blob based on ISBN and NoteID in BookNote & Notes tables. 
        update_query = """
            UPDATE Notes AS N
            SET Note = ?
            WHERE N.NoteID = ?
                AND EXISTS (
                    SELECT 1
                    FROM BookNotes AS B
                    WHERE B.ISBN = ?
                        AND B.NoteID = N.NoteID
            )
        """

        cursor.execute(update_query, (updated_blob_data, note_num, ISBN_value))
        conn.commit()
        return print(f"Note {note_num} updated to {new_blob}")


# Handle exceptions and close database connection.    
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        conn.close()


# Deletes Note in Notes table based on NoteID and ISBN from BookNotes table. 
def delete_note(ISBN_value, note_num):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("blobtest.db")
        cursor = conn.cursor()

        # Begin executing code block/transactions.
        cursor.execute("BEGIN")

        # Delete Note from Notes table filtering by NotesID and ISBN.
        delete_Notes_query = """
            DELETE FROM Notes
            WHERE NoteID = ?
                AND NoteID IN (
                    SELECT N.NoteID
                    FROM Notes AS N
                    JOIN BookNotes AS B ON N.NoteID = B.NoteID
                    WHERE B.ISBN = ?
            )
        """
        
        cursor.execute(delete_Notes_query, (note_num, ISBN_value))

        # Delete assoicated NoteID and ISBN record from BookNotes table. 
        delete_BookNote_query = """
            DELETE FROM BookNotes
            WHERE ISBN = ?
            AND NoteID = ?
        """

        cursor.execute(delete_BookNote_query, (ISBN_value, note_num))
        conn.commit()

        return print(f"Note{note_num} deleted.")

    # Handle exceptions and close database connection.    
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        conn.close()