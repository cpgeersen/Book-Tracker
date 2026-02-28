import argparse
import sqlite3

DB_PATH = "bt.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

#-------------------------------------------------------------------------
# B. Matching the recognized Genres
#-------------------------------------------------------------------------
def lookup_genre_in_ddsys(conn, genre_name: str):
    cur = conn.cursor()

    cur.execute(
        "SELECT Class_Desc FROM DD_Sys WHERE LOWER(Class_Desc) = LOWER(?)",
        (genre_name,)
    )
    row = cur.fetchone()

    if row:
        return row[0]  # Return the matched description

    return None

#--------------------------------------------------------------
# C. Adding The Recognized Genre to the Genre Table
#--------------------------------------------------------------
def _get_or_create_genre(conn, genre_desc: str) -> int:
    cur = conn.cursor()

    # Check if genre already exists
    cur.execute(
        "SELECT GenreID FROM Genre WHERE GENRE = ?",
        (genre_desc,)
    )
    row = cur.fetchone()

    if row:
        return row[0]

    # Insert new genre
    cur.execute(
        "INSERT INTO Genre (GENRE) VALUES (?)",
        (genre_desc,)
    )
    return cur.lastrowid

#-------------------------------------------------------------
# D. Link Genre to a Book In Book Genre
#-------------------------------------------------------------
def link_genre_to_book(conn, isbn: str, genre_id: int):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO BookGenre (ISBN, GenreID)
        VALUES (?, ?)
        """,
        (isbn, genre_id)
    )

#--------------------------------------------------------------
# E. Combined Function Call
#--------------------------------------------------------------
def process_book_genres(conn, isbn: str, genre_string: str):
    cur = conn.cursor()

    # 1. Split into individual genres
    genres = split_multiple_genres(genre_string)

    for genre_name in genres:

        # 2. Match against DD_Sys
        matched_desc = lookup_genre_in_ddsys(conn, genre_name)

        if not matched_desc:
            # Skip or handle unmatched genres
            # You can also choose to insert unmatched genres directly
            continue

        # 3. Create or reuse genre in Genre table
        genre_id = _get_or_create_genre(conn, matched_desc)

        # 4. Link to BookGenre
        link_genre_to_book(conn, isbn, genre_id)

#================================================================
# II. Process Book Author Function.
#================================================================
#----------------------------------------------------------------
# A. Detecting Exceptions.
#----------------------------------------------------------------
def is_corporate_author(name: str) -> bool:
    corporate_keywords = [
        "department", "society", "association", "committee", "university",
        "institute", "corporation", "corp", "press", "agency", "organization",
        "office", "council", "ministry", "board", "commission", "center",
        "centre", "foundation", "company", "co.", "group"
    ]

    lower = name.lower()

    # Keyword detection
    if any(word in lower for word in corporate_keywords):
        return True

    # Single-word uppercase (NASA, UNICEF)
    if name.isupper() and " " not in name:
        return True

    # Very long names are usually corporate
    if len(name.split()) > 3:
        return True

    return False
    
#--------------------------------------------------------
# B. Multiple Author Name Splitter Functions. 
#--------------------------------------------------------
import re

def split_multiple_authors(authors_string: str):
    # Normalize separators to semicolons
    cleaned = re.sub(r'\s+(and|&|\+)\s+', ';', authors_string, flags=re.IGNORECASE)
    cleaned = cleaned.replace(",", ";")

    # Split on semicolons
    parts = [a.strip() for a in cleaned.split(";") if a.strip()]

    return parts

#------------------------------------------------------------
# C. First/Last Name Splitter Function.
#------------------------------------------------------------
def split_author_name(full_name: str):
    parts = full_name.strip().split()

    if len(parts) == 1:
        return parts[0], ""

    last_name = parts[-1]
    first_name = " ".join(parts[:-1])
    return first_name, last_name

#-----------------------------------------------------------
# D. Create Author ISBN Association in Authors table. 
#-----------------------------------------------------------
def _get_or_create_author(conn, full_name: str) -> int:
    cur = conn.cursor()

    # Detect corporate author
    if is_corporate_author(full_name):
        first_name = full_name
        last_name = ""
    else:
        first_name, last_name = split_author_name(full_name)

    # Check if author exists
    cur.execute(
        """
        SELECT AuthorID FROM Authors
        WHERE Author_First_Name = ? AND Author_Last_Name = ?
        """,
        (first_name, last_name)
    )
    row = cur.fetchone()

    if row:
        return row[0]

    # Create new author (supports schemas with/without Author_Full_Name)
    cur.execute("PRAGMA table_info(Authors)")
    author_columns = {row[1] for row in cur.fetchall()}

    if "Author_Full_Name" in author_columns:
        cur.execute(
            """
            INSERT INTO Authors (Author_Full_Name, Author_First_Name, Author_Last_Name)
            VALUES (?, ?, ?)
            """,
            (full_name, first_name, last_name)
        )
    else:
        cur.execute(
            """
            INSERT INTO Authors (Author_First_Name, Author_Last_Name)
            VALUES (?, ?)
            """,
            (first_name, last_name)
        )
    return cur.lastrowid

#------------------------------------------------------------------------
# E. Author and AuthorID in BookAuthors Table.
#------------------------------------------------------------------------
# authors_string comes from your ISBN lookup
def process_book_authors(conn, isbn: str, authors_string: str):
    cur = conn.cursor()

    # 1. Split into individual authors
    authors_list = split_multiple_authors(authors_string)

    # 2. Process each author
    for full_author_name in authors_list:
        # Create or reuse author
        author_id = _get_or_create_author(conn, full_author_name)

        # 3. Link book ↔ author
        cur.execute(
            """
            INSERT OR IGNORE INTO BookAuthor (ISBN, AuthorID)
            VALUES (?, ?)
            """,
            (isbn, author_id)
        )

#===============================================================
# III. Complete Book Addition Function.
#===============================================================
#---------------------------------------------------------------
# A. Check for other Books by the same Publisher.
#---------------------------------------------------------------
def get_publisher_book_count(conn, publisher_name: str) -> int:
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM Books b
        JOIN Publishers p ON b.PublisherID = p.PublisherID
        WHERE LOWER(p.Publisher_Name) = LOWER(?)
    """, (publisher_name.strip(),))
    count = cur.fetchone()[0]
    return count


