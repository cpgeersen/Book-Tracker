import json
import os
from datetime import datetime, timedelta
from Analytical_Functions import (
    display_Cur_Reading,
    count_Books_Owned,
    avg_Chapter_Speed
)

#--------------------------------------------------------------
# 4.11 - Default JSON user profile
#--------------------------------------------------------------

#----------------------------------------------------------
# 4.7.1 - User Setting Storage
#---------------------------------------------------------
def user_Setting_Storage(data):
    manager = UserManager()

    # Try to read the JSON file
    existing = manager.read_user_json()

    # If the file exists → return its contents
    if existing is not None:
        return existing

    # If the file does NOT exist → write the input data
    manager.write_user_json(data)

    # Return the newly written data
    return data

#------------------------------------------------
# 4.7.2 - Read User Settings
#------------------------------------------------
def read_User_Settings():
    manager = UserManager()
    return manager.read_user_json()
#------------------------------------------------
# 4.7.3 - Update User Function
#------------------------------------------------
def update_User_Profile():
    manager = UserManager()
    return manager.edit_user_profile()


#--------------------------------
# Save Time
#--------------------------------
class UserManager:
    def __init__(self, json_path="app/data/user_settings.json"):
        self.json_path = json_path

        self.DEFAULT_USER_PROFILE = {
            "f_name": "",
            "l_name": "",
            "username": "",
            "mission_statement": "",
            "theme": "",
        }

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
    # Load user profile (JSON → default)
    # ---------------------------------------------------------
    def load_user_profile(self):
        # Case 1: JSON exists → load it
        if os.path.exists(self.json_path):
            return self.read_user_json()

        # Case 2: JSON missing → create default
        self.write_user_json(self.DEFAULT_USER_PROFILE.copy())
        return self.DEFAULT_USER_PROFILE.copy()

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
        user = self.read_user_json() or self.DEFAULT_USER_PROFILE.copy()

        # Ensure all expected keys exist
        for key, default_value in self.DEFAULT_USER_PROFILE.items():
            user.setdefault(key, default_value)

        # Rewrite JSON with normalized data
        self.write_user_json(user)

        return user