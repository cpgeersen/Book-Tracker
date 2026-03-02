#================================================================
# I. Process Genre Function.
#================================================================
#----------------------------------------------------------------
# Creating a JSON wrapper function to allow data entry:
#----------------------------------------------------------------
import argparse
import json
import os
import random
import re
import sqlite3
import string
from difflib import SequenceMatcher
from datetime import date, timedelta

# Defining the Json wrapper. 
def json_wrapper(func): 
    def wrapped(json_input):
        try:
            data = json.loads(json_input) # Take a single JSON object, unpack its keys, and pass them as keyword arguments.  

            if not isinstance(data, dict):
                raise ValueError("JSON input must be an object mapping to function arguments")
    # Wrapper calls the function **data.
            return func(**data)   # <-- unpack JSON keys into function parameters
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")
    return wrapped

# your DB logic here
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
#----------------------------------------------------------------
# A. Splitting a List of Genres.
#
# I have Created another file that doesn't use the DD_Sys 
# The other file should include the simple program as specified by the PM
#----------------------------------------------------------------
import argparse
import re
import sqlite3
from difflib import SequenceMatcher
from genre_defaults import seed_default_genres

DB_PATH = "bt.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
# This is a Genre Process Method and doesn't need to be used.
# I have Created another file that doesn't use the DD_Sys 
# The other file should include the simple program as specified by the PM
def split_multiple_genres(genre_string: str):
    cleaned = re.sub(r'\s+(and|&|\+)\s+', ';', genre_string, flags=re.IGNORECASE)
    cleaned = cleaned.replace(",", ";")

    parts = [g.strip() for g in cleaned.split(";") if g.strip()]
    return parts

#-------------------------------------------------------------------------
# B. Matching the recognized Genres
#-------------------------------------------------------------------------
# This is a genre process method and doesn't need to be used.
def _matching_character_score(left: str, right: str) -> int:
    left_clean = re.sub(r"[^a-z0-9]", "", left.lower())
    right_clean = re.sub(r"[^a-z0-9]", "", right.lower())

    if not left_clean or not right_clean:
        return 0

    matcher = SequenceMatcher(None, left_clean, right_clean)
    return max((block.size for block in matcher.get_matching_blocks()), default=0)


def lookup_genre_in_ddsys(conn, genre_name: str):
    cur = conn.cursor()

    cur.execute("SELECT Class_Desc FROM DD_Sys")
    rows = cur.fetchall()

    best_match = None
    best_score = 0

    for row in rows:
        class_desc = row[0]
        score = _matching_character_score(genre_name, class_desc)
        if score > best_score:
            best_score = score
            best_match = class_desc

    if best_score >= 3:
        return best_match  # Return the best matched description

    return None


def _prompt_fiction_or_nonfiction() -> str:
    while True:
        user_choice = input("Is this genre Fiction or Non-Fiction? [f/n]: ").strip().lower()
        if user_choice in ("f", "fiction"):
            return "fiction"
        if user_choice in ("n", "non-fiction", "nonfiction"):
            return "non-fiction"
        print("Invalid choice. Please enter 'f' for Fiction or 'n' for Non-Fiction.")


