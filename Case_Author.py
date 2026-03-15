import sqlite3

# Checks whether an Author OpenLibrary_ID is already present.
# Requires Authors.OpenLibrary_ID column to exist.
def is_author_OLID_present(author_OLID):
    try:
        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        read_query = "SELECT * FROM Authors WHERE OpenLibrary_ID = ?"
        criteria = (author_OLID,)
        cursor.execute(read_query, criteria)
        result = cursor.fetchall()

        conn.close()

        if len(result) == 0:
            return False
        else:
            return True

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        try:
            conn.close()
        except:
            pass
        return False


# Dummy function for now since Publishers.OpenLibrary_ID does not yet exist.
def is_publisher_OLID_present(publisher_OLID):
    return False


# Resolves author OLID conflict case.
# Returns True if author record was updated with OL data.
# Returns False if no update was needed or not applicable.
def resolve_author_OLID(author_OLID, author_first_name, author_last_name):
    if not author_OLID:
        return False

    # Check if OLID is already present in Authors table.
    is_author_olid = is_author_OLID_present(author_OLID)

    if is_author_olid:
        return False

    # OLID not present, so check if author name is already present locally.
    author_id_json = read_author_id(author_first_name, author_last_name)

    # Existing create_complete_book.py format returns {"AuthorID": "..."} or {"AuthorID": ""}
    author_id = author_id_json.get("AuthorID", "")

    if not author_id:
        # Author not present locally, so create it.
        # OLID parameter can be added later when schema is updated.
        create_author(author_first_name, author_last_name)
        return False

    else:
        # Author exists locally but without OLID, so update destructively.
        try:
            conn = sqlite3.connect("bt.db")
            cursor = conn.cursor()

            update_author = """
                UPDATE Authors
                SET Author_First_Name = ?,
                    Author_Last_Name = ?
                WHERE AuthorID = ?
            """

            update_info = (author_first_name, author_last_name, author_id)
            cursor.execute(update_author, update_info)
            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            try:
                conn.close()
            except:
                pass
            return False


# Resolves publisher OLID conflict case.
# Returns True if publisher record was updated with OL data.
# Returns False if no update was needed or not applicable.
def resolve_publisher_OLID(publisher_OLID, publisher_name):
    if not publisher_OLID:
        return False

    is_publisher_olid = is_publisher_OLID_present(publisher_OLID)

    if is_publisher_olid:
        return False

    # OLID not present, so check if publisher name exists locally.
    publisher_id_json = read_publisher_id(publisher_name)

    # Existing create_complete_book.py format returns {"PublisherID": "..."} or {"PublisherID": ""}
    publisher_id = publisher_id_json.get("PublisherID", "")

    if not publisher_id:
        # Publisher not present locally, so create it.
        # OLID parameter can be added later when schema is updated.
        create_publisher(publisher_name)
        return False

    else:
        # Publisher exists locally but without OLID, so update destructively.
        try:
            conn = sqlite3.connect("bt.db")
            cursor = conn.cursor()

            update_publisher = """
                UPDATE Publishers
                SET Publisher_Name = ?
                WHERE PublisherID = ?
            """

            update_info = (publisher_name, publisher_id)
            cursor.execute(update_publisher, update_info)
            conn.commit()
            conn.close()

            return True

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            try:
                conn.close()
            except:
                pass
            return False
        
