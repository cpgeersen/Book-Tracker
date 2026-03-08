import sqlite3

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


def connect_to_database():
    try:
        conn = sqlite3.connect('bt.db')
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()


def update_tags(tag_id, owned, favorite, completed, currently_reading, personal_or_academic):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Update Tags record by TagID.
    update_query = """
                UPDATE Tags
                SET Owned = ?,
                    Favorite = ?,
                    Completed = ?,
                    Currently_Reading = ?,
                    Personal_Or_Academic = ?
                WHERE Tag_ID = ?
            """
    criteria = (owned, favorite, completed, currently_reading, personal_or_academic, tag_id)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    return print(f"Tag {tag_id} updated successfully.")

def update_summary():
    pass

def update_chapters():
    pass

def update_genre():
    pass

def update_cover_image():
    pass



if __name__ == '__main__':
    pass