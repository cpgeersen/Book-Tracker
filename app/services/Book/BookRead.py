import sqlite3
import json

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
DB_PATH = "bt.db"


def connect_to_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        return cursor, conn
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.5.2.1 - read_book_table(ISBN) -> JSON
# Read Functionality for Book Table: return all records in table based on ISBN. Returns dictionary for JSON formatting.
def read_book_table(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Book Table for ISBN provided.
    read_query = "SELECT * FROM Books WHERE ISBN = ?"
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        convert_to_dict = {
            "ISBN": result[0][0],
            "Title": result[0][1],
            "Publish_Year": str(result[0][2]),
            "Publisher_ID": result[0][3],
            "Summary": result[0][4],
            "Tag_ID": result[0][5],
            "Chapters": str(result[0][6]),
            "Chapters_Completed": str(result[0][7]),
            "Cover_Image": result[0][8]
        }

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "ISBN not found" # Changed to json to make output consistent
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})


# 2.5.2.2 - read_author_id(ISBN) -> JSON
# Read Functionality for BookAuthor Table: return all records in table based on ISBN. Returns dictionary for JSON formatting.
def read_author_id(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query BookAuthor Table for ISBN provided.
    read_query = "SELECT Author_ID FROM BookAuthor WHERE ISBN = ?"
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Removes tuples inside the returned list. Convert to dictionary format for json.
        converted_list_result = [item for tup in result for item in tup]

        convert_to_dict = {"Author_IDs": []}

        count = 1
        for author_id in converted_list_result:
            convert_to_dict["Author_IDs"].append(author_id)
            count += 1
            if count > 2:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "ISBN not found" # Changed to json to make output consistent
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})


def read_author_id_from_name(author_first_name, author_last_name):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query_author_id = ''' SELECT Author_ID FROM Authors
                              WHERE Author_First_Name = ? AND Author_Last_Name = ?                
                      '''
    criteria = (author_first_name, author_last_name,)
    cursor.execute(query_author_id, criteria)
    author_id = cursor.fetchall()
    conn.close()

    if not author_id:
        author_id_json = {'Author_ID': ''}
    else:
        author_id_json = {'Author_ID': author_id[0][0]}

    return author_id_json


# 2.5.2.3 - read_author_name(author_ids_for_book) -> JSON
# Read Functionality for Author Table: return all author names in table based on AuthorIDs associated with an ISBN. Returns dictionary for JSON formatting.
def read_author_name(author_ids):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Generate the correct amount of search variables for query.
    convert_input_from_json = json.loads(author_ids)

    if convert_input_from_json.get('Error') == 'ISBN not found':
        conn.close()
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})

    criteria = convert_input_from_json["Author_IDs"]
    search_values = ','.join(['?'] * len(criteria))

    read_query = f"SELECT Author_ID, Author_First_Name, Author_Last_Name FROM Authors WHERE Author_ID IN ({search_values})"
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Convert results into dictionary.
        convert_to_dict = {}

        count = 1
        for item in result:
            key = item[0]
            values = list(item[1:])
            convert_to_dict[key] = values
            count += 1
            if count > 2:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "Author_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Author_ID not found", "Status_Code": "404"})


# Option 2 - Read Functionality for Author Table: return all values based on a book's ISBN. Returns dictionary for JSON formatting.
# This will pick up multiple authors associated with an ISBN.
def read_author_name_by_isbn(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query BookAuthor Table for ISBN provided. Joined with Author table to return AuthorID and author's first and last name.
    read_query = """
           SELECT A.Author_ID, A.Author_First_Name, A.Author_Last_Name
           FROM Authors AS A
           JOIN BookAuthor AS B ON A.Author_ID = B.Author_ID
           WHERE B.ISBN = ?
           """
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Create dictionary for JSON formatting.
        convert_to_dict = {}

        count = 1
        for item in result:
            key, value1, value2 = item
            convert_to_dict[key] = [value1, value2]
            count += 1
            if count > 2:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "ISBN not found" # Changed to json to make output consistent
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})


