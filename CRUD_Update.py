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

#----------------------------------------------------------
# Update Tag Ubiquitous Function.
#----------------------------------------------------------
# Return the TagID for a book based on the ISBN.
def get_tag_id_by_isbn(ISBN):
    try:
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        query = """
            SELECT TagID
            FROM Books
            WHERE ISBN = ?
        """
        cursor.execute(query, (ISBN,))
        result = cursor.fetchone()

        if result is None:
            raise Exception(f"No book found with ISBN: {ISBN}")

        return result[0]

    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
#--------------------------------------------------
# Generic function to update tag.
#--------------------------------------------------
# Updates Tags record in Tags table based on TagID.
def update_tag(tagID_value, owned, favorite, completed, currently_reading, personal_or_academic):
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()
                

                
        # Update Tags record by TagID.
        update_query = """
            UPDATE Tags
            SET Owned = ?,
                Favorite = ?,
                Completed = ?,
                Currently_Reading = ?,
                PersonalOrAcademic = ?
            WHERE TagID = ?
        """

        cursor.execute(update_query, (owned, favorite, completed, currently_reading, personal_or_academic, tagID_value))
        conn.commit()
        return True, f"Tag {tagID_value} updated successfully."

    # Handle exceptions and close database connection.
    except sqlite3.Error as error:
        return False, f"Database error: {error}"

    except Exception as error:
        return False, f"Unexpected error: {error}"

    finally:
        try:
            conn.close()
        except:
            pass


#---------------------------------------------------
# Update Tag Ubiquitous Function.
#----------------------------------------------------
# Prompt user for tag values.
def get_binary_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value in (0, 1):
                return value
            print("Please enter only 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter 0 or 1.")


def update_tag_cli():
    tagID_value = int(input("Enter TagID to update: "))
    owned = get_binary_input("Enter Owned (0 or 1): ")
    favorite = get_binary_input("Enter Favorite (0 or 1): ")
    completed = get_binary_input("Enter Completed (0 or 1): ")
    currently_reading = get_binary_input("Enter Currently Reading (0 or 1): ")
    personal_or_academic = get_binary_input("Enter Personal (0) or Academic (1): ")

    success, message = update_tag(
        tagID_value,
        owned,
        favorite,
        completed,
        currently_reading,
        personal_or_academic
    )

    print(message)
