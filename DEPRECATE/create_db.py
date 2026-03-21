import sqlite3
import os

#==========================================================
# [Project Manager]: Collin Geershen
# Original Author: Christopher O'Brien
# Editors:
#
# [] Is this Program Worth Code? Y/N?
#
# This is the create database file.
#==========================================================

#!!Add actual path to the database!!
DB_PATH = "../bt.db"

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

    #----------------------------
    # CREATE USER TABLE
    #----------------------------
    # added user_id = 1 to enforce only one user record, since this is a single user application.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY CHECK (user_id = 1),  
            f_name TEXT NOT NULL,
            l_name TEXT NOT NULL,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            mission_statement TEXT DEFAULT NULL,
            cur_reading TEXT DEFAULT NULL,
            fav_genres TEXT DEFAULT NULL,
            avg_chapter_speed REAL DEFAULT NULL,
            avg_page_speed REAL DEFAULT NULL,
            theme BOOLEAN DEFAULT 0
            );
            ''')
    #----------------------------
    # Beginning of the book DB
    #----------------------------
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

    # Should trigger a note creation with info for analysis functions. 
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS create_blank_note_for_book
            AFTER INSERT ON Books
            BEGIN
                -- Step 1: Create a blank note (timestamp auto-filled)
                INSERT INTO Notes (Note)
                VALUES ('Book Added to Library');

                -- Step 2: Link the new note to the new book
                INSERT INTO BookNotes (ISBN, NoteID)
                VALUES (NEW.ISBN, last_insert_rowid());
            END;


#---------------------------------------------------------------
# Here I have went ahead and added the DD_Sys table.
#---------------------------------------------------------------

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DD_Sys(
                Class_Num INT,
                Class_Desc TEXT
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
                   Author_Full_Name TEXT NOT NULL,
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
                   Note BLOB NOT NULL,
                   created_On TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   updated_At TEXT DEFAULT NULL
                   )''')

        # TRIGGER FUNCTION.
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_notes_timestamp
        AFTER UPDATE ON Notes
        FOR EACH ROW
        BEGIN
            UPDATE Notes
            SET updated_At = CURRENT_TIMESTAMP
            WHERE NoteID = NEW.NoteID;
        END;
    """)

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