# 2.5.2.4 - read_publisher_name(publisher_id) -> JSON
# Read Functionality for Publishers Table: return publisher's name based on PublisherID. Returns dictionary for JSON formatting.
def read_publisher_name(publisher_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Publishers Table for PublisherID provided.
    read_query = "SELECT Publisher_Name FROM Publishers WHERE Publisher_ID = ?"
    criteria = (publisher_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        convert_to_dict = {
            publisher_id: result[0][0]
        }

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "Publisher_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Publisher_ID not found", "Status_Code": "404"})


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

    if publisher_result is None:
        publisher_result = ''
        publisher_json = {"Publisher_ID": publisher_result}
    else:
        publisher_json = {"Publisher_ID": publisher_result}

    return publisher_json


# 2.5.2.5 - read_tag_table(tag_id) -> JSON
# Read Functionality for Tags Table: return all records in table based on TagID. Returns dictionary for JSON formatting.
def read_tag_table(tag_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Tag Table for TagID provided.
    read_query = "SELECT Owned, Favorite, Completed, Currently_Reading, Personal_Or_Academic FROM Tags WHERE Tag_ID = ?"
    criteria = (tag_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:

        # Convert result to a dictionary for json formatting
        convert_to_dict = {
            "Owned": result[0][0],
            "Favorite": result[0][1],
            "Completed": result[0][2],
            "Currently_Reading": result[0][3],
            "Personal_Or_Academic": result[0][4],
        }

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "Tag_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Tag_ID not found", "Status_Code": "404"})


# 2.5.2.6 - read_genre_ids(ISBN) -> JSON
# Read Functionality for Genre Table: return genre category based on GenreID. Returns dictionary for JSON formatting.
# Limits result to up to 4 genres.
def read_genres_ids(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Genre Table for genreID provided.
    read_query = "SELECT Genre_ID FROM BookGenre WHERE ISBN = ?"
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:

        # Removes tuples inside the returned list. Convert to dictionary format for json.
        convert_tuples_result = [item for tup in result for item in tup]

        convert_to_dict = {"Genre_IDs": []}
        index_to_append = 0
        count = 1

        # Loop through converted result list and append values to dictionary list.
        for i in convert_tuples_result:
            convert_to_dict["Genre_IDs"].append(convert_tuples_result[index_to_append])
            index_to_append += 1
            count += 1
            if count > 4:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "ISBN not found" # Changed to json to make output consistent
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})


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

    if not genre_id_result:
        genre_id_json = {"Genre_ID": ''}
    else:
        genre_id_json = {"Genre_ID": genre_id_result[0]}

    return genre_id_json


# 2.5.2.7 - read_genres(genre_id) -> JSON
#  Read Functionality for Genre Table: return genre category based on GenreID. Returns dictionary for JSON formatting.
def read_genres(genre_ids):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Generate the correct amount of search variables for query.
    convert_input_from_json = json.loads(genre_ids)
    criteria = convert_input_from_json["Genre_IDs"]
    search_values = ','.join(['?'] * len(criteria))

    read_query = f"SELECT * FROM Genre WHERE Genre_ID IN ({search_values})"
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Convert results into dictionary.
        convert_to_dict = {}

        count = 1
        for item in result:
            key, value = item
            convert_to_dict[key] = value
            count += 1
            if count > 4:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "Genre_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Genre_ID not found", "Status_Code": "404"})


# Read functions to assist with creating full book record.

