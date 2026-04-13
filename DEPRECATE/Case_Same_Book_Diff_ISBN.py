import sqlite3
import json

"""
Code for Task 3.2.3 - Case: Same book different ISBN
"""
# Note - I did not include imports to the two full record read functions used as not sure where this will land in the structure of project. 

def de_duplicate_books():

    try:
        # Connect to SQLite database. 
        conn = sqlite3.connect("bt.db")
        #Enable row factory functionality.
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query to find all occurences of AuthorIDs appearing in BookAuthor table more than once. 
        authors_with_multiple_books = """
                                    SELECT *
                                    FROM BookAuthor
                                    WHERE AuthorID IN (
                                        SELECT AuthorID
                                        FROM BookAuthor
                                        GROUP BY AuthorID
                                        HAVING COUNT(*) > 1);
                                    """
        
        cursor.execute(authors_with_multiple_books)
        # cursor.execute(query)
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()

        if result:
            # Create dict to hold duplicates.
            de_duplicate_dict = {}

            # List to hold sublists for author ID, title, and ISBN, populated by items in returned results. 
            title_author_validation_list = []

            # Iterate through result dictionary and append values to title_author_validation list. 
            for item in result:
                auth_ID = item.get("AuthorID")
                search_isbn = item.get("ISBN")
                book_title = read_book_table(search_isbn)
                converted_book_title = json.loads(book_title)
                title_author_validation_list.append([auth_ID, converted_book_title["Title"], search_isbn])

            # Iterate through title_author_validation list and look for duplicate entries, matching on title and auth ID.  
            # If found, update title to indicate possible duplicate. This allows title to be added as key in final de_duplicate_dict.

            checked_pairs = {}
            for value in title_author_validation_list:
                pair = (value[0], value[1])
                checked_pairs[pair] = checked_pairs.get(pair, 0) + 1

                if checked_pairs[pair] > 1:
                    value[1] = f"{value[1]} (Possible Duplicate_{checked_pairs[pair] - 1})"


            # Iterate over title_author_validation_list and add values to dictionary. 
            # Uses isbn to locate full book record.  If not in nested list, added to dictionary. 
            for val1, val2, val3 in title_author_validation_list:
                aID = val1
                bTitle = val2
                isbn_num = val3
               
                if aID not in de_duplicate_dict:
                    de_duplicate_dict[aID] = {}
                
                if bTitle not in de_duplicate_dict[aID]:
                    de_duplicate_dict[aID][bTitle] = []
                
                book_result = read_full_book_record(isbn_num)
              
                converted_book_result = json.loads(book_result)

                if converted_book_result not in de_duplicate_dict[aID][bTitle]:
                    de_duplicate_dict[aID][bTitle].append(converted_book_result)

            # Convert de_duplicate_dict to json formatting.  Pretty print for easier readability. 
            json_converted_de_duplicate_dict =  json.dumps(de_duplicate_dict, indent=4)

            return json_converted_de_duplicate_dict 
        
        else:
            return "Unable to process"

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()
