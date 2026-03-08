#----------------------------------------------
# 3.11 Analytical Functions
#----------------------------------------------
import sqlite3
import json
import os
from datetime import datetime

# Function 1: Favorite Genre Calculation
def fav_Genre():
    favorite_genreID = cursor.execute("""
        SELECT COUNT(a.GenreID) AS genre_quantity, b.Genre
        FROM BookGenre a
        LEFT Join Genre b ON a.GenreID = b.GenreID
        GROUP BY a.GenreID
        ORDER BY genre_quantity DESC;
    """).fetchone()[1]
    return favorite_genreID
    
# Function 2: Average Chapter Read Speed Calculation
def avg_Chapter_Speed():
    chapters_read = cursor.execute("""
        SELECT Chapters_Completed 
        FROM Books 
        WHERE ISBN = ?
    """, (ISBN,)).fetchone()[0]

    chapters_total = cursor.execute("""
    SELECT Chapters FROM Books WHERE ISBN = ?
    """, (ISBN,)).fetchone()[0] 

    date_started = cursor.execute("""SELECT c.created_On 
                                     FROM Notes c
                                     JOIN BookNotes b ON c.NoteID = b.NoteID
                                     JOIN Books a ON a.ISBN = b.ISBN
                                     WHERE a.ISBN = ?
                                     ORDER BY c.created_On ASC
                                     LIMIT 1""", (ISBN,)).fetchone()[0]

    date_started = datetime.strptime(date_started, "%Y-%m-%d %H:%M:%S")
    system_time = datetime.utcnow()   # matches SQLite UTC timestamps

    # This is the function that I used: 
    days_elipsed = julian_date(system_time) - julian_date(date_started)
    Speed = [(chapters_read / chapters_total) / (days_elipsed)]
    return Speed
    days_elapsed = (system_time - date_started).total_seconds() / 86400
    progress_fraction = chapters_read / chapters_total
    speed = (progress_fraction / days_elapsed)*chapters_total

    return speed # Output should tell Chapters per day. 


# Function 3: Average Page Read Speed Calculation
# Incomplete function.
def avg_Page_Speed():
    pages_read =
    pages_total = 
    date_started = 
    Speed = [(pages_read / pages_total) / (system_time - date_started)]
    return Page_Speed_inDays

# Function 4: Predicted Book Completion Date Calculation.
def predicted_Completion_Date():

    chapters_read = cursor.execute("""
        SELECT Chapters_Completed 
        FROM Books 
        WHERE ISBN = ?
        """, (ISBN,)).fetchone()[0]

    chapters_total = cursor.execute("""
        SELECT Chapters 
        FROM Books 
        WHERE ISBN = ?
        """, (ISBN,)).fetchone()[0] 

    date_started = cursor.execute("""
        SELECT c.created_On 
        FROM Notes c
        JOIN BookNotes b ON c.NoteID = b.NoteID
        JOIN Books a ON a.ISBN = b.ISBN
        ORDER BY created_On ASC
        WHERE a.ISBN = ?
        """, (ISBN,)).fetchone()[0]

        system_time = datetime.now()
        # This is the function that I used: 
        days_elipsed = julian_date(system_time) - julian_date(date_started)
        days_to_Complete = [[chapters_total-chapters_read]*[(chapters_read / chapters_total) / (days_elipsed)]]**(-1)

    return days_to_Complete
        
    
    

#######################################
# I'm unsure about path of the JSON import file. 
#######################################
# Function 5: Display Mission Statement.
def display_Mission_Statement():
    try:
        with open("/workspaces/Book-Tracker/user.json", "r") as f:
            profile = json.load(f)
            mission = profile.get("mission_Statement", "No mission statement found.")
        if mission and mission.strip():
            return mission
    
        mission = cursor.execute("""
                SELECT mission_statement FROM Users WHERE user_id = 1;
            """).fetchone()[0]
            return(mission)
    except FileNotFoundError:
        print("User profile file not found.")

# Function 6: Display Currently Reading.
def display_Cur_Reading():
    cur_reading = cursor.execute("""
        SELECT b.Title, b.ISBN
        FROM Tags t
        JOIN Books b ON t.TagID = b.TagID
        WHERE t.Currently_Reading = 1;
    """).fetchall()
    return cur_reading
    
# Function 7: Display Books Completed.
def display_Count_Books_Completed():
    books_completed = cursor.execute("""
        SELECT COUNT(TagId) FROM Tags WHERE Completed = 1;
    """).fetchone()[0]
    return books_completed