#---------------------------------------------------------------
# B. Check for other Books by the same Author.
#---------------------------------------------------------------
def get_author_book_counts(conn, authors_string: str):
    results = {}
    authors = split_multiple_authors(authors_string)

    for full_name in authors:
        first, last = split_author_name(full_name)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM Books b
            JOIN BookAuthor ba ON b.ISBN = ba.ISBN
            JOIN Authors a ON ba.AuthorID = a.AuthorID
            WHERE LOWER(a.Author_First_Name) = LOWER(?)
              AND LOWER(a.Author_Last_Name) = LOWER(?)
        """, (first, last))
        results[full_name] = cur.fetchone()[0]

    return results

#--------------------------------------------------------------
# C. Try Book Addition.
#--------------------------------------------------------------
def create_full_book_entry(
    isbn: str,
    title: str,
    publish_date: str,
    publisher_name: str,
    authors_string: str,
    genre_string: str,
    summary: str = None,
    tag_id: int = None,
    chapters: int = None,
    chapters_completed: int = None,
    cover_image_bytes: bytes = None
):
    try:
        with _connect() as conn:
            cur = conn.cursor()

            # -----------------------------------------------------------
            # A. Check if the Book Already Exists
            # -----------------------------------------------------------
            cur.execute("SELECT 1 FROM Books WHERE ISBN = ?", (isbn,))
            if cur.fetchone():
                return False, f"Book with ISBN {isbn} already exists."

            # -----------------------------------------------------------
            # B. Gather informational warnings (not blockers)
            # -----------------------------------------------------------
            publisher_book_count = get_publisher_book_count(conn, publisher_name)
            author_book_counts = get_author_book_counts(conn, authors_string)

            # -----------------------------------------------------------
            # 1. Publisher (Get or Create)
            # -----------------------------------------------------------
            cur.execute(
                "SELECT PublisherID FROM Publishers WHERE LOWER(Publisher_Name) = LOWER(?)",
                (publisher_name.strip(),)
            )
            row = cur.fetchone()

            if row:
                publisher_id = row[0]
            else:
                cur.execute(
                    "INSERT INTO Publishers (Publisher_Name) VALUES (?)",
                    (publisher_name.strip(),)
                )
                publisher_id = cur.lastrowid

            # -----------------------------------------------------------
            # 2. Insert Book
            # -----------------------------------------------------------
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

            # -----------------------------------------------------------
            # 3. Authors
            # -----------------------------------------------------------
            process_book_authors(conn, isbn, authors_string)

            # -----------------------------------------------------------
            # 4. Genres
            # -----------------------------------------------------------
            process_book_genres(conn, isbn, genre_string)

            # -----------------------------------------------------------
            # Return success + informational messages
            # -----------------------------------------------------------
            info = {
                "publisher_books_already_in_db": publisher_book_count,
                "author_books_already_in_db": author_book_counts
            }

            return True, info

    except sqlite3.IntegrityError as e:
        return False, f"Integrity error: {e}"
    except sqlite3.Error as e:
        return False, f"Database error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Create a complete book record using ISBN metadata.")
    parser.add_argument("isbn", help="Book ISBN")
    parser.add_argument("title", help="Book title")
    parser.add_argument("publisher", help="Publisher name")
    parser.add_argument("authors", help="Author(s), separated by ';', ',', 'and', '&', or '+'")
    parser.add_argument("genres", help="Genre(s), separated by ';', ',', 'and', '&', or '+'")
    parser.add_argument("--publish-date", dest="publish_date", default=None, help="Publish date (YYYY-MM-DD)")
    parser.add_argument("--summary", default=None, help="Book summary")
    parser.add_argument("--tag-id", dest="tag_id", type=int, default=None, help="Optional tag id")
    parser.add_argument("--chapters", type=int, default=None, help="Total chapter count")
    parser.add_argument("--chapters-completed", dest="chapters_completed", type=int, default=None, help="Completed chapters")

    args = parser.parse_args()

    success, result = create_full_book_entry(
        isbn=args.isbn,
        title=args.title,
        publish_date=args.publish_date,
        publisher_name=args.publisher,
        authors_string=args.authors,
        genre_string=args.genres,
        summary=args.summary,
        tag_id=args.tag_id,
        chapters=args.chapters,
        chapters_completed=args.chapters_completed,
        cover_image_bytes=None,
    )

    if success:
        print("Book created successfully.")
        print(result)
    else:
        print("Book creation failed.")
        print(result)


if __name__ == "__main__":
    main()