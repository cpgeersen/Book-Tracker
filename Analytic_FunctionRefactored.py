import sqlite3
import json
import os

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

#---------------------------------------------------------
# Alt - Route for Jinja Template Stats Experiment
#---------------------------------------------------------
@app.route('/user_Profile_Refactor')
def profile_page():
   total_books = total_books()
   owned_books = total_owned_books()
   currently_reading = total_current_books()
   completed = total_completed_books()
   favorite_genre = most_read_genre()

   return render_template(
   'user_Profile_Refactor.html',
   total_books=total_books,
   owned_books = owned_books, 
   currently_reading = currently_reading,
   completed=completed,
   favorite_genre=favorite_genre
   )
   
#---------------------------------------------------------
# List of completed books
#---------------------------------------------------------
def show_completed():
    cursor.execute("""
        SELECT Books.Title AS title
        FROM Books
        RIGHT JOIN Tags ON Books.TagID = Tags.TagID
        WHERE Tags.Completed = 1;
    """)

    completed = [ {"title": row[0]} for row in cursor.fetchall() ]

    html = "<h3>Books Marked As Completed</h3><ul>"

    for book in completed:
        html += f"<li>{book['title']}</li>"

    html += "</ul>"

    return html
#----------------------------------------------------------
# This function html list for currently reading tagged books.
#----------------------------------------------------------
def show_currently_reading():
    cursor.execute("""
        SELECT Books.Title AS title
        FROM Books
        RIGHT JOIN Tags ON Books.TagID = Tags.TagID
        WHERE Tags.Currently_Reading = 1;
    """)

    currently_reading = [ {"title": row[0]} for row in cursor.fetchall() ]

    html = "<h3>Books Marked As Currently Reading</h3><ul>"

    for book in currently_reading:
        html += f"<li>{book['title']}</li>"

    html += "</ul>"

    return html