#--------------------------------------------------------------
# C. Adding The Recognized Genre to the Genre Table
#--------------------------------------------------------------
def _get_or_create_genre(conn, genre_desc: str) -> int:
    cur = conn.cursor()

    normalized_genre = genre_desc.strip()

    # Check if genre already exists
    cur.execute(
        "SELECT GenreID FROM Genre WHERE LOWER(TRIM(GENRE)) = LOWER(TRIM(?))",
        (normalized_genre,)
    )
    row = cur.fetchone()

    if row:
        return row[0]

    # Insert new genre
    genre_type = _prompt_fiction_or_nonfiction()

    cur.execute("PRAGMA table_info(Genre)")
    genre_columns = {col[1] for col in cur.fetchall()}

    if "Genre_Type" not in genre_columns:
        cur.execute("ALTER TABLE Genre ADD COLUMN Genre_Type TEXT")

    cur.execute(
        "INSERT INTO Genre (GENRE, Genre_Type) VALUES (?, ?)",
        (normalized_genre, genre_type)
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


def _is_literature_input(genre_name: str) -> bool:
    normalized = re.sub(r"[^a-z]", "", genre_name.strip().lower())
    return normalized in ("literature", "lit")


def _apply_genre_limit_with_literature_override(all_genres):
    selected_genres = all_genres[:4]

    if len(all_genres) <= 4:
        return selected_genres

    has_literature_in_input = any(_is_literature_input(g) for g in all_genres)
    has_literature_in_first_four = any(_is_literature_input(g) for g in selected_genres)

    if has_literature_in_input and not has_literature_in_first_four:
        selected_genres.append("Literature")
        print("Only the first 4 genres will be processed, with Literature override.")
    else:
        print("Only the first 4 genres will be processed.")

    return selected_genres

#--------------------------------------------------------------
# E. Combined Function Call
#--------------------------------------------------------------
def process_book_genres(conn, isbn: str, genre_string: str):
    cur = conn.cursor()
    unmatched_Exceptions = []

    # 1. Split into individual genres
    all_genres = split_multiple_genres(genre_string)
    genres = _apply_genre_limit_with_literature_override(all_genres)

    for genre_name in genres:

        # 2. Match against DD_Sys
        matched_desc = lookup_genre_in_ddsys(conn, genre_name)

        if not matched_desc:
            unmatched_Exceptions.append(genre_name)
            # Skip or handle unmatched genres
            # You can also choose to insert unmatched genres directly
            continue

        # 3. Create or reuse genre in Genre table
        genre_id = _get_or_create_genre(conn, matched_desc)

        # 4. Link to BookGenre
        link_genre_to_book(conn, isbn, genre_id)

    if unmatched_Exceptions:
        cur.execute(
            "SELECT GenreID FROM Genre WHERE LOWER(TRIM(GENRE)) = LOWER(TRIM(?))",
            ("Literature",)
        )
        literature_row = cur.fetchone()

        if literature_row:
            literature_genre_id = literature_row[0]
            cur.execute(
                "SELECT 1 FROM BookGenre WHERE ISBN = ? AND GenreID = ?",
                (isbn, literature_genre_id)
            )
            if not cur.fetchone():
                link_genre_to_book(conn, isbn, literature_genre_id)

    return unmatched_Exceptions

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
# That's the Wrap.
@json_wrapper
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

            seed_default_genres(cur)

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

# This is the code that convert the results into json:
def format_to_json(data):
   return json.dumps(data)
{"isbn",
 "title",
 "publisher",
 "authors",
 "genres",
 "--publish-date",
 "--summary",
 "--tag-id",
 "--chapters",
 "--chapters-completed"
}

import argparse
import json

def format_to_json(data):
    return json.dumps(data, indent=4)

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

    output = {
        "success": success,
        "result": result,
        "isbn": args.isbn,
        "title": args.title,
        "publisher": args.publisher,
        "authors": args.authors,
        "genres": args.genres,
        "publish_date": args.publish_date,
        "summary": args.summary,
        "tag_id": args.tag_id,
        "chapters": args.chapters,
        "chapters_completed": args.chapters_completed,
    }

    print(format_to_json(output))


if __name__ == "__main__":
    main()

#Alternate Main That Accepts JSON file instead of positional args.
# def main():
#    parser = argparse.ArgumentParser(description="Create a complete book record using JSON input.")
#    parser.add_argument("--json", dest="json_file", required=True, help="Path to JSON file containing book data")
#    args = parser.parse_args()
#
#    with open(args.json_file, "r") as f:
#        json_input = f.read()
#
#    success, result = create_full_book_entry(json_input)
#
#    output = {
#        "success": success,
#        "result": result
#    }
#
#    print(format_to_json(output))
