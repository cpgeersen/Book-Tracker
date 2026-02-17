import sqlite3
from CRUD_Read import read_from_database

# Not meant to be user directly, only use through a driver

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Read all Books')
            print('2 - Read Book from ISBN')
            print('3 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Reading all books from DB')
                all_books = read_db_all()
                for book in all_books:
                    print(book)
            elif user_choice == 2:
                print('User Defined Book')
                user_isbn = int(input('Enter an ISBN to Read for: '))
                print(read_from_database(user_isbn, 'read_book'))
            elif user_choice == 3:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-3: {error}')


def read_db_isbn(isbn):
    read_from_database(isbn, 'read_book')

def read_db_all():
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query database for ISBN provided.
        cursor.execute("SELECT * FROM Books")
        result = cursor.fetchall()
        conn.close()
        return result

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()

if __name__ == '__main__':
    main()
