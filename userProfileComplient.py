import json
import os
import sqlite3
from datetime import datetime, timedelta
from Analytical_Functions import (
    display_Cur_Reading,
    count_Books_Owned,
    avg_Chapter_Speed
)

#--------------------------------------------------------------
# 4.11 - Default JSON user profile
#--------------------------------------------------------------
DEFAULT_USER_PROFILE = {
    "f_name": "",
    "l_name": "",
    "username": "",
    "mission_statement": "",
    "theme": "",
}

class UserManager:
    def __init__(self, db_path="bt.db", json_path="app/data/user.json"):
        self.db_path = db_path
        self.json_path = json_path

    # ---------------------------------------------------------
    # Write JSON file to disk
    # ---------------------------------------------------------
    def write_user_json(self, data):
        if not isinstance(data, dict):
            raise TypeError("User profile must be a dictionary.")

        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)

    # ---------------------------------------------------------
    # Load user profile (JSON → DB → default)
    # ---------------------------------------------------------
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
        self.write_user_json(DEFAULT_USER_PROFILE.copy())
        return DEFAULT_USER_PROFILE.copy()

    # ---------------------------------------------------------
    # Read JSON file into memory
    # ---------------------------------------------------------
    def read_user_json(self):
        if not os.path.exists(self.json_path):
            return None
        with open(self.json_path, "r") as f:
            return json.load(f)

    # ---------------------------------------------------------
    # Edit and save user profile
    # ---------------------------------------------------------
    def edit_user_profile(self):
        user = self.load_user_from_db()
        file_json = self.read_user_json()

        if not user:
            user = DEFAULT_USER_PROFILE.copy()

        # Sync JSON → DB dict
        for key, value in file_json.items():
            if key in user:
                user[key] = value

        # Save updated user to DB
        self.save_user_to_db(user)

        # Rewrite JSON to match DB
        self.write_user_json(user)

        return user

    # ---------------------------------------------------------
    # Load the single user from the database
    # ---------------------------------------------------------
    def load_user_from_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f_name, l_name, username, mission_statement, theme
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
            "mission_statement": row[3],
            "theme": row[4]
        }

    # ---------------------------------------------------------
    # Save user to DB (placeholder — you fill in)
    # ---------------------------------------------------------
    def save_user_to_db(self, user_dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Users
            SET f_name = ?, l_name = ?, username = ?, mission_statement = ?, theme = ?
            WHERE user_id = 1
        """, (
            user_dict["f_name"],
            user_dict["l_name"],
            user_dict["username"],
            user_dict["mission_statement"],
            user_dict["theme"]
        ))

        conn.commit()
        conn.close()