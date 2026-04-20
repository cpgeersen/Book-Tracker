import sqlite3
import csv
import os
from datetime import datetime

from app.services.user_settings.delete_database import  reset_database


# Exports full database to one CSV file in app/data/backups
# Skips Books.Cover_Image data
def export_database_to_csv():
    try:
        db_path = "bt.db"
        backup_folder = os.path.join("app", "data", "backups")

        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"bt_export_{timestamp}.csv"
        file_path = os.path.join(backup_folder, file_name)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Export order includes all tables
        # Book tables exported with Cover_Image excluded
        table_queries = {
            "Authors": "SELECT Author_ID, Author_Full_Name, Author_First_Name, Author_Last_Name FROM Authors",
            "Publishers": "SELECT Publisher_ID, Publisher_Name FROM Publishers",
            "Tags": "SELECT Tag_ID, Owned, Favorite, Completed, Currently_Reading, Personal_Or_Academic FROM Tags",
            "Books": "SELECT ISBN, Title, Publish_Year, Publisher_ID, Summary, Tag_ID, Chapters, Chapters_Completed FROM Books",
            "BookAuthor": "SELECT ISBN, Author_ID FROM BookAuthor",
            "BookGenre": "SELECT ISBN, Genre_ID FROM BookGenre",
            "Notes": "SELECT Note_ID, Note FROM Notes",
            "BookNotes": "SELECT ISBN, Note_ID FROM BookNotes"
        }

        with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            for table_name, query in table_queries.items():
                cursor.execute(query)
                rows = cursor.fetchall()

                # Write table section marker
                writer.writerow(["TABLE", table_name])

                # Write column headers
                headers = [description[0] for description in cursor.description]
                writer.writerow(headers)

                # Write table data
                for row in rows:
                    writer.writerow(row)

                # Blank row between table sections
                writer.writerow([])

        conn.close()

        return {
            "Status": "Success",
            "Message": "Database exported successfully.",
            "File_Path": file_path
        }

    except sqlite3.Error as error:
        return {
            "Status": "Failure",
            "Message": f"Database error: {error}"
        }
    except Exception as error:
        return {
            "Status": "Failure",
            "Message": str(error)
        }

# First purges and rebuilds database using reset function
def import_database_from_csv(csv_file_path, confirm_reset):
    try:
        # First purge and rebuild database
        reset_result = reset_database(confirm_reset)

        if reset_result["Status"] != "Success":
            return {
                "Status": "Failure",
                "Message": f"Import cancelled. Database reset failed: {reset_result['message']}"
            }

        conn = sqlite3.connect("bt.db")
        cursor = conn.cursor()

        current_table = ""
        headers = []

        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                # Skip blank lines
                if not row:
                    continue

                # Detect new table section
                if row[0] == "TABLE":
                    current_table = row[1]
                    headers = []
                    continue

                # First row after TABLE marker is header row
                if current_table and not headers:
                    headers = row
                    continue

                # Insert data rows
                if current_table and headers:
                    placeholders = ",".join(["?"] * len(headers))
                    columns = ",".join(headers)

                    insert_query = f"INSERT INTO {current_table} ({columns}) VALUES ({placeholders})"

                    # Convert empty strings to None for nullable columns
                    cleaned_row = [None if value == "" else value for value in row]

                    cursor.execute(insert_query, cleaned_row)

        conn.commit()
        conn.close()

        return {
            "Status": "Success",
            "Message": "Database imported successfully."
        }

    except sqlite3.Error as error:
        try:
            conn.close()
        except:
            pass
        return {
            "Status": "Failure",
            "Message": f"Database error: {error}"
        }
    except Exception as error:
        try:
            conn.close()
        except:
            pass
        return {
            "Status": "Failure",
            "Message": str(error)
        }