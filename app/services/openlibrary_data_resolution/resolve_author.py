import sqlite3
from app.services.Book.BookCreate import create_author, create_book_author_table_record
from app.services.Book.BookRead import read_author_id_from_name

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


# Checks whether an Author OpenLibrary_ID is already present.
# Requires Authors.OpenLibrary_ID column to exist.
def is_author_olid_present(author_olid):

    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    read_query = "SELECT * FROM Authors WHERE OpenLibrary_ID = ?"
    criteria = (author_olid,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()
    conn.close()

    if len(result) == 0:
        return False
    else:
        return True


# Resolves author OLID conflict case.
# Returns True if author record was updated with OL data.
# Returns False if no update was needed or not applicable.
def resolve_author_olid(old_json_data, new_json_data, author_num):
    author_olid = new_json_data.get(f'Author_{author_num}_OLID')

    # Do not update author if there is no OLID
    if author_olid is None:
        return False

    # Check if OLID is already present in Authors table.
    is_author_olid = is_author_olid_present(author_olid)

    # Get old author information
    old_author_first_name = old_json_data.get(f'Author_First_Name_{author_num}')
    old_author_last_name = old_json_data.get(f'Author_Last_Name_{author_num}')
    old_author_id_json = read_author_id_from_name(old_author_first_name, old_author_last_name)

    # Get new author information
    new_author_full_name = new_json_data.get(f'Author_Full_Name_{author_num}')
    new_author_first_name = new_json_data.get(f'Author_First_Name_{author_num}')
    new_author_last_name = new_json_data.get(f'Author_Last_Name_{author_num}')
    new_author_id_json = read_author_id_from_name(new_author_first_name, new_author_last_name)

    # Existing create_complete_book.py format returns {"AuthorID": "..."} or {"AuthorID": ""}
    old_author_id = old_author_id_json.get("Author_ID", "")
    new_author_id = new_author_id_json.get("Author_ID", "")

    # This occurs when a user did not add a second author, but they exist
    if old_author_first_name is None:
        # When the author does not exist already, create the author records
        if old_author_id == '':
            # Create new author_id
            author_id_json = create_author(new_author_first_name, new_author_last_name, new_author_full_name)

            cursor, conn = connect_to_database()

            update_author = """ UPDATE Authors
                                SET OpenLibrary_ID = ?
                                WHERE Author_ID = ?
                            """
            update_info = (author_olid, old_author_id,)
            cursor.execute(update_author, update_info)
            conn.commit()
            conn.close()

            # Tie author_id to isbn
            # Returns True if successful
            return create_book_author_table_record(old_json_data['ISBN'], author_id_json['Author_ID'])

    # When author with olid exists as a different author record
    if is_author_olid and old_author_id != new_author_id:
        try:
            # Author already in database with olid
            cursor, conn = connect_to_database()

            update_author = """ UPDATE BookAuthor
                            SET Author_ID = ?
                            WHERE ISBN = ?
                        """
            update_info = (new_author_id, old_json_data['ISBN'],)
            cursor.execute(update_author, update_info)
            conn.commit()
            conn.close()

            # Chance that a misspelled author can be orphaned with no books tied to the record
            # This deletes an author that has no olid or books
            remove_orphan_author(old_author_id)

            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

    # When olid is not present in author table
    elif not is_author_olid:
        #Author exists locally but without OLID, so update destructively.
        # Get a cursor and connection to database
        cursor, conn = connect_to_database()

        update_author = """ UPDATE Authors
                            SET Author_Full_Name = ?,
                                Author_First_Name = ?,
                                Author_Last_Name = ?,
                                OpenLibrary_ID = ?
                            WHERE Author_ID = ?
                        """
        update_info = (new_author_full_name, new_author_first_name,
                       new_author_last_name, author_olid, old_author_id,)
        cursor.execute(update_author, update_info)
        conn.commit()
        conn.close()
        return True
    else:
        # When olid is present and matches the current old_author_id
        # Do not need to update
        return False


def remove_orphan_author(author_id):
    # Get a cursor and connection to database
    cursor, conn = connect_to_database()

    read_query = "SELECT * FROM BookAuthor WHERE Author_ID = ?"
    criteria = (author_id,)
    cursor.execute(read_query, criteria)
    result = cursor.fetchall()

    # No books have author so delete record
    if len(result) == 0:
        delete_author = """ DELETE FROM Authors
                            WHERE Author_ID = ?
                        """
        criteria = (author_id,)
        cursor.execute(delete_author, criteria)
        conn.commit()
        conn.close()
        return True
    else:
        # There are books still in database that have author
        conn.close()
        return False



        
