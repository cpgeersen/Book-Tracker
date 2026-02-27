from cli_create_db import create_db
import sqlite3
from CRUD_Full_Read import read_full_book_record


create_db()

def cli_create_book():
    book_insert = ''' INSERT INTO Books(ISBN, Title, Publish_Year, Publisher_ID, Summary,
                                            Tag_ID, Chapters, Chapters_Completed, Cover_Image)
                            VALUES(
                            9781529370515, 
                            'The Stand', 
                            1978, 
                            1, 
                            'Confrontation between the forces of good and evil.',
                            1, 
                            20, 
                            20, 
                            'TEST BLOB')
                            '''
    book_author_insert = ''' INSERT INTO BookAuthor(ISBN, Author_ID)
                             VALUES(9781529370515, 1)
                             '''
    author_insert = ''' INSERT INTO Authors(Author_ID, Author_Full_Name,
                                            Author_First_Name, Author_Last_Name, OpenLibrary_ID)
                        VALUES(1, 'Stephen King', 'Stephen', 'King', 'OLID-TEST')
                    '''
    publisher_insert = ''' INSERT INTO Publishers(Publisher_ID, Publisher_Name)
                           VALUES(1, 'Double Day')
                       '''
    tags_insert = ''' INSERT INTO Tags(Tag_ID, Owned, Favorite, Completed, Currently_Reading,
                                            Personal_Or_Academic)
                      VALUES(1, 1, 1, 1, 0, 0)
    
                   '''
    book_genre_insert = ''' INSERT INTO BookGenre(ISBN, Genre_ID)
                          VALUES(9781529370515, 100)
                       '''
    genre_insert = ''' INSERT INTO Genre(Genre_ID, Genre)
                              VALUES(100, 'fiction')
                           '''


    with sqlite3.connect('bt.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(book_insert)
            cursor.execute(book_author_insert)
            cursor.execute(author_insert)
            cursor.execute(publisher_insert)
            cursor.execute(tags_insert)
            cursor.execute(book_genre_insert)
            #cursor.execute(genre_insert)
            conn.commit()
        except sqlite3.IntegrityError as error:
            print(f"Database error: {error}")


def read_db_all():
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query database for ISBN provided.
        cursor.execute("SELECT * FROM Books")
        book_result = cursor.fetchall()

        cursor.execute("SELECT * FROM BookAuthor")
        book_author_result = cursor.fetchall()

        cursor.execute("SELECT * FROM Authors")
        author_result = cursor.fetchall()

        cursor.execute("SELECT * FROM Publishers")
        publisher_result = cursor.fetchall()

        cursor.execute("SELECT * FROM Tags")
        tag_result = cursor.fetchall()


        conn.close()
        return book_result, book_author_result, author_result, publisher_result, tag_result
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()




cli_create_book()


result = read_db_all()
#print(result)


bt = read_full_book_record(9781529370515)
print(bt)




