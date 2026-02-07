import sqlite3

with sqlite3.connect("bt.db") as conn:

    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

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

    curson.execute('''
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