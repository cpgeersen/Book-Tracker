import sqlite3
from app.services.Book.BookRead import read_publisher_id, read_author_id_from_name, read_genre_id_from_genre_table
from app.services.Book.BookPredicate import is_isbn_in_book_table



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
            conn.close()



def create_tag(isbn, owned, favorite, completed, currently_reading, personal_or_academic):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_tag = ''' INSERT INTO Tags (Tag_ID, Owned, Favorite, Completed,
                                      Currently_Reading, Personal_Or_Academic, ISBN)
                     VALUES(NULL, ?, ?, ?, ?, ?, ?)
    '''
    criteria = (owned, favorite, completed, currently_reading, personal_or_academic, isbn,)
    cursor.execute(insert_tag, criteria)
    conn.commit()

    read_query = "SELECT Tag_ID FROM Tags WHERE ISBN = ?"
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    tag_result = cursor.fetchone()

    conn.close()

    tag_json = {"Tag_ID": tag_result[0]}
    return tag_json


def create_book_author_table_record(isbn, author_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query_book_author = ''' SELECT * FROM BookAuthor
                            WHERE ISBN = ? AND Author_ID = ?
                        '''
    cursor.execute(query_book_author, (isbn, author_id))
    record_combo_present = cursor.fetchall()

    if record_combo_present:
        conn.close()
        return False
    else:
        insert_book_author = ''' INSERT INTO BookAuthor (ISBN, Author_ID)
                                 VALUES(?, ?)
                             '''
        criteria = (isbn, author_id)
        cursor.execute(insert_book_author, criteria)
        conn.commit()
        conn.close()
        return True


def create_author(author_first_name, author_last_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_author = ''' INSERT INTO Authors (Author_ID, Author_First_Name, Author_Last_Name,
                                             Author_Full_Name, OpenLibrary_ID)
                        VALUES(NULL, ?, ?, ?, ?)
                    '''
    cursor.execute(insert_author, (author_first_name, author_last_name, author_first_name + ' ' + author_last_name, 'OLID_TEMP'))
    conn.commit()

    query_author = ''' SELECT Author_ID FROM Authors WHERE
                       Author_First_Name = ? AND Author_Last_Name = ?
                   '''
    criteria = (author_first_name, author_last_name)
    cursor.execute(query_author, criteria)
    author_result = cursor.fetchall()
    conn.close()

    author_result_json = {'Author_ID': author_result[0][0]}

    return author_result_json


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


def create_book_genre_table_record(isbn, genre_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    genre_id_unpack = genre_id['Genre_ID']
    query_book_genre = ''' SELECT ISBN, Genre_ID FROM BookGenre
                             WHERE ISBN = ? AND Genre_ID = ?
                         '''
    criteria = (isbn, genre_id_unpack,)
    cursor.execute(query_book_genre, criteria)
    book_genre_result = cursor.fetchone()

    if book_genre_result:
        conn.close()
        return False
    else:
        insert_book_genre = ''' INSERT INTO BookGenre(ISBN, Genre_ID)
                                VALUES(?, ?)
                            '''
        criteria = (isbn, genre_id_unpack,)
        cursor.execute(insert_book_genre, criteria)
        conn.commit()
        conn.close()
        return True

def create_book(isbn, title, publish_year, publisher_id, summary, tag_id,
                chapters, chapters_completed, cover_image):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    insert_book = ''' INSERT INTO Books(ISBN, Title, Publish_Year, Publisher_ID, Summary,
                                        Tag_ID, Chapters, Chapters_Completed, Cover_Image)
                      VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                  '''

    # Note from Collin: Bad fix, will refactor later
    if type(publisher_id) == dict:
        publisher_id_unpack = publisher_id['Publisher_ID'][0]
    else:
        publisher_id_unpack = publisher_id[0]

    criteria = (isbn, title, publish_year, publisher_id_unpack, summary, tag_id, chapters, chapters_completed, cover_image,)
    cursor.execute(insert_book, criteria)
    conn.commit()
    conn.close()
    return True

def create_book_record(json):
    # All required values have been validated by mediator at this point
    # All variables that use get() method have a default value of '', since they are optional for creation

    isbn = json['ISBN']

    # First make sure ISBN not present in Book Table
    is_isbn_present = is_isbn_in_book_table(isbn)

    try:
        if is_isbn_present:
            return 'Error: Book with ISBN present.', BAD_REQUEST
    except:
        raise INTERNAL_SERVER_ERROR

    # Book Info
    title = json['Title']
    summary = json.get('Summary', '')
    chapters = json.get('Chapters', '')
    chapters_completed = json.get('Chapters_Completed', '')

    # Primary Author
    author_first_name_1 = json['Author_First_Name_1']
    author_last_name_1 = json['Author_Last_Name_1']

    # Secondary Author
    author_first_name_2 = json.get('Author_First_Name_2', '')
    author_last_name_2 = json.get('Author_First_Name_2', '')

    # Publisher Information
    publisher_name = json['Publisher_Name']
    publish_year = json['Publish_Year']

    # Tags
    owned = json['Owned']
    favorite = json['Favorite']
    completed = json['Completed']
    currently_reading = json['Currently_Reading']
    personal_or_academic = json['Personal_Or_Academic']

    # Genre
    genre_1 = json['Genre_1']
    genre_2 = json.get('Genre_2', '')
    genre_3 = json.get('Genre_3', '')
    genre_4 = json.get('Genre_4', '')

    # Cover Image
    cover_image = json.get('Cover_Image', '')

    # Next create the new tag record and return the new tag_id
    tag_response = create_tag(isbn, owned, favorite, completed, currently_reading, personal_or_academic)
    try:
        if tag_response.get('Tag_ID', 'No_Tag') != 'No_Tag':
            tag_id = tag_response['Tag_ID']
        else:
            return 'Error: No Tag Present', BAD_REQUEST
    except:
        raise INTERNAL_SERVER_ERROR

    # Next check if Author_ID is present based on Author Name in Author Table
    try:
        author_1_response = read_author_id_from_name(author_first_name_1, author_last_name_1)

        if not author_1_response:
            return 'Error: No Author', BAD_REQUEST

        # We do author_1 first since there is always at least one author
        if author_1_response['Author_ID']:
            # Here we use existing author_id and add a new record to the BookAuthor bridging table
            author_id_1 = author_1_response['Author_ID']
            create_book_author_table_record(isbn, author_id_1)
        else:
            # Otherwise we first create a new author_id
            author_id_1 = create_author(author_first_name_1, author_last_name_1)
            create_book_author_table_record(isbn, author_id_1['Author_ID'])
    except:
        raise INTERNAL_SERVER_ERROR

    # Then we do author_2 if present
    if author_first_name_2 != '':
        author_2_response = read_author_id_from_name(author_first_name_2, author_last_name_2)

        if author_2_response['Author_ID']:
            author_id_2 = author_2_response['Author_ID']
            create_book_author_table_record(isbn, author_id_2)
        else:
            author_id_2 = create_author(author_first_name_2, author_last_name_2)
            create_book_author_table_record(isbn, author_id_2['Author_ID'])

    # Next we read or create publisher_id from publisher_name
    try:
        publisher_response = read_publisher_id(publisher_name)

        if not publisher_response:
            return 'Error: No Publisher', BAD_REQUEST

        if publisher_response['Publisher_ID']:
            publisher_id = publisher_response['Publisher_ID']
        else:
            publisher_id = create_publisher(publisher_name)
    except:
        raise INTERNAL_SERVER_ERROR

    # Next we get the genre_id from the Genre Table using the genres
    genre_id_1 = read_genre_id_from_genre_table(genre_1)

    # Create the record for the BookGenre bridging table
    try:
        genre_response_1 = create_book_genre_table_record(isbn, genre_id_1)

        if not genre_response_1:
            return 'Error: No Genre', BAD_REQUEST

        if genre_2 != '':
            genre_id_2 = read_genre_id_from_genre_table(genre_2)
            genre_response_2 = create_book_genre_table_record(isbn, genre_id_2)

        if genre_3 != '':
            genre_id_3 = read_genre_id_from_genre_table(genre_3)
            genre_response_3 = create_book_genre_table_record(isbn, genre_id_3)

        if genre_4 != '':
            genre_id_4 = read_genre_id_from_genre_table(genre_4)
            genre_response_4 = create_book_genre_table_record(isbn, genre_id_4)
    except:
        raise INTERNAL_SERVER_ERROR

    # Finally we create the Book Table Record
    create_book_response = create_book(isbn, title, publish_year, publisher_id, summary, tag_id,
                                       chapters, chapters_completed, cover_image)
    if not create_book_response:
        return 'Error: Book Present in Database', BAD_REQUEST
    else:
        return 'Successfully Created New Book Record', SUCCESS


if __name__ == '__main__':
    pass




















