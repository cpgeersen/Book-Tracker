import sqlite3
import json
import os
from datetime import datetime, timedelta

#==========================================================
# Original Author: Christopher O'Brien
# Editors:
#
# [] Is this program code? Y/N?
#
#This file contains analytic functions calculated from the Database.
# Target:
# Reference:
#==========================================================

#---------------------------------------------------------
# Connect to the Database
#---------------------------------------------------------
DB_PATH = "bt.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

#---------------------------------------------------------
# 3.11.1 - FUNCTION: NUMBER OF BOOKS
#---------------------------------------------------------
def total_books(cursor):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            
        total_Books = cursor.execute("""
            SELECT COUNT(ISBN) FROM Books;
        """).fetchone()[0]
        return {"Total Books": total_Books}

    except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None
#---------------------------------------------------------
# 3.11.2 - FUNCTION: NUMBER OF OWNED BOOKS
#---------------------------------------------------------
def total_owned_books(cursor):

    try:
            with _connect() as conn:
                cur = conn.cursor()

        total_Owned_Books = cursor.execute("""
            SELECT COUNT(t.TagID)
            FROM Books b
            JOIN Tags t ON b.TagID = t.TagID
            WHERE t.Owned = 1;
        """).fetchone()[0]

        return {"Total Owned Books": total_Owned_Books}

    except sqlite3.Error as e:
                print(f"Database connection error: {e}")
                return None

#---------------------------------------------------------
# 3.11.3 - FUNCTION: Display Currently Reading
#---------------------------------------------------------
def total_current_books(cursor):
    try:
        with _connect() as conn:
            cur = conn.cursor()

        total_Current_Books = cursor.execute("""
                SELECT COUNT(b.ISBN)
                FROM Tags t
                JOIN Books b ON t.TagID = b.TagID
             WHERE t.Currently_Reading = 1;
            """).fetchone()[0]
        return {"Currently Reading": total_Current_Books}

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

#---------------------------------------------------------
# 3.11.4 - FUNCTION: Display Books Completed
#---------------------------------------------------------
def total_completed_books(cursor):
    try:
        with _connect() as conn:
            cur = conn.cursor()
    
    
        count_Completed_Books = cursor.execute("""
            SELECT COUNT(TagId)
            FROM Tags
            WHERE Completed = 1;
        """).fetchone()[0]
        return {"Books Completed": count_Completed_Books}

    except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return None

#---------------------------------------------------------
# 3.11.5 - FUNCTION: Most Read Genres
#---------------------------------------------------------
def most_read_genre(cursor):
    try:
        with _connect() as conn:
            cur = conn.cursor()

        most_Read_Genres = cursor.execute("""
                SELECT c.Genre, COUNT(b.GenreID) AS genre_count
                FROM Books a
                JOIN BookGenre b ON a.ISBN = b.ISBN
                JOIN Genre c ON b.GenreID = c.GenreID
                GROUP BY b.GenreID
                ORDER BY genre_count DESC
                LIMIT 5;
            """).fetchall()
        for item in most_Read_Genres:
            most_read_genre = (f"Genre: {item[0]} \n Genre2: {item[2]} \n Genre3: {item[4]} \n Genre4: {item6} \n Genre5: {item8}")
        return most_read_genre

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None