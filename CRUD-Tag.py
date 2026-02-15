import sqlite3

# Contains functions for CRUD functionality for Tags table.

# Inserts new Tags record into Tags table.
def create_tag(owned, favorite, completed, currently_reading, personal_or_academic):
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Insert new tag record.
        create_query = """
            INSERT INTO Tags (Owned, Favorite, Completed, Currently_Reading, PersonalOrAcademic)
            VALUES (?,?,?,?,?)
        """
        cursor.execute(create_query, (owned, favorite, completed, currently_reading, personal_or_academic))
        conn.commit()

        # Get generated TagID.
        tagID = cursor.lastrowid
        return print(f"Tag successfully created. TagID: {tagID}")

    # Handle exceptions and close database connection.
    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


# Reads Tags record(s) from Tags table filtered by TagID.
def read_tag(tagID_value):
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Tags table for TagID.
        read_query = "SELECT * FROM Tags WHERE TagID = ?"
        criteria = (tagID_value,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
            return print(result)
        else:
            return print("TagID not found")

    # Handle exceptions and close database connection.
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


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
        return print(f"Tag {tagID_value} updated successfully.")

    # Handle exceptions and close database connection.
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        conn.close()


# Deletes Tags record in Tags table based on TagID.
def delete_tag(tagID_value):
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Begin executing code block/transactions.
        cursor.execute("BEGIN")

        # Delete Tag record from Tags table by TagID.
        delete_query = "DELETE FROM Tags WHERE TagID = ?"
        cursor.execute(delete_query, (tagID_value,))
        conn.commit()

        return print(f"Tag {tagID_value} deleted.")

    # Handle exceptions and close database connection.
    except sqlite3.Error as error:
        print(f"Database error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        conn.close()