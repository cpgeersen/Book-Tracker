import sqlite3
import os
from app.services.genres import genres_for_table

# !!Add actual path to the database!!
DB_PATH = "app/data/bt.db"

# Check if database already exists
db_exists = os.path.exists(DB_PATH)


def create_db():
    # Connect to the database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if db_exists:
        print("Database already exists.")
        conn.close()
        return False

    print("Database not found. Creating new database...")
    # Allow foreign keys in the creation of the table
    cursor.execute("PRAGMA foreign_keys = ON;")

    # First create the Books Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
                   ISBN TEXT PRIMARY KEY,
                   Title TEXT NOT NULL,
                   Publish_Year INTEGER,
                   Publisher_ID INTEGER,
                   Summary TEXT,
                   Tag_ID INTEGER,
                   Chapters INTEGER,
                   Chapters_Completed INTEGER,
                   Cover_Image BLOB,
                   FOREIGN KEY (Publisher_ID) REFERENCES Publishers(Publisher_ID),
                   FOREIGN KEY (Tag_ID) REFERENCES Tags(Tag_ID)
                   )
                    ''')

    # Next create the BookAuthor Bridging Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookAuthor (
                   ISBN TEXT NOT NULL,
                   Author_ID INTEGER NOT NULL,
                   PRIMARY KEY (ISBN, Author_ID),
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
                   FOREIGN KEY (Author_ID) REFERENCES Authors(Author_ID)
                   )''')

    # Next create the Authors Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
                   Author_ID INTEGER PRIMARY KEY,
                   Author_Full_Name TEXT NOT NULL,
                   Author_First_Name TEXT NOT NULL,
                   Author_Last_Name TEXT NOT NULL,
                   OpenLibrary_ID TEXT
                   )''')

    # Next create the Publishers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Publishers (
                   Publisher_ID INTEGER PRIMARY KEY,
                   Publisher_Name TEXT NOT NULL
                   )''')

    # Next create the BookNotes Bridging Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookNotes (
                   ISBN TEXT,
                   Note_ID INTEGER,
                   PRIMARY KEY (ISBN, Note_ID)
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
                   FOREIGN KEY (Note_ID) REFERENCES Books(Note_ID)
                   )''')

    # Next create the Notes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notes (
                   Note_ID INTEGER PRIMARY KEY,
                   Note BLOB NOT NULL
                   )''')

    # Next create the Tags Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
                    Tag_ID INTEGER PRIMARY KEY,
                    Owned TEXT NOT NULL,
                    Favorite TEXT NOT NULL,
                    Completed TEXT NOT NULL,
                    Currently_Reading TEXT NOT NULL,
                    Personal_Or_Academic TEXT NOT NULL,
                    ISBN TEXT,
                    FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
                    )''')

    # Next create the BookGenre Bridging Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookGenre (
                   ISBN TEXT,
                   Genre_ID INTEGER,
                   PRIMARY KEY (ISBN, Genre_ID),
                   FOREIGN KEY (Genre_ID) REFERENCES Genre(Genre_ID),
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
                   )''')

    # Next create the Genre Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genre (
                   Genre_ID INTEGER PRIMARY KEY,
                   Genre VARCHAR(15)
                   )''')

    # Insert the Genres into the Genre Table
    genre_insert = ''' INSERT INTO Genre (Genre_ID, Genre)
                       VALUES (?, ?)          
                   '''
    try:
        genres = genres_for_table()
        for key, value in genres.items():
            cursor.execute(genre_insert, (key, value))
    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    # Save the creation by committing
    conn.commit()
    print("Database and tables created successfully.")

    # Close connection
    conn.close()
    return True

