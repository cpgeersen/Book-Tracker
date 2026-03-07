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


def delete_book_record(isbn):
    pass




































if __name__ == 'main':
    pass