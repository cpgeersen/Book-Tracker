import sqlite3
# This file contains Create functionality for book, author, publisher, and genre records

DB_PATH = "bt.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# Create Book record
def create_book(
    isbn: str,
    title: str,
    publish_date: str = None,
    publisher_id: int = None,
    summary: str = None,
    tag_id: int = None,
    chapters: int = None,
    chapters_completed: int = None,
    cover_image_bytes: bytes = None
):
    # Inserts a record into Books table.

    if not isbn or not title:
        return False, "ISBN and Title are required."

    if chapters is not None and chapters_completed is not None:
        if chapters_completed > chapters:
            return False, "Chapters_Completed cannot exceed Chapters."

    try:
        with _connect() as conn:
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM Books WHERE ISBN = ?", (isbn,))
            if cur.fetchone():
                return False, f"Book with ISBN {isbn} already exists."

            cur.execute(
                """
                INSERT INTO Books
                (ISBN, Title, PublishDate, PublisherID, Summary,
                 TagID, Chapters, Chapters_Completed, Cover_Image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    isbn,
                    title,
                    publish_date,
                    publisher_id,
                    summary,
                    tag_id,
                    chapters,
                    chapters_completed,
                    cover_image_bytes
                )
            )

            return True, f"Book {isbn} created successfully."

    except sqlite3.IntegrityError as e:
        return False, f"Integrity error (check foreign keys): {e}"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"



# Create author record

def create_author(first_name: str, last_name: str):
    # Inserts into Authors table if not already present.
    # Returns author_id.

    if not first_name or not last_name:
        return False, "Author first and last name required.", None

    try:
        with _connect() as conn:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT AuthorID FROM Authors
                WHERE LOWER(Author_First_Name) = LOWER(?)
                AND LOWER(Author_Last_Name) = LOWER(?)
                """,
                (first_name.strip(), last_name.strip())
            )
            existing = cur.fetchone()
            if existing:
                return True, "Author already exists.", existing[0]

            cur.execute(
                """
                INSERT INTO Authors (Author_First_Name, Author_Last_Name)
                VALUES (?, ?)
                """,
                (first_name.strip(), last_name.strip())
            )

            return True, "Author created successfully.", cur.lastrowid

    except sqlite3.Error as e:
        return False, f"Database error: {e}", None



# Create publisher record

def create_publisher(publisher_name: str):
    # Inserts into Publishers table if not already present.
    # Returns publisher_id.

    if not publisher_name:
        return False, "Publisher name required.", None

    try:
        with _connect() as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT PublisherID FROM Publishers WHERE LOWER(Publisher_Name) = LOWER(?)",
                (publisher_name.strip(),)
            )
            existing = cur.fetchone()
            if existing:
                return True, "Publisher already exists.", existing[0]

            cur.execute(
                "INSERT INTO Publishers (Publisher_Name) VALUES (?)",
                (publisher_name.strip(),)
            )

            return True, "Publisher created successfully.", cur.lastrowid

    except sqlite3.Error as e:
        return False, f"Database error: {e}", None



# Create genre record

def create_genre(genre_name: str):
    # Inserts into Genre table if not already present.
    # Returns genre_id.

    if not genre_name:
        return False, "Genre name required.", None

    try:
        with _connect() as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT GenreID FROM Genre WHERE LOWER(GENRE) = LOWER(?)",
                (genre_name.strip(),)
            )
            existing = cur.fetchone()
            if existing:
                return True, "Genre already exists.", existing[0]

            cur.execute(
                "INSERT INTO Genre (GENRE) VALUES (?)",
                (genre_name.strip(),)
            )

            return True, "Genre created successfully.", cur.lastrowid

    except sqlite3.Error as e:
        return False, f"Database error: {e}", None