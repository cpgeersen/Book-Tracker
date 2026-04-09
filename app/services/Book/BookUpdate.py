import sqlite3
import json
from app.services.Book.BookPredicate import is_tag_id_in_tag_table, is_isbn_in_book_table, \
    is_publisher_name_in_publisher_table

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


def update_tags(tag_id, owned, favorite, completed, currently_reading):

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
                       Currently_Reading = ?
                       WHERE Tag_ID = ?
                   '''
    criteria = (owned, favorite, completed, currently_reading, tag_id)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    #return f"Tag {tag_id} updated successfully.", 200
    return json.dumps({"Success": f"Tag {tag_id} updated"}), 200

def update_summary(isbn, summary):

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

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
    return json.dumps({"Success": f"Book with {isbn} updated summary successfully."}), 200

def update_chapters(isbn, chapters):

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

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
    return json.dumps({"Success": f"Book with {isbn} updated chapters to {chapters}."}), 200

def update_read_chapters(isbn, chapters_competed):

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

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
    return json.dumps({"Success": f"Book with {isbn} updated chapters completed to {chapters_competed}."}), 200

# WIP - Will Implement Later
def update_genre(isbn, old_genre_id, new_genre_id):

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    update_query = ''' UPDATE BookGenre
                       SET Genre_ID = ?
                       WHERE ISBN = ?
                       AND Genre_ID = ?
                   '''
    criteria = (new_genre_id, isbn, old_genre_id,)
    cursor.execute(update_query, criteria)
    conn.commit()
    conn.close()
    return json.dumps({"Success": f"Book with {isbn} updated genre."}), 200







def update_cover_image(isbn, cover_image_path):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

    cover_image_update = ''' UPDATE Books
                             SET Cover_Image = ?
                             WHERE ISBN = ? 
                         '''
    cursor.execute(cover_image_update, (cover_image_path, isbn))
    conn.commit()
    conn.close()

    return json.dumps({"Success": f"Book with {isbn} updated cover image."}), 200

def update_publisher_year(isbn, publisher_year):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

    publisher_id_update = ''' UPDATE Books
                              SET Publish_Year = ?
                              WHERE ISBN = ? 
                          '''
    cursor.execute(publisher_id_update, (publisher_year, isbn,))
    conn.commit()
    conn.close()

    return json.dumps({"Success": f"Book with {isbn} updated publish year to {publisher_year}."}), 200



def update_publisher_id(isbn, publisher_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    isbn_presence = is_isbn_in_book_table(isbn)
    if not isbn_presence:
        return json.dumps({"Error": "ISBN not found"}), 400

    publisher_id_update = ''' UPDATE Books
                             SET Publisher_ID = ?
                             WHERE ISBN = ? 
                         '''
    cursor.execute(publisher_id_update, (publisher_id, isbn))
    conn.commit()
    conn.close()

    return json.dumps({"Success": f"Book with {isbn} updated publisher to {publisher_id}."}), 200
























if __name__ == '__main__':
    pass