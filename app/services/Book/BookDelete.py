import sqlite3
import json

from app.services.Book.BookNotes import read_note, delete_note
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


def delete_function(table, condition, condition_value, condition_2=None, condition_value_2=None):
    cursor, conn = connect_to_database()

    if condition_2 is not None and condition_value_2 is not None:
        query = f''' DELETE FROM {table}
                    WHERE {condition} = ?
                    AND {condition_2} = ?
                '''
        criteria = (condition_value, condition_value_2,)
        cursor.execute(query, criteria)
    else:
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
    # Get book info to delete off of
    book_result = json.loads(read_full_book_record(isbn))
    if book_result.get('Error') == 'Publisher_ID not found':
        return 'Error: Publisher_ID not present', BAD_REQUEST

    # First, delete the Books record
    delete_function('Books', 'ISBN', isbn)

    # Second, delete the BookGenre record(s)
    for genre_num in range(1, 5):
        genre_id_num = f'Genre_ID_{genre_num}'
        genre_id = book_result.get(genre_id_num)

        if genre_id is not None:
            delete_function('BookGenre', 'ISBN', isbn, 'Genre_ID', genre_id)

    # Third, delete the BookAuthor record(s)
    delete_function('BookAuthor', 'ISBN', isbn, 'Author_ID', book_result.get('Author_ID_1'))
    author_id_2 = book_result.get('Author_ID_2')
    if author_id_2 is not None or author_id_2 != '':
        delete_function('BookAuthor', 'ISBN', isbn, 'Author_ID', book_result.get('Author_ID_2'))

    # Third, delete the Tags record
    delete_function('Tags', 'Tag_ID', book_result['Tag_ID'])

    # Fourth, delete all note(s)
    notes = read_note(book_result)
    for note in notes.values():
        delete_note(note)

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

def delete_book_genre(isbn, genre_id):
    # Get a cursor and connection to the database
    cursor, conn = connect_to_database()
    try:
        query = f''' DELETE FROM BookGenre
                             WHERE ISBN = ?
                             AND Genre_ID = ?
                        '''
        criteria = (isbn, genre_id)
        cursor.execute(query, criteria)
        conn.commit()
        result = cursor.fetchall()
        conn.close()

        return f'Success: BookGenre record with {isbn} and {genre_id} deleted.', SUCCESS

    except:
        conn.close()
        return f'Error: Book with {isbn} does not have genre with id {genre_id}', BAD_REQUEST


if __name__ == '__main__':
    pass