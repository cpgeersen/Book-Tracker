import json
import os
from datetime import datetime, timedelta
# Flask Import 
from flask import Flask, request, redirect, url_for, render_template

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
# The JSON path defined in !init statement!
#----------------------------------------------------------
# 4.7.1 - User Setting Storage (Unused)
# Definition: I am unsure of what exactly the purpose of this function is.
#---------------------------------------------------------
def user_Setting_Storage():
    manager = UserManager()
    data = manager.load_user_profile()
    return data

#------------------------------------------------
# 4.7.2 - Read User Settings (Unused)
#------------------------------------------------
def read_User_Settings():
    manager = UserManager()
    return manager.read_user_json()
#------------------------------------------------
# 4.7.3 - Update User Function
#------------------------------------------------

# I removed the first iteration of the pathway.
#----------------------------------------------
# User Profile Jinja Template Route
#----------------------------------------------
@app.route('/user_Profile_Refactor') # When the page loads.
def user_profile_page():
    if True:
        return "terminal print statement!"
        
    data = user_Setting_Storage(data)

    username = data["username"]
    mission_statement = data["mission_statement"]
    theme = data["theme"]
#this should render the Jinja
    return render_template(
        'user_Profile_Refactor.html',
        username=data["username"],
        mission_statement=data["mission_statement"],
        theme=data["theme"]
    ) 

#------------------------------------------------
# 4.4 - Reset User Profile (This is ok now)
#----------------------------------------------
# reset_User_Profile Function
# This function should return a dict object 
# that I can continue to use as values.
def reset_User_Profile():
    manager = UserManager()
    manager.delete_user_profile()
    manager.write_user_json(manager.DEFAULT_USER_PROFILE.copy())
    return manager.DEFAULT_USER_PROFILE
# reset_User_Path
@app.route("/reset_Button", methods=["POST"])
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
    # Write new file.
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
    # Load user profile (CREATES DEFAULT IF NO)
    # ---------------------------------------------------------
    def load_user_profile(self):
        # Case 1: JSON exists → load it
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as f:
                data = json.load(f)
            return data
        # Case 2: JSON missing → create default
        else:
            self.write_user_json(self.DEFAULT_USER_PROFILE.copy())
            data = self.DEFAULT_USER_PROFILE.copy()
            return data

    # ---------------------------------------------------------
    # Read JSON file into memory ("NONE" IF NO FILE EXISTS)
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
        for key, default_value in self.user.items():
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


    