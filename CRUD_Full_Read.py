import sqlite3

# Code contains functions 2.5.2 - Read Full Book Record (i.e. return all entries)

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
            return convert_to_dict
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

            for id in converted_list_result:
                convert_to_dict["AuthorIDs"].append(id)
              
            return convert_to_dict
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
        criteria = auth_IDs["AuthorIDs"]
        search_values =','.join(['?'] * len(criteria))
    
        read_query = f"SELECT * FROM Author WHERE AuthorID IN ({search_values})"
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
           # Convert results into dictionary.
            convert_to_dict = {}

            for item in result:
                key = item[0]
                values = list(item[1:])
                convert_to_dict[key] = values
                
            return convert_to_dict
        
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

            for item in result:
                key, value1, value2 = item
                convert_to_dict[key] = [value1, value2]
              
            return convert_to_dict
            
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
            return convert_to_dict
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
            
            return convert_to_dict
        
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

            return convert_to_dict
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
        criteria = genre_IDs["GenreIDs"]
        search_values =','.join(['?'] * len(criteria))
    
        read_query = f"SELECT * FROM Genre WHERE GenreID IN ({search_values})"
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()
        conn.close()

        # Check to confirm value found in table.
        if result:
           # Convert results into dictionary.
            convert_to_dict = {}

            for item in result:
                key, value = item
                convert_to_dict[key] = value

            return convert_to_dict
        
        else:
            return "GenreID not found"
        
    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()
