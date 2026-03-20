import sqlite3

DB_PATH = "bt.db"

def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()

def is_isbn_in_book_table(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query if the ISBN is in Book Table
    read_query = "SELECT * FROM Books WHERE ISBN = ?"
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()

    conn.close()

    # Return False when there is no ISBN that matches
    if len(result) == 0:
        return False
    else:
        return True

def is_tag_id_in_tag_table(tag_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query if the Tag_ID is in Tags Table
    read_query = "SELECT * FROM Tags WHERE Tag_ID = ?"
    criteria = (tag_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()

    conn.close()

    # Return False when there is no Tag_ID that matches
    if len(result) == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    pass