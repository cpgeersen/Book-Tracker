import json
import os
from datetime import datetime, timedelta
# Flask Import 
from flask import Flask, request, redirect, url_for
from your_module import update_User_Profile

app = Flask(__name__)


#===========================================================
# Original Author: Christopher O'Brien
# Second Author: 
#
# [] Is this code program worthy? Y/N?
#
# 4.11-Create JSON user file 4 
# + 3.11 - Count Completed Books [code at bottom]
# I think I need to do more work on this file 
# to allow for for calculated fields to be generated
#===========================================================

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
    return UserManager.read_user_json()
#------------------------------------------------
# 4.7.3 - Update User Function
#------------------------------------------------
# Update Function
def update_User_Profile():
    return UserManager.edit_user_profile()
# Update Profile Route (potential problem is route name document vs whatever)
@app.route("/submit_Button", methods=["POST"])
def update_Profile_Route():
    return update_User_Profile()
#------------------------------------------------
# 4.4 - Reset User Profile 
#----------------------------------------------
# reset_User_Profile Function
def reset_User_Profile():
    manager = UserManager()
    manager.delete_user_profile()
    return manager.DEFAULT_USER_PROFILE
# reset_User_Path
@app.route("/reset_Button", method=["POST"])
def reset_Profile_Route():
    return reset_User_Profile()
#--------------------------------------------------------------
# 4.11 - Default JSON user profile
#--------------------------------------------------------------
#--------------------------------
# Class Definition and Default Profile
#--------------------------------
class UserManager:
    def __init__(self, json_path="app/data/user_settings.json"):
        self.json_path = json_path

        self.DEFAULT_USER_PROFILE = {
            "username": "",
            "mission_statement": "",
            "theme": ""
        }
    # ---------------------------------------------------------
    # Write JSON file to disk
    # ---------------------------------------------------------
    def write_user_json(self, data):
        if not isinstance(data, dict):
            raise TypeError("User profile must be a dictionary.")
            return False
        else:    
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

            with open(self.json_path, "w") as f:
                json.dump(data, f, indent=4)
            return True
            
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
    #----------------------------------------------------------
    # Delete user profie
    #----------------------------------------------------------
    def delete_user_profile(self):
        if os.path.exists(self.json_path):
            os.remove(self.json_path)
            self.load_user_profile()  # Recreate default profile
            return True
        else:
            self.load_user_profile()  # Ensure default profile exists
            return False