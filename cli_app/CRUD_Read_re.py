import sqlite3
# This file contains Read functionality for book, author, publisher, and genre records.
# Uses ISBN as parameter.

# Connect to SQLite database.
with sqlite3.connect('bt.db') as conn:
    cursor = conn.cursor()

# Read functionality for book records.
def read_book(x):
    try:
        # Query database for ISBN provided.
        read_query = "SELECT * FROM Books WHERE ISBN = ?"
        criteria = (x,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()

        # Check to confirm value found in table
        if result:
            return print(result)
        else:
            return print("ISBN not found")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


# Read functionality for author records (returns author's first and last name).
def read_author(x):
    try:
        # Query database for ISBN provided.
        read_query = "SELECT Author_First_Name, Author_Last_Name FROM Authors as A JOIN BookAuthor as B ON A.AuthorID = B.AuthorID WHERE ISBN = ?"
        criteria = (x,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()

        # Check to confirm value found in table
        if result:
            return print(result)
        else:
            return print("ISBN not found")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()

# Read functionality for publisher records (returns publisher's name).
def read_publisher(x):
    try:
        # Query database for ISBN provided.
        read_query = "SELECT P.Publisher_Name FROM Publishers as P JOIN Books as B ON P.PublisherID = B.PublisherID WHERE B.ISBN = ?"
        criteria = (x,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()

        # Check to confirm value found in table
        if result:
            return print(result)
        else:
            return print("ISBN not found")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()


# Read functionality for genre records (returns genre).
def read_genre(x):
    try:
        # Query database for ISBN provided.
        read_query = "SELECT Genre FROM Genre as G JOIN BookGenre as B on G.GenreID = B.GenreID WHERE B.ISBN = ?"
        criteria = (x,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()

        # Check to confirm value found in table
        if result:
            return print(result)
        else:
            return print("ISBN not found")

    except sqlite3.Error as error:
        print(f"Database error: {error}")

    finally:
        conn.close()
