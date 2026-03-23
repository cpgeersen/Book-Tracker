import sqlite3
import json

# Code contains functions 2.5.2 - Read Full Book Record (i.e. return all entries)

# Author: Holly Green

#2.5.2.1 - read_book_table(ISBN) -> JSON
# Read Functionality for Book Table: return all records in table based on ISBN. Returns dictionary for JSON formatting.
def read_book_table(ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Book Table for ISBN provided. 
        read_query = "SELECT * FROM Book WHERE ISBN = ?"
        criteria = (ISBN_value,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
            convert_to_dict = {
                "ISBN": result[0][0],
                "title": result[0][1],
                "publish_date": result[0][2],
                "publisher_id": result[0][3],
                "summary": result[0][4],
                "tag_id": result[0][5],
                "chapters": result[0][6],
                "chapters_completed": result[0][7],
                "cover_image_bytes": result[0][8]
            }

            json_format = json.dumps(convert_to_dict)
            return json_format
        else:
            return "ISBN not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.5.2.2 - read_author_id(ISBN) -> JSON
# Read Functionality for BookAuthor Table: return all records in table based on ISBN. Returns dictionary for JSON formatting.
def read_author_id(ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query BookAuthor Table for ISBN provided. 
        read_query = "SELECT AuthorID FROM BookAuthor WHERE ISBN = ?"
        criteria = (ISBN_value,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
            # Removes tuples inside the returned list. Convert to dictionary format for json. 
            converted_list_result = [item for tup in result for item in tup]

            convert_to_dict = {"AuthorIDs": []}

            count = 1
            for id in converted_list_result:
                convert_to_dict["AuthorIDs"].append(id)
                count += 1
                if count > 2:
                    break

            json_format = json.dumps(convert_to_dict)
            return json_format
        else:
            return "ISBN not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.5.2.3 - read_author_name(author_ids_for_book) -> JSON
# Read Functionality for Author Table: return all author names in table based on AuthorIDs associated with an ISBN. Returns dictionary for JSON formatting.

def read_auth_name(auth_IDs):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Generate the correct amount of search variables for query.
        convert_input_from_json = json.loads(auth_IDs)
        criteria = convert_input_from_json["AuthorIDs"]
        search_values =','.join(['?'] * len(criteria))
    
        read_query = f"SELECT AuthorID, Author_First_Name, Author_Last_Name FROM Author WHERE AuthorID IN ({search_values})"
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
            return "AuthorID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# Option 2 - Read Functionality for Author Table: return all values based on a book's ISBN. Returns dictionary for JSON formatting. 
# This will pick up multiple authors associated with an ISBN. 
def read_author_name_by_ISBN (ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query BookAuthor Table for ISBN provided. Joined with Author table to return AuthorID and author's first and last name. 
        read_query = """
        SELECT A.AuthorID, A.Author_First_Name, A.Author_Last_Name
        FROM Author AS A
        JOIN BookAuthor AS B ON A.AuthorID = B.AuthorID
        WHERE B.ISBN = ?
        """
        criteria = (ISBN_value,)
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
            return "ISBN not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()



# 2.5.2.4 - read_publisher_name(publisher_id) -> JSON
# Read Functionality for Publishers Table: return publisher's name based on PublisherID. Returns dictionary for JSON formatting.
def read_publisher_name (publisher_ID):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Publishers Table for PublisherID provided. 
        read_query = "SELECT Publisher_Name FROM Publishers WHERE PublisherID = ?"
        criteria = (publisher_ID,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
            convert_to_dict = {
                publisher_ID: result[0][0]
            }
            
            json_format = json.dumps(convert_to_dict)
            return json_format            
        else:
            return "PublisherID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.5.2.5 - read_tag_table(tag_id) -> JSON
# Read Functionality for Tags Table: return all records in table based on TagID. Returns dictionary for JSON formatting.
def read_tag_table(tag_ID):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Tag Table for TagID provided. 
        read_query = "SELECT Owned, Favorite, Completed, Currently_Reading, PersonalOrAcademic FROM Tags WHERE TagID = ?"
        criteria = (tag_ID,)
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
                "PersonalOrAcademic": result[0][4],
            }

            # Convert 0 or 1 boolean values to "Yes"/"No" or "Personal"/"Academic"
            if convert_to_dict["Owned"] == 0:
                convert_to_dict["Owned"] = "No"
            else:
                convert_to_dict["Owned"] = "Yes"

            if convert_to_dict["Favorite"] == 0:
                convert_to_dict["Favorite"] = "No"
            else:
                convert_to_dict["Favorite"] = "Yes"
            
            if convert_to_dict["Completed"] == 0:
                convert_to_dict["Completed"] = "No"
            else:
                convert_to_dict["Completed"] = "Yes"
            
            if convert_to_dict["Currently_Reading"] == 0:
                convert_to_dict["Currently_Reading"] = "No"
            else:
                convert_to_dict["Currently_Reading"] = "Yes"
            
            if convert_to_dict["PersonalOrAcademic"] == 0:
                convert_to_dict["PersonalOrAcademic"] = "Personal"
            else:
                convert_to_dict["PersonalOrAcademic"] = "Academic"
            
            json_format = json.dumps(convert_to_dict)
            return json_format
        else:
            return "TagID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()



# 2.5.2.6 - read_genre_ids(ISBN) -> JSON
# Read Functionality for Genre Table: return genre category based on GenreID. Returns dictionary for JSON formatting.
# Limits result to up to 4 genres. 
def read_genres_IDs(ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Genre Table for genreID provided. 
        read_query = "SELECT GenreID FROM BookGenre WHERE ISBN = ?"
        criteria = (ISBN_value,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:

           # Removes tuples inside the returned list. Convert to dictionary format for json. 
            convert_tuples_result = [item for tup in result for item in tup]


            convert_to_dict = {"GenreIDs": []}
            index_to_append = 0
            count = 1
            
            # Loop through converted result list and append values to dictionary list. 
            for i in convert_tuples_result:
                convert_to_dict["GenreIDs"].append(convert_tuples_result[index_to_append])
                index_to_append += 1
                count += 1
                if count > 4:
                    break

            json_format = json.dumps(convert_to_dict)
            return json_format
        else:
            return "ISBN not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()



# 2.5.2.7 - read_genres(genre_id) -> JSON
#  Read Functionality for Genre Table: return genre category based on GenreID. Returns dictionary for JSON formatting.
def read_genres (genre_IDs):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Generate the correct amount of search variables for query.
        convert_input_from_json = json.loads(genre_IDs)
        criteria = convert_input_from_json["GenreIDs"]
        search_values =','.join(['?'] * len(criteria))
    
        read_query = f"SELECT * FROM Genre WHERE GenreID IN ({search_values})"
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
            return "GenreID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# Read functions to assist with creating full book record. 

# Revised function for publisher name in order to have output match what is needed for reading full book record. 
def read_publisher_name_for_full_book_record (publisher_ID):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Publishers Table for PublisherID provided. 
        read_query = "SELECT Publisher_Name FROM Publishers WHERE PublisherID = ?"
        criteria = (publisher_ID,)
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
            return "PublisherID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# Revised function for author name in order to have output match what is needed for reading full book record. 
def read_author_name_by_ISBN_full_record (ISBN_value):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query BookAuthor Table for ISBN provided. Joined with Author table to return AuthorID and author's first and last name. 
        read_query = """
        SELECT A.AuthorID, A.Author_First_Name, A.Author_Last_Name
        FROM Author AS A
        JOIN BookAuthor AS B ON A.AuthorID = B.AuthorID
        WHERE B.ISBN = ?
        """
        criteria = (ISBN_value,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
            # Create dictionary for JSON formatting.
            convert_to_dict = {}

            count = 1

            for index, tup in enumerate(result):
                convert_to_dict[f"AuthorID_{index+1}"] = tup[0]
                convert_to_dict[f"Author_First_Name_{index+1}"] = tup[1]
                convert_to_dict[f"Author_Last_Name{index+1}"] = tup[2]
                count += 1
                if count > 2:
                    break
            
            json_format = json.dumps(convert_to_dict)
            return json_format
            
        else:
            return "ISBN not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# Revised function for genre name in order to have output match what is needed for reading full book record. 
def read_genres_for_full_book_record (genre_IDs):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Generate the correct amount of search variables for query.
        convert_input_from_json = json.loads(genre_IDs)
        criteria = convert_input_from_json["GenreIDs"]
    
        search_values =','.join(['?'] * len(criteria))
    
        read_query = f"SELECT * FROM Genre WHERE GenreID IN ({search_values})"
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
           # Convert results into dictionary.
            convert_to_dict = {}
            
            count = 1

            for index, tup in enumerate(result):
                convert_to_dict[f"GenreID_{index+1}"] = tup[0]
                convert_to_dict[f"Genre_{index+1}"] = tup[1]
           
                count += 1
                if count > 4:
                    break
            
            json_format = json.dumps(convert_to_dict)
            return json_format
   
        else:
            return "GenreID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()



# Returns full book record based on ISBN. 
def read_full_book_record (ISBN_value): 

    #Return Book table records for ISBN. 
    read_book_table_record = read_book_table(ISBN_value)
    converted_books = json.loads(read_book_table_record)

    # Return Author Names associated with ISBN. 
    author_names = read_author_name_by_ISBN_full_record(ISBN_value)
    converted_auth_names = json.loads(author_names)

    # Return Publisher name from an associated publisher ID in the Books record. 
    pub_ID = converted_books["publisher_id"]
    book_publisher = read_publisher_name_for_full_book_record(pub_ID)
    converted_publisher = json.loads(book_publisher)

    # Return all tags associated with a book record.
    tag = converted_books["tag_id"]
    book_tags = read_tag_table(tag)
    converted_tags = json.loads(book_tags)

    # Return Genre IDs by ISBN.  Return values passed to Read_Genre_Names.
    read_genIDs = read_genres_IDs(ISBN_value)

    # Return Genre Names by Genre IDs obtained through read_genre_IDs function for an ISBN. 
    genre_names = read_genres_for_full_book_record(read_genIDs)
    converted_genres = json.loads(genre_names)

   # Cobmine results for all functions to create full book record. 
    read_full_book = converted_books | converted_auth_names | converted_publisher | converted_tags | converted_genres

   # Convert to JSON, printing the result "pretty".
    read_full_book_pretty = json.dumps(read_full_book, indent=4)

    return read_full_book_pretty



# Function needed for 2.11.1. Returns all ISBNs when searching by title. Return results in JSON formatting. 
def read_isbn_by_title(title):
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Query Genre Table for genreID provided. 
        read_query = "SELECT ISBN FROM Book WHERE Title = ?"
        criteria = (title,)
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
            return "Title not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.11.1 - Read Book Record by Title function. Returns all book records based on title searching. Return results in JSON formatting. 
def read_full_book_by_title(title):

    # Block searches for specific single words with potential for too many results. 
    # Inserting a temporary block list.  Can be modified later as block list confirmed/refined.
    BLOCK_LIST = ['the', 'a', 'be', 'that', 'of', 'this', 'and']
    if title.lower().strip() in BLOCK_LIST:
        return "Unable to search by that title."
    
    # Query Book table for title matches. 
    isbn_results = read_isbn_by_title(title)

    # Convert isbn_results to python dictionary object for parsing. 
    converted_isbn_results = json.loads(isbn_results)
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
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        # Convert arguments into a list to determine search criteria. 
        criteria = [value for value in (author_last_name, author_first_name) if value is not None ]
        
        # Returns results when both author's last name and first name provided as search criteria.
        if len(criteria) == 2:
            last_name = criteria[0]
            first_name = criteria[1]
            read_query = f"SELECT B.ISBN FROM BookAuthor AS B JOIN Author as A ON A.AuthorID = B.AuthorID WHERE A.Author_Last_Name = ? AND A.Author_First_Name = ?"
            cursor.execute(read_query, (last_name, first_name))
            result = cursor.fetchall()
            conn.close()

        # Returns results when author's last name provided as search criteria.
        else:
            last_name = criteria[0]
            read_query = f"SELECT B.ISBN FROM BookAuthor AS B JOIN Author as A ON A.AuthorID = B.AuthorID WHERE A.Author_Last_Name = ?"
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
            return "Author not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.11.2 - Read Book Record(s) Based on Author. Returns all book records based on author's name. Return results in JSON formatting. 
def read_full_book_by_author(author_last_name, author_first_name=None):
    # Obtain list of ISBNs associated with author.Author's last name is required as a parameter, first name is optional. 
    isbn_results = read_isbn_by_author(author_last_name, author_first_name)

# Convert isbn_results to python dictionary object for parsing. 
    converted_isbn_results = json.loads(isbn_results)
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
    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()
        
        # Query BookGenre and Genre Tables for genreID provided to return ISBN. 
        read_query = f"SELECT B.ISBN FROM BookGenre AS B JOIN Genre as G ON B.GenreID = G.GenreID WHERE G.GenreID = ?"
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
            return "Genre not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()


# 2.11.3 - Read Book Record(s) Based on Genre. Returns all book records based on genre ID. Return results in JSON formatting. 
def read_full_book_by_genre_id(genreID):
    # Obtain list of ISBNs associated with GenreID
    isbn_results = read_isbn_by_genre_id(genreID)

# Convert isbn_results to python dictionary object for parsing. 
    converted_isbn_results = json.loads(isbn_results)
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
