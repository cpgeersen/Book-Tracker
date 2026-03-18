import sqlite3
import json
from app.services.Book.BookPredicate import is_tag_id_in_tag_table

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

DB_PATH = "bt.db"

def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()


def update_tags(tag_id, owned, favorite, completed, currently_reading, personal_or_academic):

    tag_id_presence = is_tag_id_in_tag_table(tag_id)
    if not tag_id_presence:
        return json.dumps({"Error": "Tag_ID not found"}), 400

    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Update Tags record by TagID.
    update_query = ''' UPDATE Tags
                       SET Owned = ?,
                       Favorite = ?,
                       Completed = ?,
                       Currently_Reading = ?,
                       Personal_Or_Academic = ?
                       WHERE Tag_ID = ?
                   '''
    criteria = (owned, favorite, completed, currently_reading, personal_or_academic, tag_id)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    #return f"Tag {tag_id} updated successfully.", 200
    return json.dumps({"Success": f"Tag {tag_id} updated"}), 200

def update_summary(isbn, summary):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    update_query = ''' UPDATE Books
                       SET Summary = ?
                       WHERE ISBN = ?
                   '''
    criteria = (summary, isbn,)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    return f"Book with {isbn} updated summary successfully.", 200

def update_chapters(isbn, chapters):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    update_query = ''' UPDATE Books
                       SET Chapters = ?
                       WHERE ISBN = ?
                   '''
    criteria = (chapters, isbn,)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    return f"Book with {isbn} updated number of chapters successfully.", 200

def update_read_chapters(isbn, chapters_competed):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    update_query = ''' UPDATE Books
                       SET Chapters_Completed = ?
                       WHERE ISBN = ?
                   '''
    criteria = (chapters_competed, isbn,)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    return f"Book with {isbn} updated number of completed chapters successfully.", 200

# WIP - Will Implement Later
def update_genre(isbn, genre):
    pass

# WIP - Will Implement Later
def update_cover_image(isbn, cover_image):
    pass






























if __name__ == '__main__':
    pass