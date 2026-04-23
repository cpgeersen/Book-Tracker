import sqlite3

SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
DB_PATH = "bt.db"

"""
    Reworked functions from Chris. Most of the logic is from Chris, just refactored.
"""

def analytics_for_dashboard():
    json_output = {}

    total = total_books()
    owned = owned_books()
    reading = currently_reading_books()
    completed = completed_books()
    genres = most_read_genres()

    if total is not None:
        json_output.update(total)
    if owned is not None:
        json_output.update(owned)
    if reading is not None:
        json_output.update(reading)
    if completed is not None:
        json_output.update(completed)
    if genres is not None:
        json_output.update(genres)

    return json_output


def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()


def total_books():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()
    try:
        query = ''' SELECT COUNT(ISBN) FROM Books '''
        cursor.execute(query)
        result = cursor.fetchone()[0]
        conn.close()
        return {"Total_Books": result}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def owned_books():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()
    try:
        query = ''' SELECT COUNT(t.Tag_ID)
                    FROM Books b
                    JOIN Tags t ON b.Tag_ID = t.Tag_ID
                    WHERE t.Owned = 'yes'
                '''
        cursor.execute(query)
        result = cursor.fetchone()[0]
        conn.close()
        return {"Total_Owned": result}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def currently_reading_books():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()
    try:
        query = ''' SELECT COUNT(b.ISBN)
                    FROM Tags t
                    JOIN Books b ON t.Tag_ID = b.Tag_ID
                    WHERE t.Currently_Reading = 'yes'
                '''
        cursor.execute(query)
        result = cursor.fetchone()[0]
        conn.close()
        return {"Total_Reading": result}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def completed_books():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()
    try:
        query = ''' SELECT COUNT(b.ISBN)
                    FROM Tags t
                    JOIN Books b ON t.Tag_ID = b.Tag_ID
                    WHERE t.Completed = 'yes'
                '''
        cursor.execute(query)
        result = cursor.fetchone()[0]
        conn.close()
        return {"Total_Completed": result}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def most_read_genres():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()
    try:
        query = ''' SELECT c.Genre, COUNT(b.Genre_ID) AS genre_count
                    FROM Books a
                    JOIN BookGenre b ON a.ISBN = b.ISBN
                    JOIN Genre c ON b.Genre_ID = c.Genre_ID
                    GROUP BY b.Genre_ID
                    ORDER BY genre_count DESC
                    LIMIT 5
                '''
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return {"Genres": result}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

















