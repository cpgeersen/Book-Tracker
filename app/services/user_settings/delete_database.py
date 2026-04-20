import sqlite3
import os
import shutil
from datetime import datetime

from app.services import create_db


# Deletes existing database and recreates all tables.
# Includes confirmation safeguard and automatic backup.
def reset_database(confirm_reset):
    backup_path = ""

    try:
        db_path = "bt.db"

        # Confirmation safeguard
        if confirm_reset != "RESET":
            return {
                "status": "failure",
                "message": "Database reset cancelled. Confirmation value did not match."
            }

        # Create backup before delete
        if os.path.exists(db_path):
            backup_folder = os.path.join("app", "data", "backups")

            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_folder, f"bt_backup_{timestamp}.db")

            shutil.copy2(db_path, backup_path)
            os.remove(db_path)

        # Recreate database
        create_db()

        return {
            "Status": "Success",
            "Message": "Database reset successfully.",
            "Backup_Path": backup_path
        }

    except Exception as error:
        return {
            "Status": "Failure",
            "Message": str(error)
        }

# Deletes Cover Images when that database is deleted
def purge_cover_images():
    try:
        cover_image_folder = os.path.join("app", "static", "images", "cover_images")

        # If folder does not exist, nothing to delete
        if not os.path.exists(cover_image_folder):
            return {
                "status": "success",
                "message": "Cover image folder does not exist. No files deleted."
            }

        deleted_count = 0

        # Loop through all files in cover image folder
        for file_name in os.listdir(cover_image_folder):
            file_path = os.path.join(cover_image_folder, file_name)

            # Only delete files, not subfolders
            if os.path.isfile(file_path):
                os.remove(file_path)
                deleted_count += 1

        return {
            "status": "success",
            "message": f"{deleted_count} cover image file(s) deleted."
        }

    except Exception as error:
        return {
            "status": "failure",
            "message": str(error)
        }