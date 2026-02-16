import sqlite3

# This code should use ISBN to Update Chapters_Completed.  
# Additionally, an automatic update is made to the tags table to mark a book completed.

def update_chapters(ISBN, Chapters_Completed):
    try:
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        # Begin transaction
        conn.execute("BEGIN")

        # 1. Update Books table
        update_books_query = """
            UPDATE Books
            SET Chapters_Completed = ?
            WHERE ISBN = ?
        """
        cursor.execute(update_books_query, (Chapters_Completed, ISBN))

        # 2. Get the book's Chapters and TagID
        cursor.execute("""
            SELECT Chapters, TagID
            FROM Books
            WHERE ISBN = ?
        """, (ISBN,))
        result = cursor.fetchone()

        if result is None:
            raise Exception(f"No book found with ISBN: {ISBN}")

        total_chapters, tag_id = result

        # 3. Decide how to update Tags
        if Chapters_Completed >= total_chapters:
            # Books is finished
            update_tags_query = """
                UPDATE Tags
                SET Completed = 1,
                    Currently_Reading = 0
                WHERE TagID = ?
            """
        else:
            # Still reading
            update_tags_query = """
                UPDATE Tags
                SET Completed = 0,
                    Currently_Reading = 1
                WHERE TagID = ?
            """

        cursor.execute(update_tags_query, (tag_id,))

        conn.commit()

        if Chapters_Completed >= total_chapters:
            return f"Congratulations! You've completed the book."
        else:
            return f"Nice progress! {Chapters_Completed} chapters completed."

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.rollback()

    except Exception as error:
        print(f"Unexpected error: {error}")
        conn.rollback()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("Connection closed.")