# Revised function for publisher name in order to have output match what is needed for reading full book record.
def read_publisher_name_for_full_book_record(publisher_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Publishers Table for PublisherID provided.
    read_query = "SELECT Publisher_Name FROM Publishers WHERE Publisher_ID = ?"
    criteria = (publisher_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        convert_to_dict = {
            "Publisher_Name": result[0][0]
        }

        json_format = json.dumps(convert_to_dict)
        return json_format
    else:
        #return "Publisher_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Publisher_ID not found", "Status_Code": "404"})


# Revised function for author name in order to have output match what is needed for reading full book record.
def read_author_name_by_isbn_full_record(isbn):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query BookAuthor Table for ISBN provided. Joined with Author table to return AuthorID and author's first and last name.
    read_query = """
           SELECT A.Author_ID, A.Author_First_Name, A.Author_Last_Name
           FROM Authors AS A
           JOIN BookAuthor AS B ON A.Author_ID = B.Author_ID
           WHERE B.ISBN = ?
           """
    criteria = (isbn,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Create dictionary for JSON formatting.
        convert_to_dict = {}

        count = 1

        for index, tup in enumerate(result):
            convert_to_dict[f"Author_ID_{index + 1}"] = tup[0]
            convert_to_dict[f"Author_First_Name_{index + 1}"] = tup[1]
            convert_to_dict[f"Author_Last_Name_{index + 1}"] = tup[2]
            count += 1
            if count > 2:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format

    else:
        #return "ISBN not found" # Changed to json to make output consistent
        return json.dumps({"Error": "ISBN not found", "Status_Code": "404"})


# Revised function for genre name in order to have output match what is needed for reading full book record.
def read_genres_for_full_book_record(genre_ids):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Generate the correct amount of search variables for query.
    convert_input_from_json = json.loads(genre_ids)
    criteria = convert_input_from_json["Genre_IDs"]

    search_values = ','.join(['?'] * len(criteria))

    read_query = f"SELECT * FROM Genre WHERE Genre_ID IN ({search_values})"
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:
        # Convert results into dictionary.
        convert_to_dict = {}

        count = 1

        for index, tup in enumerate(result):
            convert_to_dict[f"Genre_ID_{index + 1}"] = tup[0]
            convert_to_dict[f"Genre_{index + 1}"] = tup[1]

            count += 1
            if count > 4:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format

    else:
        #return "Genre_ID not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Genre_ID not found", "Status_Code": "404"})



# Returns full book record based on ISBN.
def read_full_book_record(isbn):
    # Return Book table records for ISBN.
    read_book_table_record = read_book_table(isbn)
    # print(read_book_table_record)
    converted_books = json.loads(read_book_table_record)

    # Return Author Names associated with ISBN.
    author_names = read_author_name_by_isbn_full_record(isbn)
    # print(author_names)
    converted_auth_names = json.loads(author_names)

    # Return Publisher name from an associated publisher ID in the Books record.
    if converted_books.get('Publisher_ID') is None:
        return json.dumps({"Error": "Publisher_ID not found", "Status_Code": "400"})
    publisher_id = converted_books["Publisher_ID"]
    book_publisher = read_publisher_name_for_full_book_record(publisher_id)
    converted_publisher = json.loads(book_publisher)

    # Return all tags associated with a book record.
    tag = converted_books["Tag_ID"]
    book_tags = read_tag_table(tag)
    converted_tags = json.loads(book_tags)

    # Return Genre IDs by ISBN.  Return values passed to Read_Genre_Names.
    read_genre_ids = read_genres_ids(isbn)

    # Return Genre Names by Genre IDs obtained through read_genre_IDs function for an ISBN.
    genre_names = read_genres_for_full_book_record(read_genre_ids)
    converted_genres = json.loads(genre_names)

    # Combine results for all functions to create full book record.
    read_full_book = converted_books | converted_auth_names | converted_publisher | converted_tags | converted_genres

    # Convert to JSON, printing the result "pretty".
    read_full_book_pretty = json.dumps(read_full_book, indent=4)

    return read_full_book_pretty


# Additional Functions that will be used later from the frontend


# Function needed for 2.11.1. Returns all ISBNs when searching by title. Return results in JSON formatting.
def read_isbn_by_title(title):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query Genre Table for genreID provided.
    read_query = "SELECT ISBN FROM Books WHERE Title LIKE ?"
    criteria = ('%'+title.strip()+'%',)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value found in table.
    if result:

        # Removes tuples inside the returned list. Convert to dictionary format for json.
        convert_tuples_result = [item for tup in result for item in tup]

        convert_to_dict = {"ISBN": []}
        index_to_append = 0
        count = 1

        # Loop through converted result list and append values to dictionary list.
        for i in convert_tuples_result:
            convert_to_dict["ISBN"].append(convert_tuples_result[index_to_append])
            index_to_append += 1
            count += 1
            if count > 2:
                break

        json_format = json.dumps(convert_to_dict)
        return json_format

    else:
        #return "Title not found" # Changed to json to make output consistent
        return json.dumps({"Error": "Title not found", "Status_Code": "404"})


# 2.11.1 - Read Book Record by Title function. Returns all book records based on title searching. Return results in JSON formatting.
def read_full_book_by_title(title):
    # Block searches for specific single words with potential for too many results.
    # Inserting a temporary block list.  Can be modified later as block list confirmed/refined.
    BLOCK_LIST = ['the', 'a', 'be', 'that', 'of', 'this', 'and', 'by']
    if title.lower().strip() in BLOCK_LIST:
        return json.dumps({"Error": "Unable to search by that title.", "Status_Code": "400"})

    # Query Book table for title matches.
    isbn_results = json.loads(read_isbn_by_title(title))

    if isbn_results.get('Error') == 'Title not found':
        return json.dumps({"Error": "Title not found", "Status_Code": "404"})

    # Convert isbn_results to python dictionary object for parsing.
    converted_isbn_results = isbn_results
    isbn_list = []
    for value in converted_isbn_results['ISBN']:
        isbn_list.append(value)

    # Create list of returned results and convert back to JSON formatting.
    all_results_list = []
    for result in isbn_list:
        get_book_json = (read_full_book_record(result))
        convert_book_json_to_dict = json.loads(get_book_json)
        all_results_list.append(convert_book_json_to_dict)

    json_format = json.dumps(all_results_list, indent=4)

    return json_format


# Function needed for 2.11.2. Returns all ISBNs when searching by author's name. Return results in JSON formatting.
def read_isbn_by_author(author_last_name, author_first_name=None):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    #read_query = "SELECT ISBN FROM Books WHERE Title LIKE ?"
    #criteria = ('%'+title.strip()+'%',)
    #cursor.execute(read_query, criteria)
    #result = cursor.fetchall()
    #conn.close()

    # Convert arguments into a list to determine search criteria.
    criteria = [value for value in (author_last_name, author_first_name) if value is not None]

    # Returns results when both author's last name and first name provided as search criteria.
    if len(criteria) == 2:
        last_name = criteria[0]
        first_name = criteria[1]
        read_query = f"SELECT B.ISBN FROM BookAuthor AS B JOIN Authors as A ON A.Author_ID = B.Author_ID WHERE A.Author_Last_Name LIKE ? AND A.Author_First_Name LIKE ?"
        cursor.execute(read_query, (last_name, first_name))
        result = cursor.fetchall()
        print(result)
        conn.close()

    # Returns results when author's last name provided as search criteria.
    else:
        last_name = criteria[0]
        read_query = f"SELECT B.ISBN FROM BookAuthor AS B JOIN Authors as A ON A.Author_ID = B.Author_ID WHERE A.Author_Last_Name LIKE ?"
        cursor.execute(read_query, (last_name,))
        result = cursor.fetchall()
        conn.close()

    # Check to confirm value(s) found in table.
    if result:
        # Removes tuples inside the returned list.
        convert_tuples_result = [item for tup in result for item in tup]

        # Loop through converted result list and append values to dictionary list. Convert to JSON formatting.
        convert_to_dict = {"ISBN": []}
        index_to_append = 0

        for i in convert_tuples_result:
            convert_to_dict["ISBN"].append(convert_tuples_result[index_to_append])
            index_to_append += 1

        json_format = json.dumps(convert_to_dict)
        return json_format

    else:
        #return "Author not found"
        return json.dumps({"Error": "Author not found", "Status_Code": "404"})


# 2.11.2 - Read Book Record(s) Based on Author. Returns all book records based on author's name. Return results in JSON formatting.
def read_full_book_by_author(author_last_name, author_first_name=None):
    # Obtain list of ISBNs associated with author.Author's last name is required as a parameter, first name is optional.
    isbn_results = read_isbn_by_author(author_last_name, author_first_name)

    # Convert isbn_results to python dictionary object for parsing.
    converted_isbn_results = json.loads(isbn_results)

    if converted_isbn_results.get('Error') == 'Author not found':
        return json.dumps({"Error": "Author not found", "Status_Code": "404"})

    isbn_list = []
    for value in converted_isbn_results['ISBN']:
        isbn_list.append(value)

    # Create list of returned results and convert back to JSON formatting.
    all_results_list = []
    for result in isbn_list:
        get_book_json = (read_full_book_record(result))
        convert_book_json_to_dict = json.loads(get_book_json)
        all_results_list.append(convert_book_json_to_dict)

    json_format = json.dumps(all_results_list, indent=4)

    return json_format


# Function needed for 2.11.3. Returns all ISBNs when searching by genre ID. Return results in JSON formatting.
def read_isbn_by_genre_id(genre_id):

    if len(str(genre_id)) == 0:
        return json.dumps({"Error": "Genre not found", "Status_Code": "404"})

    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    # Query BookGenre and Genre Tables for genreID provided to return ISBN.
    read_query = f"SELECT B.ISBN FROM BookGenre AS B JOIN Genre as G ON B.Genre_ID = G.Genre_ID WHERE G.Genre_ID = ?"
    criteria = (genre_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    # Check to confirm value(s) found in table.
    if result:
        # Removes tuples inside the returned list.
        convert_tuples_result = [item for tup in result for item in tup]

        # Loop through converted result list and append values to dictionary list. Convert to JSON formatting.
        convert_to_dict = {"ISBN": []}
        index_to_append = 0

        for i in convert_tuples_result:
            convert_to_dict["ISBN"].append(convert_tuples_result[index_to_append])
            index_to_append += 1

        json_format = json.dumps(convert_to_dict)
        return json_format

    else:
        #return "Genre not found"
        return json.dumps({"Error": "No books with genre", "Status_Code": "404"})


# 2.11.3 - Read Book Record(s) Based on Genre. Returns all book records based on genre ID. Return results in JSON formatting.
def read_full_book_by_genre_id(genre_id):

    if len(str(genre_id)) == 0:
        return json.dumps({"Error": "Genre not found", "Status_Code": "404"})

    # Obtain list of ISBNs associated with GenreID
    isbn_results = read_isbn_by_genre_id(genre_id)

    # Convert isbn_results to python dictionary object for parsing.
    converted_isbn_results = json.loads(isbn_results)

    if converted_isbn_results.get('Error') == 'No books with genre':
        return json.dumps({"Error": "No books with genre", "Status_Code": "404"})

    isbn_list = []
    for value in converted_isbn_results['ISBN']:
        isbn_list.append(value)

    # Create list of returned results and convert back to JSON formatting.
    all_results_list = []
    for result in isbn_list:
        get_book_json = (read_full_book_record(result))
        convert_book_json_to_dict = json.loads(get_book_json)
        all_results_list.append(convert_book_json_to_dict)

    json_format = json.dumps(all_results_list, indent=4)

    return json_format

def get_all_book_isbn():
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    query = "SELECT * FROM Books"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == '__main__':
    pass