import sqlite3
from CRUD_Read import read_book
from os import remove

example_book_isbn = 1234567890123

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Create Example Book')
            print('2 - Create Book from User Data')
            print('3 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Creating Example Book')
                cli_create_book()
                result = read_book(example_book_isbn)
                print(result)
            elif user_choice == 2:
                print('User Defined Book')
                read_book(cli_create_book_from_data())
            elif user_choice == 3:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-3: {error}')


def cli_create_book_from_data():
    book_isbn = int(input('ISBN: '))
    book_title = input('Title: ')
    book_pub_year = int(input('Pub Year: '))
    book_pub_id = int(input('PubID: '))
    book_summary = input('Summary: ')
    book_tag_id = int(input('TagID: '))
    book_total_chapters = int(input('Total Chapters: '))
    book_finished_chapters = int(input('Finished Chapters: '))
    book_cover_image = input('PLACEHOLDER (enter any string): ')

    with sqlite3.connect('bt.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(''' INSERT INTO Books(ISBN, Title, PublishDate, PublisherID, Summary,
                                            TagID, Chapters, Chapters_Completed, Cover_Image)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (book_isbn, book_title, book_pub_year, book_pub_id, book_summary, book_tag_id,
                            book_total_chapters, book_finished_chapters, book_cover_image))
            conn.commit()
            return book_isbn
        except sqlite3.IntegrityError as error:
            print(f"Database error: {error}")


def cli_create_book():
    default_insert = ''' INSERT INTO Books(ISBN, Title, PublishDate, PublisherID, Summary,
                                            TagID, Chapters, Chapters_Completed, Cover_Image)
                            VALUES(1234567890123, 'SomeBook Title', 2026, 1, 'Long Summary sadfgasgsagsags',
                                    1, 20, 3, 'TEST BLOB')'''
    with sqlite3.connect('bt.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(default_insert)
            conn.commit()
        except sqlite3.IntegrityError as error:
            print(f"Database error: {error}")



if __name__ == '__main__':
    main()
