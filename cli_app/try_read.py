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
                        VALUES(Null, 'Stephen King', 'Stephen', 'King', 'OLID-TEST')
                    '''
    publisher_insert = ''' INSERT INTO Publishers(Publisher_ID, Publisher_Name)
                           VALUES(1, 'Double Day')
                       '''
    tags_insert = ''' INSERT INTO Tags(Tag_ID, Owned, Favorite, Completed, Currently_Reading,
                                            Personal_Or_Academic, ISBN)
                      VALUES(NULL, 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 9781529370515)
    
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
            # cursor.execute(genre_insert)
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
# print(result)

the_stand_isbn = 9781529370515
bt = read_full_book_record(the_stand_isbn)
print(bt)


def connect_to_database():
    try:
        conn = sqlite3.connect('bt.db')
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
        print(f"Database error: {error}")


def read_author_id(author_first_name, author_last_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query_author_id = ''' SELECT Author_ID FROM Authors
                              WHERE Author_First_Name = ? AND Author_Last_Name = ?                
                      '''
    cursor.execute(query_author_id, (author_first_name, author_last_name))
    author_id = cursor.fetchone()
    conn.close()

    return author_id

print(read_author_id('Stephen', 'King'))

def create_author(author_first_name, author_last_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_author = ''' INSERT INTO Authors (Author_ID, Author_First_Name, Author_Last_Name,
                                             Author_Full_Name, OpenLibrary_ID)
                        VALUES(NULL, ?, ?, ?, ?)
                    '''
    cursor.execute(insert_author, (author_first_name, author_last_name, author_first_name + author_last_name, None))
    conn.commit()

    cursor.execute("SELECT * FROM Authors")
    author_result = cursor.fetchall()

    conn.close()

    return author_result

test_author = create_author('Love', 'Man')
print(test_author)


def read_publisher_id(publisher_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query_publisher = ''' SELECT Publisher_ID FROM Publishers 
                          WHERE Publisher_Name = ?
                      '''
    criteria = (publisher_name,)
    cursor.execute(query_publisher, criteria)
    publisher_result = cursor.fetchone()
    conn.close()

    publisher_json = {"Publisher_ID": publisher_result[0]}

    return publisher_json

pub = 'Double Day'
test_publisher = read_publisher_id(pub)
print(test_publisher)

def create_publisher(publisher_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_publisher = ''' INSERT INTO Publishers(Publisher_ID, Publisher_Name)
                           Values(Null, ?)
                       '''
    criteria = (publisher_name,)
    cursor.execute(insert_publisher, criteria)
    conn.commit()
    conn.close()

    publisher_id = read_publisher_id(publisher_name)
    return publisher_id

test_create_publisher = create_publisher('hhhh')
print(test_create_publisher)


def read_genre_id_from_genre_table(genre):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query_genre_id = ''' SELECT Genre_ID FROM Genre
                         WHERE Genre = ?
                     '''
    criteria = (genre,)
    cursor.execute(query_genre_id, criteria)
    genre_id_result = cursor.fetchone()
    conn.close()

    genre_id_json = {"Genre_ID": genre_id_result[0]}

    return genre_id_json


test_genre_id = read_genre_id_from_genre_table('fiction')
print(test_genre_id)


def create_book_genre_table_record(isbn, genre_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_book_genre = ''' INSERT INTO BookGenre(ISBN, Genre_ID)
                            VALUES(?, ?)
                        '''
    criteria = (isbn, genre_id,)
    cursor.execute(insert_book_genre, criteria)
    conn.commit()

    query_book_genre = ''' SELECT ISBN, Genre_ID FROM BookGenre
                         WHERE ISBN = ? AND Genre_ID = ?
                     '''
    criteria = (isbn, genre_id,)
    cursor.execute(query_book_genre, criteria)
    book_genre_result = cursor.fetchone()
    conn.close()

    book_genre_json = {"ISBN": book_genre_result[0], "Genre_ID": book_genre_result[1]}
    return  book_genre_json

test_book_genre = create_book_genre_table_record(978152937515, 100)
print(test_book_genre)


def create_book_author_table_record(isbn, author_id):
    pass





