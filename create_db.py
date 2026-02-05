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
                   Cover_Image,
                   FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID),
                   FOREIGN KEY (TagID) REFERENCES Tags(TagsID)
                   )
                    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BookAuthor (
                   ISBN TEXT NOT NULL,
                   AuthorID INTEGER NOT NULL,
                   PRIMARY KEY (ISBN, AuthorID)
                   )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
                   AuthorID INTEGER PRIMARY KEY,
                   Author_First_Name TEXT NOT NULL,
                   AUthor_Last_Name TEXT NOT NULL
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
                   PRIMARY KEY (ISBN, GenreID)
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
                   Note TEXT NOT NULL
                   )''') 

