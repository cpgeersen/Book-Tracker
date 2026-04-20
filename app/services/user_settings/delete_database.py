import sqlite3
import os
import shutil
from datetime import datetime

from app.services.genres import genres_for_table


# Deletes existing database and recreates all tables.
# Includes confirmation safeguard and automatic backup.
def reset_database(confirm_reset):
    backup_path = ""

    try:
        db_path = "bt.db"

        # Confirmation safeguard
        if confirm_reset != "RESET":
            return {
                "status": "failure",
                "message": "Database reset cancelled. Confirmation value did not match."
            }

        # Create backup before delete
        if os.path.exists(db_path):
            backup_folder = os.path.join("app", "data", "backups")

            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_folder, f"bt_backup_{timestamp}.db")

            shutil.copy2(db_path, backup_path)
            os.remove(db_path)

        # Recreate database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

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
                           Note TEXT NOT NULL
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

        conn.commit()
        conn.close()

        return {
            "Status": "Success",
            "Message": "Database reset successfully.",
            "Backup_Path": backup_path
        }

    except Exception as error:
        return {
            "Status": "Failure",
            "Message": str(error)
        }

# Deletes Cover Images when that database is deleted
def purge_cover_images():
    try:
        cover_image_folder = os.path.join("app", "static", "images", "cover_images")

        # If folder does not exist, nothing to delete
        if not os.path.exists(cover_image_folder):
            return {
                "status": "success",
                "message": "Cover image folder does not exist. No files deleted."
            }

        deleted_count = 0

        # Loop through all files in cover image folder
        for file_name in os.listdir(cover_image_folder):
            file_path = os.path.join(cover_image_folder, file_name)

            # Only delete files, not subfolders
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1

        return {
            "Status": "Success",
            "Message": f"{deleted_count} cover image file(s) deleted."
        }

    except Exception as error:
        return {
            "Status": "Failure",
            "Message": str(error)
        }