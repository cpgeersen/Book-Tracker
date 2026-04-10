import sqlite3
import json
from app.services.Book.BookRead import read_full_book_record, read_author_id_from_name

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

DB_PATH = "bt.db"


def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
        print(f"Database error: {error}")


def delete_function(table, condition, condition_value):
    cursor, conn = connect_to_database()

    query = f''' DELETE FROM {table}
                WHERE {condition} = ?
            '''
    criteria = (condition_value,)
    cursor.execute(query, criteria)
    conn.commit()
    result = cursor.fetchall()
    conn.close()

    return f'Successfully deleted from {table} table where {condition} is {condition_value}'


def delete_book_record(isbn):

    # Get the book record for Tag_ID and NoteID
    book_result = json.loads(read_full_book_record(isbn))
    if book_result.get('Error') == 'Publisher_ID not found':
        return 'Error: Publisher_ID not present', BAD_REQUEST

    # First, delete the Books record
    delete_function('Books', 'ISBN', isbn)

    # Second, delete the BookGenre records
    delete_function('BookGenre', 'ISBN', isbn)

    # Third, delete the Tags record
    delete_function('Tags', 'Tag_ID', book_result['Tag_ID'])

    # Fourth, delete Notes !!WIP!!

    return f'Success: Book with {isbn} deleted.', SUCCESS

def delete_book_author_table_record(isbn, author_first_name, author_last_name):

    # Get the author_id if it exists
    author_id = read_author_id_from_name(author_first_name, author_last_name)

    # When no author_id exists, error out
    if author_id == '':
        return 'Error: Author_ID not present', BAD_REQUEST

    # Get a cursor and connection to the database
    cursor, conn = connect_to_database()

    query = f''' DELETE FROM BookAuthor
                 WHERE ISBN = ?
                 AND Author_ID = ?
            '''
    criteria = (isbn, author_id['Author_ID'],)
    cursor.execute(query, criteria)
    conn.commit()
    result = cursor.fetchall()
    conn.close()

    return f'Success: BookAuthor record with {isbn} and {author_id} deleted.', SUCCESS

if __name__ == '__main__':
    pass