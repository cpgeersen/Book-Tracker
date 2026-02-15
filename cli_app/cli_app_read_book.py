import sqlite3
from CRUD_Read import read_book
from os import remove

# Not meant to be user directly, only use through a driver

def read_db():
    test_isbn = 1234567890123
    insert_statement = ''' INSERT INTO Books(ISBN, Title, PublishDate, PublisherID, Summary,
                                            TagID, Chapters, Chapters_Completed, Cover_Image)
                           VALUES(1234567890123, 'SomeBook Title', 2026, 1, 'Long Summary sadfgasgsagsags',
                                  1, 20, 3, 'TEST BLOB')'''

    with sqlite3.connect('bt.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(insert_statement)
        except sqlite3.IntegrityError as error:
            pass

    read_book(test_isbn)
    conn.commit()
    #remove('bt.db')

if __name__ == '__main__':
    read_db()
