import sqlite3
import json

from app.services.Book.BookRead import read_book_table, read_full_book_record

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

        # Query to find all occurrences of Author_IDs appearing in BookAuthor table more than once.
        authors_with_multiple_books = """
                                    SELECT *
                                    FROM BookAuthor
                                    WHERE Author_ID IN (
                                        SELECT Author_ID
                                        FROM BookAuthor
                                        GROUP BY Author_ID
                                        HAVING COUNT(*) > 1);
                                    """
        
        cursor.execute(authors_with_multiple_books)
        # cursor.execute(query)
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()

        print(result)

        if result:
            # Create dict to hold duplicates.
            de_duplicate_dict = {}

            # List to hold sublists for author ID, title, and ISBN, populated by items in returned results. 
            title_author_validation_list = []

            # Iterate through result dictionary and append values to title_author_validation list. 
            for item in result:
                auth_ID = item.get("Author_ID")
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


def de_duplicate_books_refactor():
    try:
        # Connect to SQLite database.
        conn = sqlite3.connect("bt.db")
        # Enable row factory functionality.
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query to find all occurrences of Author_IDs appearing in BookAuthor table more than once.
        authors_with_multiple_books = """
                                    SELECT *
                                    FROM BookAuthor
                                    WHERE Author_ID IN (
                                        SELECT Author_ID
                                        FROM BookAuthor
                                        GROUP BY Author_ID
                                        HAVING COUNT(*) > 1);
                                    """

        cursor.execute(authors_with_multiple_books)
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()

        # When there are authors with more than one book
        if result:

            # Temporary Dict that is used to slowly filter and construct the final output
            temp_dict = {}

            # Final json that will be returned
            json_output = {}

            # For each result, unpack the variables
            for item in result:
                author_id = item.get('Author_ID')
                isbn = item.get('ISBN')
                book_title = json.loads(read_book_table(isbn)).get('Title')

                # This can occur when a previously deleted duplicate has Author records
                if book_title is None:
                    continue

                # If the author_id not present in temp_dict, add it with book_title and isbn
                if author_id not in temp_dict.keys():
                    temp_dict.update({author_id : {book_title : [isbn]}})

                # When the author_id already in temp_dict
                else :
                    # When the book title for a given author_id is already present
                    # append the isbn to the isbn list
                    if temp_dict[author_id].get(book_title) is not None:
                        temp_dict[author_id][book_title].append(isbn)
                    # When the author_id is present but not the book title
                    else:
                        temp_dict[author_id][book_title] = [isbn]

            # Note: This can be streamlined but this works slightly better than previous implementation and puts the
            # json_output in a slightly easier format for the front
            # Now using the temp_dict, construct the final output adding only books with dupes
            # tuple used to filter repeats that can happen when books have multiple authors
            tuple_list = []
            dup_book_result_num = 1
            # Unpack the author_id and book_info in temp_dict
            for author_id, book_info in temp_dict.items():

                # Unpack the book_title and isbn_list in book_info
                for book_title, isbn_list in book_info.items():

                    # When the isbn_list has more than one result
                    if len(isbn_list) > 1:
                        # Then for each isbn in the isbn_list
                        # Get the book information and append to the added base key for the duplicate result
                        for isbn in isbn_list:
                            # Get information for given isbn
                            book_result = json.loads(read_full_book_record(isbn))
                            author_first_name_1 = book_result['Author_First_Name_1']
                            author_last_name_1 = book_result['Author_Last_Name_1']
                            author_first_name_2 = book_result.get('Author_First_Name_2')
                            author_last_name_2 = book_result.get('Author_Last_Name_2')

                            # Construct a new tuple entry to filter
                            book_tuple = (isbn, book_title, author_first_name_1, author_last_name_1, author_first_name_2, author_last_name_2)

                            # When a tuple combination is present, skip making a new entry
                            if book_tuple in tuple_list:
                                continue

                            tuple_list.append(book_tuple)

                            # Create entry as a duplicate result
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}'] = {'Title': book_title}
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}']['Author_First_Name_1'] = book_result['Author_First_Name_1']
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}']['Author_Last_Name_1'] = book_result['Author_Last_Name_1']
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}']['Author_First_Name_2'] = book_result.get('Author_First_Name_2')
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}']['Author_Last_Name_2'] = book_result.get('Author_Last_Name_2')
                            json_output[f'Duplicate_Book_Result_{dup_book_result_num}']['ISBNs'] = isbn_list

                        dup_book_result_num += 1

            return json_output

        return {'Error': 'No Results'}



    except sqlite3.Error as error:
        print(f"Database error: {error}")
        conn.close()