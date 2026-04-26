import os

from app.services.user_settings.delete_database import reset_database as delete_database


def test_database_reset():
    response = delete_database('RESET')
    assert response['Status'] == 'Success'

    # Clean up
    backup_folder = os.path.join("app", "data", "backups")
    for file_name in os.listdir(backup_folder):

        file_path = os.path.join(backup_folder, file_name)

        # Only delete files, not subfolders

        if os.path.isfile(file_path):
            os.remove(file_path)

def test_database_reset_no_confirm():
    response = delete_database('')
    assert response['status'] == 'failure'
