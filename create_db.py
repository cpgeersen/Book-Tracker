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
    # <I am experimenting with making this table temporary>
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DD_Sys(
                Class_Num INT,
                Class_Desc TEXT
                )
                ''')

    with open('/workspaces/Book-Tracker/genre_inserts.sql', 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)

    cursor.execute ('''
        CREATE TABLE IF NOT EXISTS Books (
                   ISBN TEXT PRIMARY KEY,
                   Title TEXT NOT NULL,
                   PublishDate TEXT,
                   PublisherID INTEGER,
                   Summary TEXT,
                   TagID INTEGER,
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
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN), -- Constraint enforces realtional integrity, by ensuring items exist.
                   FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
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
                   FOREIGN KEY (GenreID) REFERENCES Genre(GenreID),
                   FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
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
                   PRIMARY KEY (ISBN, NoteID)
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