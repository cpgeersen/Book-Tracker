import json
import os
import sqlite3
import datetime
#######################################
# I'm unsure about path of the JSON import file. 
#######################################

#--------------------------------------------------------------
# 4.11-Create JSON user file 4 
# + 3.11 - Count Completed Books [code at bottom]
# I think I need to do more work on this file 
# to allow for for calculated fields to be generated
#---------------------------------------------------------------
class UserManager:
    def __init__(self, db_path="bt.db", json_path="app/data/user.json"):
        self.db_path = db_path
        self.json_path = json_path

        self.DEFAULT_USER_PROFILE = {
            "f_name": "",
            "l_name": "",
            "username": "",
            "email": "",
            "mission_statement": "",
            "cur_reading": "",
            "fav_genres": "",
            "avg_chapter_speed": "",
            "avg_page_speed": "",
            "theme": "",
            "calculated_fields": {
                "avg_chapter_read_speed": "",
                "avg_page_read_speed": "",
                "fav_genres": "",
                "cur_reading": ""
            }
        }

    # ---------------------------------------------------------
    # 4.1.1(A) - FUNCTION: Write JSON file to disk
    # ---------------------------------------------------------
    def write_user_json(self, data):
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)

    #----------------------------------------------
    # 4.1.1(B) - FUNCTION: Create User 
    #-----------------------------------------------
    def load_user_profile(self):
        # Case 1: JSON exists → load it
        if os.path.exists(self.json_path):
            return self.read_user_json()
        # Case 2: JSON missing → check DB
        user_from_db = self.load_user_from_db()
        if user_from_db:
            self.write_user_json(user_from_db)
            return user_from_db
        # Case 3: No JSON + no DB user → create default
        self.write_user_json(self.DEFAULT_USER_PROFILE)
        return self.DEFAULT_USER_PROFILE.copy()

    # ---------------------------------------------------------
    # 4.1.1(C) - FUNCTION: Save user to DB (overwrite the single row)
    # ---------------------------------------------------------
    def save_user_to_db(self, user):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users")  # enforce single-user rule
        cursor.execute("""
            INSERT INTO Users (
                user_id, f_name, l_name, username, email, mission_statement,
                cur_reading, fav_genres, avg_chapter_speed, avg_page_speed, theme
            ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user["f_name"],
            user["l_name"],
            user["username"],
            user["email"],
            user["mission_statement"],
            user["cur_reading"],
            user["fav_genres"],
            user["avg_chapter_speed"],
            user["avg_page_speed"],
            user["theme"]
        ))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # 4.1.2(A1) - FUNCTION: Load JSON file into memory
    # ---------------------------------------------------------
    def read_user_json(self):
        with open(self.json_path, "r") as f:
        return json.load(f)

    # ---------------------------------------------------------
    # 4.1.2(A2) - FUNCTION: Load the single user from the database
    # ---------------------------------------------------------
    def load_user_from_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT f_name, l_name, username, email, mission_statement,
                   cur_reading, fav_genres, avg_chapter_speed,
                   avg_page_speed, theme
            FROM Users
            WHERE user_id = 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return {
            "f_name": row[0],
            "l_name": row[1],
            "username": row[2],
            "email": row[3],
            "mission_statement": row[4],
            "cur_reading": row[5],
            "fav_genres": row[6],
            "avg_chapter_speed": row[7],
            "avg_page_speed": row[8],
            "theme": row[9],
            "calculated_fields": {
                "avg_chapter_read_speed": "",
                "avg_page_read_speed": "",
                "fav_genres": "",
                "cur_reading": ""
            }
        }

    #---------------------------------------------
    # 4.1.2(B) - FUNCTION: Edit JSON user file
    #---------------------------------------------
    def edit_user_profile(self):
        # Load DB user
        user = self.load_user_from_db()
        if user is None:
            raise ValueError("No user exists in the database to edit.")

        # Load JSON file (this is the editable version)
        file_json = self.read_user_json()

        # Stage 1: Apply JSON values to the in-memory user
        for key, value in file_json.items():
            if key in user:
                user[key] = value
            elif key in user["calculated_fields"]:
                user["calculated_fields"][key] = value
            else:
                raise KeyError(f"Invalid field in JSON: {key}")

        # Stage 2: Save updated user to DB
        self.save_user_to_db(user)

        # Stage 3: Rewrite JSON to match DB
        self.write_user_json(user)

        return user

    #---------------------------------------------
    # 4.1.3 - FUNCTION: Read JSON user file
    #---------------------------------------------
    def read_user_json(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError("User JSON file does not exist.")
        with open(self.json_path, "r") as f:
            return json.load(f)

    #---------------------------
    # [ALTERNATE] 3.11.4 - Function 7: Display Books Completed.
    # [REQUIRED MODIFICATION] - DELETE OLD BOOKS - SHOULD STORE INCREMENT IN USER INFO TABLE
    # JSON Path = `app/data/list_Books_Completed.json'
    #---------------------------
    # This could Get messy. 
    #def display_Count_Books_Completed():
    #    books_completed = cursor.execute("""
    #        SELECT COUNT(TagId) FROM Tags WHERE Completed = 1;
    #        """).fetchone()[0]
    #    return books_completed
#
    #def ALT_display_Count_Books_Completed():
#
    #    
    #def load_list_Books_Completed(self):
    #    # Case 1: JSON exists → load it
    #    if os.path.exists('app/data/list_Books_Completed.json'):
    #        return self.read_user_json()
    #    # Case 2: JSON missing → check DB
    #    user_from_db = self.load_user_from_db()
    #    if user_from_db:
    #        self.write_user_json(user_from_db)
    #    return user_from_db
    #    # Case 3: No JSON + no DB user → create default
    #    self.write_user_json(self.DEFAULT_USER_PROFILE)
    #    return self.DEFAULT_USER_PROFILE.copy()
#
    ## IDEA IS TO PUT IBN OF COMPLETED BOOKS INTO A JSON FILE (SO THE COUNT CAN INCREMENT)
    # The Json file will need to be referenced before a new entry to prevent duplication.
    # THIS FUNCTION WILL BE TRIGGERED WHENEVER A BOOK IS MARKED COMPLETED.
    # (So this function should actually be in the create or update files)
    # THE FUNCTION WILL RETURN A COUNT OF THE LISTED ISBNs.  