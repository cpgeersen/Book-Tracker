#----------------------------------------------
# 3.11 Analytical Functions
#----------------------------------------------
import sqlite3
import json
import os
from datetime import datetime

#######################################
# I'm unsure about path of the JSON import file. 
#######################################
# Note: JSON Path = `app/data/list_Books_Completed.json'
#----------------------------
# 3.11.1 - FUNCTION: NUMBER OF BOOKS
#----------------------------
def count_Books():
    book_count = cursor.execute("""
        SELECT COUNT(ISBN) FROM Books;
    """).fetchone()[0]
    return book_count

#---------------------------- 
# 3.11.2 - FUNCTION: NUMBER OF OWNED BOOKS
#----------------------------
def count_Books_Owned():
    books_owned = cursor.execute("""
        SELECT COUNT(t.TagID)
        FROM Books b
        JOIN Tags t ON b.TagID = t.TagID
        WHERE t.Owned = 1;
    """).fetchone()[0]
    return books_owned
# CHECK TO MAKE SURE THERE IS AN "OWNED" TAG IN TABLE

#---------------------------
# 3.11.3 - FUNCTION 6: Display Currently Reading.
#---------------------------
def display_Cur_Reading():
    cur_reading = cursor.execute("""
        SELECT b.Title, b.ISBN
        FROM Tags t
        JOIN Books b ON t.TagID = b.TagID
        WHERE t.Currently_Reading = 1;
    """).fetchall()
    return cur_reading

#---------------------------
# ![ALTERNATE FUNCTION in userProfileF.py]
# Function 7: Display Books Completed.
# 3.11.4 
# [REQUIRED MODIFICATION] - DELETE OLD BOOKS - SHOULD STORE INCREMENT IN USER INFO TABLE
# JSON Path = `app/data/list_Books_Completed.json'
#---------------------------

def display_Count_Books_Completed():
    books_completed = cursor.execute("""
        SELECT COUNT(TagId) FROM Tags WHERE Completed = 1;
    """).fetchone()[0]
    return books_completed

# IDEA IS TO PUT IBN OF COMPLETED BOOKS INTO A JSON FILE (SO THE COUNT CAN INCREMENT)
# The Json file will need to be referenced before a new entry to prevent duplication.
# THIS FUNCTION WILL BE TRIGGERED WHENEVER A BOOK IS MARKED COMPLETED.
# (So this function should actually be in the create or update files)
# THE FUNCTION WILL RETURN A COUNT OF THE LISTED ISBNs.  

#--------------------------------
# 3.11.5 - FUNCTION: most_Read_Genre 
#--------------------------------
def most_Read_Genre():
    list_Fav_Genres = cursor.execute("""
        SELECT c.Genre, COUNT(b.GenreID) AS genre_count
        FROM Books a
        JOIN BookGenre b ON a.ISBN = b.ISBN
        JOIN Genre c ON b.GenreID = c.GenreID
        GROUP BY b.GenreID
        ORDER BY genre_count DESC
        LIMIT 5;
    """).fetchall()
    return list_Fav_Genres

#------------------------------
# 
# Function 2: Average Chapter Read Speed Calculation
# CURRENTLY OUT OF SCOPE. 
# [REMOVAL OF THIS FUNCTION WOULD CHANGE THE DB]
# [REMOVAL REQUIRES REMOVAL OF TRIGGER FUNCTIONS]
# [REMOVAL REQUIRES MODIFICATION OF CREATE FUNCTION]
# [REMOVAL REMOVES ORIGINAL NOTES GENERATED AT BOOK ADDITION (FOR TIMESTAMP)]
#
#------------------------------
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

#----------------------
# 
# !Function 3: Average Page Read Speed Calculation
# [Incomplete function[] - CURRENT DB IS CHAPTER ORIENTED
# [OUT OF SCOPE] - CHANGES TRIGGER FUNCTION AND ORIGIANL TIMESTAMP
#
#----------------------
def avg_Page_Speed():
    pages_read =
    pages_total = 
    date_started = 
    Speed = [(pages_read / pages_total) / (system_time - date_started)]
    return Page_Speed_inDays

#----------------------
#
# Function 4: Predicted Book Completion Date Calculation.
# [OUT OF SCOPE] - REMOVE TRIGGER: ORIGINAL BOOKNOTE
#
#----------------------
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
        
#-----------------------
#
# Function 5: Display Mission Statement.
# (MAYBE CALL THIS A MINDFULNESS MESSAGE)-SEEMS USEFUL TO ME.
# [OUT OF SCOPE] - i like this one.
#
#-----------------------
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






















