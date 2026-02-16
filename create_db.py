import sqlite3
import os

#!!Add actual path to the database!!
DB_PATH = "bt.db"

# Check if database already exists
db_exists = os.path.exists(DB_PATH)

# Connect to the database (it will create the file if it doesn't exist)
con = sqlite3.connect(DB_PATH)
cursor = con.cursor()
if not db_exists:
    print("Database not found. Creating new database...")

    # ---------------------------
    # BEGIN ORIGINAL create_db.py
    # ---------------------------

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS Books (
                   ISBN TEXT PRIMARY KEY,
                   Title TEXT NOT NULL,
                   PublishDate TEXT,
                   PublisherID INTEGER,
                   Summary TEXT,
                   TagID INTEGER UNIQUE,
                   Chapters INTEGER,
                   Chapters_Completed INTEGER,
                   Cover_Image BLOB,
                   FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID),
                   FOREIGN KEY (TagID) REFERENCES Tags(TagID)
                   )
                    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookAuthor (
                   ISBN TEXT NOT NULL,
                   AuthorID INTEGER NOT NULL,
                   PRIMARY KEY (ISBN, AuthorID), -- The composite key removes redundency.
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE,
                   FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID) ON DELETE CASCADE
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
                   AuthorID INTEGER PRIMARY KEY,
                   Author_First_Name TEXT NOT NULL,
                   Author_Last_Name TEXT NOT NULL
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Publishers (
                   PublisherID INTEGER PRIMARY KEY,
                   Publisher_Name TEXT NOT NULL
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookGenre (
                   ISBN TEXT,
                   GenreID INTEGER,
                   PRIMARY KEY (ISBN, GenreID),
                   FOREIGN KEY (GenreID) REFERENCES Genre(GenreID) ON DELETE CASCADE,
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genre (
                   GenreID INTEGER PRIMARY KEY,
                   GENRE VARCHAR(15)
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookNotes (
                   ISBN TEXT,
                   NoteID INTEGER,
                   PRIMARY KEY (ISBN, NoteID),
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE,
                   FOREIGN KEY (NoteID) REFERENCES Notes(NoteID) ON DELETE CASCADE
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notes (
                   NoteID INTEGER PRIMARY KEY,
                   Note BLOB NOT NULL
                   )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tags (
                    TagID INTEGER PRIMARY KEY,
                    Owned BOOLEAN NOT NULL, -- Does the user own the book.
                    Favorite BOOLEAN NOT NULL, -- 1 = "Favorite"
                    Completed BOOLEAN NOT NULL,
                    Currently_Reading BOOLEAN NOT NULL, -- = 0= "Not Reading" & 1="Reading"
                    PersonalOrAcademic BOOLEAN NOT NULL -- 0="Personal" & 1="Academic"
                    )''')

    # ---------------------------
    # END ORIGINAL create_db.py
    # ---------------------------

    con.commit()
    print("Database and tables created successfully.")

else:
    print("Database already exists.")

# Close connection
con.close()