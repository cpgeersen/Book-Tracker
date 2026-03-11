import sqlite3
import json
from app.services.Book.BookRead import read_full_book_record

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

    if not result:  # When the result is empty, meaning it was deleted
        return f'Successfully deleted from {table} table where {condition} is {condition_value}'
    else:
        return f'No records exist for {condition} being {condition_value} in {table}'


def delete_book_record(isbn):
    try:
        # Get the book record for Tag_ID and NoteID
        book_result = json.loads(read_full_book_record(isbn))

        # First, delete the Books record
        delete_function('Books', 'ISBN', isbn)

        # Second, delete the BookGenre records
        delete_function('BookGenre', 'ISBN', isbn)

        # Third, delete the Tags record
        delete_function('Tags', 'Tag_ID', book_result['Tag_ID'])

        return f'Success: Book with {isbn} deleted.', SUCCESS
    except json.decoder.JSONDecodeError:
        return f'Error: Book with {isbn} not present', BAD_REQUEST


if __name__ == 'main':
    pass