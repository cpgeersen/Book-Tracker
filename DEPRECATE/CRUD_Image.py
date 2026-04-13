import sqlite3
import os
import json
import requests
import base64

#========================================================
# Original Author: Christopher O'Brien
# Second Author: 
#[03/12/2026] - Initial Creation
#
# [] Is this file program worthy? Y/N?
#
# This File Contains Functions to Import an Image of Book
#========================================================

###########################################################
stored_Image_Path = "app/data/cover_images/Image.json"
'''metadata_path = ?'''
###########################################################
#----------------------------------------------------------
# 3.13.1 - Create Cover Image
#----------------------------------------------------------
def create_Cover_Image(ISBN, input_URL):
    url1 = databaseImage.get_URL(ISBN)
    url2 = input_URL
    if(url1 == url2):
        print("Cover image already exists for this ISBN.")
        return True
    elif (url2 != url1):
        print("The previous cover has been replaced with the new cover.")
        databaseImage.delete_URL(ISBN)
        databaseImage.add_URL(ISBN, url2)
        try:
            fileImage.delete_File()
            fileImage.add_Image(url2)
            return True;
        except:
            fileImage.create_Default_File()
            return False
        
#----------------------------------------------------------
# 3.13.2 - Read Cover Image
#----------------------------------------------------------
def read_Cover_Image(ISBN):
    url = databaseImage.get_URL(ISBN)
    if not url:
        print("No cover image found.")
        return None

    response = requests.get(url)
    response.raise_for_status()
    return response.content  # raw bytes

#----------------------------------------------------------
# 3.13.3 - Update Cover Image
#-----------------------------------------------------------
def update_Cover_Image(stored_Image_Path, ISBN, new_cover_image_url):
    url1 = stored_Image_Path
    url2 = new_cover_image_url
    fileImage = fileImage(stored_Image_Path)
    try:
        databaseImage.delete_URL(ISBN)
        databaseImage.add_URL(ISBN, url2)
        fileImage.delete_File()
        fileImage.add_Image(url2)
        return True;
    except Exception as e:
        fileImage.create_Default_File()
        return False

#-----------------------------------------------------------
# 3.13.4 - Delete Cover Image
#-----------------------------------------------------------
def delete_Cover_Image(stored_Image_Path, ISBN):
    fileImage = fileImage(stored_Image_Path)
    url = database.get_URL(ISBN)
    if not url:
        print("No cover image found for the given ISBN.")
        return True
    databaseImage.delete_URL(ISBN)
    
    try:
        fileImage.delete_File()
        return True;
    except:
        print("Error deleting cover image file.")
        return False

#---------------------------------------------------------
# Functions 
#---------------------------------------------------------
#---------------------------------------------------------
# FILE FUNCTIONS
#---------------------------------------------------------


class fileImage:
    def __init__(self, stored_Image_Path=None):
        # Use provided path OR default path
        self.stored_Image_Path = stored_Image_Path or "app/data/cover_images/Image.json"

#-----------------------------------------------------------
# Create a Default Blank File
#-----------------------------------------------------------
    def create_Default_File(self):
        os.makedirs(os.path.dirname(self.stored_Image_Path), exist_ok=True)

        if not os.path.exists(self.stored_Image_Path):
            with open(self.stored_Image_Path, "w") as f:
                json.dump({}, f, indent=4)

#------------------------------------------------------------
# Delete a File
#-------------------------------------------------------------
    def delete_File(self):
        if os.path.exists(self.stored_Image_Path):
            os.remove(self.stored_Image_Path)
            print(f"Deleted file: {self.stored_Image_Path}")
        else:
            print(f"File not found: {self.stored_Image_Path}")

#-----------------------------------------------------------
# Save Image to File
#-----------------------------------------------------------
    def add_Image(self, image_url):
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()

        # Convert image bytes to base64
        image_base64 = base64.b64encode(response.content).decode("utf-8")

        # Create JSON data
        data = {
            "image_url": image_url,
            "image_base64": image_base64
        }

        # Save to JSON file (using stored_Image_Path!)
        with open(self.stored_Image_Path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Image saved to {self.stored_Image_Path}")

#------------------------------------------------------------------
# DATABASE FUNCTIONS
#------------------------------------------------------------------
#------------------------------------------------------------------
# Read Image from DB 
#------------------------------------------------------------------  
class databaseImage:    
    def get_URL(self, ISBN)
        try:
            # Connect to SQLite database.
            conn = sqlite3.connect("bt.db")
            cursor = conn.cursor()

            # Query database for ISBN provided.
            read_query = "SELECT ISBN, Cover_Image FROM Books WHERE ISBN = ?"
            criteria = (ISBN,)
            cursor.execute(read_query, criteria)
            result = cursor.fetchone()
            conn.close()

            return result[0] if result else None

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()

#------------------------------------------------------------------
# Add Image and Image Path to DB
#------------------------------------------------------------------
    def add_URL(ISBN, cover_image_path):
        try:
            # Connect to SQLite database.
            conn = sqlite3.connect("bt.db")
            cursor = conn.cursor()

            # Update database with new cover image path for ISBN provided.
            update_query = "UPDATE Books SET Cover_Image = ? WHERE ISBN = ?"
            criteria = (cover_image_path, ISBN)
            cursor.execute(update_query, criteria)
            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            return False

#-----------------------------------------------------------------
# Delete Image Path from DB
#-----------------------------------------------------------------
    def delete_URL(ISBN):
        try:
            # Connect to SQLite database.
            conn = sqlite3.connect("bt.db")
            cursor = conn.cursor()

            # Update database to remove cover image path for ISBN provided.
            delete_query = "UPDATE Books SET Cover_Image = NULL WHERE ISBN = ?"
            criteria = (ISBN,)
            cursor.execute(delete_query, criteria)
            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as error:
            print(f"Database error: {error}")
            conn.close()
            return False

#-------------------------------------------------
# Read Cover Image
#-------------------------------------------------
    def read_Cover_Image(self, ISBN):
        pass

#-------------------------------------------------
# Update Image
#-------------------------------------------------
    def update_Image(self, ISBN, new_cover_image_url):
        return update_Cover_Image(self.stored_Image_Path, ISBN, new_cover_image_url)

#==================================================================
# End of File
#==================================================================
    

