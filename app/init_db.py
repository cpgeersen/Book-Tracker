import sqlite3
import os
#!!Add actual path to the database!!
DB_PATH = "mock.db"
# Check if database already exists
db_exists = os.path.exists(DB_PATH)
# Connect to the database (it will create the file if it doesn't exist)
con = sqlite3.connect(DB_PATH)
cursor = con.cursor()

if not db_exists:
    print("Database not found. Creating new database...")
    # Create the database
# 1.1.4 Publishers Table
    cursor.execute("""
        CREATE TABLE Publishers (
            PublisherID INTEGER PRIMARY KEY AUTOINCREMENT,
            PublisherName TEXT NOT NULL
        );
    """)

    # 1.1.7 Genres Table
    cursor.execute("""
        CREATE TABLE Genres (
            GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
            Genre TEXT NOT NULL
        );
    """)

    # 1.1.5 Tags Table
    cursor.execute("""
        CREATE TABLE Tags (
            TagID INTEGER PRIMARY KEY AUTOINCREMENT,
            Owned INTEGER DEFAULT 0,
            Favorite INTEGER DEFAULT 0,
            Read INTEGER DEFAULT 0,
            CurrentlyReading INTEGER DEFAULT 0,
            PersonalOrAcademic TEXT
        );
    """)

    # 1.1.3 Authors Table
    cursor.execute("""
        CREATE TABLE Authors (
            AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL
        );
    """)

    # 1.1.9 Notes Table
    cursor.execute("""
        CREATE TABLE Notes (
            NoteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Note BLOB
        );
    """)

    # 1.1.1 Books Table
    cursor.execute("""
        CREATE TABLE Books (
            ISBN TEXT PRIMARY KEY,
            Title TEXT NOT NULL,
            PublishDate TEXT,
            PublisherID INTEGER,
            Summary TEXT,
            TagID INTEGER,
            Chapters INTEGER DEFAULT 0,
            CompletedChapters INTEGER DEFAULT 0,
            CoverImage BLOB,
            FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID),
            FOREIGN KEY (TagID) REFERENCES Tags(TagID)
        );
    """)

    # 1.1.2 BookAuthor (Bridging Table)
    cursor.execute("""
        CREATE TABLE BookAuthor (
            ISBN TEXT,
            AuthorID INTEGER,
            PRIMARY KEY (ISBN, AuthorID),
            FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
            FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID)
        );
    """)

    # 1.1.6 BookGenre (Bridging Table)
    cursor.execute("""
        CREATE TABLE BookGenre (
            ISBN TEXT,
            GenreID INTEGER,
            PRIMARY KEY (ISBN, GenreID),
            FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
            FOREIGN KEY (GenreID) REFERENCES Genres(GenreID)
        );
    """)

    # 1.1.8 BookNote (Bridging Table)
    cursor.execute("""
        CREATE TABLE BookNote (
            ISBN TEXT,
            NoteID INTEGER,
            PRIMARY KEY (ISBN, NoteID),
            FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
            FOREIGN KEY (NoteID) REFERENCES Notes(NoteID)
        );
    """)
    # Commit changes
    con.commit()
    print("Database and tables created successfully.")
else:
    print("Database already exists.")    # Commit changes and close the connection
con.close()

"""/*
# RUN ON PYTHON SHELL
import sqlite3

con = sqlite3.connect("mock.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
*/"""