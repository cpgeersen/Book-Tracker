import create_db # Must be first import to auto-execute database creation
#from cli_app.cli_app_create_book import cli_create_book
from cli_app_read_book import read_db
import sqlite3

#read_db()



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

    insert_statement = (''' INSERT INTO Books(ISBN, Title, PublishDate, PublisherID, Summary,
                                            TagID, Chapters, Chapters_Completed, Cover_Image)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (book_isbn, book_title, book_pub_year, book_pub_id, book_summary, book_tag_id,
                                         book_total_chapters, book_finished_chapters, book_cover_image))
    with sqlite3.connect('bt.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(''' INSERT INTO Books(ISBN, Title, PublishDate, PublisherID, Summary,
                                            TagID, Chapters, Chapters_Completed, Cover_Image)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (book_isbn, book_title, book_pub_year, book_pub_id, book_summary, book_tag_id,
                                         book_total_chapters, book_finished_chapters, book_cover_image))
            conn.commit()
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
