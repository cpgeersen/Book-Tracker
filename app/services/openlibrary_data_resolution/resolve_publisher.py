import sqlite3
from app.services.Book.BookCreate import create_publisher
from app.services.Book.BookRead import read_publisher_id

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


# Dummy function for now since Publishers.OpenLibrary_ID does not yet exist.
def is_publisher_olid_present(publisher_OLID):
    return False



# Resolves publisher OLID conflict case.
# Returns True if publisher record was updated with OL data.
# Returns False if no update was needed or not applicable.
def resolve_publisher_olid(publisher_olid, publisher_name):
    if not publisher_olid:
        return False

    is_publisher_olid = is_publisher_olid_present(publisher_olid)

    if is_publisher_olid:
        return False

    # OLID not present, so check if publisher name exists locally.
    publisher_id_json = read_publisher_id(publisher_name)

    # Existing create_complete_book.py format returns {"PublisherID": "..."} or {"PublisherID": ""}
    publisher_id = publisher_id_json.get("Publisher_ID", "")

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
                WHERE Publisher_ID = ?
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